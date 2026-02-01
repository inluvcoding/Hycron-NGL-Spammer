HYCRON NGL SPAMMER v2.0 - High Performance Edition

═════════════════════════════════════════════════════════════

QUICK START:

1. Install Python 3.8+
2. Run: pip install -r requirements.txt
3. Run: python tool.py

═════════════════════════════════════════════════════════════

FEATURES:

✓ Async/Concurrent Engine (aiohttp) - 100+ RPS per thread
✓ Unlimited Threads (no limits)
✓ Unlimited Duration (no time limits)
✓ Unlimited Concurrent Tasks
✓ Auto Proxy Rotation (SOCKS4/SOCKS5)
✓ Live Dashboard Monitoring
✓ High Performance TCP Connections
✓ Custom Messages from GitHub
✓ Beautiful Terminal UI

═════════════════════════════════════════════════════════════

MENU OPTIONS:

[1] - START ATTACK
   • Enter target username
   • Set number of threads (unlimited)
   • Set duration in minutes (unlimited)
   • Attack starts immediately

[2] - RELOAD MESSAGES
   • Fetches from GitHub
   • Falls back to local messages.txt
   • Uses defaults if not found

[3] - CONFIG SETTINGS
   • Set default threads
   • Set default duration
   • Quick reload options
   • No limits!

[4] - LIVE DASHBOARD
   • Real-time attack monitoring
   • View RPS/minute rate
   • Check sent vs errors
   • Progress bar
   • Press Ctrl+C to return

[5] - RELOAD PROXIES
   • Downloads SOCKS4/SOCKS5 from GitHub
   • Auto-rotates during attacks
   • Falls back to local proxies.txt

[6] - HELP & INFO
   • View features
   • Command information
   • File format guide

[0] - EXIT
   • Close application

═════════════════════════════════════════════════════════════

FILE FORMATS:

messages.txt (one message per line):
---
Targetted by Hycron
You got boomed by Hycron
Custom message here
---

proxies.txt (IP:PORT format):
---
192.168.1.1:1080
10.0.0.1:9050
127.0.0.1:8080
---

═════════════════════════════════════════════════════════════

CONFIGURATION:

Default Threads: 50 (change via option 3)
Default Duration: 5 minutes (change via option 3)

Settings apply to next attack immediately.
No restart needed!

═════════════════════════════════════════════════════════════

PERFORMANCE TIPS:

• Use 50-100 threads for optimal RPS
• Enable proxies for best results
• Monitor live dashboard (option 4)
• Custom messages = better impact
• No throttling or rate limits!

═════════════════════════════════════════════════════════════

REQUIREMENTS:

✓ Python 3.8+
✓ aiohttp (async HTTP client)
✓ aiofiles (async file I/O)
✓ requests (HTTP library)

All included in requirements.txt

═════════════════════════════════════════════════════════════

TROUBLESHOOTING:

Error: ModuleNotFoundError
→ Run: pip install -r requirements.txt

Error: Address already in use
→ Close other instances or wait 1 minute

Slow RPS
→ Increase threads in config (option 3)
→ Use proxies (option 5)
→ Check internet connection

═════════════════════════════════════════════════════════════

NOTES:

• Proxies auto-enabled and rotating
• No toggle proxy option (always on)
• Messages auto-fetch from GitHub
• No limits on duration, threads, or tasks
• Async engine for maximum throughput
• Thread-safe session management

═════════════════════════════════════════════════════════════
