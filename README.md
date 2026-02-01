# HYCRON NGL SPAM TOOL - Python Edition

═══════════════════════════════════════════════════════════

QUICK START:

1. Open Command Prompt / Terminal
2. Navigate to the folder with tool.py
3. Run: pip install -r requirements.txt
4. Run: python tool.py

═══════════════════════════════════════════════════════════

IF YOU GET ERRORS:

If you still get module errors, try these fixes:

Option 1 (Recommended):
- Uninstall problematic packages: pip uninstall rich pysocks -y
- Run: pip install requests --upgrade
- Run: python tool.py

Option 2:
- Delete your Python installation
- Download fresh Python 3.11 or 3.12 from python.org
- Install with default settings
- Run: pip install requests
- Run: python tool.py

Option 3:
- Use py instead of python: py tool.py
- Or: python3 tool.py

═══════════════════════════════════════════════════════════

WHAT YOU NEED:

✓ Python 3.8+ installed
✓ requests library (pip install requests)
✓ messages.txt (optional, uses defaults if missing)
✓ proxies.txt (optional, will try to load from GitHub)

═══════════════════════════════════════════════════════════

FILES INCLUDED:

- tool.py - Main application (no external UI library)
- requirements_fixed.txt - Only requests library
- messages.txt - Custom spam messages
- proxies.txt - Proxy list template

═══════════════════════════════════════════════════════════

MENU OPTIONS:

1 - Start NGL Spam
   • Enter target username
   • Set duration (1-5 minutes)
   • Spam starts automatically

2 - Load Messages
   • Reloads messages.txt
   • Uses defaults if not found

3 - Load Proxies
   • Downloads from GitHub (SOCKS4/SOCKS5)
   • Falls back to proxies.txt if offline

4 - Active Sessions
   • View all running spam attacks
   • Shows stats (sent, errors, time left)

5 - Toggle Proxy
   • Enable/disable proxy usage
   • Auto-loads if enabled with no proxies

6 - Show Help
   • Display help information

7 - Toggle Bot
   • Enable/disable the tool

8 - Exit
   • Close the application

═══════════════════════════════════════════════════════════

FILE FORMATS:

messages.txt (one message per line):
---
Targetted by Hycron
You got boomed by Hycron
Hycron always on top!
---

proxies.txt (IP:PORT format):
---
192.168.1.1:1080
10.0.0.1:9050
127.0.0.1:8080
---

═══════════════════════════════════════════════════════════

FEATURES:

✓ Colorful neon dashboard (no external UI library)
✓ Multi-threaded spam (2 default threads)
✓ Proxy rotation (SOCKS4/SOCKS5)
✓ Custom messages
✓ Real-time stats
✓ Rate limit handling
✓ Error logging
✓ Session management
✓ Max 1 concurrent task (configurable)

═══════════════════════════════════════════════════════════

DEFAULT SETTINGS:

Max Duration: 5 minutes
Default Threads: 2
Max Concurrent Tasks: 1
Update Interval: Every 2 seconds

═══════════════════════════════════════════════════════════
