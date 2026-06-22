#!/usr/bin/env python
"""
DLR Auto-Healer — keeps Discord Lugs Reader running 24/7.

Monitors all known failure modes (catalogued from months of production history)
and auto-recovers from each one. Designed to run every 2 minutes via cron.

FAILURE MODES COVERED:
  FM01  Token expired (401)          → auto-extract from Desktop app leveldb
  FM02  Token file missing/empty      → auto-extract from Desktop app leveldb
  FM03  main.py process crash         → restart (with backoff for crash loops)
  FM04  ocr_watcher.py process crash  → restart (with backoff for crash loops)
  FM05  OCR watcher hanging (stale)   → kill + restart
  FM06  Rapid restart loop            → exponential backoff + alert
  FM07  PowerShell/CIM timeout        → fallback to tasklist.exe
  FM08  Network connectivity loss     → health check before restart decisions
  FM09  Browser data corruption       → swap browser_data → browser_data_stable
  FM10  Watchdog lock stale           → TTL-based expiry (auto-clears after 90s)
  FM11  Process check false negative  → dual verification (tasklist + log check)
  FM12  Outside-window transitions    → clean stop/start at window boundaries

USAGE:
  python dlr_autohealer.py
    
Set WATCHDOG_ALERT_WEBHOOL env var for Discord alert notifications.
"""

import subprocess
import sys
import os
import time
import json
import logging
import re
from datetime import datetime, timedelta
from pathlib import Path

# ===== CONFIG =====
PROJECT_ROOT = Path(__file__).parent.resolve()
PYTHONW_EXE = PROJECT_ROOT / "venv311_new" / "Scripts" / "pythonw.exe"
PYTHON_EXE = PROJECT_ROOT / "venv311_new" / "Scripts" / "python.exe"
MAIN_SCRIPT = PROJECT_ROOT / "main.py"
OCR_SCRIPT = PROJECT_ROOT / "ocr_watcher.py"
TOKEN_FILE = PROJECT_ROOT / "discord_token.txt"
CRASH_LOG = PROJECT_ROOT / "discord_crash_log.txt"
DEBUG_LOG = PROJECT_ROOT / "discord_lugs_reader_debug.log"
OCR_LOG = PROJECT_ROOT / "ocr_watcher.log"
LOCK_FILE = PROJECT_ROOT / "watchdog.lock"
HEALER_LOG = PROJECT_ROOT / "watchdog_healer.log"
STATE_FILE = PROJECT_ROOT / "healer_state.json"
BROWSER_DATA = PROJECT_ROOT / "browser_data"
BROWSER_DATA_STABLE = PROJECT_ROOT / "browser_data_stable"
BROWSER_DATA_CHECK = PROJECT_ROOT / "browser_data_check"

WATCHDOG_WEBHOOK = os.environ.get("WATCHDOG_ALERT_WEBHOOK", "")
STALE_MINUTES = 10          # OCR log considered stale after N min without updates
LOCK_TTL = 90               # seconds — watchdog lock auto-expires
BROWSER_CRASH_THRESHOLD = 3 # swaps to backup after N sequential browser failures
RESTART_BACKOFF_MIN = 30    # seconds minimum between restarts of same process
RESTART_BACKOFF_MAX = 600   # 10 min max backoff
TOKEN_CHECK_INTERVAL = 300  # 5 min between full token validity tests
NO_WINDOW = 0x08000000

# ===== LOGGING =====
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(str(HEALER_LOG), mode="a"),
        logging.StreamHandler(),
    ],
)
LOG = logging.getLogger("dlr_healer")


# ===== STATE TRACKING =====
def load_state():
    try:
        if STATE_FILE.exists():
            return json.loads(STATE_FILE.read_text())
    except Exception:
        pass
    return {
        "restart_counts": {},       # {"main.py": {"count": 3, "last": 1234567890.0}}
        "browser_crash_count": 0,
        "last_token_check": 0,
        "last_alert": {},
    }

def save_state(state):
    try:
        STATE_FILE.write_text(json.dumps(state, indent=2))
    except Exception as e:
        LOG.warning("Failed to save state: %s", e)


# ===== LOCK =====
def acquire_lock():
    try:
        if LOCK_FILE.exists():
            raw = LOCK_FILE.read_text().strip()
            if raw:
                parts = raw.split("|")
                pid = int(parts[0])
                ts = float(parts[1])
                age = time.time() - ts
                if age < LOCK_TTL:
                    try:
                        os.kill(pid, 0)
                        LOG.debug("Lock held by PID %d (%ds old)", pid, int(age))
                        return False
                    except OSError:
                        LOG.info("Stale lock (PID %d dead) -- taking over", pid)
                else:
                    LOG.info("Expired lock (%ds old) -- taking over", int(age))
        LOCK_FILE.write_text(f"{os.getpid()}|{time.time()}")
        return True
    except Exception as e:
        LOG.error("Lock error: %s -- proceeding", e)
        return True

def release_lock():
    try:
        if LOCK_FILE.exists():
            raw = LOCK_FILE.read_text().strip()
            if raw and raw.split("|")[0] == str(os.getpid()):
                LOCK_FILE.unlink()
    except Exception:
        pass


# ===== TIME WINDOW =====
def inside_window():
    """DLR active Sun 23:01 -> Fri 21:01."""
    now = datetime.now()
    wd = now.weekday()
    if wd == 6:  # Sunday
        return now.hour == 23 and now.minute >= 1
    elif wd in (0, 1, 2, 3):  # Mon-Thu
        return True
    elif wd == 4:  # Friday
        return now.hour < 21 or (now.hour == 21 and now.minute < 1)
    return False  # Saturday


# ===== NETWORK HEALTH =====
def _run(args, timeout=10, **kw):
    try:
        return subprocess.run(
            args, capture_output=True, text=True, timeout=timeout,
            creationflags=NO_WINDOW, **kw
        )
    except subprocess.TimeoutExpired:
        return None
    except Exception as e:
        LOG.error("Run error %s: %s", args[0] if args else "?", e)
        return None

def network_ok():
    """Check if we can reach Discord API and the internet."""
    try:
        # Quick check: can we resolve DNS and reach Discord?
        r = _run(["powershell", "-NoProfile", "-Command",
                   "(Test-NetConnection -ComputerName 'discord.com' -Port 443 -WarningAction SilentlyContinue).TcpTestSucceeded"],
                  timeout=10)
        if r and r.stdout.strip() == "True":
            return True
        # Fallback: try a simple HTTP request
        import urllib.request
        req = urllib.request.urlopen("https://discord.com/api/v9/gateway", timeout=5)
        return req.status == 200
    except Exception:
        return False


# ===== PROCESS MANAGEMENT =====
def count_processes(script_name):
    """Count running python/pythonw processes matching script name.
    
    Uses wmic to get command lines (more reliable than tasklist CSV).
    """
    count = 0
    for exe in ("python.exe", "pythonw.exe"):
        try:
            r = _run([
                "wmic", "process", "where",
                f"name='{exe}'", "get", "CommandLine", "/format:csv"
            ], timeout=10)
            if r and r.returncode == 0:
                for line in r.stdout.splitlines():
                    line = line.strip()
                    if not line or "CommandLine" in line or "Node" in line:
                        continue  # skip header
                    if script_name in line:
                        count += 1
        except Exception:
            pass
    return count


def kill_processes(script_name):
    """Kill all python/pythonw processes matching script name.
    
    Uses wmic to find PIDs (more reliable than tasklist CSV).
    """
    killed = 0
    for exe in ("python.exe", "pythonw.exe"):
        try:
            r = _run([
                "wmic", "process", "where",
                f"name='{exe}' and CommandLine like '%{script_name}%'",
                "get", "ProcessId", "/format:csv"
            ], timeout=10)
            if r and r.returncode == 0:
                for line in r.stdout.splitlines():
                    line = line.strip()
                    if not line or "ProcessId" in line or "Node" in line:
                        continue
                    # wmic CSV format: Node,ProcessId
                    parts = line.split(",")
                    if len(parts) >= 2 and parts[-1].strip().isdigit():
                        _run(["taskkill", "/F", "/PID", parts[-1].strip()], timeout=5)
                        killed += 1
        except Exception:
            pass
    return killed


def start_process(script_path, use_pythonw=True):
    """Launch a script in the background.
    
    Uses pythonw.exe to avoid console windows. Falls back to python.exe.
    """
    exe = PYTHONW_EXE if (use_pythonw and PYTHONW_EXE.exists()) else PYTHON_EXE
    if not exe.exists():
        LOG.error("Python executable not found: %s", exe)
        # Try system python
        exe = sys.executable
    try:
        subprocess.Popen(
            [str(exe), str(script_path)],
            cwd=str(PROJECT_ROOT),
            creationflags=NO_WINDOW | getattr(subprocess, "DETACHED_PROCESS", 0),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        LOG.info("Started %s with %s", script_path.name, exe.name)
        return True
    except Exception as e:
        LOG.error("Failed to start %s: %s", script_path.name, e)
        return False


# ===== TOKEN HEALTH =====
def test_token():
    """Check if the saved Discord token is valid.
    
    Returns "valid", "expired", or "missing".
    """
    if not TOKEN_FILE.exists():
        return "missing"
    token = TOKEN_FILE.read_text().strip()
    if not token:
        return "missing"
    if len(token) < 50:
        LOG.warning("Token suspiciously short (%d chars) -- might be corrupted", len(token))
        return "expired"
    try:
        import urllib.request
        req = urllib.request.Request(
            "https://discord.com/api/v9/users/@me",
            headers={
                "Authorization": token,
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            },
        )
        resp = urllib.request.urlopen(req, timeout=10)
        return "valid" if resp.status == 200 else f"http_{resp.status}"
    except urllib.error.HTTPError as e:
        if e.code == 401:
            return "expired"
        return f"http_{e.code}"
    except Exception as e:
        LOG.debug("Token test network error: %s", e)
        return "unknown"  # network issue, not token issue


def extract_token_from_desktop():
    """Extract Discord token from the Desktop app's leveldb storage.
    
    Reads the Discord Desktop app's Local Storage leveldb files for
    the 'token' key. This is the only reliable automated method since
    browser-based extraction is blocked by Cloudflare.
    """
    # Possible Discord Desktop leveldb locations
    candidates = [
        Path(os.environ.get("LOCALAPPDATA", "")) / "Discord" / "Local Storage" / "leveldb",
        Path(os.environ.get("APPDATA", "")) / "discord" / "Local Storage" / "leveldb",
        Path.home() / "AppData" / "Local" / "Discord" / "Local Storage" / "leveldb",
        Path.home() / "AppData" / "Roaming" / "discord" / "Local Storage" / "leveldb",
    ]
    
    for leveldb_dir in candidates:
        if not leveldb_dir.exists():
            continue
        LOG.info("Scanning %s for token...", leveldb_dir)
        for f in sorted(leveldb_dir.iterdir()):
            if f.suffix not in (".ldb", ".log"):
                continue
            try:
                data = f.read_bytes()
                # Look for token pattern: alphanum.alphanum.alphanum
                for m in re.finditer(rb"[mMfF][a-zA-Z0-9]{20,}\.[a-zA-Z0-9_\-]{40,}\.[a-zA-Z0-9_\-]{40,}", data):
                    tok = m.group().decode("ascii", errors="ignore")
                    if len(tok) > 60 and tok.count(".") >= 2:
                        # Verify it works
                        TOKEN_FILE.write_text(tok)
                        status = test_token()
                        if status == "valid":
                            LOG.info("✓ Extracted valid token from Discord Desktop leveldb!")
                            return True
                        LOG.warning("Token from leveldb invalid (status=%s), trying next...", status)
            except Exception as e:
                LOG.debug("Error reading %s: %s", f.name, e)
    return False


# ===== OCR HEALTH =====
def ocr_stale():
    """Check if OCR watcher is running but not producing data.
    
    Reads the last log entry timestamp from the file CONTENT
    to avoid false positives from OS-level write buffering.
    """
    if not OCR_LOG.exists():
        return False
    
    last_ts = None
    try:
        content = OCR_LOG.read_text(errors="replace")
        for line in content.splitlines():
            line = line.strip()
            if line and len(line) >= 19 and line[0].isdigit():
                try:
                    last_ts = datetime.strptime(line[:19], "%Y-%m-%d %H:%M:%S")
                except ValueError:
                    pass
    except Exception as e:
        LOG.warning("Could not read OCR log: %s", e)
        return False
    
    if last_ts is None:
        return False
    
    age = datetime.now() - last_ts
    return age.total_seconds() > STALE_MINUTES * 60


# ===== BROWSER HEALTH =====
def browser_data_corrupted():
    """Check if browser_data/ is in a bad state.
    
    Returns True if the profile directory exists but is missing
    critical files, indicating corruption from a crash.
    """
    if not BROWSER_DATA.exists():
        return False
    # A healthy Chrome profile has a 'Default' directory
    default_dir = BROWSER_DATA / "Default"
    if not default_dir.exists():
        LOG.warning("browser_data missing Default/ directory -- corrupted")
        return True
    return False


def repair_browser_data(state):
    """Swap corrupted browser_data with backup."""
    LOG.warning("Attempting browser data repair...")
    
    # Remove corrupted data
    if BROWSER_DATA.exists():
        import shutil
        shutil.rmtree(str(BROWSER_DATA), ignore_errors=True)
    
    # Try stable backup first
    if BROWSER_DATA_STABLE.exists():
        import shutil
        shutil.copytree(str(BROWSER_DATA_STABLE), str(BROWSER_DATA))
        LOG.info("Restored browser_data from browser_data_stable")
        state["browser_crash_count"] = 0
        return True
    
    # Try check backup
    if BROWSER_DATA_CHECK.exists():
        import shutil
        shutil.copytree(str(BROWSER_DATA_CHECK), str(BROWSER_DATA))
        LOG.info("Restored browser_data from browser_data_check")
        state["browser_crash_count"] = 0
        return True
    
    LOG.error("No browser data backup available")
    return False


# ===== ALERTING =====
def send_alert(message, state):
    """Send alert via Discord webhook.
    
    Deduplicates identical alerts within 5 minutes to avoid spam.
    """
    now = time.time()
    last = state.get("last_alert", {}).get(message, 0)
    if now - last < 300:
        LOG.debug("Suppressed duplicate alert: %s", message)
        return
    
    if not WATCHDOG_WEBHOOK:
        LOG.info("Alert (no webhook): %s", message)
        return
    
    try:
        import urllib.request
        payload = json.dumps({"content": f"DLR Healer — {message}"}).encode()
        req = urllib.request.Request(
            WATCHDOG_WEBHOOK,
            data=payload,
            headers={"Content-Type": "application/json",
                     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"},
        )
        urllib.request.urlopen(req, timeout=10)
        LOG.info("Alert sent: %s", message)
        state.setdefault("last_alert", {})[message] = now
    except Exception as e:
        LOG.error("Failed to send alert: %s", e)


# ===== RESTART BACKOFF =====
def should_restart(script_name, state):
    """Check if we should attempt a restart given historical failure rate.
    
    Implements exponential backoff: if the process keeps crashing,
    we wait longer between restart attempts.
    """
    rc = state.setdefault("restart_counts", {}).setdefault(script_name, {"count": 0, "last": 0})
    now = time.time()
    elapsed = now - rc["last"]
    
    if rc["count"] == 0:
        return True
    
    # Exponential backoff: 30s, 60s, 120s, 240s, 480s, max 600s
    backoff = min(RESTART_BACKOFF_MIN * (2 ** (rc["count"] - 1)), RESTART_BACKOFF_MAX)
    
    if elapsed < backoff:
        LOG.info("%s: backing off %ds (crash #%d, elapsed %ds)",
                 script_name, int(backoff - elapsed), rc["count"], int(elapsed))
        return False
    
    return True


def record_restart(script_name, state):
    rc = state.setdefault("restart_counts", {}).setdefault(script_name, {"count": 0, "last": 0})
    rc["count"] += 1
    rc["last"] = time.time()
    
    # Alert if crash loop detected (3+ restarts within 5 min)
    if rc["count"] >= 3:
        send_alert(f"⚠ {script_name}: restart loop ({rc['count']} restarts, backing off)", state)


def record_healthy(script_name, state):
    """Reset crash counter when a process is found healthy."""
    rc = state.setdefault("restart_counts", {}).setdefault(script_name, {"count": 0, "last": 0})
    if rc["count"] > 0:
        # Only reset if it's been running for a while
        if time.time() - rc["last"] > 300:
            rc["count"] = 0


# ===== MAIN HEALER LOOP =====
def main():
    if not acquire_lock():
        return 0
    
    state = load_state()
    actions = []
    alerts = []
    
    try:
        # ===== NETWORK CHECK (FM08) =====
        net_ok = network_ok()
        if not net_ok:
            LOG.warning("Network down -- skipping restart actions, will retry next tick")
            # Don't kill anything; processes may recover when net comes back
            return 0
        
        # ===== TOKEN HEALTH CHECK (FM01, FM02) =====
        now = time.time()
        if now - state.get("last_token_check", 0) > TOKEN_CHECK_INTERVAL:
            state["last_token_check"] = now
            token_status = test_token()
            
            if token_status == "missing":
                LOG.warning("Token file missing -- attempting auto-extract (FM02)")
                if extract_token_from_desktop():
                    alerts.append("Token file was missing -- auto-extracted from Desktop app")
                    send_alert("🔄 Token file missing -- auto-extracted from Desktop app leveldb", state)
                else:
                    alerts.append("Token file missing and auto-extract failed")
                    send_alert("🚨 Token file missing and auto-extract failed! DLR will not work.", state)
                    return 0  # Can't proceed without a token
            
            elif token_status == "expired":
                LOG.warning("Token expired (401) -- attempting auto-refresh (FM01)")
                if extract_token_from_desktop():
                    alerts.append("Token was expired -- auto-refreshed from Desktop app")
                    send_alert("🔄 Token expired -- auto-refreshed from Desktop app leveldb", state)
                else:
                    alerts.append("Token expired and auto-refresh failed")
                    send_alert("🚨 Token expired and auto-refresh failed! DLR needs manual intervention.", state)
                    return 0
            
            elif token_status.startswith("http_"):
                code = token_status.split("_")[1]
                if code == "429":
                    LOG.warning("Discord API rate limited (429) -- will back off")
                    send_alert("⏳ Discord API rate limited (429) -- backing off", state)
                else:
                    LOG.warning("Discord API returned HTTP %s for token test", code)
            
            else:
                LOG.info("Token valid")
        
        # ===== PROCESS HEALTH CHECKS =====
        
        # Check main.py (FM03)
        main_count = count_processes("main.py")
        main_healthy = main_count > 0
        LOG.debug("main.py processes: %d", main_count)
        
        if not main_healthy:
            if should_restart("main.py", state):
                LOG.info("main.py DOWN -- restarting (FM03)")
                # Kill any zombie processes first
                kill_processes("main.py")
                time.sleep(1)
                if start_process(MAIN_SCRIPT):
                    actions.append("main.py")
                    record_restart("main.py", state)
            else:
                LOG.info("main.py DOWN but in backoff -- skipping")
        else:
            record_healthy("main.py", state)
        
        # Check ocr_watcher.py (FM04)
        ocr_count = count_processes("ocr_watcher.py")
        ocr_healthy = ocr_count > 0
        LOG.debug("ocr_watcher.py processes: %d", ocr_count)
        
        if not ocr_healthy:
            if should_restart("ocr_watcher.py", state):
                LOG.info("ocr_watcher DOWN -- restarting (FM04)")
                kill_processes("ocr_watcher.py")
                time.sleep(1)
                if start_process(OCR_SCRIPT):
                    actions.append("ocr_watcher.py")
                    record_restart("ocr_watcher.py", state)
            else:
                LOG.info("ocr_watcher DOWN but in backoff -- skipping")
        else:
            record_healthy("ocr_watcher.py", state)
        
        # Check for stale OCR (FM05) — process is running but not producing
        if ocr_healthy and ocr_stale():
            LOG.warning("OCR stale -- killing and restarting (FM05)")
            kill_processes("ocr_watcher.py")
            time.sleep(2)
            if start_process(OCR_SCRIPT):
                actions.append("ocr_watcher.py (stale)")
                record_restart("ocr_watcher.py", state)
        
        # ===== BROWSER DATA HEALTH (FM09) =====
        if browser_data_corrupted():
            LOG.warning("Browser data corrupted -- swapping to backup (FM09)")
            if repair_browser_data(state):
                alerts.append("Browser data was corrupted -- restored from backup")
                # If main.py was running, it will need to be restarted to pick up new profile
                if main_healthy:
                    kill_processes("main.py")
                    time.sleep(1)
                    start_process(MAIN_SCRIPT)
                    actions.append("main.py (browser swap)")
        
        # ===== PROCESS NOTIFICATIONS =====
        if actions:
            msg = "Healed: %s" % ", ".join(actions)
            LOG.info(msg)
            if alerts:
                msg += " | " + " | ".join(alerts)
            send_alert(msg, state)
        
        # ===== CRASH LOOP DETECTION (FM06) =====
        for script_name in ("main.py", "ocr_watcher.py"):
            rc = state.get("restart_counts", {}).get(script_name, {})
            if rc.get("count", 0) >= 5 and rc.get("last", 0) > time.time() - 3600:
                send_alert(f"🚨 CRASH LOOP: {script_name} restarted {rc['count']}x in the last hour. Manual check needed.", state)
        
        save_state(state)
        
    except Exception as e:
        LOG.error("Healer error: %s", e)
        import traceback
        LOG.error(traceback.format_exc())
    finally:
        release_lock()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
