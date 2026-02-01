import os
import sys
import time
import random
import asyncio
import threading
import json
from datetime import datetime
from collections import defaultdict

try:
    import aiohttp
except ImportError:
    print("Error: aiohttp not installed")
    print("Run: pip install aiohttp requests")
    sys.exit(1)

class Colors:
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    WHITE = '\033[97m'
    BLACK = '\033[90m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'
    DIM = '\033[2m'
    
    BRIGHT_MAGENTA = '\033[105m'
    BRIGHT_CYAN = '\033[106m'
    BRIGHT_GREEN = '\033[102m'

class NGLSpamTool:
    def __init__(self):
        self.active_sessions = {}
        self.proxies = []
        self.current_proxy_index = 0
        self.custom_messages = []
        self.default_threads = 50
        self.default_duration = 5
        
        self.default_messages = [
            'Targetted by Hycron',
            'You got boomed by Hycron',
            'Hycron always on top!'
        ]
        
        self.session_lock = threading.Lock()
        self.load_proxies()
        self.load_custom_messages()

    def print_header(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        header = f"""{Colors.BOLD}{Colors.BRIGHT_MAGENTA}
╔════════════════════════════════════════════════════════════════╗
║                                                                ║
║                 ⚡ HYCRON NGL SPAMMER v2.0 ⚡                  ║
║              Advanced Message Delivery System                   ║
║                   Async Engine - Unlimited RPS                  ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
{Colors.END}"""
        print(header)

    def print_section(self, title):
        print(f"\n{Colors.BRIGHT_MAGENTA}╭{'─' * 60}╮{Colors.END}")
        print(f"{Colors.BRIGHT_MAGENTA}│ {Colors.BRIGHT_CYAN}{title:<58}{Colors.BRIGHT_MAGENTA}│{Colors.END}")
        print(f"{Colors.BRIGHT_MAGENTA}╰{'─' * 60}╯{Colors.END}")

    def load_custom_messages(self):
        try:
            github_url = 'https://raw.githubusercontent.com/inluvcoding/Hycron-NGL-Spammer/refs/heads/main/messages.txt'
            
            try:
                import requests
                response = requests.get(github_url, timeout=10)
                if response.status_code == 200:
                    messages = [line.strip() for line in response.text.split('\n') if line.strip()]
                    if messages:
                        self.custom_messages = messages
                        print(f"{Colors.GREEN}✓ Loaded {len(self.custom_messages)} messages from GitHub{Colors.END}")
                        return True
            except:
                pass
            
            if os.path.exists('messages.txt'):
                with open('messages.txt', 'r', encoding='utf-8') as f:
                    messages = [line.strip() for line in f if line.strip()]
                if messages:
                    self.custom_messages = messages
                    print(f"{Colors.GREEN}✓ Loaded {len(self.custom_messages)} messages from local file{Colors.END}")
                    return True
                else:
                    self.custom_messages = self.default_messages
                    print(f"{Colors.YELLOW}⚠ Using default messages{Colors.END}")
                    return False
            else:
                self.custom_messages = self.default_messages
                print(f"{Colors.YELLOW}⚠ Using default messages{Colors.END}")
                return False
        except Exception as e:
            print(f"{Colors.RED}✗ Error loading messages: {e}{Colors.END}")
            self.custom_messages = self.default_messages
            return False

    def get_random_message(self):
        messages = self.custom_messages if self.custom_messages else self.default_messages
        return random.choice(messages)

    def load_proxies(self):
        try:
            print(f"{Colors.CYAN}⟳ Loading proxies...{Colors.END}")
            
            import requests
            socks5_url = 'https://github.com/monosans/proxy-list/raw/refs/heads/main/proxies/socks5.txt'
            socks4_url = 'https://github.com/monosans/proxy-list/raw/refs/heads/main/proxies/socks4.txt'
            
            all_proxies = []
            
            try:
                response = requests.get(socks5_url, timeout=10)
                if response.status_code == 200:
                    socks5_proxies = [line.strip() for line in response.text.split('\n') if ':' in line.strip()]
                    all_proxies.extend(socks5_proxies)
                    print(f"{Colors.GREEN}✓ Loaded {len(socks5_proxies)} SOCKS5 proxies{Colors.END}")
            except:
                pass
            
            try:
                response = requests.get(socks4_url, timeout=10)
                if response.status_code == 200:
                    socks4_proxies = [line.strip() for line in response.text.split('\n') if ':' in line.strip()]
                    all_proxies.extend(socks4_proxies)
                    print(f"{Colors.GREEN}✓ Loaded {len(socks4_proxies)} SOCKS4 proxies{Colors.END}")
            except:
                pass
            
            random.shuffle(all_proxies)
            self.proxies = all_proxies
            print(f"{Colors.GREEN}✓ Total proxies: {len(self.proxies)}{Colors.END}")
            
            if len(self.proxies) == 0 and os.path.exists('proxies.txt'):
                with open('proxies.txt', 'r') as f:
                    local_proxies = [line.strip() for line in f if ':' in line.strip()]
                self.proxies = local_proxies
                print(f"{Colors.GREEN}✓ Loaded {len(self.proxies)} proxies from local file{Colors.END}")
        
        except Exception as e:
            print(f"{Colors.YELLOW}⚠ Proxy loading failed: {e}{Colors.END}")
            if os.path.exists('proxies.txt'):
                with open('proxies.txt', 'r') as f:
                    local_proxies = [line.strip() for line in f if ':' in line.strip()]
                self.proxies = local_proxies
                print(f"{Colors.GREEN}✓ Loaded {len(self.proxies)} proxies from local file{Colors.END}")

    def get_next_proxy(self):
        if not self.proxies:
            return None
        proxy = self.proxies[self.current_proxy_index]
        self.current_proxy_index = (self.current_proxy_index + 1) % len(self.proxies)
        return proxy

    async def send_spam_async(self, username, session_id, semaphore):
        session_data = self.active_sessions.get(session_id)
        if not session_data:
            return

        while session_data['active'] and time.time() < session_data['end_time']:
            async with semaphore:
                try:
                    message = self.get_random_message()
                    device_id = os.urandom(21).hex()
                    url = 'https://ngl.link/api/submit'
                    
                    headers = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0',
                        'Accept': '*/*',
                        'Accept-Language': 'en-US,en;q=0.5',
                        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                        'X-Requested-With': 'XMLHttpRequest',
                        'Referer': f'https://ngl.link/{username}',
                        'Origin': 'https://ngl.link'
                    }
                    
                    data = {
                        'username': username,
                        'question': message,
                        'deviceId': device_id,
                        'gameSlug': '',
                        'referrer': ''
                    }
                    
                    proxy_url = None
                    if self.proxies:
                        proxy = self.get_next_proxy()
                        if proxy:
                            proxy_url = f"http://{proxy}"
                    
                    try:
                        connector = aiohttp.TCPConnector(limit=1000, ttl_dns_cache=300)
                        timeout = aiohttp.ClientTimeout(total=10)
                        
                        async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
                            async with session.post(url, headers=headers, data=data, proxy=proxy_url, ssl=False) as response:
                                if response.status == 429:
                                    session_data['errors'] += 1
                                    session_data['last_error'] = 'Rate Limited'
                                    await asyncio.sleep(5)
                                elif response.status == 200:
                                    session_data['sent'] += 1
                                    session_data['last_success'] = time.time()
                                else:
                                    session_data['errors'] += 1
                                    session_data['last_error'] = f'HTTP {response.status}'
                    
                    except asyncio.TimeoutError:
                        session_data['errors'] += 1
                        session_data['last_error'] = 'Timeout'
                    except Exception as e:
                        session_data['errors'] += 1
                        session_data['last_error'] = str(e)[:30]
                
                except Exception as e:
                    session_data['errors'] += 1
                    session_data['last_error'] = str(e)[:30]

        with self.session_lock:
            if session_id in self.active_sessions:
                session_data['active'] = False

    def run_async_spam(self, username, session_id, threads):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            semaphore = asyncio.Semaphore(threads)
            tasks = [self.send_spam_async(username, session_id, semaphore) for _ in range(threads)]
            loop.run_until_complete(asyncio.gather(*tasks))
        finally:
            loop.close()

    def display_status(self):
        active_count = sum(1 for s in self.active_sessions.values() if s['active'])
        proxy_count = len(self.proxies)
        
        status_line = f"{Colors.BRIGHT_CYAN}📊 Active: {active_count} | 🌐 Proxies: {proxy_count}{Colors.END}"
        print(f"\n{status_line}\n")

    def show_menu(self):
        menu = f"""{Colors.BRIGHT_MAGENTA}
╔════════════════════════════════════════════════════════════════╗
║                        MAIN MENU                               ║
╠════════════════════════════════════════════════════════════════╣
║                                                                ║
║  {Colors.BRIGHT_CYAN}[1]{Colors.BRIGHT_MAGENTA} Start Attack       {Colors.BRIGHT_CYAN}[4]{Colors.BRIGHT_MAGENTA} Live Dashboard     ║
║  {Colors.BRIGHT_CYAN}[2]{Colors.BRIGHT_MAGENTA} Reload Messages    {Colors.BRIGHT_CYAN}[5]{Colors.BRIGHT_MAGENTA} Reload Proxies      ║
║  {Colors.BRIGHT_CYAN}[3]{Colors.BRIGHT_MAGENTA} Config Settings    {Colors.BRIGHT_CYAN}[6]{Colors.BRIGHT_MAGENTA} Help & Info        ║
║                                      {Colors.BRIGHT_CYAN}[0]{Colors.BRIGHT_MAGENTA} Exit        ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
{Colors.END}"""
        print(menu)

    def start_spam(self):
        self.print_section("START ATTACK")
        
        username = input(f"\n{Colors.BRIGHT_CYAN}Target Username: {Colors.END}").strip()
        if not username:
            print(f"{Colors.RED}✗ Username cannot be empty{Colors.END}\n")
            time.sleep(1)
            return
        
        try:
            threads = int(input(f"{Colors.BRIGHT_CYAN}Number of Threads [{self.default_threads}]: {Colors.END}").strip() or self.default_threads)
            duration = int(input(f"{Colors.BRIGHT_CYAN}Duration in Minutes [{self.default_duration}]: {Colors.END}").strip() or self.default_duration)
        except ValueError:
            print(f"{Colors.RED}✗ Invalid input{Colors.END}\n")
            time.sleep(1)
            return
        
        if threads <= 0 or duration <= 0:
            print(f"{Colors.RED}✗ Values must be greater than 0{Colors.END}\n")
            time.sleep(1)
            return
        
        session_id = f"{time.time()}-{random.randint(10000, 99999)}"
        start_time = time.time()
        end_time = start_time + (duration * 60)
        
        session_data = {
            'session_id': session_id,
            'username': username,
            'duration': duration,
            'threads': threads,
            'sent': 0,
            'errors': 0,
            'start_time': start_time,
            'end_time': end_time,
            'active': True,
            'last_error': None,
            'last_success': None
        }
        
        with self.session_lock:
            self.active_sessions[session_id] = session_data
        
        print(f"\n{Colors.GREEN}✓ Attack started on @{username}{Colors.END}")
        print(f"{Colors.BRIGHT_CYAN}├─ Duration: {duration}m{Colors.END}")
        print(f"{Colors.BRIGHT_CYAN}├─ Threads: {threads}{Colors.END}")
        print(f"{Colors.BRIGHT_CYAN}├─ Proxies: {len(self.proxies)}{Colors.END}")
        print(f"{Colors.BRIGHT_CYAN}└─ Messages: {len(self.custom_messages)}{Colors.END}\n")
        
        thread = threading.Thread(target=self.run_async_spam, args=(username, session_id, threads), daemon=True)
        thread.start()
        
        time.sleep(2)

    def reload_messages(self):
        self.print_section("RELOAD MESSAGES")
        print(f"\n{Colors.CYAN}⟳ Fetching messages...{Colors.END}\n")
        self.load_custom_messages()
        print()
        time.sleep(2)

    def reload_proxies(self):
        self.print_section("RELOAD PROXIES")
        print()
        self.load_proxies()
        print()
        time.sleep(2)

    def show_live_dashboard(self):
        try:
            while True:
                self.print_header()
                self.print_section("LIVE DASHBOARD")
                
                if not self.active_sessions:
                    print(f"\n{Colors.YELLOW}No active sessions{Colors.END}\n")
                    time.sleep(2)
                    break
                
                session_count = 0
                for session_id, session_data in list(self.active_sessions.items()):
                    if not session_data['active'] and session_data['sent'] > 0:
                        continue
                    
                    session_count += 1
                    elapsed = time.time() - session_data['start_time']
                    remaining = max(0, session_data['end_time'] - time.time())
                    
                    minutes = int(remaining // 60)
                    seconds = int(remaining % 60)
                    
                    rate = (session_data['sent'] / elapsed * 60) if elapsed > 0 else 0
                    progress = self.create_progress_bar(elapsed, session_data['duration'] * 60)
                    status = f"{Colors.GREEN}🟢 ACTIVE{Colors.END}" if session_data['active'] else f"{Colors.RED}🔴 DONE{Colors.END}"
                    
                    print(f"\n{Colors.BRIGHT_YELLOW}┌─ Session {session_count} ─────────────────────────────────┐{Colors.END}")
                    print(f"{Colors.BRIGHT_CYAN}│ Target     : {Colors.BRIGHT_GREEN}{session_data['username']:<48}{Colors.BRIGHT_CYAN}│{Colors.END}")
                    print(f"{Colors.BRIGHT_CYAN}│ Sent/Error : {Colors.BRIGHT_GREEN}{session_data['sent']:<10}{Colors.BRIGHT_CYAN} / {Colors.RED}{session_data['errors']:<10}{Colors.BRIGHT_CYAN}       │{Colors.END}")
                    print(f"{Colors.BRIGHT_CYAN}│ RPS/Rate   : {Colors.BRIGHT_MAGENTA}{rate:>6.1f}/min{Colors.BRIGHT_CYAN}                                    │{Colors.END}")
                    print(f"{Colors.BRIGHT_CYAN}│ Time Left  : {Colors.BRIGHT_YELLOW}{minutes}m {seconds}s{Colors.BRIGHT_CYAN}                                      │{Colors.END}")
                    print(f"{Colors.BRIGHT_CYAN}│ Progress   : {progress} {Colors.BRIGHT_CYAN}│{Colors.END}")
                    print(f"{Colors.BRIGHT_CYAN}│ Status     : {status}{Colors.BRIGHT_CYAN}                          │{Colors.END}")
                    
                    if session_data['last_error']:
                        print(f"{Colors.BRIGHT_CYAN}│ Last Error : {Colors.RED}{session_data['last_error']:<42}{Colors.BRIGHT_CYAN}│{Colors.END}")
                    
                    print(f"{Colors.BRIGHT_CYAN}└──────────────────────────────────────────────────────┘{Colors.END}")
                
                if session_count == 0:
                    print(f"\n{Colors.YELLOW}No active sessions{Colors.END}\n")
                    time.sleep(2)
                    break
                
                print(f"\n{Colors.YELLOW}[Press Ctrl+C to return to menu]{Colors.END}")
                time.sleep(2)
        
        except KeyboardInterrupt:
            print(f"\n{Colors.GREEN}✓ Returning to menu...{Colors.END}\n")
            time.sleep(1)

    def create_progress_bar(self, elapsed, total):
        if total <= 0:
            return ""
        
        percent = min(100, (elapsed / total) * 100)
        filled = int(percent / 5)
        empty = 20 - filled
        
        bar = f"{Colors.GREEN}{'█' * filled}{Colors.RED}{'░' * empty}{Colors.END}"
        return f"{bar} {int(percent)}%"

    def config_settings(self):
        self.print_section("CONFIGURATION")
        
        print(f"\n{Colors.BRIGHT_CYAN}Current Settings:{Colors.END}\n")
        print(f"{Colors.BRIGHT_CYAN}[1]{Colors.END} Default Threads  : {Colors.BRIGHT_GREEN}{self.default_threads}{Colors.END}")
        print(f"{Colors.BRIGHT_CYAN}[2]{Colors.END} Default Duration : {Colors.BRIGHT_GREEN}{self.default_duration}{Colors.END} minutes")
        print(f"{Colors.BRIGHT_CYAN}[3]{Colors.END} Reload Messages")
        print(f"{Colors.BRIGHT_CYAN}[4]{Colors.END} Reload Proxies")
        print(f"{Colors.BRIGHT_CYAN}[0]{Colors.END} Back to Menu\n")
        
        choice = input(f"{Colors.BRIGHT_MAGENTA}▶ Select option: {Colors.END}").strip()
        
        if choice == '1':
            try:
                threads = int(input(f"{Colors.BRIGHT_CYAN}Enter default threads: {Colors.END}"))
                if threads > 0:
                    self.default_threads = threads
                    print(f"{Colors.GREEN}✓ Updated to {threads} threads{Colors.END}\n")
                else:
                    print(f"{Colors.RED}✗ Must be greater than 0{Colors.END}\n")
            except ValueError:
                print(f"{Colors.RED}✗ Invalid input{Colors.END}\n")
            time.sleep(1)
        
        elif choice == '2':
            try:
                duration = int(input(f"{Colors.BRIGHT_CYAN}Enter default duration (minutes): {Colors.END}"))
                if duration > 0:
                    self.default_duration = duration
                    print(f"{Colors.GREEN}✓ Updated to {duration} minutes{Colors.END}\n")
                else:
                    print(f"{Colors.RED}✗ Must be greater than 0{Colors.END}\n")
            except ValueError:
                print(f"{Colors.RED}✗ Invalid input{Colors.END}\n")
            time.sleep(1)
        
        elif choice == '3':
            self.reload_messages()
        
        elif choice == '4':
            self.reload_proxies()

    def show_help(self):
        self.print_section("HELP & INFORMATION")
        
        help_text = f"""
{Colors.BRIGHT_GREEN}Features:{Colors.END}
  ✓ Async/Concurrent requests (aiohttp)
  ✓ Unlimited threads & duration
  ✓ Auto proxy rotation
  ✓ Live dashboard monitoring
  ✓ High RPS (100+ messages/sec per thread)
  ✓ Custom messages from GitHub
  ✓ SOCKS4/SOCKS5 support

{Colors.BRIGHT_YELLOW}Menu Options:{Colors.END}
  [1] - Start Attack
  [2] - Reload Messages from GitHub
  [3] - Configuration Settings
  [4] - Live Dashboard (View Active Attacks)
  [5] - Reload Proxies
  [6] - Help & Information
  [0] - Exit Application

{Colors.BRIGHT_CYAN}Files:{Colors.END}
  messages.txt - Custom spam messages (optional)
  proxies.txt - Local proxy list (optional)

{Colors.BRIGHT_MAGENTA}Notes:{Colors.END}
  • Proxies auto-load and rotate
  • Messages auto-fetch from GitHub
  • No limits on threads, duration, or tasks
  • Async engine for maximum performance
"""
        print(help_text)
        time.sleep(3)

    def run(self):
        while True:
            try:
                self.print_header()
                self.display_status()
                self.show_menu()
                
                choice = input(f"{Colors.BOLD}{Colors.BRIGHT_MAGENTA}▶ Select option: {Colors.END}").strip()
                
                if choice == '1':
                    self.start_spam()
                elif choice == '2':
                    self.reload_messages()
                elif choice == '3':
                    self.config_settings()
                elif choice == '4':
                    self.show_live_dashboard()
                elif choice == '5':
                    self.reload_proxies()
                elif choice == '6':
                    self.show_help()
                elif choice == '0':
                    print(f"\n{Colors.BRIGHT_MAGENTA}👋 Goodbye!{Colors.END}\n")
                    sys.exit(0)
                else:
                    print(f"{Colors.RED}✗ Invalid option{Colors.END}\n")
                    time.sleep(1)
            
            except KeyboardInterrupt:
                print(f"\n{Colors.BRIGHT_MAGENTA}👋 Goodbye!{Colors.END}\n")
                sys.exit(0)
            except Exception as e:
                print(f"{Colors.RED}✗ Error: {e}{Colors.END}\n")
                time.sleep(2)

if __name__ == '__main__':
    tool = NGLSpamTool()
    tool.run()
