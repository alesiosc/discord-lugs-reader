# Discord Lugs Reader (DLR)

Automated Discord ticker monitoring system. Uses Playwright to read messages from a Discord channel, extracts ticker data (NQ, ES, YM, GC, RTY, CL) via OCR/screenshot, and forwards parsed messages to a configured webhook.

## Quick Start

1. Configure credentials in `discord_lugs_portable_venv/app/login.env`
2. Run `RUN_LUGS_READER.bat` to launch (starts both the reader and OCR watcher)
3. Messages are read from the configured Discord channel and posted to the webhook

## Config

- `DISCORD_CHANNEL_URL` — channel to monitor
- `WEBHOOK_URL` — where parsed tickers get posted
- `HEADLESS_MODE` — `true` for invisible browser, `false` for debugging
