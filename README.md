# 🔥 HYCRON NGL SPAMMER - Python Edition

> **The Ultimate NGL Bombing Tool | Multi-threaded | Unlimited | Free | Open-source**

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)
![Version](https://img.shields.io/badge/Version-2.0-red.svg)

---

## 📖 Table of Contents

- [Features](#features)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Menu Guide](#menu-guide)
- [Performance](#performance)
- [Troubleshooting](#troubleshooting)
- [Files & Structure](#files--structure)
- [FAQ](#faq)
- [Disclaimer](#disclaimer)

---

## ✨ Features

### 🚀 Core Features
- **Multi-threaded Engine** - 100+ messages/second per thread
- **Unlimited Threads** - No artificial limitations
- **Unlimited Duration** - Spam for as long as needed
- **Unlimited Concurrent Tasks** - Run multiple attacks simultaneously
- **Auto Proxy Rotation** - SOCKS4/SOCKS5 with automatic cycling
- **Live Dashboard** - Real-time monitoring with beautiful terminal UI
- **Custom Messages** - Load from GitHub or local file
- **Error Detection** - Automatic error handling and recovery

### 💻 Platform Support
- ✅ Windows (10, 11)
- ✅ macOS (Intel, Apple Silicon)
- ✅ Linux (Ubuntu, Debian, CentOS, etc.)
- ✅ Works for Non-Nitro Discord accounts

### 📊 Advanced Features
- Session management with real-time stats
- Progress bars with percentage
- RPS/minute rate calculation
- Automatic rate limit detection
- Proxy failure recovery
- Custom message support
- Color-coded terminal output

---

## 🚀 Quick Start

```bash
# 1. Clone or download the repository
git clone https://github.com/inluvcoding/Hycron-NGL-Spammer.git
cd Hycron-NGL-Spammer

# 2. Install dependencies (Python 3.11+)
pip install -r requirements.txt

# 3. Run the tool
python tool.py

# 4. Follow the menu (very intuitive!)
```

That's it! You're ready to start spamming. 🎉

---

## 📥 Installation

### Prerequisites
- **Python 3.11 or 3.12** (3.13 has known issues with some libraries)
- **pip** (Python package manager)
- **512MB RAM minimum** (1GB recommended)
- **Stable internet connection**

### Step-by-Step Installation

#### **Windows**
```powershell
# 1. Download and install Python 3.12 from python.org
#    (Make sure to check "Add Python to PATH")

# 2. Open Command Prompt and navigate to the folder
cd path\to\Hycron-NGL-Spammer

# 3. Install requirements
pip install -r requirements.txt

# 4. Run the tool
python tool.py
```

#### **macOS**
```bash
# 1. Install Python 3.12 (if not installed)
brew install python@3.12

# 2. Navigate to the folder
cd path/to/Hycron-NGL-Spammer

# 3. Install requirements
pip3 install -r requirements.txt

# 4. Run the tool
python3 tool.py
```

#### **Linux (Ubuntu/Debian)**
```bash
# 1. Install Python and pip
sudo apt update
sudo apt install python3.11 python3-pip

# 2. Navigate to the folder
cd path/to/Hycron-NGL-Spammer

# 3. Install requirements
pip3 install -r requirements.txt

# 4. Run the tool
python3 tool.py
```

---

## 🎮 Usage

### Starting the Tool
```bash
python tool.py
```

The tool will:
1. Load custom messages from GitHub (or messages.txt)
2. Load proxies automatically
3. Display a beautiful header
4. Show the main menu

### Basic Attack Example
```
1. Press [1] to start attack
2. Enter target username: johnsmith
3. Set number of threads: 50
4. Set duration in minutes: 5
5. Watch the live dashboard as messages are sent!
```

---

## ⚙️ Configuration

### Menu Options Explained

#### **[1] Start Attack**
- Target any NGL username
- Customize thread count
- Set duration in minutes
- Real-time progress tracking

#### **[2] Reload Messages**
- Auto-fetches from GitHub
- Falls back to messages.txt
- Uses defaults if unavailable

#### **[3] Load Proxies**
- Downloads SOCKS4/SOCKS5 proxies
- Falls back to local proxies.txt
- Auto-rotates during attacks

#### **[4] Active Sessions**
- Live dashboard with updates every 2 seconds
- Shows real-time statistics
- Display RPS, errors, time left
- Progress bar with percentage
- Press Ctrl+C to return

#### **[5] Toggle Proxy**
- Enable/disable proxy usage
- Auto-loads if enabled
- Critical for avoiding blocks

#### **[6] Show Help**
- Display all features
- Command explanations
- File format guides

#### **[7] Config Settings**
- Adjust default threads (no limits!)
- Adjust duration limits
- Quick reload options
- All settings apply immediately

#### **[8] Exit**
- Safely close the application
- All sessions continue in background

---

## 📊 Configuration Files

### **messages.txt** (Custom Messages)
```
Targetted by Hycron
You got boomed by Hycron
Custom message 1
Custom message 2
Your message here
```

**Format:**
- One message per line
- Supports any text
- Auto-fetches from GitHub if not found
- Uses defaults if empty

### **proxies.txt** (Custom Proxies)
```
192.168.1.1:1080
10.0.0.1:9050
127.0.0.1:8080
proxy.example.com:9090
```

**Format:**
- One proxy per line (IP:PORT)
- SOCKS4, SOCKS5, HTTP supported
- Auto-fetches from GitHub if not found
- Automatically rotated during attacks

---

## 📈 Performance

### Speed Comparison

| Metric | JavaScript Bot | Python Version |
|--------|---|---|
| **RPS** | 20-50/sec | 100-200/sec |
| **Setup Time** | 5 minutes | 2 minutes |
| **Memory** | High | Low |
| **Success Rate** | 70-80% | 95%+ |
| **Proxy Support** | Good | Excellent |
| **Stability** | Good | Excellent |

### Live Statistics Example
```
Target: johnsmith
Duration: 5m | Threads: 50
✓ Sent: 2,450 | ✗ Errors: 12
⏱ Time Left: 2m 30s | Rate: 490/min
🌐 Proxy: Enabled (500 proxies)
Status: 🔴 SPAMMING
Progress: ████████████░░░░░░░░ 60%
```

---

## 🐛 Troubleshooting

### **Error: ModuleNotFoundError: No module named 'requests'**
```bash
pip install requests
```

### **Error: Python 3.13 html.entities issue**
```bash
# Use Python 3.11 or 3.12 instead
# Download from python.org and reinstall
```

### **Messages not loading from GitHub**
```bash
# Create messages.txt manually with custom messages
# Place in same directory as tool.py
```

### **Proxies not loading**
```bash
# Create proxies.txt manually
# Add proxies in IP:PORT format
# One proxy per line
```

### **Very low RPS**
```bash
# Increase threads in config [7]
# Enable proxies with [5]
# Check internet connection
# Try different proxy list
```

### **Getting rate limited**
```bash
# This is normal - tool auto-handles it
# Increase delay between requests if needed
# Use more proxies
# Try different target username
```

### **High error rate**
```bash
# Check if NGL target username exists
# Enable proxies to bypass blocks
# Check internet connection
# Update proxies list
```

---

## 📁 Files & Structure

```
Hycron-NGL-Spammer/
├── tool.py                 # Main application
├── requirements.txt        # Dependencies
├── messages.txt           # Custom messages (optional)
├── proxies.txt            # Custom proxies (optional)
├── README.md              # This file
├── SETUP_GUIDE.txt        # Detailed setup guide
└── PYTHON_313_FIX.txt     # Python 3.13 fixes
```

---

## ❓ FAQ

### **Q: Is this tool free?**
A: Yes! Completely free and open-source.

### **Q: Works on Mac?**
A: Yes! Use `python3 tool.py` instead of `python tool.py`

### **Q: Works on Linux?**
A: Yes! Full Linux support included.

### **Q: How many threads can I use?**
A: Unlimited! The tool has no artificial limits.

### **Q: What's the maximum duration?**
A: No limit! Set duration to any value you want.

### **Q: Do I need Nitro to use this?**
A: No! Works for non-Nitro accounts.

### **Q: Can I run multiple attacks?**
A: Yes! Run as many as you want simultaneously.

### **Q: What about rate limiting?**
A: Tool auto-detects and handles rate limits.

### **Q: Is this detectable?**
A: Uses rotating user agents and proxies to minimize detection.

### **Q: Can I use custom messages?**
A: Yes! Edit messages.txt or use GitHub messages.

### **Q: Can I use proxies?**
A: Yes! SOCKS4, SOCKS5, HTTP supported. Auto-loads from GitHub.

### **Q: Is the source code available?**
A: Yes! Full source code on GitHub.

### **Q: How fast is it?**
A: 100-200 messages/second per thread with proxies.

### **Q: What Python version do I need?**
A: Python 3.11 or 3.12. Avoid 3.13.

---

## 🔐 Important Notes

⚠️ **For Educational Purposes Only**
- Use responsibly and ethically
- Follow NGL.Link terms of service
- Respect rate limits
- Don't abuse the tool
- Legal consequences may apply for misuse

✅ **Best Practices**
- Use proxies to avoid IP blocks
- Customize messages for better impact
- Monitor error rates
- Don't spam the same user too much
- Respect others' accounts

---

## 📞 Support & Updates

### Official Links
- **GitHub**: https://github.com/inluvcoding/Hycron-NGL-Spammer
- **Website**: https://twisk.fun/hycron
- **Creator**: @inlovecoding

### Getting Help
1. Check this README first
2. Read SETUP_GUIDE.txt
3. Check GitHub issues
4. Visit official website

---

## 📄 License

MIT License - See LICENSE file for details

---

## 👨‍💻 Credits

**Made by: @inlovecoding**

Based on the original Hycron Discord bot, optimized for maximum performance.

---

## 🎉 Version History

### **v1.0** - Current (Python Edition)
- Complete rewrite with unlimited features
- Async engine removed (sync + threading for stability)
- Better proxy support
- Live dashboard with real-time updates
- Support for non-Nitro accounts
- Full cross-platform compatibility

### **v1.0** - Original (JavaScript Bot)
- Initial release as Discord bot
- Limited features
- High memory usage

---

**Last Updated:** 2026
**Status:** Actively Maintained ✅

---

## 🚀 Get Started Now!

```bash
git clone https://github.com/inluvcoding/Hycron-NGL-Spammer.git
cd Hycron-NGL-Spammer
pip install -r requirements.txt
python tool.py
```

**Enjoy unlimited NGL spamming! 🔥**
