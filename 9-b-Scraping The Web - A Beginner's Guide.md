Welcome, Apprentice, to the Grimoire of Web Scraping.
Within these pages lies the scattered wisdom of a master, a chaotic collection of secrets and powerful arts now brought into order. This is not a mere book of spells, but a guide to seeing the web's hidden architecture, gathering its boundless knowledge, and navigating its guardians with respect and skill.
Forget the crude methods of the past. The path you are about to walk is one of elegance, precision, and deep understanding. Study these chapters, practice these techniques, and the web's secrets will unfold before you. Your journey begins now.
Part I: The First Steps - Learning to See the Web
Reconnaissance: Drawing Your Map
A scraper who acts without looking is a scraper who fails. The first and most crucial step is to study your target. Understand its structure, watch how it breathes, and learn its secret pathways before you write a single line of code.
Inspect Network Traffic: Use your browser's Developer Tools (F12) and watch the "Network" tab (filtered to "Fetch/XHR") to see how data is secretly delivered to the page, often revealing a hidden API.
GATHER SITE ANTI BOT TECHNIQUES USED FIRST: Before writing code, use a tool to analyze the target and identify which anti-bot system it uses (e.g., Cloudflare, PerimeterX, Akamai), as this determines your entire strategy.
ShieldEye: A GitHub tool designed to analyze a target URL and tell you which specific anti-bot guardian (like Cloudflare or Datadome) it uses.
Rebrowser Bot Detector: A set of modern tests to check how easily your automated browser can be detected, helping you understand a site's defenses.
Check robots.txt: Always visit www.example.com/robots.txt to see the rules the website owners have set for bots; respecting these is the first step in ethical scraping.
Sources: The Scraper's Library
No master is self-made. They stand on the shoulders of giants and learn from a library of sacred texts. These articles and guides are your foundation.
Roll your own bot detection: fingerprinting/JavaScript (part 1): An essential article from blog.castle.io explaining from the ground up how anti-bot systems use browser fingerprinting to detect automation.
From Puppeteer stealth to Nodriver: A guide from blog.castle.io that details the evolution of anti-bot frameworks and the cat-and-mouse game between scrapers and websites.
Why traditional bot detection techniques are not enough: An article from blog.castle.io that explains the limitations of old methods (like IP bans and WAFs) and what is needed to succeed in 2025.
This is How I Scrape 99% of Sites (John Watson Rooney): A video transcript outlining the modern API-first approach to scraping that bypasses most HTML-based challenges.
How dare you trust the user agent for bot detection?: A blog.castle.io article explaining that the User-Agent is a "claimed identity" that must be verified against other signals to detect inconsistencies.
Libraries: Your First Magic Wands
These are the core tools of your craft. Each is a powerful wand for a specific purpose. Master them, and you can conjure data from the most stubborn of sites.
curl-cffi: A Python library that is the modern replacement for requests, designed to impersonate real browsers and bypass TLS fingerprinting blocks.
rnet: A high-performance Python networking library built in Rust, designed for extreme speed and stealthy requests that can bypass WAFs like Cloudflare.
Scrapy: A powerful, all-in-one Python framework for building large-scale, structured web crawlers and managing complex scraping projects.
Playwright: A modern browser automation library from Microsoft used to control browsers like Chrome and Firefox for scraping dynamic, JavaScript-heavy websites.
Selenium: A classic browser automation framework used to control a web browser, essential for websites that require user interaction to display data.
Beautiful Soup: A Python library that makes it easy to parse and extract data from website code (HTML and XML) once you have fetched it.
Scrapling: An all-in-one scraping library that provides different "fetchers" for static, dynamic, and anti-bot protected sites.
Pydantic: A Python library for data validation and settings management, used to create structured models for the data you scrape.
hrequests: A Python library designed to mimic human browser requests, useful for bypassing bot detection.
GitHubs: Blueprints and Spellbooks
These repositories are the collected spellbooks of masters who came before you. Study their code to find powerful tools, clever techniques, and inspiration for your own work.
lexiforest/curl_cffi: The essential Python library for making HTTP requests that impersonate real browsers to bypass TLS fingerprinting.
0x676e67/rnet: A high-performance Python networking library for making stealthy, high-speed requests that can defeat WAFs like Cloudflare.
omkarcloud/botasaurus: A powerful, user-friendly framework specifically built to defeat advanced anti-bot systems like Cloudflare.
ultrafunkamsterdam/nodriver: A revolutionary Python framework that avoids Chrome DevTools Protocol (CDP), making it exceptionally difficult for advanced bot detectors to spot.
D4Vinci/Scrapling: A versatile, all-in-one scraping library with different "fetchers" for static sites, dynamic JS-heavy sites, and sites with anti-bot systems.
diegopzz/ShieldEye: A reconnaissance tool to run against a target URL to determine which anti-bot system it's using.
scrapy/scrapy: The core framework for building large-scale, structured web crawlers in Python.
ScrapeGraphAI/Scrapegraph-ai: An AI-powered library that lets you scrape websites using natural language prompts instead of writing code.
unclecode/crawl4ai: A specialized crawler designed to take a URL and convert its content into a clean format optimized for Large Language Models (LLMs).
scrapeless-ai/scrapeless-mcp-server: A server that acts as an unblockable web interface for AI models, allowing them to perform complex, multi-step scraping tasks.
seleniumbase/SeleniumBase: A powerful framework built on Selenium that includes an "Undetected Chromedriver" mode to automatically hide automation.
berstend/puppeteer-extra-plugin-stealth: A foundational plugin for the Puppeteer framework that applies a suite of evasions to make headless browsers harder to detect.
FlareSolverr/FlareSolverr: A standalone proxy server you run that uses a headless browser to solve Cloudflare challenges for your main scraper.
Pr0t0ns/perimeterx-solution: A specialized solver for websites protected by PerimeterX, focusing on generating correct sensor data to bypass its checks.
justhyped/... (Hyper Solutions SDK): A Python script designed to solve Akamai's crypto challenge by reverse-engineering its sensor data and cookie generation process.
sneakykiwi/bmak-tools: A tool written in Go for generating valid Akamai cookies, an alternative to other Akamai solvers.
dessant/buster: A CAPTCHA solver extension that automatically solves audio CAPTCHA challenges using speech-to-text APIs.
art3m4ik3/cloudflare-solver: A specialized Node.js library for solving Cloudflare's JavaScript challenges, meant to be integrated into a larger script.
Xetera/ghost-cursor: A library for Playwright and Puppeteer that generates realistic, human-like mouse movements to bypass behavioral anti-bot systems.
Kaliiiiiiiiii-Vinyzu/patchright-python: An advanced browser automation framework focused on patching fingerprinting leaks at a low level to avoid detection.
kaliiiiiiiiii/Selenium-Driverless: A modified version of Selenium that aims to be "driverless," making the browser instance much harder to fingerprint.
daijro/camoufox: A JavaScript anti-detect automation framework that removes known static fingerprinting attributes like navigator.webdriver.
rebrowser/rebrowser-playwright: A drop-in replacement for Playwright that is patched to pass modern automation detection tests.
rebrowser/rebrowser-puppeteer: The Puppeteer equivalent of rebrowser-playwright, offering enhanced stealth capabilities.
ZFC-Digital/puppeteer-real-browser: A Node.js package that controls a real, installed Chrome browser (not headless) to bypass some detection methods.
MiddleSchoolStudent/BotBrowser: An advanced stealth browser where the Chromium source code itself is modified to eliminate fingerprinting leaks.
pim97/scrappey.js: A Node.js web scraping library that focuses on bypassing Cloudflare and other anti-bot measures.
lafftar/requestSpeedTest: A benchmark project demonstrating how to achieve massive request throughput by combining rnet with OS-level tuning.
ChrisRoark/beagle_scraper: A purpose-built scraper whose code can be studied as an example of how to tackle a specific website.
Part II: The Art of Extraction - Gathering Your Ingredients
Scraping: The Core Techniques
This is the heart of the craft: reaching into the web's code and pulling out the data you seek. To do this, you must speak the language of the web itself.
Parse LD+JSON: Look for <script type="application/ld+json"> tags in a page's HTML, as they often contain clean, structured data that is much easier to parse than the rest of the page.
Selector Caching: A technique where you store a website's CSS selectors in a JSON file, allowing your scraper to adapt if the site layout changes slightly.
Parsing with CSS Selectors: Use libraries like Beautiful Soup or select to find and extract data from HTML by targeting elements with specific IDs, classes, or attributes.
Handling JSON: Learn to work directly with JSON data returned from backend APIs, which is often cleaner and more reliable than scraping HTML.
Browser Automation: Commanding a Golem
Some websites are enchanted with JavaScript, refusing to reveal their secrets until a user interacts with them. For these, you must command a golem—an automated browser that can click, scroll, and type as a human would.
Playwright: A modern browser automation library for controlling browsers, excellent for scraping dynamic and interactive websites.
Selenium: The classic tool for automating web browsers, allowing your scripts to interact with buttons, forms, and other dynamic elements.
Puppeteer: A Node.js library that provides a high-level API to control headless Chrome, ideal for scraping JavaScript-heavy websites.
SeleniumBase (in UC Mode): A powerful framework that enhances Selenium with an "Undetected Chromedriver" mode to automatically hide the signs of automation.
Nodriver: An advanced Python framework that avoids using the Chrome DevTools Protocol (CDP), making it extremely difficult for anti-bot systems to detect.
Patchright: An advanced automation framework focused on patching fingerprinting leaks at a low level to create a stealthy browser.
puppeteer-extra-plugin-stealth: A popular plugin for Puppeteer that applies a suite of evasions to make a standard headless browser much harder to detect.
--disable-blink-features=AutomationControlled: A Chrome command-line argument used to hide the basic navigator.webdriver flag from bot detectors.
API Backend Endpoints and TLS Fingerprinting: Finding Secret Passages
The most elegant scraping does not break down the front door; it finds the secret passages. The most valuable data is often retrieved via hidden APIs, but accessing them requires you to look like a trusted visitor.
Find the Backend API: The most effective modern scraping technique: use browser developer tools to find the hidden API a website uses to load its own data, then request the data directly.
TLS Fingerprinting: A technique where servers inspect the signature of your connection (JA3 hash) to see if it comes from a known script or a real browser.
curl-cffi: The primary tool for bypassing TLS fingerprinting, as it allows your Python script to impersonate the connection signature of a real browser like Chrome.
rnet: A high-performance Python library built on Rust, designed to impersonate browser TLS/JA3 fingerprints and make requests at very high speeds.
Replaying Network Calls: A method where you look at the network call that supplies data to the page, then replay that exact call (with identical headers and cookies) in your script.
Part III: The Cloak of Invisibility - Avoiding Detection
Anti-Bot Detection: Understanding the Guardians
To walk unseen, you must first understand how the guardians see. Learn their methods, and you will learn how to avoid their gaze.
Browser Fingerprinting: The technique of collecting a set of attributes from a browser (screen resolution, fonts, WebGL renderer) to create a unique signature and detect inconsistencies.
Inconsistency Detection: The core of modern bot detection, where a system checks if your claimed identity (e.g., Chrome on Windows) matches your technical signals (e.g., a Mac-specific WebGL renderer).
navigator.webdriver: The simplest automation indicator; a JavaScript property that is true when a browser is being controlled by a framework like Selenium or Playwright.
CDP (Chrome DevTools Protocol) Detection: An advanced technique where websites detect automation by looking for side effects caused by the protocol that tools like Puppeteer and Playwright use to control the browser.
Behavioral Analysis: The practice of tracking mouse movements, scrolling patterns, and request timing to distinguish a predictable bot from an erratic human.
IP Reputation: Blocking or challenging requests that come from known datacenter IP addresses or IPs associated with malicious activity.
Anti-Cloudflare and Captcha: Solving the Riddles
Some paths are guarded by riddles and magical barriers. These tools and services are your keys to solving them.
Botasaurus: A powerful, open-source framework specifically designed to defeat advanced anti-bot systems, with a strong reputation for handling Cloudflare.
FlareSolverr: A proxy server you run locally that uses a headless browser to solve Cloudflare challenges before passing the clean HTML to your scraper.
Scrapling's StealthyFetcher: A tool within the Scrapling library that uses a modified browser and fingerprint spoofing to bypass systems like Cloudflare Turnstile.
Buster: An open-source CAPTCHA solver that focuses on solving audio challenges by using speech-to-text APIs.
CAPTCHA Solving Services (2Captcha, Anti-CAPTCHA): Commercial services that solve CAPTCHAs for your bot via an API call, often using a combination of AI and human workers.
AI-based CAPTCHA Solvers (CapSolver): Modern solvers that rely on AI models to solve visual and audio recognition challenges automatically and cheaply.
Humanizing Behaviour: Walking Without Leaving Footprints
To appear human, you must act human. Introduce flaws, randomness, and the subtle imperfections that define natural interaction.
User Agent Rotation: The practice of changing your User-Agent header to mimic different real browsers, but it must be done consistently with other headers.
Randomized Delays: Adding random waits between requests to break up robotic, predictable scraping patterns and reduce server load.
Exponential Backoff: A crucial error handling strategy where you wait for progressively longer periods after a failed request before retrying.
Realistic Mouse Movements (ghost-cursor): Instead of instantly teleporting the cursor, use a library to generate curved, human-like mouse paths to bypass behavioral detectors.
Mimic Header Consistency: Ensure all HTTP headers (User-Agent, Accept-Language, Sec-CH-UA) are consistent with the browser profile you are pretending to be.
Sync Timezones: Make sure your browser's timezone is in sync with the timezone of your proxy to avoid a simple but powerful detection signal.
Rotating Proxies: The Mask of a Thousand Faces
A single face seen a thousand times is instantly suspicious. To scrape at scale, you must wear a thousand different masks.
Proxy Types: Understand the differences between datacenter (cheap, easily detected), residential (hard to detect, uses real home IPs), mobile (hardest to detect), and ISP proxies.
Total Cost of Ownership: Realize that the cost of proxies is not just the price per GB, but also includes wasted bandwidth from headers, failed requests, and challenge pages.
Sticky Sessions: A technique where you use the same proxy IP for a short period (e.g., 5 minutes) to mimic a real user session before rotating.
Proxy Pools: Use a large pool of proxies to spread requests across thousands of different IP addresses, making it difficult for a website to identify your scraper.
Part IV: Advanced Alchemy & Best Practices
Deep Research: Scrying for Deeper Truths
The true master goes beyond simple data collection. They investigate, correlate, and uncover the deeper truths hidden within the web's fabric.
Reverse-Engineer Anti-Bot JavaScript: A highly advanced technique where you analyze the client-side protection scripts to understand their logic and emulate them in your scraper.
Use AI for Anomaly Detection: Employ machine learning models to analyze traffic patterns and dynamically adapt your scraping strategy to avoid triggering new blocking rules.
Analyze Fingerprinting Articles: Study the detailed articles from blog.castle.io to understand how anti-detect browsers work and how defenders spot inconsistencies in navigator.deviceMemory, canvas, and WebGL fingerprints.
Investigate Attack Infrastructure: Read case studies on how attackers use CAPTCHA solvers, disposable emails, and custom domains to understand the full ecosystem of abuse.
OCR (Optical Character Recognition): Reading the Unreadable
Not all knowledge is written in text. Some is trapped in images. OCR is the art of reading this unreadable script.
DeepSeek-OCR: A powerful open-source OCR tool for extracting text from images.
PaddleOCR: Another high-quality OCR library for recognizing text within images or screenshots.
Extracting Text by Size: A technique where you use an OCR tool like pytesseract to get the bounding boxes of all text, then filter for only the largest text based on its height.
Recommended Practices: The Scraper's Code of Conduct
Power without discipline leads to chaos. A master's work is clean, efficient, and built to last.
Create a Virtual Environment (venv): Always isolate your project's dependencies to avoid conflicts and ensure reproducibility.
Use a .env File: Store all sensitive information (API keys, passwords, proxy credentials) in a .env file and never commit it to version control.
Plan Your Project: Create markdown files like PLANNING_YOUR_PROJECT.md and HOW_TO_RUN.md to document your goals, process, and setup instructions.
Create a .gitignore file: Prevent sensitive files, virtual environments, and logs from being accidentally committed to your repository.
Make Scripts Configurable: Place all settings (URLs, selectors, delays) at the top of your script or in a separate configuration file for easy modification.
Provide Terminal Feedback: Make your scripts user-friendly by telling the user what is happening, showing progress bars, and estimating completion times.
Error Handling: The Art of Resilience
The web is ever-changing and unpredictable. A master's scraper does not break; it bends, adapts, and continues its work.
Intelligent Retry Logic: Don't just retry on failure. Implement exponential backoff, which waits for progressively longer durations between retries to handle temporary blocks or network errors.
Selector Fallbacks: If a CSS selector fails, have a backup XPath or an alternative selector ready to try before giving up on the element.
Adaptive Scraping (Scrapling): Use intelligent tools that can relocate elements after a website changes its design, making your scraper more resilient.
Handle HTTP Status Codes: Check the status code of every response and handle errors like 403 Forbidden, 429 Too Many Requests, and 5xx server errors gracefully.
Security Best Practices: Protecting Yourself and Others
With great power comes great responsibility. The ethical scraper gathers knowledge without causing harm.
Respect robots.txt: Always check and honor the rules set out in a website's robots.txt file.
Rate Limit Your Requests: Never hammer a server. Use delays and throttling to scrape at a reasonable pace and avoid impacting the site's performance for real users.
Sanitize Scraped Content: If passing data to an LLM or another system, clean it first to prevent prompt injection or other security vulnerabilities.
Use APIs When Available: If a website provides a public API, always prefer using it over scraping, as it is the officially sanctioned method of accessing data.
Useful MCP (Miscellaneous Cool Projects): The Cabinet of Curiosities
Here lie unique artifacts and powerful constructs that defy simple categorization but hold immense value for the curious apprentice.
Scrapeless MCP Server: An innovative project that connects Large Language Models (like ChatGPT and Claude) to the live web, allowing them to perform complex, real-time scraping and browser automation tasks.
Crawl4ai: A specialized crawler designed to scrape a website and convert its content into clean, structured Markdown, perfect for feeding into an AI model for analysis.
Jina.ai Reader: A tool that can take a URL and convert the page content into clean Markdown, useful for preprocessing data.
uv: An extremely fast Python package installer and resolver, written in Rust, that can be used as a high-speed replacement for pip and venv.


# Browser & Network Fingerprinting

This module covers browser and network fingerprinting, a critical aspect of modern web automation and detection systems.

Fingerprinting sits at the intersection of network protocols, cryptography, browser internals, and behavioral analysis. It encompasses the techniques used to identify and track devices, browsers, and users across sessions without relying on traditional identifiers like cookies or IP addresses.

## Why This Matters

Every browser connection to a website exposes multiple characteristics, from the precise order of TCP options in network packets, to GPU-specific canvas rendering, to JavaScript execution timing patterns. Individually, these characteristics may appear innocuous. Combined, they create a fingerprint that can uniquely identify a device or browser instance.

For automation engineers, bot developers, and privacy-conscious users, understanding fingerprinting is essential for building effective detection evasion systems and understanding how tracking mechanisms operate at a technical level.

**Multi-Layer Detection Systems**

Modern anti-bot systems employ comprehensive analysis across multiple layers:

- **Network-level**: TCP/IP stack behavior, TLS handshake patterns, HTTP/2 settings
- **Browser-level**: Canvas rendering, WebGL vendor strings, JavaScript property enumeration
- **Behavioral**: Mouse movement entropy, keystroke timing, scroll patterns

A single inconsistency (such as a Chrome User-Agent with Firefox TLS fingerprint) can trigger immediate blocking.

## Module Scope and Methodology

Fingerprinting techniques are documented across multiple sources with varying levels of accessibility and reliability:

- Academic papers (often paywalled and theoretical)
- Browser source code (millions of lines to analyze)
- Security researcher blogs (technical but fragmented)
- Anti-bot vendor whitepapers (marketing-focused, details omitted)
- Underground forums (practical but unreliable)

This module centralizes, validates, and organizes this knowledge into a cohesive technical guide. Every technique described here has been:

- **Verified** against browser source code and RFCs
- **Tested** in real automation scenarios
- **Cited** with authoritative references
- **Explained** from first principles to implementation

## Module Structure

This module is organized into three progressive layers, from network fundamentals to practical evasion techniques:

### 1. Network-Level Fingerprinting

[**Network Fingerprinting**](https://pydoll.tech/docs/deep-dive/fingerprinting/network-fingerprinting/)

Covers device identification through network behavior at the transport and session layers, before browser rendering begins.

- **TCP/IP fingerprinting**: TTL, window size, option ordering
- **TLS fingerprinting**: JA3/JA4, cipher suites, ALPN negotiation
- **HTTP/2 fingerprinting**: SETTINGS frames, priority patterns
- **Tools & techniques**: p0f, Nmap, Scapy, tshark analysis

**Technical significance**: Network fingerprints are the most challenging to spoof because they require OS-level modifications. Inconsistencies at this layer are detected before JavaScript execution begins.

### 2. Browser-Level Fingerprinting

[**Browser Fingerprinting**](https://pydoll.tech/docs/deep-dive/fingerprinting/browser-fingerprinting/)

Examines browser identification through JavaScript APIs, rendering engines, and plugin ecosystems at the application layer.

- **Canvas & WebGL fingerprinting**: GPU-specific rendering artifacts
- **Audio fingerprinting**: Subtle differences in audio API output
- **Font enumeration**: Installed fonts reveal OS and locale
- **JavaScript properties**: Navigator object, screen dimensions, timezone
- **Header analysis**: Accept-Language, User-Agent consistency

**Technical significance**: This layer accounts for the majority of detection events. Even with correct network-level fingerprints, exposed automation properties (e.g., `navigator.webdriver`) can trigger blocking.

### 3. Behavioral Fingerprinting

[**Behavioral Fingerprinting**](https://pydoll.tech/docs/deep-dive/fingerprinting/behavioral-fingerprinting/)

Analyzes user interaction patterns to distinguish human behavior from automated systems.

- **Mouse movement analysis**: Trajectory curvature, velocity profiles, Fitts's Law compliance
- **Keystroke dynamics**: Typing rhythm, dwell time, flight time, bigram patterns
- **Scroll patterns**: Momentum, inertia, deceleration curves
- **Event sequences**: Natural interaction ordering (mousemove → click), timing analysis
- **Machine learning**: ML models trained on billions of behavioral signals

**Technical significance**: Behavioral analysis can detect automation even when network and browser fingerprints are correctly spoofed. This layer is particularly challenging because it requires replicating biomechanical human behavior patterns.

### 4. Evasion Techniques

[**Evasion Techniques**](https://pydoll.tech/docs/deep-dive/fingerprinting/evasion-techniques/)

Practical implementation of fingerprinting evasion using Pydoll's CDP integration, JavaScript overrides, and architectural features.

- **CDP-based spoofing**: Timezone, geolocation, device metrics
- **JavaScript property overrides**: Redefining navigator objects, canvas poisoning
- **Request interception**: Forcing header consistency
- **Behavioral mimicry**: Human-like timing, entropy injection
- **Detection testing**: Tools to validate your evasion setup

**Technical significance**: This section demonstrates practical application of fingerprinting concepts to real automation scenarios, integrating techniques from all previous layers.

## Who Should Read This

### **You MUST read this if you're:**

- Building automation that interacts with anti-bot protected sites
- Developing scraping infrastructure at scale
- Implementing privacy-preserving browser automation
- Researching bot detection for offensive or defensive purposes

### **This is advanced material if you're:**

- New to network protocols (start with [Network Fundamentals](https://pydoll.tech/docs/deep-dive/network/network-fundamentals/))
- Unfamiliar with CDP (read [Chrome DevTools Protocol](https://pydoll.tech/docs/deep-dive/fundamentals/cdp/) first)
- Just learning Python typing (see [Type System](https://pydoll.tech/docs/deep-dive/fundamentals/typing-system/))

### **This is NOT:**

- A "silver bullet" anti-detection solution (no such thing exists)
- Legal advice on web scraping (consult [Legal & Ethical](https://pydoll.tech/docs/deep-dive/network/proxy-legal/))
- A replacement for respecting robots.txt and rate limits

## The Technical Philosophy

Fingerprinting defense is **not about becoming invisible**—it's about becoming **indistinguishable from legitimate traffic**. This means:

1. **Consistency over perfection**: A perfectly configured Firefox fingerprint is better than a "perfect" but inconsistent Chrome fingerprint
2. **Holistic approach**: You must align network, browser, and behavioral layers
3. **Continuous adaptation**: Fingerprinting techniques evolve monthly; this is a living document

**The Golden Rule**

**Every layer must tell the same story.** If your TLS fingerprint says "Chrome 120", your HTTP/2 settings must match Chrome 120, your User-Agent must say Chrome 120, and your canvas rendering must produce Chrome 120 artifacts. One mismatch = detection.

## Ethical Considerations

Fingerprinting knowledge is **dual-use technology**:

- **Defensive**: Protect your privacy from invasive tracking
- **Offensive**: Evade detection systems for automation

We trust you to use this knowledge **responsibly and ethically**:

**Recommended practices:**

- Respect website terms of service
- Implement rate limiting and respectful crawling patterns
- Evaluate whether automation is necessary
- Be transparent when appropriate

**Prohibited uses:**

- Fraud, account abuse, or illegal activities
- Overwhelming servers with aggressive scraping
- Weaponizing this knowledge without understanding consequences

## Ready to Dive Deep?

Fingerprinting is a complex and technical domain that requires systematic study. Understanding these techniques is essential for effective web automation in environments with detection systems.

Begin with [**Network Fingerprinting**](https://pydoll.tech/docs/deep-dive/fingerprinting/network-fingerprinting/) to establish foundational knowledge, continue with [**Browser Fingerprinting**](https://pydoll.tech/docs/deep-dive/fingerprinting/browser-fingerprinting/) for application-layer understanding, and conclude with [**Evasion Techniques**](https://pydoll.tech/docs/deep-dive/fingerprinting/evasion-techniques/) for practical implementation.

---

**Documentation Status**

This module represents **extensive research** combining academic papers, browser source code, real-world testing, and community knowledge. Every claim is cited and validated. If you find inaccuracies or have updates, contributions are welcome.


Network-Level Fingerprinting
This document explores fingerprinting at the network protocol level, from TCP/IP characteristics to TLS handshake patterns. Understanding how devices are identified **before the browser even loads** is crucial for evading sophisticated detection systems.

**Module Navigation**

- [**← Fingerprinting Overview**](https://pydoll.tech/docs/deep-dive/fingerprinting/) - Module introduction and philosophy
- [**→ Browser Fingerprinting**](https://pydoll.tech/docs/deep-dive/fingerprinting/browser-fingerprinting/) - Application-layer fingerprinting
- [**→ Evasion Techniques**](https://pydoll.tech/docs/deep-dive/fingerprinting/evasion-techniques/) - Practical countermeasures

For network fundamentals, see [**Network Fundamentals**](https://pydoll.tech/docs/deep-dive/network/network-fundamentals/) and [**Proxy Architecture**](https://pydoll.tech/docs/deep-dive/network/http-proxies/).

**OS-Level Characteristics**

Network fingerprinting operates at layers 3-6 of the OSI model. Unlike browser-level characteristics (modifiable with JavaScript), network-level fingerprints require **OS-level** or **kernel-level** changes to spoof effectively.

## Network-Level Fingerprinting

Network fingerprinting operates at layers 3-7 of the OSI model, analyzing characteristics of network packets, protocols, and connections to identify the client.

### Why Network Fingerprinting Matters

Unlike browser-level fingerprinting (which can be modified with JavaScript), network-level characteristics are:

- **Harder to modify**: Require OS-level or kernel changes
- **More persistent**: Can't be cleared like cookies or localStorage
- **Cross-application**: Same fingerprint across all applications on the device
- **Proxy-resistant**: Some characteristics survive proxy/VPN tunneling

**Layered Fingerprinting**

Sophisticated detection systems use **multiple layers** of fingerprinting. Even if you spoof browser-level characteristics, network-level inconsistencies can reveal automation.

### The OSI Model and Fingerprinting Layers

**Fingerprinting occurs at:**

- **Layer 3 (Network)**: IP TTL, fragmentation behavior
- **Layer 4 (Transport)**: TCP/UDP options, initial sequence numbers, window scaling
- **Layer 6 (Presentation)**: TLS handshake, cipher suites, extensions
- **Layer 7 (Application)**: HTTP headers, HTTP/2 settings, protocol-specific behavior

## TCP/IP Fingerprinting (Layer 3-4)

TCP/IP fingerprinting analyzes characteristics of TCP and IP packets to identify the operating system and network stack implementation.

### TCP Packet Structure

`# TCP header fields used for fingerprinting
{
    'ip_ttl': 64,                    # Initial TTL value (OS-specific)
    'window_size': 65535,            # TCP window size
    'window_scaling': 7,             # Window scale factor
    'mss': 1460,                     # Maximum Segment Size
    'timestamp': True,               # TCP timestamp option
    'sack': True,                    # Selective Acknowledgment
    'options_order': ['MSS', 'SACK_PERM', 'TIMESTAMP', 'NOP', 'WSCALE']
}`

### Key TCP/IP Characteristics

### **1. Time To Live (TTL)**

TTL values are OS-specific and decrease with each network hop:

| **Operating System** | **Initial TTL** | **After 10 Hops** |
| --- | --- | --- |
| **Linux** | 64 | 54 |
| **Windows** | 128 | 118 |
| **macOS** | 64 | 54 |
| **Cisco/Routers** | 255 | 245 |

`# TTL fingerprinting
def detect_os_by_ttl(ttl: int) -> str:
    """
    Detect OS based on TTL value.
    Note: TTL decreases by 1 for each router hop.
    """
    if ttl <= 64:
        return 'Linux/macOS (initial: 64)'
    elif ttl <= 128:
        return 'Windows (initial: 128)'
    elif ttl <= 255:
        return 'Network device (initial: 255)'
    else:
        return 'Unknown'
# Example: Received TTL = 54
# → Original TTL likely 64 (Linux/macOS)
# → Packet traveled through ~10 hops`

**TTL and Proxies**

When using proxies, the TTL value resets at the proxy server. However, inconsistencies can reveal proxy usage:

- User-Agent says "Windows" → TTL suggests Linux (proxy server OS)
- TTL too low for claimed location (suggests VPN/proxy routing)

### **2. TCP Window Size**

Initial TCP window size varies by OS and configuration:

`# Common window sizes by OS
OS_WINDOW_SIZES = {
    'Windows 10': 8192,          # Default
    'Windows 11': 65535,         # More aggressive
    'Linux (recent)': 29200,     # Modern kernels
    'macOS': 65535,              # Optimistic
    'Android': 65535,            # Mobile-optimized
}`

### **3. TCP Options and Their Order**

The presence and **order** of TCP options creates a unique fingerprint:

`# Example TCP options in SYN packet
{
    # Windows 10 typical order
    'windows': ['MSS', 'NOP', 'WSCALE', 'NOP', 'NOP', 'SACK_PERM'],
    # Linux typical order  
    'linux': ['MSS', 'SACK_PERM', 'TIMESTAMP', 'NOP', 'WSCALE'],
    # macOS typical order
    'macos': ['MSS', 'NOP', 'WSCALE', 'NOP', 'NOP', 'TIMESTAMP', 'SACK_PERM', 'EOL']
}`

**TCP Option Codes:**

| **Code** | **Name** | **Purpose** |
| --- | --- | --- |
| 0 | EOL | End of Options List |
| 1 | NOP | No Operation (padding) |
| 2 | MSS | Maximum Segment Size |
| 3 | WSCALE | Window Scale Factor |
| 4 | SACK_PERM | SACK Permitted |
| 8 | TIMESTAMP | Timestamp for RTT calculation |

### Passive OS Fingerprinting with p0f

[p0f](http://lcamtuf.coredump.cx/p0f3/) is a powerful passive OS fingerprinting tool created by Michal Zalewski that analyzes TCP/IP packet characteristics without sending any traffic to the target.

`# Install p0f
sudo apt-get install p0f
# Passive fingerprinting (reads from interface)
sudo p0f -i eth0
# Read from pcap file
p0f -r capture.pcap
# Output example:
# 192.168.1.100:12345 → 93.184.216.34:443
#   OS: Linux 3.11 and newer
#   Signature: 4:64:0:*:mss*20,10:mss,sok,ts,nop,ws:df,id+:0`

**p0f Signature Database**

p0f maintains an extensive signature database (`p0f.fp`) with thousands of OS fingerprints. The tool is particularly effective because it performs **passive** fingerprinting, analyzing traffic without generating any packets that might alert intrusion detection systems.

**p0f Signature Format:**

`version:ittl:olen:mss:wsize,scale:olayout:quirks:pclass`

- `version`: IP version (4 or 6)
- `ittl`: Initial TTL
- `olen`: Options length
- `mss`: Maximum Segment Size
- `wsize,scale`: Window size and scaling
- `olayout`: Options layout (order and types)
- `quirks`: Unusual behaviors (df=don't fragment, id+=non-zero IP ID)
- `pclass`: Payload classification

### Active OS Fingerprinting with Nmap

[Nmap](https://nmap.org/) (Network Mapper) is the de facto standard for active OS fingerprinting, developed by Gordon Lyon (Fyodor). It sends specially crafted packets and analyzes the responses to determine OS characteristics.

`# OS detection
nmap -O 93.184.216.34
# Detailed OS detection with version scanning
nmap -A 93.184.216.34
# TCP/IP fingerprinting only
nmap -sV --script=banner 93.184.216.34
# Output example:
# OS details: Linux 5.4 - 5.10
# Network Distance: 11 hops
# TCP Sequence Prediction: Difficulty=260 (Good luck!)`

**Nmap's OS Detection Tests:**

- **TCP ISN sampling**: Analyzes Initial Sequence Number generation
- **TCP options**: Tests window size, MSS, SACK, and option ordering
- **ICMP responses**: Sends echo requests and analyzes TTL, code, and payloads
- **Closed port TCP responses**: Sends packets to closed ports and analyzes RST responses
- **IP ID sequence**: Tests how the OS generates IP identification fields

**Nmap Fingerprint Database**

Nmap maintains one of the most comprehensive OS fingerprint databases in the world (`nmap-os-db`), updated regularly by the community. You can submit new fingerprints to improve detection accuracy.

### Python Implementation: TCP Fingerprinting

The following implementation uses [Scapy](https://scapy.net/), a powerful Python library for packet manipulation and network analysis created by Philippe Biondi.

`from scapy.all import IP, TCP, sr1, sniff
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
class TCPFingerprinter:
    """
    Analyze TCP/IP characteristics to fingerprint the remote host.
    """
    def __init__(self, target_ip: str, target_port: int = 80):
        self.target_ip = target_ip
        self.target_port = target_port
        self.fingerprint = {}
    def capture_syn_ack(self) -> dict:
        """
        Send SYN packet and capture SYN-ACK response.
        """
        # Craft SYN packet
        ip = IP(dst=self.target_ip)
        syn = TCP(sport=40000, dport=self.target_port, flags='S', seq=1000)
        # Send and receive
        logger.info(f"Sending SYN to {self.target_ip}:{self.target_port}")
        syn_ack = sr1(ip/syn, timeout=2, verbose=0)
        if not syn_ack or not syn_ack.haslayer(TCP):
            logger.error("No SYN-ACK received")
            return {}
        # Extract fingerprint characteristics
        tcp_layer = syn_ack.getlayer(TCP)
        ip_layer = syn_ack.getlayer(IP)
        fingerprint = {
            'ip_ttl': ip_layer.ttl,
            'ip_id': ip_layer.id,
            'ip_flags': ip_layer.flags,
            'tcp_window': tcp_layer.window,
            'tcp_flags': tcp_layer.flags,
            'tcp_options': self._parse_tcp_options(tcp_layer.options),
            'tcp_options_order': [opt[0] for opt in tcp_layer.options if opt[0] != 'Padding'],
        }
        self.fingerprint = fingerprint
        return fingerprint
    def _parse_tcp_options(self, options: list) -> dict:
        """Parse TCP options into a readable format."""
        parsed = {}
        for option in options:
            opt_name = option[0]
            if opt_name == 'MSS':
                parsed['mss'] = option[1]
            elif opt_name == 'WScale':
                parsed['window_scale'] = option[1]
            elif opt_name == 'Timestamp':
                parsed['timestamp'] = option[1]
            elif opt_name == 'SAckOK':
                parsed['sack_permitted'] = True
            elif opt_name == 'NOP':
                pass  # Padding
            elif opt_name == 'EOL':
                break  # End of options
        return parsed
    def generate_signature(self) -> str:
        """
        Generate p0f-like signature string.
        """
        if not self.fingerprint:
            return ''
        fp = self.fingerprint
        # Format: version:ttl:window:options_order
        version = 4  # IPv4
        ttl = fp.get('ip_ttl', 0)
        window = fp.get('tcp_window', 0)
        # Options order as string
        opts = ','.join(fp.get('tcp_options_order', []))
        signature = f"{version}:{ttl}:{window}:{opts}"
        return signature
    def detect_os(self) -> str:
        """
        Detect OS based on collected fingerprint.
        """
        if not self.fingerprint:
            return 'Unknown (no data)'
        ttl = self.fingerprint.get('ip_ttl', 0)
        window = self.fingerprint.get('tcp_window', 0)
        opts_order = self.fingerprint.get('tcp_options_order', [])
        # Simple heuristic-based detection
        if ttl <= 64:
            if window == 29200:
                return 'Linux (recent kernel)'
            elif window == 65535:
                if 'Timestamp' in opts_order and 'SAckOK' in opts_order:
                    return 'Linux 3.x+'
                else:
                    return 'macOS'
            else:
                return 'Linux/Unix'
        elif ttl <= 128:
            if window == 8192:
                return 'Windows 10'
            elif window == 65535:
                return 'Windows 11 or Windows Server'
            else:
                return 'Windows'
        elif ttl <= 255:
            return 'Network device (router/firewall)'
        return 'Unknown OS'
    def print_fingerprint(self):
        """Pretty print the fingerprint."""
        if not self.fingerprint:
            print("No fingerprint data available")
            return
        print("\n=== TCP/IP Fingerprint ===")
        print(f"Target: {self.target_ip}:{self.target_port}")
        print(f"\nIP Layer:")
        print(f"  TTL: {self.fingerprint.get('ip_ttl')}")
        print(f"  IP ID: {self.fingerprint.get('ip_id')}")
        print(f"  Flags: {self.fingerprint.get('ip_flags')}")
        print(f"\nTCP Layer:")
        print(f"  Window Size: {self.fingerprint.get('tcp_window')}")
        print(f"  Flags: {self.fingerprint.get('tcp_flags')}")
        print(f"\nTCP Options:")
        for opt, value in self.fingerprint.get('tcp_options', {}).items():
            print(f"  {opt}: {value}")
        print(f"\nOptions Order: {' → '.join(self.fingerprint.get('tcp_options_order', []))}")
        print(f"\nSignature: {self.generate_signature()}")
        print(f"Detected OS: {self.detect_os()}")
        print("=" * 30)
# Usage example
def fingerprint_target(ip: str, port: int = 80):
    """Fingerprint a target host."""
    fingerprinter = TCPFingerprinter(ip, port)
    try:
        fingerprinter.capture_syn_ack()
        fingerprinter.print_fingerprint()
    except PermissionError:
        print("Error: Raw socket access requires root/admin privileges")
        print("Run with: sudo python3 script.py")
    except Exception as e:
        print(f"Error: {e}")
# Example usage (requires root):
# fingerprint_target('93.184.216.34', 80)  # example.com`

**Example Output:**

`=== TCP/IP Fingerprint ===
Target: 93.184.216.34:80
IP Layer:
  TTL: 54
  IP ID: 0
  Flags: DF (Don't Fragment)
TCP Layer:
  Window Size: 29200
  Flags: SA (SYN-ACK)
TCP Options:
  mss: 1460
  window_scale: 7
  sack_permitted: True
  timestamp: (123456789, 0)
Options Order: MSS → SAckOK → Timestamp → NOP → WScale
Signature: 4:54:29200:MSS,SAckOK,Timestamp,NOP,WScale
Detected OS: Linux (recent kernel)
==============================`

### TCP Initial Sequence Number (ISN) Analysis

`def analyze_isn_randomness(target_ip: str, samples: int = 10) -> dict:
    """
    Analyze TCP Initial Sequence Number generation.
    Different OSes use different ISN generation algorithms.
    """
    import statistics
    sequence_numbers = []
    for i in range(samples):
        syn = IP(dst=target_ip)/TCP(sport=40000+i, dport=80, flags='S')
        syn_ack = sr1(syn, timeout=2, verbose=0)
        if syn_ack and syn_ack.haslayer(TCP):
            isn = syn_ack[TCP].seq
            sequence_numbers.append(isn)
        # Small delay between probes
        time.sleep(0.1)
    if len(sequence_numbers) < 2:
        return {'error': 'Insufficient data'}
    # Calculate statistics
    deltas = [sequence_numbers[i+1] - sequence_numbers[i] 
              for i in range(len(sequence_numbers)-1)]
    return {
        'sample_count': len(sequence_numbers),
        'isn_values': sequence_numbers,
        'deltas': deltas,
        'avg_delta': statistics.mean(deltas),
        'stdev_delta': statistics.stdev(deltas) if len(deltas) > 1 else 0,
        'min_delta': min(deltas),
        'max_delta': max(deltas),
        'randomness': 'High' if statistics.stdev(deltas) > 100000 else 'Low'
    }`

**ISN Generation by OS:**

| **OS** | **ISN Algorithm** | **Predictability** |
| --- | --- | --- |
| **Linux (modern)** | [RFC 6528](https://tools.ietf.org/html/rfc6528) (hash-based) | Very random |
| **Windows** | RFC 6528 | Very random |
| **Old Linux** | Time-based counter | Somewhat predictable |
| **BSD** | [RFC 1948](https://tools.ietf.org/html/rfc1948) (MD5-based) | Random |

**ISN Prediction Attacks**

Historically, predictable ISNs enabled **TCP hijacking attacks** (see [Mitnick attack, 1995](https://en.wikipedia.org/wiki/Kevin_Mitnick#Arrest,_conviction,_and_incarceration)). Modern systems implement [RFC 6528](https://tools.ietf.org/html/rfc6528) "Defending against Sequence Number Attacks" using cryptographically secure random number generators for ISN, making prediction computationally infeasible.

## TLS/SSL Fingerprinting (Layer 6)

TLS fingerprinting is one of the most powerful techniques for identifying clients, as the TLS handshake reveals detailed information about the client's cryptographic capabilities and implementation.

### TLS Handshake Overview

ServerClientServerClientClient prepares ClientHelloServer analyzes fingerprintJA3 hash calculatedEncrypted Application DataClientHello[Version, Random, Cipher Suites,Extensions, Curves, Formats]ServerHello[Chosen Cipher, Extensions]CertificateServerHelloDoneClientKeyExchangeChangeCipherSpecFinishedChangeCipherSpecFinished

### JA3: TLS Client Fingerprinting

[JA3](https://github.com/salesforce/ja3) is a method developed by John Althouse, Jeff Atkinson, and Josh Atkins at Salesforce for creating fingerprints of TLS clients by analyzing the ClientHello packet. The technique has become an industry standard for TLS fingerprinting.

**JA3 Components:**

`# JA3 fingerprint components (in order)
ja3_components = {
    1: 'TLS Version',          # e.g., 771 = TLS 1.2, 772 = TLS 1.3
    2: 'Cipher Suites',        # e.g., '49195,49199,52393'
    3: 'Extensions',           # e.g., '0,10,11,13'  
    4: 'Elliptic Curves',      # e.g., '23,24,25'
    5: 'EC Point Formats',     # e.g., '0'
}
# JA3 string format (comma-separated)
ja3_string = f"{version},{ciphers},{extensions},{curves},{formats}"
# JA3 hash (MD5 of the string)
ja3_hash = hashlib.md5(ja3_string.encode()).hexdigest()`

**Example JA3:**

`String: 771,49195-49199-52393-49196-49200-52392,0-10-11-13-65281,23-24-25,0
Hash:   579ccef312d18482fc42e2b822ca2430`

### Generating JA3 Fingerprints with Python

`import hashlib
import ssl
import socket
from typing import Optional, Dict, List
class JA3Generator:
    """
    Generate JA3 fingerprints from TLS ClientHello packets.
    """
    # TLS Version mappings
    TLS_VERSIONS = {
        0x0301: 'TLS 1.0',
        0x0302: 'TLS 1.1',
        0x0303: 'TLS 1.2',
        0x0304: 'TLS 1.3',
    }
    # Common cipher suites
    CIPHER_SUITES = {
        0x002f: 'TLS_RSA_WITH_AES_128_CBC_SHA',
        0x0035: 'TLS_RSA_WITH_AES_256_CBC_SHA',
        0xc013: 'TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA',
        0xc014: 'TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA',
        0xc02f: 'TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256',
        0xc02b: 'TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256',
        0x1301: 'TLS_AES_128_GCM_SHA256',          # TLS 1.3
        0x1302: 'TLS_AES_256_GCM_SHA384',          # TLS 1.3
        0x1303: 'TLS_CHACHA20_POLY1305_SHA256',    # TLS 1.3
    }
    # TLS Extensions
    EXTENSIONS = {
        0: 'server_name',
        1: 'max_fragment_length',
        5: 'status_request',
        10: 'supported_groups',
        11: 'ec_point_formats',
        13: 'signature_algorithms',
        16: 'application_layer_protocol_negotiation',
        18: 'signed_certificate_timestamp',
        23: 'extended_master_secret',
        27: 'compress_certificate',
        35: 'session_ticket',
        43: 'supported_versions',
        45: 'psk_key_exchange_modes',
        51: 'key_share',
        65281: 'renegotiation_info',
    }
    @staticmethod
    def parse_client_hello(client_hello_bytes: bytes) -> Dict:
        """
        Parse ClientHello packet and extract JA3 components.
        """
        if len(client_hello_bytes) < 43:
            raise ValueError("Invalid ClientHello packet (too short)")
        # TLS Record Header (5 bytes)
        # Content Type (1) | Version (2) | Length (2)
        content_type = client_hello_bytes[0]
        record_version = int.from_bytes(client_hello_bytes[1:3], 'big')
        # Handshake Header (4 bytes)
        # Handshake Type (1) | Length (3)
        handshake_type = client_hello_bytes[5]
        if handshake_type != 0x01:  # ClientHello
            raise ValueError("Not a ClientHello packet")
        # ClientHello Version (2 bytes at offset 9)
        client_version = int.from_bytes(client_hello_bytes[9:11], 'big')
        # Random (32 bytes)
        offset = 11 + 32  # Skip version + random
        # Session ID
        session_id_length = client_hello_bytes[offset]
        offset += 1 + session_id_length
        # Cipher Suites
        cipher_suites_length = int.from_bytes(client_hello_bytes[offset:offset+2], 'big')
        offset += 2
        cipher_suites = []
        for i in range(0, cipher_suites_length, 2):
            cipher = int.from_bytes(client_hello_bytes[offset+i:offset+i+2], 'big')
            cipher_suites.append(cipher)
        offset += cipher_suites_length
        # Compression Methods
        compression_length = client_hello_bytes[offset]
        offset += 1 + compression_length
        # Extensions
        extensions = []
        elliptic_curves = []
        ec_point_formats = []
        if offset < len(client_hello_bytes) - 2:
            extensions_length = int.from_bytes(client_hello_bytes[offset:offset+2], 'big')
            offset += 2
            extensions_end = offset + extensions_length
            while offset < extensions_end:
                ext_type = int.from_bytes(client_hello_bytes[offset:offset+2], 'big')
                ext_length = int.from_bytes(client_hello_bytes[offset+2:offset+4], 'big')
                offset += 4
                extensions.append(ext_type)
                # Parse specific extensions
                if ext_type == 10:  # supported_groups
                    curves_length = int.from_bytes(client_hello_bytes[offset:offset+2], 'big')
                    for i in range(2, curves_length + 2, 2):
                        curve = int.from_bytes(client_hello_bytes[offset+i:offset+i+2], 'big')
                        elliptic_curves.append(curve)
                elif ext_type == 11:  # ec_point_formats
                    formats_length = client_hello_bytes[offset]
                    for i in range(1, formats_length + 1):
                        fmt = client_hello_bytes[offset + i]
                        ec_point_formats.append(fmt)
                offset += ext_length
        # Filter GREASE values (randomized by browsers to prevent ossification)
        # GREASE (RFC 8701): Generate Random Extensions And Sustain Extensibility
        # GREASE values: 0x0a0a, 0x1a1a, 0x2a2a, 0x3a3a, etc.
        def is_grease(value: int) -> bool:
            return (value & 0x0f0f) == 0x0a0a
        cipher_suites = [c for c in cipher_suites if not is_grease(c)]
        extensions = [e for e in extensions if not is_grease(e)]
        elliptic_curves = [c for c in elliptic_curves if not is_grease(c)]
        return {
            'version': client_version,
            'cipher_suites': cipher_suites,
            'extensions': extensions,
            'elliptic_curves': elliptic_curves,
            'ec_point_formats': ec_point_formats,
        }
    @staticmethod
    def generate_ja3(parsed_hello: Dict) -> tuple[str, str]:
        """
        Generate JA3 string and hash from parsed ClientHello.
        Note: GREASE values should already be filtered from parsed_hello
        to ensure consistent fingerprints across connections.
        """
        # Join components with '-'
        version = str(parsed_hello['version'])
        ciphers = '-'.join(str(c) for c in parsed_hello['cipher_suites'])
        extensions = '-'.join(str(e) for e in parsed_hello['extensions'])
        curves = '-'.join(str(c) for c in parsed_hello['elliptic_curves'])
        formats = '-'.join(str(f) for f in parsed_hello['ec_point_formats'])
        # JA3 string (comma-separated components)
        ja3_string = f"{version},{ciphers},{extensions},{curves},{formats}"
        # JA3 hash (MD5)
        ja3_hash = hashlib.md5(ja3_string.encode()).hexdigest()
        return ja3_string, ja3_hash
    @staticmethod
    def capture_tls_handshake(hostname: str, port: int = 443) -> Optional[bytes]:
        """
        Capture the ClientHello from a TLS connection.
        Note: This is simplified. For production, use scapy or mitmproxy.
        """
        try:
            # Create socket but don't complete handshake
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            sock.connect((hostname, port))
            # In practice, you'd need to intercept the actual bytes sent
            # This is just a placeholder - use packet capture tools instead
            sock.close()
            return None  # Would return captured ClientHello bytes
        except Exception as e:
            print(f"Error capturing handshake: {e}")
            return None
!!! info "GREASE Values in TLS"
    [GREASE (RFC 8701)](https://tools.ietf.org/html/rfc8701) - "Generate Random Extensions And Sustain Extensibility" - is a technique used by modern browsers to prevent protocol ossification. Browsers randomly insert reserved values (like 0x0a0a, 0x1a1a, 0x2a2a) into cipher suites, extensions, and other fields.
    **Why GREASE matters for fingerprinting:**
    - These values change on every connection, making raw TLS handshakes non-deterministic
    - JA3 implementations must **filter out** GREASE values to create consistent fingerprints
    - Servers that reject GREASE values are non-compliant and reveal themselves
    - Missing GREASE in automation can be a detection signal (real browsers always use it)
def analyze_ja3_from_pcap(pcap_file: str):
    """
    Analyze JA3 fingerprints from a pcap file.
    Requires scapy and tls parsing capabilities.
    """
    from scapy.all import rdpcap, TCP
    from scapy.layers.tls.record import TLS
    from scapy.layers.tls.handshake import TLSClientHello
    packets = rdpcap(pcap_file)
    ja3_results = []
    for packet in packets:
        if packet.haslayer(TLS) and packet.haslayer(TLSClientHello):
            try:
                # Extract ClientHello layer
                client_hello = packet[TLSClientHello]
                # Build JA3 components
                version = client_hello.version
                ciphers = client_hello.ciphers
                extensions = [ext.type for ext in client_hello.ext] if hasattr(client_hello, 'ext') else []
                # Parse extensions for curves and formats
                curves = []
                formats = []
                if hasattr(client_hello, 'ext'):
                    for ext in client_hello.ext:
                        if ext.type == 10:  # supported_groups
                            curves = ext.groups if hasattr(ext, 'groups') else []
                        elif ext.type == 11:  # ec_point_formats
                            formats = ext.formats if hasattr(ext, 'formats') else []
                # Generate JA3
                ja3_str = f"{version},{'-'.join(map(str, ciphers))},{'-'.join(map(str, extensions))},{'-'.join(map(str, curves))},{'-'.join(map(str, formats))}"
                ja3_hash = hashlib.md5(ja3_str.encode()).hexdigest()
                ja3_results.append({
                    'src_ip': packet[IP].src if packet.haslayer(IP) else 'unknown',
                    'dst_ip': packet[IP].dst if packet.haslayer(IP) else 'unknown',
                    'ja3_string': ja3_str,
                    'ja3_hash': ja3_hash,
                })
            except Exception as e:
                print(f"Error parsing packet: {e}")
                continue
    return ja3_results
# Example: Known browser JA3 hashes
KNOWN_JA3_FINGERPRINTS = {
    '579ccef312d18482fc42e2b822ca2430': 'Chrome 90+ on Windows',
    'cd08e31efaa7a0a82988099039d4a289': 'Firefox 88+ on Windows',
    'ac1a36f8b3f5e5d4a6e4f0c3e5a5e5e5': 'Safari 14+ on macOS',
    'b32309a26951912be7dba376398abc3b': 'Python requests library',
    'e7d705a3286e19bd28ca826f69a8b2c9': 'curl 7.88+'
}
def identify_client(ja3_hash: str) -> str:
    """Identify client based on JA3 hash."""
    return KNOWN_JA3_FINGERPRINTS.get(ja3_hash, 'Unknown client')`

### Tools for TLS Fingerprinting

### **1. ja3 (Original Implementation)**

The original [JA3 implementation from Salesforce](https://github.com/salesforce/ja3) provides tools for generating fingerprints from pcap files.

`# Install ja3
git clone https://github.com/salesforce/ja3.git
cd ja3/python
# Generate JA3 from pcap
python3 ja3.py -a capture.pcap
# Output:
# [JA3] 192.168.1.100:12345 → 93.184.216.34:443
# JA3: 579ccef312d18482fc42e2b822ca2430
# JA3S: e35df3e00ca4ef31d42b34bebaa2f86e`

### **2. pmercury (Python Library)**

[pmercury](https://pypi.org/project/pmercury/) is a Python library from Cisco for network fingerprinting, including TLS analysis.

`# Install
pip install pmercury
# Use in Python
from pmercury.protocols.tls import TLS
tls = TLS()
protocol_type, fp_str, approx_str, server_name = tls.fingerprint(data)`

### **3. ts1-signatures (Advanced TLS/HTTP2 Fingerprinting)**

[ts1-signatures](https://pypi.org/project/ts1-signatures/) provides more detailed fingerprinting with JSON output format.

`# Install
pip install ts1-signatures
# Use in Python
import ts1
with open("capture.pcap", "rb") as pcap:
    for tls_client in ts1.tls.process_pcap(pcap):
        signature = tls_client["signature"]
        print(f"TLS Fingerprint: {signature.hash().hexdigest()}")`

### **4. tlsfp (Educational TLS Fingerprint Server)**

[tlsfp](https://github.com/elpy1/tlsfp) is a Python HTTPS server for TLS fingerprinting, useful for testing and education.

`# Install
git clone https://github.com/elpy1/tlsfp.git
cd tlsfp
python3 tlsfp.py
# Access https://localhost:8443 to see your client's fingerprint`

### **5. curl-impersonate**

[curl-impersonate](https://github.com/lwthiker/curl-impersonate) allows you to mimic browser TLS fingerprints, useful for understanding evasion techniques.

`# Install (example for Chrome)
wget https://github.com/lwthiker/curl-impersonate/releases/...
chmod +x curl-impersonate-chrome
# Make request mimicking Chrome's TLS fingerprint
./curl-impersonate-chrome https://example.com`

**Wireshark with JA3**

Wireshark can display JA3 hashes with the [JA3 plugin](https://github.com/salesforce/ja3/tree/master/wireshark). This allows real-time fingerprint analysis during packet capture.

### JA3S: TLS Server Fingerprinting

JA3S is the server-side equivalent, fingerprinting servers based on ServerHello:

`def generate_ja3s(server_hello_bytes: bytes) -> tuple[str, str]:
    """
    Generate JA3S fingerprint from ServerHello.
    Format: Version,Cipher,Extensions
    """
    # Parse ServerHello (similar to ClientHello parsing)
    version = parse_version(server_hello_bytes)
    cipher = parse_selected_cipher(server_hello_bytes)
    extensions = parse_extensions(server_hello_bytes)
    # JA3S string (simpler than JA3)
    ja3s_string = f"{version},{cipher},{'-'.join(map(str, extensions))}"
    ja3s_hash = hashlib.md5(ja3s_string.encode()).hexdigest()
    return ja3s_string, ja3s_hash`

**JA3S Use Cases:**

- Identify server software (nginx, Apache, Cloudflare, etc.)
- Detect load balancers and CDNs
- Map infrastructure
- Identify potential vulnerabilities based on server stack

## Further Reading and References

### Technical Documents and RFCs

- [**RFC 6528**](https://tools.ietf.org/html/rfc6528): "Defending against Sequence Number Attacks" - Modern ISN generation
- [**RFC 1948**](https://tools.ietf.org/html/rfc1948): "Defending Against Sequence Number Attacks" - Original MD5-based ISN
- [**RFC 8701**](https://tools.ietf.org/html/rfc8701): "Applying Generate Random Extensions And Sustain Extensibility (GREASE) to TLS"
- [**RFC 5246**](https://tools.ietf.org/html/rfc5246): "The Transport Layer Security (TLS) Protocol Version 1.2"
- [**RFC 8446**](https://tools.ietf.org/html/rfc8446): "The Transport Layer Security (TLS) Protocol Version 1.3"

### Tools and Libraries

- [**JA3 by Salesforce**](https://github.com/salesforce/ja3): Original JA3 TLS fingerprinting implementation
- [**p0f**](http://lcamtuf.coredump.cx/p0f3/): Passive OS fingerprinting tool by Michal Zalewski
- [**Nmap**](https://nmap.org/): Network mapper and OS fingerprinting tool by Gordon Lyon
- [**Scapy**](https://scapy.net/): Python packet manipulation library by Philippe Biondi
- [**pmercury**](https://pypi.org/project/pmercury/): Python library for network fingerprinting from Cisco
- [**ts1-signatures**](https://pypi.org/project/ts1-signatures/): Advanced TLS/HTTP2 fingerprinting library
- [**tlsfp**](https://github.com/elpy1/tlsfp): Educational HTTPS TLS fingerprinting server
- [**curl-impersonate**](https://github.com/lwthiker/curl-impersonate): cURL with browser TLS fingerprint mimicry

### Articles and Blog Posts

- [**TLS Fingerprinting: How it works, where it is used and how to control your signature**](https://lwthiker.com/networks/2022/06/17/tls-fingerprinting.html) by lwthiker - Comprehensive guide on TLS fingerprinting mechanisms
- [**TLS Fingerprinting: Advanced Guide for Security Engineers 2025**](https://rebrowser.net/blog/tls-fingerprinting-advanced-guide-for-security-engineers) by Rebrowser - Modern TLS fingerprinting techniques
- [**Overcoming TLS Fingerprinting in Web Scraping**](https://rayobyte.com/blog/tls-fingerprinting/) by Rayobyte - Practical perspective on TLS fingerprinting in automation
- [**JA3: A Method for Profiling SSL/TLS Clients**](https://engineering.salesforce.com/tls-fingerprinting-with-ja3-and-ja3s-247362855967) by Salesforce Engineering - Original JA3 announcement

### Academic Papers and Research

- **"Remote OS Detection via TCP/IP Stack Fingerprinting"** - Early research on OS fingerprinting techniques
- **"A TCP Initial Sequence Number Attack"** - Historical paper on ISN vulnerabilities
- **"TLS Fingerprinting: New Techniques for Identifying Applications"** - Modern research on TLS-based identification

### Security Resources

- [**OWASP Fingerprinting Guide**](https://owasp.org/): Web application fingerprinting techniques
- [**IANA TLS Parameters**](https://www.iana.org/assignments/tls-parameters/tls-parameters.xhtml): Official cipher suite and extension registries
- [**Wireshark Display Filters for TLS**](https://wiki.wireshark.org/TLS): Guide to analyzing TLS traffic

### Historical References

- [**Kevin Mitnick TCP Hijacking Attack (1995)**](https://en.wikipedia.org/wiki/Kevin_Mitnick#Arrest,_conviction,_and_incarceration): Famous example of ISN prediction exploitation
- [**Evolution of TCP/IP Fingerprinting**](https://lcamtuf.coredump.cx/p0f3/): Historical perspective from p0f creator

**Stay Updated**

Fingerprinting techniques evolve constantly as new protocols emerge and systems adapt. Follow security blogs, subscribe to relevant RFCs, and monitor tool repositories for the latest developments.



Browser-Level Fingerprinting
This document explores fingerprinting at the application layer (HTTP/2, JavaScript, Canvas, WebGL). While network-level fingerprinting identifies the **OS and network stack**, browser-level fingerprinting reveals the **specific browser, version, and configuration**.

**Module Navigation**

- [**← Fingerprinting Overview**](https://pydoll.tech/docs/deep-dive/fingerprinting/) - Module introduction and philosophy
- [**← Network Fingerprinting**](https://pydoll.tech/docs/deep-dive/fingerprinting/network-fingerprinting/) - Protocol-level fingerprinting
- [**→ Evasion Techniques**](https://pydoll.tech/docs/deep-dive/fingerprinting/evasion-techniques/) - Practical countermeasures

For practical browser configuration, see [**Browser Options**](https://pydoll.tech/docs/features/configuration/browser-options/) and [**Browser Preferences**](https://pydoll.tech/docs/features/configuration/browser-preferences/).

**Consistency is Key**

Browser fingerprinting is **the primary detection layer** for most anti-bot systems. A single inconsistency (like a Chrome User-Agent with Firefox canvas artifacts) triggers immediate blocking.

## Browser-Level Fingerprinting

While network-level fingerprinting operates at the protocol level, browser-level fingerprinting exploits characteristics of the browser environment itself. This section covers modern techniques used to identify browsers, including HTTP/2 analysis, JavaScript APIs, rendering engines, and CDP-based evasion strategies.

## HTTP/2 Fingerprinting

HTTP/2's binary framing and multiplexing capabilities introduced new fingerprinting vectors. Companies like [Akamai](https://www.akamai.com/) pioneered HTTP/2 fingerprinting techniques to detect bots and automated tools.

### SETTINGS Frame Fingerprinting

The HTTP/2 `SETTINGS` frame sent during connection initialization reveals implementation-specific preferences. Different browsers send distinctly different settings.

**Chrome SETTINGS (as of v120+):**

`chrome_http2_settings = {
    'SETTINGS_HEADER_TABLE_SIZE': 65536,        # 0x1
    'SETTINGS_MAX_CONCURRENT_STREAMS': 1000,    # 0x3
    'SETTINGS_INITIAL_WINDOW_SIZE': 6291456,    # 0x4 (6MB)
    'SETTINGS_MAX_HEADER_LIST_SIZE': 262144,    # 0x6
}`

**Firefox SETTINGS (as of v120+):**

`firefox_http2_settings = {
    'SETTINGS_HEADER_TABLE_SIZE': 65536,        # 0x1
    'SETTINGS_INITIAL_WINDOW_SIZE': 131072,     # 0x4 (128KB - much smaller!)
    'SETTINGS_MAX_FRAME_SIZE': 16384,           # 0x5 (16KB)
}`

**Key differences:**

| **Setting** | **Chrome** | **Firefox** | **Safari** | **curl** |
| --- | --- | --- | --- | --- |
| **HEADER_TABLE_SIZE** | 65536 | 65536 | 4096 | 4096 |
| **MAX_CONCURRENT_STREAMS** | 1000 | 100 | 100 | 100 |
| **INITIAL_WINDOW_SIZE** | 6291456 | 131072 | 2097152 | 65535 |
| **MAX_FRAME_SIZE** | 16384 | 16384 | 16384 | 16384 |
| **MAX_HEADER_LIST_SIZE** | 262144 | (not set) | (not set) | (not set) |

**HTTP/2 Settings Detection**

Automated tools like `requests`, `httpx`, and even `curl` send **different** HTTP/2 settings than real browsers. This is one of the easiest ways to detect automation.

### WINDOW_UPDATE Frame Analysis

HTTP/2 uses `WINDOW_UPDATE` frames for flow control. The **size** and **timing** of these updates vary by implementation:

`# Connection-level window updates
http2_window_updates = {
    'Chrome': 15 * 1024 * 1024,      # 15MB
    'Firefox': 12 * 1024 * 1024,     # 12MB  
    'curl': 32 * 1024 * 1024,        # 32MB (suspicious!)
    'Python httpx': 65535,           # 64KB (default, suspicious!)
}`

**Detection technique:**

`# Server-side HTTP/2 fingerprinting pseudocode
def fingerprint_http2_client(connection):
    """
    Analyze HTTP/2 characteristics to identify client.
    """
    fingerprint = {
        'settings': parse_settings_frame(connection),
        'window_update': get_initial_window_update(connection),
        'priority_tree': analyze_stream_priorities(connection),
        'header_order': get_pseudo_header_order(connection),
    }
    # Compare against known browser fingerprints
    if fingerprint['window_update'] > 20_000_000:
        return 'Likely curl or httpx (too large)'
    if 'MAX_CONCURRENT_STREAMS' not in fingerprint['settings']:
        return 'Likely Python/Go library (missing setting)'
    if fingerprint['settings']['INITIAL_WINDOW_SIZE'] == 6291456:
        return 'Likely Chrome/Chromium'
    return 'Unknown client'`

### Stream Priority and Dependency

HTTP/2 allows clients to specify stream priorities and dependencies using `PRIORITY` frames. Browsers create sophisticated priority trees to optimize page loading.

**Chrome's priority tree (simplified):**

`Stream 0 (connection)
├─ Stream 3 (HTML document) - weight: 256
├─ Stream 5 (CSS) - weight: 220, depends on Stream 3
├─ Stream 7 (JavaScript) - weight: 220, depends on Stream 3
├─ Stream 9 (Image) - weight: 110, depends on Stream 3
└─ Stream 11 (Font) - weight: 110, depends on Stream 3`

**Python requests/httpx (no priorities):**

`Stream 0 (connection)
└─ Stream 3 (request) - no priority, no dependencies`

**Priority Tree Mismatch**

Automated HTTP clients rarely implement sophisticated priority trees. Missing or simplistic priorities are **strong indicators** of automation.

### Pseudo-Header Ordering

HTTP/2 replaces HTTP/1.1 request line with pseudo-headers (`:method`, `:path`, `:authority`, `:scheme`). The **order** of these headers varies:

`# Chrome/Edge order
chrome_order = [':method', ':path', ':authority', ':scheme']
# Firefox order  
firefox_order = [':method', ':path', ':authority', ':scheme']
# Safari order
safari_order = [':method', ':scheme', ':path', ':authority']
# curl/httpx order (often different)
automated_order = [':method', ':authority', ':scheme', ':path']`

**Detection code:**

`def detect_pseudo_header_order(headers: list[tuple[str, str]]) -> str:
    """Detect client based on pseudo-header order."""
    pseudo_headers = [h[0] for h in headers if h[0].startswith(':')]
    order_str = ','.join(pseudo_headers)
    patterns = {
        ':method,:path,:authority,:scheme': 'Chrome/Edge/Firefox',
        ':method,:scheme,:path,:authority': 'Safari',
        ':method,:authority,:scheme,:path': 'Automated tool (curl/httpx)',
    }
    return patterns.get(order_str, 'Unknown')`

### Analyzing HTTP/2 with Python

`from h2.connection import H2Connection
from h2.config import H2Configuration
from h2.events import SettingsAcknowledged, WindowUpdated
import socket
import ssl
class HTTP2Analyzer:
    """
    Analyze HTTP/2 connection characteristics.
    """
    def __init__(self, hostname: str, port: int = 443):
        self.hostname = hostname
        self.port = port
        self.settings = {}
        self.window_updates = []
    def analyze_server_http2(self) -> dict:
        """
        Connect to server and analyze its HTTP/2 implementation.
        """
        # Create socket
        sock = socket.create_connection((self.hostname, self.port))
        # Wrap with TLS
        context = ssl.create_default_context()
        context.set_alpn_protocols(['h2'])
        sock = context.wrap_socket(sock, server_hostname=self.hostname)
        # Create H2 connection
        config = H2Configuration(client_side=True)
        conn = H2Connection(config=config)
        conn.initiate_connection()
        # Send initial data
        sock.sendall(conn.data_to_send())
        # Receive server preface
        data = sock.recv(65535)
        events = conn.receive_data(data)
        # Analyze events
        for event in events:
            if isinstance(event, SettingsAcknowledged):
                # Server acknowledged our settings
                pass
            elif isinstance(event, WindowUpdated):
                self.window_updates.append({
                    'stream_id': event.stream_id,
                    'delta': event.delta,
                })
        # Extract server settings
        server_settings = conn.remote_settings
        sock.close()
        return {
            'settings': dict(server_settings),
            'window_updates': self.window_updates,
            'alpn_protocol': sock.selected_alpn_protocol(),
        }
# Usage
analyzer = HTTP2Analyzer('www.google.com')
result = analyzer.analyze_server_http2()
print(f"Server HTTP/2 Settings: {result['settings']}")
print(f"Window Updates: {result['window_updates']}")`

**HTTP/2 Fingerprinting References**

- [**Understanding HTTP/2 Fingerprinting**](https://www.trickster.dev/post/understanding-http2-fingerprinting/) by Trickster Dev - Comprehensive guide on HTTP/2 fingerprinting
- [**HTTP/2 Fingerprinting**](https://lwthiker.com/networks/2022/06/17/http2-fingerprinting.html) by lwthiker - Technical deep-dive into HTTP/2 characteristics
- [**Akamai Bot Manager**](https://www.akamai.com/products/bot-manager) - Commercial solution using HTTP/2 fingerprinting
- [**Multilogin HTTP/2 Fingerprinting Guide**](https://multilogin.com/glossary/http2-fingerprinting/) - Practical perspective on HTTP/2 detection

## HTTP Headers Consistency

Beyond HTTP/2-specific frames, standard HTTP headers provide rich fingerprinting data. The key is **consistency** across multiple characteristics.

### User-Agent Header Analysis

The `User-Agent` header is the most obvious fingerprinting vector, but it's also the most commonly spoofed:

`# Typical Chrome User-Agent
chrome_ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
# Typical Firefox User-Agent
firefox_ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0'
# Suspicious User-Agent (outdated version)
suspicious_ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.0.0 Safari/537.36'`

**Common issues with spoofed User-Agents:**

1. **Outdated version**: Claims Chrome 90 in 2025
2. **OS mismatch**: Claims "Windows NT 10.0" but sends Linux TTL values
3. **Platform inconsistency**: Claims "Windows" but `navigator.platform` returns "Linux"
4. **Missing browser features**: Claims Chrome 120 but doesn't support features introduced in v110

### Accept-Language Consistency

The `Accept-Language` header should match browser/OS language settings:

`# Inconsistency examples
inconsistencies = {
    # Header says English, but timezone is GMT+9 (Japan)
    'accept_language': 'en-US,en;q=0.9',
    'timezone': 'Asia/Tokyo',  # Suspicious!
    # Header has single language, but navigator.languages has many
    'header': 'en-US',
    'navigator_languages': ['en-US', 'en', 'pt-BR', 'pt', 'es'],  # Mismatch!
}`

**Proper configuration:**

`import pytz
from datetime import datetime
def generate_consistent_accept_language(primary_lang: str, timezone_str: str) -> dict:
    """
    Generate consistent language headers based on timezone.
    """
    # Language-timezone mappings (simplified)
    tz_to_lang = {
        'America/New_York': 'en-US,en;q=0.9',
        'Europe/London': 'en-GB,en;q=0.9',
        'Asia/Tokyo': 'ja-JP,ja;q=0.9,en;q=0.8',
        'Europe/Berlin': 'de-DE,de;q=0.9,en;q=0.8',
        'America/Sao_Paulo': 'pt-BR,pt;q=0.9,en;q=0.8',
    }
    expected_lang = tz_to_lang.get(timezone_str, 'en-US,en;q=0.9')
    if primary_lang not in expected_lang:
        print(f"Warning: Language {primary_lang} inconsistent with timezone {timezone_str}")
    return {
        'accept_language_header': expected_lang,
        'navigator_languages': expected_lang.replace(';q=0.9', '').replace(';q=0.8', '').split(','),
        'timezone': timezone_str,
    }
# Example
config = generate_consistent_accept_language('ja', 'Asia/Tokyo')
print(config)
# Output:
# {
#     'accept_language_header': 'ja-JP,ja;q=0.9,en;q=0.8',
#     'navigator_languages': ['ja-JP', 'ja', 'en'],
#     'timezone': 'Asia/Tokyo'
# }`

### Accept-Encoding Header

Modern browsers support specific compression algorithms:

`# Chrome/Edge (Brotli support)
chrome_encoding = 'gzip, deflate, br, zstd'
# Firefox  
firefox_encoding = 'gzip, deflate, br'
# Old/Automated tools (no Brotli)
automated_encoding = 'gzip, deflate'  # Suspicious in 2024+`

**Brotli Support Detection**

Any modern browser (2024+) **must** support Brotli (`br`). Missing Brotli indicates an automated tool or heavily outdated browser.

### Sec-CH-UA (Client Hints)

Modern Chromium browsers send [Client Hints](https://developer.mozilla.org/en-US/docs/Web/HTTP/Client_hints) headers:

`Sec-CH-UA: "Chromium";v="120", "Google Chrome";v="120", "Not:A-Brand";v="99"
Sec-CH-UA-Mobile: ?0
Sec-CH-UA-Platform: "Windows"
Sec-CH-UA-Platform-Version: "15.0.0"
Sec-CH-UA-Arch: "x86"
Sec-CH-UA-Bitness: "64"
Sec-CH-UA-Full-Version: "120.0.6099.130"
Sec-CH-UA-Model: ""`

**Consistency checks:**

`def validate_client_hints(headers: dict, navigator_props: dict) -> list[str]:
    """
    Validate Client Hints consistency with navigator properties.
    """
    issues = []
    # Extract Sec-CH-UA
    sec_ch_ua = headers.get('sec-ch-ua', '')
    sec_ch_platform = headers.get('sec-ch-ua-platform', '').strip('"')
    sec_ch_mobile = headers.get('sec-ch-ua-mobile', '')
    # Check platform consistency
    nav_platform = navigator_props.get('platform', '')
    if sec_ch_platform == 'Windows' and 'Win' not in nav_platform:
        issues.append(f"Platform mismatch: Sec-CH-UA says {sec_ch_platform}, navigator.platform says {nav_platform}")
    # Check mobile consistency
    nav_mobile = navigator_props.get('userAgentData', {}).get('mobile', False)
    if sec_ch_mobile == '?1' and not nav_mobile:
        issues.append("Mobile mismatch: Sec-CH-UA-Mobile says mobile, but navigator says desktop")
    # Check brand consistency with User-Agent
    user_agent = headers.get('user-agent', '')
    if 'Chrome' in sec_ch_ua and 'Chrome' not in user_agent:
        issues.append("Brand mismatch: Sec-CH-UA mentions Chrome, but User-Agent doesn't")
    return issues
# Example
headers = {
    'sec-ch-ua': '"Chromium";v="120", "Google Chrome";v="120"',
    'sec-ch-ua-platform': '"Windows"',
    'sec-ch-ua-mobile': '?0',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
}
navigator = {
    'platform': 'Win32',
    'userAgentData': {'mobile': False},
}
issues = validate_client_hints(headers, navigator)
if issues:
    print("Inconsistencies detected:")
    for issue in issues:
        print(f"  - {issue}")
else:
    print("Client Hints are consistent")`

### Header Order Fingerprinting

The **order** of HTTP headers is browser-specific and often overlooked when spoofing:

`# Chrome header order (typical)
chrome_header_order = [
    ':method',
    ':path',
    ':authority',
    ':scheme',
    'cache-control',
    'sec-ch-ua',
    'sec-ch-ua-mobile',
    'sec-ch-ua-platform',
    'upgrade-insecure-requests',
    'user-agent',
    'accept',
    'sec-fetch-site',
    'sec-fetch-mode',
    'sec-fetch-dest',
    'referer',
    'accept-encoding',
    'accept-language',
    'cookie',
]
# Firefox header order (different!)
firefox_header_order = [
    ':method',
    ':path',
    ':authority',
    ':scheme',
    'user-agent',
    'accept',
    'accept-language',
    'accept-encoding',
    'referer',
    'dnt',
    'connection',
    'upgrade-insecure-requests',
    'sec-fetch-dest',
    'sec-fetch-mode',
    'sec-fetch-site',
    'cookie',
]`

**Detection:**

`def fingerprint_by_header_order(request_headers: list[tuple[str, str]]) -> str:
    """
    Identify browser based on header order.
    """
    header_names = [h[0].lower() for h in request_headers]
    order_signature = ','.join(header_names[:10])  # First 10 headers
    # Known browser signatures
    signatures = {
        ':method,:path,:authority,:scheme,cache-control,sec-ch-ua': 'Chrome/Edge',
        ':method,:path,:authority,:scheme,user-agent,accept': 'Firefox',
        'host,connection,accept,user-agent,referer': 'Requests/httpx (suspicious!)',
    }
    for sig, browser in signatures.items():
        if order_signature.startswith(sig):
            return browser
    return 'Unknown (possibly spoofed)'`

**HTTP Header Fingerprinting References**

- [**HTTP Fingerprinting**](https://www.yeswehack.com/learn-bug-bounty/recon-series-http-fingerprinting) by YesWeHack - Guide to HTTP-based reconnaissance
- [**Client Hints (MDN)**](https://developer.mozilla.org/en-US/docs/Web/HTTP/Client_hints) - Official documentation on Sec-CH-UA headers
- [**HTTP Header Order Fingerprinting**](https://lwthiker.com/networks/2022/06/17/tls-fingerprinting.html) - Discussion of header ordering techniques

## JavaScript Properties Fingerprinting

JavaScript provides extensive access to browser and system properties via the `window` and `navigator` objects. These properties are the most commonly fingerprinted attributes.

### Navigator Object Properties

The `navigator` object exposes dozens of properties that reveal browser characteristics:

`// Core navigator properties
const fingerprint = {
    // User Agent
    userAgent: navigator.userAgent,
    appVersion: navigator.appVersion,
    platform: navigator.platform,
    // Language
    language: navigator.language,
    languages: navigator.languages,
    // Hardware
    hardwareConcurrency: navigator.hardwareConcurrency,  // CPU cores
    deviceMemory: navigator.deviceMemory,  // RAM in GB (approximation)
    // Features
    cookieEnabled: navigator.cookieEnabled,
    doNotTrack: navigator.doNotTrack,
    maxTouchPoints: navigator.maxTouchPoints,
    // Vendor
    vendor: navigator.vendor,
    vendorSub: navigator.vendorSub,
    // Product
    product: navigator.product,
    productSub: navigator.productSub,
    // OS CPU (legacy, but still available)
    oscpu: navigator.oscpu,  // Firefox only
};`

**Chrome-specific properties:**

`// Chrome User Agent Data (Client Hints API)
if (navigator.userAgentData) {
    const uaData = {
        brands: navigator.userAgentData.brands,
        mobile: navigator.userAgentData.mobile,
        platform: navigator.userAgentData.platform,
    };
    // Request high entropy values (requires permission)
    navigator.userAgentData.getHighEntropyValues([
        'architecture',
        'bitness',
        'model',
        'platformVersion',
        'uaFullVersion',
    ]).then(highEntropyValues => {
        console.log('High Entropy Values:', highEntropyValues);
        // {
        //     architecture: "x86",
        //     bitness: "64",
        //     model: "",
        //     platformVersion: "15.0.0",
        //     uaFullVersion: "120.0.6099.130"
        // }
    });
}`

### Screen and Window Properties

Display characteristics are highly distinctive:

`const screenFingerprint = {
    // Screen dimensions
    width: screen.width,
    height: screen.height,
    availWidth: screen.availWidth,
    availHeight: screen.availHeight,
    // Color depth
    colorDepth: screen.colorDepth,
    pixelDepth: screen.pixelDepth,
    // Device pixel ratio (Retina displays)
    devicePixelRatio: window.devicePixelRatio,
    // Window dimensions
    innerWidth: window.innerWidth,
    innerHeight: window.innerHeight,
    outerWidth: window.outerWidth,
    outerHeight: window.outerHeight,
    // Screen orientation
    orientation: {
        type: screen.orientation?.type,
        angle: screen.orientation?.angle,
    },
};`

**Detection of virtualized/headless environments:**

`def detect_headless_chrome(properties: dict) -> list[str]:
    """
    Detect headless Chrome based on property inconsistencies.
    """
    issues = []
    # Headless Chrome has outerWidth/Height = innerWidth/Height (no UI chrome)
    if properties['outerWidth'] == properties['innerWidth']:
        issues.append("outerWidth == innerWidth (suspicious for headed browser)")
    # Headless often has screen dimensions == window dimensions
    if properties['screen']['width'] == properties['innerWidth']:
        issues.append("Screen width == window width (possibly headless)")
    # Headless Chrome reports specific user agent
    if 'HeadlessChrome' in properties.get('userAgent', ''):
        issues.append("User-Agent explicitly says HeadlessChrome")
    # navigator.webdriver should be undefined in real browsers
    if properties.get('webdriver') == True:
        issues.append("navigator.webdriver is true (automation detected)")
    return issues`

### Plugins and MIME Types (Legacy)

Modern browsers have deprecated plugin enumeration, but it's still a fingerprinting vector:

`// Plugins (deprecated, but still exposed)
const plugins = [];
for (let i = 0; i < navigator.plugins.length; i++) {
    plugins.push({
        name: navigator.plugins[i].name,
        description: navigator.plugins[i].description,
        filename: navigator.plugins[i].filename,
    });
}
// MIME types (deprecated)
const mimeTypes = [];
for (let i = 0; i < navigator.mimeTypes.length; i++) {
    mimeTypes.push({
        type: navigator.mimeTypes[i].type,
        description: navigator.mimeTypes[i].description,
        suffixes: navigator.mimeTypes[i].suffixes,
    });
}`

**Plugin Enumeration Detection**

**Modern Chrome/Firefox**: Return empty arrays for `navigator.plugins` and `navigator.mimeTypes` to prevent fingerprinting.

**Headless Chrome**: Often returns **empty** arrays even when plugins exist, revealing automation.

**Detection**: If browser claims to be Chrome but has no plugins, it's suspicious.

### Timezone and Date Properties

Timezone information is surprisingly revealing:

`const timezoneFingerprint = {
    // Timezone offset in minutes
    timezoneOffset: new Date().getTimezoneOffset(),
    // IANA timezone name (e.g., "America/New_York")
    timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
    // Locale
    locale: Intl.DateTimeFormat().resolvedOptions().locale,
    // Date formatting
    dateFormat: new Date().toLocaleDateString(),
    timeFormat: new Date().toLocaleTimeString(),
};`

**Consistency check:**

`def validate_timezone_consistency(tz_offset: int, tz_name: str, accept_language: str) -> list[str]:
    """
    Validate timezone consistency with language/location.
    """
    issues = []
    # Timezone-language expected mappings
    tz_to_languages = {
        'America/New_York': ['en-US', 'en'],
        'Europe/London': ['en-GB', 'en'],
        'Asia/Tokyo': ['ja-JP', 'ja'],
        'Europe/Berlin': ['de-DE', 'de'],
    }
    expected_langs = tz_to_languages.get(tz_name, [])
    primary_lang = accept_language.split(',')[0].split(';')[0]
    if expected_langs and primary_lang not in expected_langs:
        issues.append(f"Timezone {tz_name} inconsistent with language {primary_lang}")
    # Timezone offset validation
    expected_offsets = {
        'America/New_York': -300,  # EST (minutes)
        'Europe/London': 0,        # GMT
        'Asia/Tokyo': -540,        # JST
    }
    expected_offset = expected_offsets.get(tz_name)
    if expected_offset and tz_offset != expected_offset:
        issues.append(f"Timezone offset {tz_offset} doesn't match {tz_name}")
    return issues`

### Permissions and Battery API

Some APIs require user permission but can still fingerprint:

`// Battery API (if available)
if (navigator.getBattery) {
    navigator.getBattery().then(battery => {
        const batteryInfo = {
            charging: battery.charging,
            chargingTime: battery.chargingTime,
            dischargingTime: battery.dischargingTime,
            level: battery.level,
        };
        // Battery level can be used as entropy
    });
}
// Permissions
navigator.permissions.query({name: 'geolocation'}).then(result => {
    console.log('Geolocation permission:', result.state);
    // 'granted', 'denied', 'prompt'
});`

**navigator.webdriver Detection**

The `navigator.webdriver` property is **the most obvious** automation indicator:

`if (navigator.webdriver === true) {
    alert('Automation detected!');
}`

**Selenium, Puppeteer, Playwright** all set this to `true` by default. CDP automation (like Pydoll) does **not** set this property, making it more stealthy.

### Python Implementation: Collecting Browser Properties

`async def collect_browser_fingerprint(tab) -> dict:
    """
    Collect comprehensive browser fingerprint using Pydoll.
    """
    fingerprint = await tab.execute_script('''
        () => {
            return {
                // Navigator
                userAgent: navigator.userAgent,
                platform: navigator.platform,
                language: navigator.language,
                languages: navigator.languages,
                hardwareConcurrency: navigator.hardwareConcurrency,
                deviceMemory: navigator.deviceMemory,
                maxTouchPoints: navigator.maxTouchPoints,
                vendor: navigator.vendor,
                cookieEnabled: navigator.cookieEnabled,
                doNotTrack: navigator.doNotTrack,
                webdriver: navigator.webdriver,
                // Screen
                screen: {
                    width: screen.width,
                    height: screen.height,
                    availWidth: screen.availWidth,
                    availHeight: screen.availHeight,
                    colorDepth: screen.colorDepth,
                    pixelDepth: screen.pixelDepth,
                },
                // Window
                window: {
                    innerWidth: window.innerWidth,
                    innerHeight: window.innerHeight,
                    outerWidth: window.outerWidth,
                    outerHeight: window.outerHeight,
                    devicePixelRatio: window.devicePixelRatio,
                },
                // Timezone
                timezone: {
                    offset: new Date().getTimezoneOffset(),
                    name: Intl.DateTimeFormat().resolvedOptions().timeZone,
                },
                // Plugins (legacy, but still checked)
                plugins: Array.from(navigator.plugins).map(p => ({
                    name: p.name,
                    description: p.description,
                })),
                // User Agent Data (Chrome)
                userAgentData: navigator.userAgentData ? {
                    brands: navigator.userAgentData.brands,
                    mobile: navigator.userAgentData.mobile,
                    platform: navigator.userAgentData.platform,
                } : null,
            };
        }
    ''')
    return fingerprint
# Usage example
import asyncio
from pydoll.browser.chromium import Chrome
async def main():
    async with Chrome() as browser:
        tab = await browser.start()
        await tab.go_to('https://example.com')
        fingerprint = await collect_browser_fingerprint(tab)
        print("Browser Fingerprint:")
        print(f"  User-Agent: {fingerprint['userAgent']}")
        print(f"  Platform: {fingerprint['platform']}")
        print(f"  Languages: {fingerprint['languages']}")
        print(f"  Hardware Concurrency: {fingerprint['hardwareConcurrency']}")
        print(f"  Screen: {fingerprint['screen']['width']}x{fingerprint['screen']['height']}")
        print(f"  Timezone: {fingerprint['timezone']['name']}")
        print(f"  Webdriver: {fingerprint['webdriver']}")
asyncio.run(main())`

**JavaScript Properties References**

- [**Fingerprint.com: Browser Fingerprinting Techniques**](https://fingerprint.com/blog/browser-fingerprinting-techniques/) - Comprehensive guide to all fingerprinting methods
- [**NordLayer: Browser Fingerprinting Guide**](https://nordlayer.com/learn/browser-security/browser-fingerprinting/) - How browser fingerprinting works
- [**AIMultiple: Browser Fingerprinting Best Practices**](https://research.aimultiple.com/browser-fingerprinting/) - Technical analysis of fingerprinting techniques
- [**Bureau.id: Top 9 Fingerprinting Techniques**](https://www.bureau.id/blog/browser-fingerprinting-techniques) - Detailed breakdown of detection methods

## Canvas Fingerprinting

Canvas fingerprinting exploits subtle differences in how browsers render graphics on the HTML5 `<canvas>` element. These differences arise from variations in hardware (GPU), graphics drivers, operating systems, and browser implementations.

### How Canvas Fingerprinting Works

The technique involves: 1. Drawing specific text/shapes on a canvas 2. Extracting the pixel data with `toDataURL()` or `getImageData()` 3. Hashing the result to create a unique fingerprint

**Factors affecting canvas rendering:** - **GPU and drivers**: Different GPUs render anti-aliasing differently - **Operating System**: Font rendering varies (ClearType on Windows, FreeType on Linux) - **Browser engine**: WebKit vs Blink vs Gecko have different rendering pipelines - **Graphics libraries**: Skia (Chrome) vs Cairo (Firefox)

### Canvas Fingerprinting Technique

`function generateCanvasFingerprint() {
    // Create canvas
    const canvas = document.createElement('canvas');
    canvas.width = 220;
    canvas.height = 30;
    const ctx = canvas.getContext('2d');
    // Text rendering (most distinctive)
    ctx.textBaseline = 'top';
    ctx.font = '14px "Arial"';
    ctx.textBaseline = 'alphabetic';
    // Add color gradients (exposes rendering differences)
    ctx.fillStyle = '#f60';
    ctx.fillRect(125, 1, 62, 20);
    // Add semi-transparent color (blending differences)
    ctx.fillStyle = '#069';
    ctx.fillText('Cwm fjordbank glyphs vext quiz, 😃', 2, 15);
    ctx.fillStyle = 'rgba(102, 204, 0, 0.7)';
    ctx.fillText('Cwm fjordbank glyphs vext quiz, 😃', 4, 17);
    // Extract data URL
    const dataURL = canvas.toDataURL();
    // Generate hash (MD5, SHA-256, etc.)
    return hashString(dataURL);
}
// Simpler hash function for demo
function hashString(str) {
    let hash = 0;
    for (let i = 0; i < str.length; i++) {
        const char = str.charCodeAt(i);
        hash = ((hash << 5) - hash) + char;
        hash = hash & hash; // Convert to 32-bit integer
    }
    return hash.toString(16);
}`

**Why the specific test string?**

- **"Cwm fjordbank glyphs vext quiz"**: Pangram with unusual characters to maximize font rendering variations
- **Emoji (😃)**: Emoji rendering varies significantly across systems
- **Mixed fonts/sizes**: Increases entropy

### Canvas Fingerprint Uniqueness

Research by [USENIX](https://www.usenix.org/conference/usenixsecurity12/technical-sessions/presentation/mowery) shows:

- **5.5% chance** of two random users having the same canvas fingerprint
- When combined with other techniques, uniqueness increases to **99.24%**

### Detecting Canvas Fingerprinting

Websites detect fingerprint modification attempts:

`// Detect if canvas is being blocked/modified
const originalToDataURL = HTMLCanvasElement.prototype.toDataURL;
HTMLCanvasElement.prototype.toDataURL = function() {
    // Check if fingerprint is consistent
    const result = originalToDataURL.apply(this, arguments);
    // If result changes on every call → fake fingerprint detected
    return result;
};
// Advanced detection: Check for noise injection
function detectCanvasNoise(canvas) {
    const ctx = canvas.getContext('2d');
    // Draw known pattern
    ctx.fillStyle = '#ff0000';
    ctx.fillRect(0, 0, 10, 10);
    // Read back pixels
    const imageData = ctx.getImageData(0, 0, 10, 10);
    const pixels = imageData.data;
    // Check if exactly red (255, 0, 0) or if there's noise
    for (let i = 0; i < pixels.length; i += 4) {
        if (pixels[i] !== 255 || pixels[i + 1] !== 0 || pixels[i + 2] !== 0) {
            return true;  // Noise detected = fingerprint blocking
        }
    }
    return false;  // Clean canvas
}`

### Python Implementation with Pydoll

`import hashlib
import asyncio
from pydoll.browser.chromium import Chrome
async def get_canvas_fingerprint(tab) -> str:
    """
    Generate canvas fingerprint using Pydoll.
    """
    fingerprint = await tab.execute_script('''
        () => {
            const canvas = document.createElement('canvas');
            canvas.width = 220;
            canvas.height = 30;
            const ctx = canvas.getContext('2d');
            // Text rendering
            ctx.textBaseline = 'top';
            ctx.font = '14px "Arial"';
            ctx.textBaseline = 'alphabetic';
            // Color blocks
            ctx.fillStyle = '#f60';
            ctx.fillRect(125, 1, 62, 20);
            // Text with emoji
            ctx.fillStyle = '#069';
            ctx.fillText('Cwm fjordbank glyphs vext quiz, 😃', 2, 15);
            ctx.fillStyle = 'rgba(102, 204, 0, 0.7)';
            ctx.fillText('Cwm fjordbank glyphs vext quiz, 😃', 4, 17);
            // Return data URL
            return canvas.toDataURL();
        }
    ''')
    # Hash the canvas data
    canvas_hash = hashlib.sha256(fingerprint.encode()).hexdigest()
    return canvas_hash
async def compare_canvas_consistency(tab, iterations: int = 3) -> bool:
    """
    Check if canvas fingerprint is consistent (not randomly generated).
    """
    fingerprints = []
    for _ in range(iterations):
        fp = await get_canvas_fingerprint(tab)
        fingerprints.append(fp)
        await asyncio.sleep(0.1)
    # All fingerprints should be identical
    is_consistent = len(set(fingerprints)) == 1
    if not is_consistent:
        print("Canvas fingerprint is inconsistent (possible fake)")
        print(f"  Unique values: {len(set(fingerprints))}")
    return is_consistent
# Usage
async def main():
    async with Chrome() as browser:
        tab = await browser.start()
        await tab.go_to('https://example.com')
        canvas_fp = await get_canvas_fingerprint(tab)
        print(f"Canvas Fingerprint: {canvas_fp}")
        is_consistent = await compare_canvas_consistency(tab)
        print(f"Consistency check: {'PASS' if is_consistent else 'FAIL'}")
asyncio.run(main())`

**Canvas Fingerprint Blocking Detection**

Many anti-fingerprinting tools inject **random noise** into canvas data to prevent tracking. However, this creates an **inconsistent fingerprint** that changes on every request, which is itself detectable!

**Detection technique:**

1. Request canvas fingerprint multiple times
2. If values differ → noise injection detected
3. Flag as "fingerprint blocking = suspicious behavior"

## WebGL Fingerprinting

WebGL fingerprinting is more powerful than Canvas because it exposes detailed information about the **GPU, drivers, and graphics stack**.

### WebGL Renderer Information

The most distinctive WebGL data comes from the `WEBGL_debug_renderer_info` extension:

`function getWebGLFingerprint() {
    const canvas = document.createElement('canvas');
    const gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl');
    if (!gl) {
        return null;  // WebGL not supported
    }
    const fingerprint = {
        // Get debug info (most distinctive)
        debugInfo: (() => {
            const ext = gl.getExtension('WEBGL_debug_renderer_info');
            if (ext) {
                return {
                    vendor: gl.getParameter(ext.UNMASKED_VENDOR_WEBGL),
                    renderer: gl.getParameter(ext.UNMASKED_RENDERER_WEBGL),
                };
            }
            return {
                vendor: gl.getParameter(gl.VENDOR),
                renderer: gl.getParameter(gl.RENDERER),
            };
        })(),
        // Supported extensions
        extensions: gl.getSupportedExtensions(),
        // WebGL parameters
        parameters: {
            version: gl.getParameter(gl.VERSION),
            shadingLanguageVersion: gl.getParameter(gl.SHADING_LANGUAGE_VERSION),
            maxTextureSize: gl.getParameter(gl.MAX_TEXTURE_SIZE),
            maxViewportDims: gl.getParameter(gl.MAX_VIEWPORT_DIMS),
            maxRenderbufferSize: gl.getParameter(gl.MAX_RENDERBUFFER_SIZE),
            maxVertexAttribs: gl.getParameter(gl.MAX_VERTEX_ATTRIBS),
            maxVertexUniformVectors: gl.getParameter(gl.MAX_VERTEX_UNIFORM_VECTORS),
            maxFragmentUniformVectors: gl.getParameter(gl.MAX_FRAGMENT_UNIFORM_VECTORS),
            maxVaryingVectors: gl.getParameter(gl.MAX_VARYING_VECTORS),
            aliasedLineWidthRange: gl.getParameter(gl.ALIASED_LINE_WIDTH_RANGE),
            aliasedPointSizeRange: gl.getParameter(gl.ALIASED_POINT_SIZE_RANGE),
        },
        // Precision formats
        precisionFormats: {
            vertexShader: {
                highFloat: getShaderPrecisionFormat(gl, gl.VERTEX_SHADER, gl.HIGH_FLOAT),
                mediumFloat: getShaderPrecisionFormat(gl, gl.VERTEX_SHADER, gl.MEDIUM_FLOAT),
                lowFloat: getShaderPrecisionFormat(gl, gl.VERTEX_SHADER, gl.LOW_FLOAT),
            },
            fragmentShader: {
                highFloat: getShaderPrecisionFormat(gl, gl.FRAGMENT_SHADER, gl.HIGH_FLOAT),
                mediumFloat: getShaderPrecisionFormat(gl, gl.FRAGMENT_SHADER, gl.MEDIUM_FLOAT),
                lowFloat: getShaderPrecisionFormat(gl, gl.FRAGMENT_SHADER, gl.LOW_FLOAT),
            },
        },
    };
    return fingerprint;
}
function getShaderPrecisionFormat(gl, shaderType, precisionType) {
    const format = gl.getShaderPrecisionFormat(shaderType, precisionType);
    return {
        rangeMin: format.rangeMin,
        rangeMax: format.rangeMax,
        precision: format.precision,
    };
}`

**Example output:**

`{
    "debugInfo": {
        "vendor": "Google Inc. (NVIDIA)",
        "renderer": "ANGLE (NVIDIA, NVIDIA GeForce RTX 3080 Direct3D11 vs_5_0 ps_5_0)"
    },
    "extensions": [
        "ANGLE_instanced_arrays",
        "EXT_blend_minmax",
        "EXT_color_buffer_half_float",
        "EXT_disjoint_timer_query",
        "EXT_float_blend",
        "EXT_frag_depth",
        "EXT_shader_texture_lod",
        "EXT_texture_compression_bptc",
        "EXT_texture_filter_anisotropic",
        "WEBKIT_EXT_texture_filter_anisotropic",
        "EXT_sRGB",
        "OES_element_index_uint",
        "OES_fbo_render_mipmap",
        "OES_standard_derivatives",
        "OES_texture_float",
        "OES_texture_float_linear",
        "OES_texture_half_float",
        "OES_texture_half_float_linear",
        "OES_vertex_array_object",
        "WEBGL_color_buffer_float",
        "WEBGL_compressed_texture_s3tc",
        "WEBGL_compressed_texture_s3tc_srgb",
        "WEBGL_debug_renderer_info",
        "WEBGL_debug_shaders",
        "WEBGL_depth_texture",
        "WEBGL_draw_buffers",
        "WEBGL_lose_context",
        "WEBGL_multi_draw"
    ],
    "parameters": {
        "version": "WebGL 1.0 (OpenGL ES 2.0 Chromium)",
        "shadingLanguageVersion": "WebGL GLSL ES 1.0 (OpenGL ES GLSL ES 1.0 Chromium)",
        "maxTextureSize": 16384,
        "maxViewportDims": [32767, 32767],
        "maxRenderbufferSize": 16384
    }
}`

### WebGL Rendering Fingerprint

Beyond metadata, WebGL can render a 3D scene and analyze pixel output:

`function getWebGLRenderFingerprint() {
    const canvas = document.createElement('canvas');
    canvas.width = 256;
    canvas.height = 128;
    const gl = canvas.getContext('webgl');
    // Vertex shader
    const vertexShaderSource = `
        attribute vec2 position;
        void main() {
            gl_Position = vec4(position, 0.0, 1.0);
        }
    `;
    // Fragment shader with gradient
    const fragmentShaderSource = `
        precision mediump float;
        void main() {
            gl_FragColor = vec4(gl_FragCoord.x/256.0, gl_FragCoord.y/128.0, 0.5, 1.0);
        }
    `;
    // Compile shaders
    const vertexShader = gl.createShader(gl.VERTEX_SHADER);
    gl.shaderSource(vertexShader, vertexShaderSource);
    gl.compileShader(vertexShader);
    const fragmentShader = gl.createShader(gl.FRAGMENT_SHADER);
    gl.shaderSource(fragmentShader, fragmentShaderSource);
    gl.compileShader(fragmentShader);
    // Link program
    const program = gl.createProgram();
    gl.attachShader(program, vertexShader);
    gl.attachShader(program, fragmentShader);
    gl.linkProgram(program);
    gl.useProgram(program);
    // Draw triangle
    const vertices = new Float32Array([-1, -1, 1, -1, 0, 1]);
    const buffer = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, buffer);
    gl.bufferData(gl.ARRAY_BUFFER, vertices, gl.STATIC_DRAW);
    const position = gl.getAttribLocation(program, 'position');
    gl.enableVertexAttribArray(position);
    gl.vertexAttribPointer(position, 2, gl.FLOAT, false, 0, 0);
    gl.drawArrays(gl.TRIANGLES, 0, 3);
    // Extract rendered image
    return canvas.toDataURL();
}`

### Python Implementation with Pydoll

`async def get_webgl_fingerprint(tab) -> dict:
    """
    Collect WebGL fingerprint data.
    """
    fingerprint = await tab.execute_script('''
        () => {
            const canvas = document.createElement('canvas');
            const gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl');
            if (!gl) {
                return null;
            }
            // Get debug info
            const debugInfo = gl.getExtension('WEBGL_debug_renderer_info');
            const vendor = debugInfo ? 
                gl.getParameter(debugInfo.UNMASKED_VENDOR_WEBGL) : 
                gl.getParameter(gl.VENDOR);
            const renderer = debugInfo ? 
                gl.getParameter(debugInfo.UNMASKED_RENDERER_WEBGL) : 
                gl.getParameter(gl.RENDERER);
            return {
                vendor: vendor,
                renderer: renderer,
                version: gl.getParameter(gl.VERSION),
                shadingLanguageVersion: gl.getParameter(gl.SHADING_LANGUAGE_VERSION),
                extensions: gl.getSupportedExtensions(),
                maxTextureSize: gl.getParameter(gl.MAX_TEXTURE_SIZE),
                maxViewportDims: gl.getParameter(gl.MAX_VIEWPORT_DIMS),
            };
        }
    ''')
    return fingerprint
async def main():
    async with Chrome() as browser:
        tab = await browser.start()
        await tab.go_to('https://example.com')
        webgl_fp = await get_webgl_fingerprint(tab)
        if webgl_fp:
            print("WebGL Fingerprint:")
            print(f"  Vendor: {webgl_fp['vendor']}")
            print(f"  Renderer: {webgl_fp['renderer']}")
            print(f"  Version: {webgl_fp['version']}")
            print(f"  Extensions: {len(webgl_fp['extensions'])} available")
        else:
            print("WebGL not available")
asyncio.run(main())`

**WebGL Fingerprint Blocking**

Some privacy tools attempt to block WebGL fingerprinting by:

1. **Disabling WEBGL_debug_renderer_info extension**
2. **Returning generic "SwiftShader" renderer** (software rendering)
3. **Spoofing GPU vendor/renderer strings**

However, **missing or generic WebGL data is suspicious** because: - 97% of browsers support WebGL - Generic renderers have performance implications (detectable via timing) - Absence of common extensions reveals blocking



Fingerprint Evasion Techniques
This document provides **practical, actionable techniques** for evading fingerprinting using Pydoll's CDP integration, JavaScript overrides, and request interception. Everything described here has been tested and validated.

**Module Navigation**

- [**← Fingerprinting Overview**](https://pydoll.tech/docs/deep-dive/fingerprinting/) - Module introduction and philosophy
- [**← Network Fingerprinting**](https://pydoll.tech/docs/deep-dive/fingerprinting/network-fingerprinting/) - Protocol-level fingerprinting
- [**← Browser Fingerprinting**](https://pydoll.tech/docs/deep-dive/fingerprinting/browser-fingerprinting/) - Application-layer fingerprinting
- [**← Behavioral Fingerprinting**](https://pydoll.tech/docs/deep-dive/fingerprinting/behavioral-fingerprinting/) - Human behavior analysis

For practical Pydoll usage, see [**Human-Like Interactions**](https://pydoll.tech/docs/features/automation/human-interactions/) and [**Behavioral Captcha Bypass**](https://pydoll.tech/docs/features/advanced/behavioral-captcha-bypass/).

**Theory → Practice**

This is where everything you've learned about network and browser fingerprinting gets applied. Each technique includes **working code examples** ready to integrate with Pydoll.

## CDP-Based Fingerprint Evasion

The Chrome DevTools Protocol (CDP) provides powerful methods to modify browser behavior at a deep level, far beyond what JavaScript injection can achieve. This makes CDP-based automation (like Pydoll) **significantly more stealthy** than Selenium or Puppeteer.

### The User-Agent Mismatch Problem

One of the **most common** fingerprinting inconsistencies in automation is the mismatch between:

1. **HTTP `User-Agent` header** (sent with every request)
2. **`navigator.userAgent`** property (JavaScript-accessible)

**The problem:**

`# Bad approach: Setting User-Agent via command-line argument
options = ChromiumOptions()
options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)...')
# Result:
# HTTP header: Mozilla/5.0 (Windows NT 10.0; Win64; x64)... (correct)
# navigator.userAgent: Chrome/120.0.0.0 (original value - wrong!)
# → MISMATCH DETECTED!`

**Why this happens:**

- `-user-agent` flag only modifies **HTTP headers**
- `navigator.userAgent` is set **before** page load from internal Chromium values
- JavaScript cannot see HTTP headers directly, but servers can compare both values

**Detection technique (server-side):**

`def detect_user_agent_mismatch(request):
    """
    Server-side detection of User-Agent inconsistency.
    """
    # Get HTTP header
    http_user_agent = request.headers.get('User-Agent')
    # Execute JavaScript to get navigator.userAgent
    # (done via challenge/captcha page)
    navigator_user_agent = get_client_navigator_ua()
    if http_user_agent != navigator_user_agent:
        return 'AUTOMATION_DETECTED'  # Clear mismatch
    return 'OK'`

### Solution: CDP Emulation Domain

The correct way to set User-Agent is via CDP's **Emulation.setUserAgentOverride** method, which modifies **both** the HTTP header and navigator properties. In Pydoll, you can execute CDP commands directly:

`import asyncio
from pydoll.browser.chromium import Chrome
from pydoll.commands import PageCommands
async def set_user_agent_correctly(tab, user_agent: str, platform: str = 'Win32'):
    """
    Set User-Agent properly using CDP Emulation domain.
    This ensures consistency between HTTP headers and navigator properties.
    Note: Pydoll doesn't expose Emulation commands directly yet, so we use
    execute_script to override navigator properties for now.
    """
    # Override navigator.userAgent via JavaScript
    override_script = f'''
        Object.defineProperty(Navigator.prototype, 'userAgent', {{
            get: () => '{user_agent}'
        }});
        Object.defineProperty(Navigator.prototype, 'platform', {{
            get: () => '{platform}'
        }});
    '''
    await tab.execute_script(override_script)
async def main():
    async with Chrome() as browser:
        # Set User-Agent via command-line argument (affects HTTP headers)
        options = browser.options
        custom_ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        options.add_argument(f'--user-agent={custom_ua}')
        tab = await browser.start()
        # Also override navigator.userAgent via JavaScript for consistency
        await set_user_agent_correctly(tab, custom_ua)
        # Navigate (User-Agent now consistent)
        await tab.go_to('https://example.com')
        # Verify consistency
        result = await tab.execute_script('return navigator.userAgent')
        nav_ua = result['result']['result']['value']
        print(f"navigator.userAgent: {nav_ua}")
        # Both match now!
asyncio.run(main())`

**Client Hints Consistency**

When setting a custom User-Agent, you **must** also set consistent `userAgentMetadata` (Client Hints), otherwise modern Chromium will send **inconsistent** `Sec-CH-UA` headers!

**Example inconsistency:**

- User-Agent: "Chrome/120.0.0.0"
- Sec-CH-UA: "Chrome/119" (wrong version!)
- → Detection!

### Fingerprint Modification Techniques

While Pydoll doesn't expose all CDP Emulation commands directly, you can achieve similar results using JavaScript overrides and browser options:

### **1. Timezone Override (via JavaScript)**

`async def set_timezone(tab, timezone_id: str):
    """
    Override timezone via JavaScript.
    Example: 'America/New_York', 'Europe/London', 'Asia/Tokyo'
    Note: This overrides the JavaScript API but doesn't affect system-level
    timezone. Use --tz command-line argument for complete emulation.
    """
    script = f'''
        // Override Intl.DateTimeFormat
        const originalDateTimeFormat = Intl.DateTimeFormat;
        Intl.DateTimeFormat = function(...args) {{
            const options = args[1] || {{}};
            options.timeZone = '{timezone_id}';
            return new originalDateTimeFormat(args[0], options);
        }};
        // Override Date.prototype.getTimezoneOffset
        const timezoneOffsets = {{
            'America/New_York': 300,
            'Europe/London': 0,
            'Asia/Tokyo': -540,
            'America/Los_Angeles': 480,
        }};
        Date.prototype.getTimezoneOffset = function() {{
            return timezoneOffsets['{timezone_id}'] || 0;
        }};
    '''
    await tab.execute_script(script)
# Usage
await set_timezone(tab, 'America/Los_Angeles')
# Verify
result = await tab.execute_script('return Intl.DateTimeFormat().resolvedOptions().timeZone')
tz = result['result']['result']['value']
print(f"Timezone: {tz}")  # America/Los_Angeles`

### **2. Locale Override (via Browser Options)**

`# Set locale via command-line arguments
from pydoll.browser.chromium import Chrome
from pydoll.browser.options import ChromiumOptions
options = ChromiumOptions()
options.add_argument('--lang=pt-BR')
options.set_accept_languages('pt-BR,pt;q=0.9,en;q=0.8')
async with Chrome(options=options) as browser:
    tab = await browser.start()
    # Verify
    result = await tab.execute_script('return navigator.language')
    locale = result['result']['result']['value']
    print(f"Locale: {locale}")  # pt-BR`

### **3. Geolocation Override (via JavaScript)**

`async def set_geolocation(tab, latitude: float, longitude: float, accuracy: int = 1):
    """
    Override geolocation via JavaScript.
    """
    script = f'''
        navigator.geolocation.getCurrentPosition = function(success) {{
            const position = {{
                coords: {{
                    latitude: {latitude},
                    longitude: {longitude},
                    accuracy: {accuracy},
                    altitude: null,
                    altitudeAccuracy: null,
                    heading: null,
                    speed: null
                }},
                timestamp: Date.now()
            }};
            success(position);
        }};
    '''
    await tab.execute_script(script)
# Example: New York City
await set_geolocation(tab, 40.7128, -74.0060)`

### **4. Device Metrics (via Browser Options)**

`# Mobile emulation via command-line arguments
options = ChromiumOptions()
options.add_argument('--window-size=393,852')
options.add_argument('--device-scale-factor=3')
options.add_argument('--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1')
async with Chrome(options=options) as browser:
    tab = await browser.start()
    # Override additional mobile properties
    mobile_script = '''
        Object.defineProperty(Navigator.prototype, 'maxTouchPoints', {
            get: () => 5
        });
        // Override screen properties
        Object.defineProperty(window.screen, 'width', { get: () => 393 });
        Object.defineProperty(window.screen, 'height', { get: () => 852 });
        Object.defineProperty(window.screen, 'availWidth', { get: () => 393 });
        Object.defineProperty(window.screen, 'availHeight', { get: () => 852 });
    '''
    await tab.execute_script(mobile_script)`

### **5. Touch Events (via JavaScript)**

`async def enable_touch_events(tab, max_touch_points: int = 5):
    """
    Override touch-related properties.
    """
    script = f'''
        Object.defineProperty(Navigator.prototype, 'maxTouchPoints', {{
            get: () => {max_touch_points}
        }});
        // Add touch event support
        if (!window.TouchEvent) {{
            window.TouchEvent = class TouchEvent extends UIEvent {{}};
        }}
    '''
    await tab.execute_script(script)
# Verify
result = await tab.execute_script('return navigator.maxTouchPoints')
touch_points = result['result']['result']['value']
print(f"Max Touch Points: {touch_points}")  # 5`

### Request Interception for Header Modification

Pydoll provides native support for request interception via the Fetch domain. This allows you to modify headers, block requests, or provide custom responses:

`import asyncio
from pydoll.browser.chromium import Chrome
from pydoll.protocol.fetch.events import FetchEvent
async def setup_request_interception(tab):
    """
    Intercept all requests and modify headers using Pydoll's native methods.
    """
    # Enable Fetch domain for request interception
    await tab.enable_fetch_events()
    # Listen for request paused events
    async def handle_request(event):
        """Handle intercepted requests."""
        request_id = event['params']['requestId']
        request = event['params']['request']
        # Get current headers
        headers = request.get('headers', {})
        # Fix common inconsistencies
        if 'Accept-Encoding' in headers:
            # Ensure Brotli support
            if 'br' not in headers['Accept-Encoding']:
                headers['Accept-Encoding'] = 'gzip, deflate, br, zstd'
        # Remove automation markers
        headers.pop('X-Requested-With', None)
        # Convert headers to HeaderEntry format
        header_list = [{'name': k, 'value': v} for k, v in headers.items()]
        # Continue request with modified headers
        await tab.continue_request(
            request_id=request_id,
            headers=header_list
        )
    # Register event listener for request paused events
    await tab.on(FetchEvent.REQUEST_PAUSED, handle_request)
async def main():
    async with Chrome() as browser:
        tab = await browser.start()
        # Setup interception before navigation
        await setup_request_interception(tab)
        # All requests will now have modified headers
        await tab.go_to('https://example.com')
asyncio.run(main())`

### Complete Fingerprint Evasion Example

Here's a comprehensive example combining all techniques using Pydoll's API:

`import asyncio
from pydoll.browser.chromium import Chrome
from pydoll.browser.options import ChromiumOptions
class FingerprintEvader:
    """
    Comprehensive fingerprint evasion using browser options and JavaScript.
    """
    def __init__(self, profile: dict):
        """
        Initialize with target profile (OS, location, device, etc.)
        """
        self.profile = profile
        self.options = ChromiumOptions()
        self._configure_browser_options()
    def _configure_browser_options(self):
        """Configure browser launch options based on profile."""
        # 1. User-Agent
        self.options.add_argument(f'--user-agent={self.profile["userAgent"]}')
        # 2. Language and locale
        self.options.add_argument(f'--lang={self.profile["locale"]}')
        self.options.set_accept_languages(self.profile["acceptLanguage"])
        # 3. Window size (screen dimensions)
        screen = self.profile['screen']
        self.options.add_argument(f'--window-size={screen["width"]},{screen["height"]}')
        # 4. Device scale factor (for high-DPI displays)
        if screen.get('deviceScaleFactor', 1.0) != 1.0:
            self.options.add_argument(f'--device-scale-factor={screen["deviceScaleFactor"]}')
    async def apply_to_tab(self, tab):
        """
        Apply JavaScript overrides to tab after launch.
        """
        script = f'''
            // Override User-Agent (for consistency)
            Object.defineProperty(Navigator.prototype, 'userAgent', {{
                get: () => '{self.profile["userAgent"]}'
            }});
            // Override platform
            Object.defineProperty(Navigator.prototype, 'platform', {{
                get: () => '{self.profile["platform"]}'
            }});
            // Override hardware concurrency
            Object.defineProperty(Navigator.prototype, 'hardwareConcurrency', {{
                get: () => {self.profile.get('hardwareConcurrency', 8)}
            }});
            // Override device memory
            Object.defineProperty(Navigator.prototype, 'deviceMemory', {{
                get: () => {self.profile.get('deviceMemory', 8)}
            }});
            // Override languages
            Object.defineProperty(Navigator.prototype, 'languages', {{
                get: () => {self.profile['languages']}
            }});
            // Override vendor
            Object.defineProperty(Navigator.prototype, 'vendor', {{
                get: () => '{self.profile.get('vendor', 'Google Inc.')}'
            }});
            // Override max touch points (for mobile)
            Object.defineProperty(Navigator.prototype, 'maxTouchPoints', {{
                get: () => {self.profile.get('maxTouchPoints', 0)}
            }});
        '''
        await tab.execute_script(script)
        # Apply geolocation if provided
        if 'geolocation' in self.profile:
            await self._override_geolocation(tab)
        # Apply timezone if provided
        if 'timezone' in self.profile:
            await self._override_timezone(tab)
    async def _override_geolocation(self, tab):
        """Override geolocation API."""
        geo = self.profile['geolocation']
        script = f'''
            navigator.geolocation.getCurrentPosition = function(success) {{
                const position = {{
                    coords: {{
                        latitude: {geo['latitude']},
                        longitude: {geo['longitude']},
                        accuracy: 1,
                        altitude: null,
                        altitudeAccuracy: null,
                        heading: null,
                        speed: null
                    }},
                    timestamp: Date.now()
                }};
                success(position);
            }};
        '''
        await tab.execute_script(script)
    async def _override_timezone(self, tab):
        """Override timezone-related functions."""
        timezone = self.profile['timezone']
        # Map of timezone to offset in minutes
        offsets = {
            'America/New_York': 300,
            'Europe/London': 0,
            'Asia/Tokyo': -540,
            'America/Los_Angeles': 480,
        }
        offset = offsets.get(timezone, 0)
        script = f'''
            // Override Intl.DateTimeFormat
            const originalDateTimeFormat = Intl.DateTimeFormat;
            Intl.DateTimeFormat = function(...args) {{
                const options = args[1] || {{}};
                options.timeZone = '{timezone}';
                return new originalDateTimeFormat(args[0], options);
            }};
            // Override Date.prototype.getTimezoneOffset
            Date.prototype.getTimezoneOffset = function() {{
                return {offset};
            }};
        '''
        await tab.execute_script(script)
# Usage example
async def main():
    # Define target profile
    profile = {
        'userAgent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'platform': 'Win32',
        'acceptLanguage': 'en-US,en;q=0.9',
        'languages': ['en-US', 'en'],
        'timezone': 'America/New_York',
        'locale': 'en-US',
        'geolocation': {
            'latitude': 40.7128,
            'longitude': -74.0060
        },
        'screen': {
            'width': 1920,
            'height': 1080,
            'deviceScaleFactor': 1.0
        },
        'hardwareConcurrency': 8,
        'deviceMemory': 8,
        'vendor': 'Google Inc.',
        'maxTouchPoints': 0,  # Desktop
    }
    # Create evader with profile
    evader = FingerprintEvader(profile)
    # Launch browser with configured options
    async with Chrome(options=evader.options) as browser:
        tab = await browser.start()
        # Apply JavaScript overrides
        await evader.apply_to_tab(tab)
        # Navigate with consistent fingerprint
        await tab.go_to('https://example.com')
        # Verify fingerprint
        result = await tab.execute_script('''
            return {
                userAgent: navigator.userAgent,
                platform: navigator.platform,
                languages: navigator.languages,
                hardwareConcurrency: navigator.hardwareConcurrency,
                deviceMemory: navigator.deviceMemory,
                timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
                maxTouchPoints: navigator.maxTouchPoints,
            };
        ''')
        fingerprint = result['result']['result']['value']
        print("Applied Fingerprint:")
        for key, value in fingerprint.items():
            print(f"  {key}: {value}")
asyncio.run(main())`

**Fingerprint Consistency is Key**

The most important aspect of fingerprint evasion is **consistency across all layers**:

1. **HTTP headers** (User-Agent, Accept-Language, Sec-CH-UA)
2. **Navigator properties** (userAgent, platform, languages)
3. **System properties** (timezone, locale, screen resolution)
4. **Network fingerprint** (TLS, HTTP/2 settings)

A single inconsistency can reveal automation!

**CDP Emulation References**

- [**Chrome DevTools Protocol: Emulation Domain**](https://chromedevtools.github.io/devtools-protocol/tot/Emulation/) - Official CDP Emulation documentation
- [**Chrome DevTools Protocol: Fetch Domain**](https://chromedevtools.github.io/devtools-protocol/tot/Fetch/) - Request interception documentation
- [**Chromium Emulation Source**](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/inspector/inspector_emulation_agent.cc) - Emulation implementation in Chromium
- [**Pydoll CDP Guide**](https://pydoll.tech/docs/deep-dive/fingerprinting/evasion-techniques/cdp.md) - Using CDP with Pydoll

## Behavioral Evasion Strategies

Given Pydoll's CDP-based architecture, behavioral fingerprinting requires careful attention to human-like interaction patterns. For theoretical background on behavioral detection, see [Behavioral Fingerprinting](https://pydoll.tech/docs/deep-dive/fingerprinting/behavioral-fingerprinting/).

### Current State: Manual Randomization Required

As documented in [Human-Like Interactions](https://pydoll.tech/docs/features/automation/human-interactions/), Pydoll **currently requires manual implementation** of behavioral realism:

- **Mouse movements**: Must be implemented with Bezier curves and randomization
- **Typing**: Requires character-by-character input with variable intervals
- **Scrolling**: Needs manual JavaScript with momentum simulation
- **Event sequences**: Must ensure proper ordering (mousemove → mousedown → mouseup → click)

### Future Improvements

Future versions of Pydoll will include automated behavioral realism:

`# Future API (not yet implemented)
await element.click(
    realistic=True,              # Automatic Bezier curve movement
    offset='random',             # Random offset within bounds
    thinking_time=(1.0, 3.0)     # Random delay before action
)
await input_field.type_text(
    "human-like text",
    realistic=True,              # Variable typing speed with bigram timing
    error_rate=0.05              # 5% chance of typo + backspace
)
await tab.scroll_to(
    target_y=1000,
    realistic=True,              # Momentum + inertia simulation
    speed='medium'               # Human-like scroll speed
)`

### Practical Implementation Now

Until automation is built-in, follow these practices:

### **1. Mouse Movement Before Clicks**

`# Bad: Instant click without movement
await element.click()  # Teleports cursor and clicks center
# Good: Realistic movement first
# (Manual implementation required)
await move_mouse_realistically(element)
await asyncio.sleep(random.uniform(0.1, 0.3))
await element.click(x_offset=random.randint(-10, 10))`

### **2. Variable Typing Speed**

`# Bad: Constant interval
await input.type_text("text", interval=0.1)  # Robotic timing
# Good: Variable intervals per character
for char in "text":
    await input.type_text(char, interval=0)
    await asyncio.sleep(random.uniform(0.08, 0.22))`

### **3. Thinking Time**

`# Bad: Instant action after page load
await tab.go_to('https://example.com')
await button.click()  # Too fast!
# Good: Natural delay for reading/scanning
await tab.go_to('https://example.com')
await asyncio.sleep(random.uniform(2.0, 5.0))  # Read page
await random_mouse_movement()  # Scan with cursor
await button.click()  # Then act`

### **4. Scrolling with Momentum**

`# Bad: Instant scroll
await tab.execute_script("window.scrollTo(0, 1000)")
# Good: Gradual scroll with deceleration
scroll_events = simulate_human_scroll(target=1000)
for delta, delay in scroll_events:
    await tab.execute_script(f"window.scrollBy(0, {delta})")
    await asyncio.sleep(delay)`

**Behavioral Detection is ML-Powered**

Modern anti-bot systems use machine learning trained on billions of interactions. They don't use simple rules—they detect **statistical patterns**. Focus on:

1. **Variability**: No two actions should be identical
2. **Context**: Actions must follow natural sequences
3. **Timing**: Realistic intervals based on human biomechanics
4. **Consistency**: Don't mix bot-like and human-like patterns

## Best Practices for Fingerprint Evasion

Based on all the techniques covered in this guide, here are the essential best practices for successful fingerprint evasion in web automation:

### 1. Start with Real Browser Profiles

Don't invent fingerprints from scratch. Capture real browser profiles and use them:

`# Capture a real fingerprint from your own browser
# Visit https://browserleaks.com/ and collect all data
REAL_PROFILES = {
    'windows_chrome': {
        'userAgent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36...',
        'platform': 'Win32',
        'hardwareConcurrency': 8,
        'deviceMemory': 8,
        'canvas_hash': 'captured_from_real_browser',
        # ... all other properties
    }
}`

### 2. Maintain Consistency Across All Layers

**Check these consistency points:**

- User-Agent matches navigator.userAgent
- Platform matches User-Agent OS
- Language matches timezone/geolocation
- Screen resolution is realistic for claimed device
- Hardware specs match claimed platform (CPU cores, RAM)
- Canvas/WebGL fingerprints are stable (not randomized)
- Timezone matches Accept-Language header
- Client Hints match User-Agent

### 3. Use Browser Preferences for Stealth

Leverage Pydoll's browser preferences (see [Browser Preferences](https://pydoll.tech/docs/deep-dive/fingerprinting/features/configuration/browser-preferences.md)):

`from pydoll.browser.options import ChromiumOptions
options = ChromiumOptions()
options.browser_preferences = {
    # Simulate usage history
    'profile': {
        'created_by_version': '120.0.6099.130',
        'creation_time': str(time.time() - (90 * 24 * 60 * 60)),  # 90 days old
        'exit_type': 'Normal',
    },
    # Realistic content settings
    'profile.default_content_setting_values': {
        'cookies': 1,
        'images': 1,
        'javascript': 1,
        'notifications': 2,  # Ask (realistic)
    },
    # WebRTC IP handling (prevent leaks)
    'webrtc': {
        'ip_handling_policy': 'disable_non_proxied_udp',
    },
}`

### 4. Rotate Fingerprints Wisely

**Don't** change fingerprints too frequently on the same site:

`# Bad: New fingerprint every request
for url in urls:
    fingerprint = generate_random_fingerprint()  # Suspicious!
    apply_fingerprint(tab, fingerprint)
    await tab.go_to(url)
# Good: Consistent fingerprint per session
fingerprint = select_fingerprint_for_target(target_site)
apply_fingerprint(tab, fingerprint)
for url in urls:
    await tab.go_to(url)  # Same fingerprint`

### 5. Test Your Fingerprint

Use these tools to verify your fingerprint before deploying:

| **Tool** | **URL** | **Tests** |
| --- | --- | --- |
| **BrowserLeaks** | https://browserleaks.com/ | Comprehensive: Canvas, WebGL, Fonts, IP, WebRTC |
| **AmIUnique** | https://amiunique.org/ | Fingerprint uniqueness analysis |
| **CreepJS** | https://abrahamjuliot.github.io/creepjs/ | Advanced lie detection |
| **Fingerprint.com Demo** | https://fingerprint.com/demo/ | Commercial-grade detection |
| **PixelScan** | https://pixelscan.net/ | Bot detection analysis |
| **IPLeak** | https://ipleak.net/ | WebRTC, DNS, IP leaks |

**Verification script:**

`async def verify_fingerprint(tab):
    """
    Verify fingerprint consistency before actual use.
    """
    tests = []
    # Test 1: User-Agent consistency
    nav_ua = await tab.execute_script('return navigator.userAgent')
    print(f"User-Agent: {nav_ua[:50]}...")
    # Test 2: Timezone/Language consistency
    tz = await tab.execute_script('return Intl.DateTimeFormat().resolvedOptions().timeZone')
    lang = await tab.execute_script('return navigator.language')
    print(f"Timezone: {tz}, Language: {lang}")
    # Test 3: WebDriver detection
    webdriver = await tab.execute_script('return navigator.webdriver')
    if webdriver:
        print("navigator.webdriver is true! (DETECTED)")
        tests.append(False)
    else:
        print("navigator.webdriver is undefined (OK)")
        tests.append(True)
    # Test 4: Canvas consistency
    canvas1 = await get_canvas_fingerprint(tab)
    await asyncio.sleep(0.5)
    canvas2 = await get_canvas_fingerprint(tab)
    if canvas1 == canvas2:
        print("Canvas fingerprint is consistent (OK)")
        tests.append(True)
    else:
        print("Canvas fingerprint is inconsistent, noise detected (DETECTED)")
        tests.append(False)
    # Test 5: Plugins
    plugins = await tab.execute_script('return navigator.plugins.length')
    print(f"Plugins: {plugins}")
    return all(tests)`

### 6. Combine with Behavioral Realism

Fingerprint evasion alone is not enough. Combine with:

- **Human-like interactions** (see [Human Interactions](https://pydoll.tech/docs/deep-dive/fingerprinting/features/automation/human-interactions.md))
- **Natural timing** (random delays, realistic page interaction time)
- **Behavioral captcha handling** (see [Behavioral Captcha Bypass](https://pydoll.tech/docs/deep-dive/fingerprinting/features/advanced/behavioral-captcha-bypass.md))
- **Realistic cookies** (see [Cookies & Sessions](https://pydoll.tech/docs/deep-dive/fingerprinting/features/browser-management/cookies-sessions.md))

### 7. Monitor for Detection

Implement logging to detect when your automation is flagged:

`async def monitor_detection_signals(tab):
    """
    Monitor for signs of detection.
    """
    signals = await tab.execute_script('''
        () => {
            return {
                // Check for known detection scripts
                fpjs: typeof window.Fingerprint !== 'undefined',
                datadome: typeof window.DD_RUM !== 'undefined',
                perimeter_x: typeof window._pxAppId !== 'undefined',
                cloudflare: document.querySelector('script[src*="challenges.cloudflare.com"]') !== null,
                // Check for challenge pages
                is_captcha: document.title.includes('Captcha') || 
                           document.title.includes('Challenge') ||
                           document.body.innerText.includes('verification'),
            };
        }
    ''')
    if any(signals.values()):
        print("Detection signals found:")
        for key, value in signals.items():
            if value:
                print(f"  - {key}: detected")`

### 8. Use Proxies Correctly

Network-level fingerprinting requires proper proxy usage:

- **Match proxy location** with timezone/language
- **Use residential proxies** for high-value targets
- **Rotate proxies** but maintain fingerprint consistency per proxy
- **Test for WebRTC leaks** (see [Proxy Configuration](https://pydoll.tech/docs/deep-dive/fingerprinting/features/configuration/proxy.md))

## Common Mistakes to Avoid

### Mistake 1: Randomizing Everything

`# Bad: Random fingerprint that doesn't make sense
fingerprint = {
    'userAgent': 'Chrome 120 on Windows',
    'platform': 'Linux x86_64',  # Mismatch!
    'hardwareConcurrency': random.randint(1, 32),  # Too random
    'deviceMemory': random.choice([0.5, 128]),  # Unrealistic values
}`

**Why it fails**: Real browsers have **consistent, realistic** configurations. Random values create impossible combinations.

### Mistake 2: Ignoring Client Hints

`# Bad: Setting User-Agent without Client Hints
await tab.send_cdp_command('Emulation.setUserAgentOverride', {
    'userAgent': 'Chrome/120...',
    # Missing userAgentMetadata!
})
# Result: Sec-CH-UA headers will be inconsistent`

### Mistake 3: Canvas Noise Injection

`# Bad: Adding random noise to canvas
def add_canvas_noise(ctx):
    # Randomize pixel values
    imageData = ctx.getImageData(0, 0, 100, 100)
    for i in range(len(imageData.data)):
        imageData.data[i] += random.randint(-5, 5)  # Noise injection
    ctx.putImageData(imageData, 0, 0)`

**Why it fails**: Noise makes fingerprint **inconsistent**, which is itself detectable. Sites can request fingerprint multiple times and detect variations.

### Mistake 4: Outdated User-Agents

`# Bad: Using old browser version
userAgent = 'Mozilla/5.0 ... Chrome/90.0.0.0'  # 2 years old!`

**Why it fails**: Old versions missing modern features are easily detected. Use versions from the last 3-6 months.

### Mistake 5: Headless Mode Detection

`# Bad: Using headless without proper configuration
options = ChromiumOptions()
options.headless = True  # Detectable via window dimensions`

**Fix**: Use `--headless=new` with realistic window size:

`options = ChromiumOptions()
options.add_argument('--headless=new')
options.add_argument('--window-size=1920,1080')`

## Conclusion

Browser and network fingerprinting is a sophisticated cat-and-mouse game between automation developers and anti-bot systems. Success requires understanding fingerprinting at **multiple layers**:

**Network Level:** - TCP/IP characteristics (TTL, window size, options) - TLS handshake patterns (JA3, cipher suites, GREASE) - HTTP/2 settings and stream priorities

**Browser Level:** - HTTP headers consistency - JavaScript API properties (navigator, screen, etc.) - Canvas and WebGL rendering - CDP-based evasion techniques

**Behavioral Level:** - Mouse movement patterns and physics (Fitts's Law, Bezier curves) - Keystroke dynamics and typing rhythm (bigrams, dwell/flight time) - Scroll momentum and inertia - Event sequences and timing analysis

**Key Takeaways:**

1. **Consistency is paramount** - A single mismatch can reveal automation
2. **Use real profiles** - Don't invent fingerprints from scratch
3. **CDP is powerful** - Leverage Emulation domain for deep modifications
4. **Test thoroughly** - Use fingerprinting test sites before deployment
5. **Combine layers** - Network + Browser + Behavioral evasion
6. **Stay updated** - Detection techniques evolve; keep fingerprints current

**Pydoll's Advantages:**

- **No `navigator.webdriver`** (unlike Selenium/Puppeteer)
- **Direct CDP access** for deep browser control
- **Request interception** via Fetch domain
- **Browser preferences** for realistic history/settings
- **Async architecture** for natural timing patterns

With the techniques in this guide, you can create **highly stealthy** browser automation that mimics real user behavior at every level.

**Keep Learning**

Fingerprinting is an active research area. Stay updated by:

- Following security conferences (USENIX, Black Hat, DEF CON)
- Monitoring anti-bot vendors (Akamai, Cloudflare, DataDome)
- Testing your fingerprints regularly on detection sites
- Reading Chromium source code for new fingerprinting vectors

## Further Reading

### Comprehensive Guides

- [**Pydoll Core Concepts**](https://pydoll.tech/docs/deep-dive/fingerprinting/features/core-concepts.md) - Understanding Pydoll's architecture
- [**Chrome DevTools Protocol**](https://pydoll.tech/docs/deep-dive/fingerprinting/evasion-techniques/cdp.md) - Deep dive into CDP usage
- [**Network Fingerprinting**](https://pydoll.tech/docs/deep-dive/fingerprinting/network-fingerprinting/) - Protocol-level identification techniques
- [**Browser Fingerprinting**](https://pydoll.tech/docs/deep-dive/fingerprinting/browser-fingerprinting/) - Application-layer detection methods
- [**Behavioral Fingerprinting**](https://pydoll.tech/docs/deep-dive/fingerprinting/behavioral-fingerprinting/) - Human behavior analysis and detection
- [**Browser Options**](https://pydoll.tech/docs/deep-dive/fingerprinting/features/configuration/browser-options.md) - Command-line arguments for stealth
- [**Browser Preferences**](https://pydoll.tech/docs/deep-dive/fingerprinting/features/configuration/browser-preferences.md) - Internal settings for realism
- [**Proxy Configuration**](https://pydoll.tech/docs/deep-dive/fingerprinting/features/configuration/proxy.md) - Network-level anonymization
- [**Proxy Architecture**](https://pydoll.tech/docs/deep-dive/fingerprinting/evasion-techniques/proxy-architecture.md) - Network fundamentals and detection
- [**Human Interactions**](https://pydoll.tech/docs/deep-dive/fingerprinting/features/automation/human-interactions.md) - Behavioral realism
- [**Behavioral Captcha Bypass**](https://pydoll.tech/docs/deep-dive/fingerprinting/features/advanced/behavioral-captcha-bypass.md) - Handling modern challenges

### External Resources

- [**Chromium Source Code**](https://source.chromium.org/chromium/chromium/src) - Official Chromium codebase
- [**Chrome DevTools Protocol Viewer**](https://chromedevtools.github.io/devtools-protocol/) - Interactive CDP documentation
- [**W3C Web Standards**](https://www.w3.org/standards/) - Official web specifications
- [**IETF RFCs**](https://www.ietf.org/rfc/) - Network protocol standards
