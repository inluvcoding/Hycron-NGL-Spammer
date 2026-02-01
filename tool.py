import os
import sys
import time
import random
import hashlib
import requests
import threading
import json
from datetime import datetime
from urllib.parse import urlencode
from collections import defaultdict

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
    
    BRIGHT_MAGENTA = '\033[105m'
    BRIGHT_CYAN = '\033[106m'
    BRIGHT_GREEN = '\033[102m'

class NGLSpamTool:
    def __init__(self):
        self.active_sessions = {}
        self.use_proxy = False
        self.proxies = []
        self.current_proxy_index = 0
        self.custom_messages = []
        self.max_duration = 5
        self.default_threads = 2
        self.max_concurrent_tasks = 1
        
        self.default_messages = [
            'Targetted by Hycron',
            'You got boomed by Hycron',
            'Hycron always on top!'
        ]
        
        self.load_custom_messages()

    def print_header(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"""{Colors.BOLD}{Colors.MAGENTA}
╔═══════════════════════════════════════════════════╗
║                                                   ║
║         HYCRON NGL SPAM TOOL v1.0                 ║
║      Advanced Message Delivery System             ║
║                                                   ║
╚═══════════════════════════════════════════════════╝
{Colors.END}""")

    def load_custom_messages(self):
        try:
            if os.path.exists('messages.txt'):
                with open('messages.txt', 'r', encoding='utf-8') as f:
                    messages = [line.strip() for line in f if line.strip()]
                if messages:
                    self.custom_messages = messages
                    print(f"{Colors.CYAN}✓ Loaded {len(self.custom_messages)} custom messages{Colors.END}")
                    return True
                else:
                    self.custom_messages = self.default_messages
                    print(f"{Colors.YELLOW}⚠ messages.txt is empty, using defaults{Colors.END}")
                    return False
            else:
                self.custom_messages = self.default_messages
                print(f"{Colors.YELLOW}⚠ messages.txt not found, using defaults{Colors.END}")
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
            print(f"{Colors.CYAN}⟳ Fetching proxies from GitHub...{Colors.END}")
            
            socks5_url = 'https://github.com/monosans/proxy-list/raw/refs/heads/main/proxies/socks5.txt'
            socks4_url = 'https://github.com/monosans/proxy-list/raw/refs/heads/main/proxies/socks4.txt'
            
            all_proxies = []
            
            try:
                response = requests.get(socks5_url, timeout=10)
                if response.status_code == 200:
                    socks5_proxies = [{'proxy': line.strip(), 'type': 'socks5'} 
                                     for line in response.text.split('\n') 
                                     if ':' in line.strip()]
                    all_proxies.extend(socks5_proxies)
                    print(f"{Colors.CYAN}✓ Loaded {len(socks5_proxies)} SOCKS5 proxies{Colors.END}")
            except:
                pass
            
            try:
                response = requests.get(socks4_url, timeout=10)
                if response.status_code == 200:
                    socks4_proxies = [{'proxy': line.strip(), 'type': 'socks4'} 
                                     for line in response.text.split('\n') 
                                     if ':' in line.strip()]
                    all_proxies.extend(socks4_proxies)
                    print(f"{Colors.CYAN}✓ Loaded {len(socks4_proxies)} SOCKS4 proxies{Colors.END}")
            except:
                pass
            
            random.shuffle(all_proxies)
            self.proxies = all_proxies
            print(f"{Colors.CYAN}✓ Total proxies: {len(self.proxies)}{Colors.END}")
            
            if len(self.proxies) == 0 and os.path.exists('proxies.txt'):
                with open('proxies.txt', 'r') as f:
                    local_proxies = [{'proxy': line.strip(), 'type': 'auto'} 
                                    for line in f if ':' in line.strip()]
                self.proxies = local_proxies
                print(f"{Colors.CYAN}✓ Loaded {len(self.proxies)} proxies from local file{Colors.END}")
        
        except Exception as e:
            print(f"{Colors.RED}✗ Error loading proxies: {e}{Colors.END}")
            if os.path.exists('proxies.txt'):
                with open('proxies.txt', 'r') as f:
                    local_proxies = [{'proxy': line.strip(), 'type': 'auto'} 
                                    for line in f if ':' in line.strip()]
                self.proxies = local_proxies
                print(f"{Colors.CYAN}✓ Fallback: Loaded {len(self.proxies)} proxies from local file{Colors.END}")

    def get_next_proxy(self):
        if not self.proxies:
            return None
        proxy_obj = self.proxies[self.current_proxy_index]
        self.current_proxy_index = (self.current_proxy_index + 1) % len(self.proxies)
        return proxy_obj

    def send_ngl_message(self, username, session_id, thread_id):
        session_data = self.active_sessions.get(session_id)
        if not session_data:
            return

        while session_data['active'] and time.time() < session_data['end_time']:
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
                
                proxies_dict = None
                if self.use_proxy and self.proxies:
                    proxy_obj = self.get_next_proxy()
                    if proxy_obj:
                        proxy_url = f"http://{proxy_obj['proxy']}"
                        proxies_dict = {'http': proxy_url, 'https': proxy_url}
                
                try:
                    if proxies_dict:
                        response = requests.post(url, headers=headers, data=data, timeout=10, proxies=proxies_dict)
                    else:
                        response = requests.post(url, headers=headers, data=data, timeout=10)
                    
                    if response.status_code == 429:
                        session_data['errors'] += 1
                        session_data['last_error'] = 'Rate Limited'
                        time.sleep(25)
                    elif response.status_code != 200:
                        session_data['errors'] += 1
                        session_data['last_error'] = f'HTTP {response.status_code}'
                        time.sleep(5)
                    else:
                        session_data['sent'] += 1
                        session_data['last_success'] = time.time()
                
                except Exception as req_error:
                    session_data['errors'] += 1
                    session_data['last_error'] = str(req_error)[:50]
                    time.sleep(5)
            
            except Exception as e:
                session_data['errors'] += 1
                session_data['last_error'] = str(e)[:50]
                time.sleep(5)

        session_data['threads_completed'] += 1
        if session_data['threads_completed'] >= session_data['threads']:
            session_data['active'] = False

    def display_status(self):
        print(f"\n{Colors.BOLD}{Colors.CYAN}═══════════════════════════════════════════════════{Colors.END}")
        print(f"{Colors.BOLD}{Colors.MAGENTA}          ACTIVE SESSIONS{Colors.END}")
        print(f"{Colors.BOLD}{Colors.CYAN}═══════════════════════════════════════════════════{Colors.END}\n")
        
        if not self.active_sessions:
            print(f"{Colors.YELLOW}No active sessions{Colors.END}\n")
            return
        
        for session_id, session_data in list(self.active_sessions.items()):
            if not session_data['active'] and session_data['threads_completed'] >= session_data['threads']:
                continue
            
            elapsed = time.time() - session_data['start_time']
            remaining = max(0, session_data['end_time'] - time.time())
            
            minutes = int(remaining // 60)
            seconds = int(remaining % 60)
            
            rate = (session_data['sent'] / elapsed * 60) if elapsed > 0 else 0
            proxy_status = f"Enabled ({len(self.proxies)})" if self.use_proxy else "Disabled"
            status = f"{Colors.RED}🔴 Spamming{Colors.END}" if session_data['active'] else f"{Colors.GREEN}🟢 Completed{Colors.END}"
            
            print(f"{Colors.BOLD}{Colors.CYAN}Target:{Colors.END} {Colors.MAGENTA}{session_data['username']}{Colors.END}")
            print(f"{Colors.BOLD}{Colors.CYAN}Duration:{Colors.END} {session_data['duration']}m | {Colors.BOLD}{Colors.CYAN}Threads:{Colors.END} {session_data['threads']}")
            print(f"{Colors.BOLD}{Colors.GREEN}Sent:{Colors.END} {session_data['sent']} | {Colors.BOLD}{Colors.RED}Errors:{Colors.END} {session_data['errors']}")
            print(f"{Colors.BOLD}{Colors.YELLOW}Time Left:{Colors.END} {minutes}m {seconds}s | {Colors.BOLD}{Colors.MAGENTA}Rate:{Colors.END} {rate:.1f}/min")
            print(f"{Colors.BOLD}{Colors.BLUE}Proxy:{Colors.END} {proxy_status} | {Colors.BOLD}{Colors.CYAN}Status:{Colors.END} {status}")
            if session_data['last_error']:
                print(f"{Colors.BOLD}{Colors.RED}Last Error:{Colors.END} {session_data['last_error']}")
            print(f"{Colors.CYAN}─────────────────────────────────────────────────{Colors.END}\n")

    def show_menu(self):
        print(f"""{Colors.BOLD}{Colors.YELLOW}
╔═════════════════════════════════════════════════╗
║             MAIN MENU                           ║
╠═════════════════════════════════════════════════╣
║                                                 ║
║  {Colors.CYAN}1{Colors.YELLOW}. Start NGL Spam          {Colors.CYAN}5{Colors.YELLOW}. Toggle Proxy      ║
║  {Colors.CYAN}2{Colors.YELLOW}. Load Messages         {Colors.CYAN}6{Colors.YELLOW}. Show Help        ║
║  {Colors.CYAN}3{Colors.YELLOW}. Load Proxies          {Colors.CYAN}7{Colors.YELLOW}. Config Settings  ║
║  {Colors.CYAN}4{Colors.YELLOW}. Active Sessions       {Colors.CYAN}8{Colors.YELLOW}. Exit              ║
║                                                 ║
╚═════════════════════════════════════════════════╝
{Colors.END}""")

    def start_spam(self):
        print(f"\n{Colors.BOLD}{Colors.CYAN}▶ Start NGL Spam{Colors.END}\n")
        
        username = input(f"{Colors.CYAN}Target username: {Colors.END}").strip()
        if not username:
            print(f"{Colors.RED}✗ Username cannot be empty{Colors.END}")
            time.sleep(1)
            return
        
        try:
            duration = int(input(f"{Colors.CYAN}Duration in minutes (max {self.max_duration}): {Colors.END}").strip())
        except ValueError:
            print(f"{Colors.RED}✗ Duration must be a number{Colors.END}")
            time.sleep(1)
            return
        
        if duration <= 0 or duration > self.max_duration:
            print(f"{Colors.RED}✗ Duration must be between 1 and {self.max_duration} minutes{Colors.END}")
            time.sleep(1)
            return
        
        user_active = [s for s in self.active_sessions.values() if s['active']]
        if len(user_active) >= self.max_concurrent_tasks:
            print(f"{Colors.RED}✗ Maximum {self.max_concurrent_tasks} concurrent task(s) allowed{Colors.END}")
            time.sleep(1)
            return
        
        session_id = f"{time.time()}-{random.randint(1000, 9999)}"
        start_time = time.time()
        end_time = start_time + (duration * 60)
        
        session_data = {
            'session_id': session_id,
            'username': username,
            'duration': duration,
            'threads': self.default_threads,
            'sent': 0,
            'errors': 0,
            'start_time': start_time,
            'end_time': end_time,
            'active': True,
            'threads_completed': 0,
            'last_error': None,
            'last_success': None
        }
        
        self.active_sessions[session_id] = session_data
        
        print(f"\n{Colors.GREEN}✓ Starting spam on @{username}{Colors.END}")
        print(f"{Colors.CYAN}Duration: {duration}m | Threads: {self.default_threads}{Colors.END}\n")
        
        for i in range(self.default_threads):
            thread = threading.Thread(target=self.send_ngl_message, args=(username, session_id, i), daemon=True)
            thread.start()
        
        time.sleep(2)

    def reload_messages(self):
        self.load_custom_messages()
        print(f"{Colors.GREEN}✓ Messages reloaded{Colors.END}\n")
        time.sleep(2)

    def load_proxies_menu(self):
        self.load_proxies()
        if self.proxies:
            print(f"{Colors.GREEN}✓ Proxies loaded: {len(self.proxies)}{Colors.END}\n")
        else:
            print(f"{Colors.RED}✗ Failed to load proxies{Colors.END}\n")
        time.sleep(2)

    def show_active_sessions(self):
        if not self.active_sessions:
            print(f"\n{Colors.YELLOW}No active sessions{Colors.END}\n")
            time.sleep(1)
            return
        
        print(f"\n{Colors.BOLD}{Colors.CYAN}═══════════════════════════════════════════════════{Colors.END}")
        print(f"{Colors.BOLD}{Colors.CYAN}              ACTIVE SESSIONS{Colors.END}")
        print(f"{Colors.BOLD}{Colors.CYAN}═══════════════════════════════════════════════════{Colors.END}\n")
        
        print(f"{Colors.BOLD}{Colors.CYAN}{'Username':<20} {'Sent':<10} {'Errors':<10} {'Status':<15}{Colors.END}")
        print(f"{Colors.CYAN}─────────────────────────────────────────────────{Colors.END}")
        
        for session_data in self.active_sessions.values():
            status = f"{Colors.RED}🔴 Active{Colors.END}" if session_data['active'] else f"{Colors.GREEN}🟢 Done{Colors.END}"
            print(f"{session_data['username']:<20} {session_data['sent']:<10} {session_data['errors']:<10} {status:<15}")
        
        print()
        time.sleep(2)

    def show_help(self):
        print(f"""{Colors.BOLD}{Colors.CYAN}
╔═════════════════════════════════════════════════╗
║         HYCRON NGL SPAM TOOL - HELP             ║
╠═════════════════════════════════════════════════╣

{Colors.MAGENTA}Commands:{Colors.CYAN}
  1 - Start spamming a target
  2 - Load custom messages from messages.txt
  3 - Load proxies (SOCKS4/SOCKS5)
  4 - View all active sessions
  5 - Toggle proxy usage on/off
  6 - Show this help menu
  7 - Configure tool settings (threads, duration, etc)
  8 - Exit application

{Colors.MAGENTA}Config Settings:{Colors.CYAN}
  • Max Duration - Maximum time for spam (1-∞ minutes)
  • Default Threads - Number of threads per spam (1-10)
  • Max Concurrent Tasks - Run multiple spams (1-5)

{Colors.MAGENTA}Files:{Colors.CYAN}
  messages.txt - Add custom messages (one per line)
  proxies.txt - Add local proxies (IP:PORT format)

{Colors.MAGENTA}Requirements:{Colors.CYAN}
  messages.txt - Optional (defaults provided)
  proxies.txt - Optional (downloads from GitHub)

{Colors.MAGENTA}Features:{Colors.CYAN}
  ✓ Colorful neon dashboard
  ✓ Multi-threaded spam attacks
  ✓ SOCKS4/SOCKS5 proxy support
  ✓ Custom message loading
  ✓ Real-time status tracking
  ✓ Automatic proxy rotation
  ✓ Rate limiting handling
  ✓ Configurable settings

╚═════════════════════════════════════════════════╝
{Colors.END}""")
        time.sleep(4)

    def toggle_proxy(self):
        self.use_proxy = not self.use_proxy
        status = f"{Colors.GREEN}ENABLED{Colors.END}" if self.use_proxy else f"{Colors.RED}DISABLED{Colors.END}"
        print(f"\n{Colors.CYAN}Proxy Status: {status}{Colors.END}\n")
        if self.use_proxy and not self.proxies:
            print(f"{Colors.YELLOW}Loading proxies...{Colors.END}")
            self.load_proxies()
        time.sleep(2)

    def config_settings(self):
        print(f"\n{Colors.BOLD}{Colors.CYAN}═══════════════════════════════════════════════════{Colors.END}")
        print(f"{Colors.BOLD}{Colors.MAGENTA}              CONFIG SETTINGS{Colors.END}")
        print(f"{Colors.BOLD}{Colors.CYAN}═══════════════════════════════════════════════════{Colors.END}\n")
        
        print(f"{Colors.YELLOW}Current Configuration:{Colors.END}\n")
        print(f"{Colors.CYAN}1. Max Duration:{Colors.END} {Colors.GREEN}{self.max_duration}{Colors.END} minutes")
        print(f"{Colors.CYAN}2. Default Threads:{Colors.END} {Colors.GREEN}{self.default_threads}{Colors.END} threads")
        print(f"{Colors.CYAN}3. Max Concurrent Tasks:{Colors.END} {Colors.GREEN}{self.max_concurrent_tasks}{Colors.END} task(s)")
        print(f"{Colors.CYAN}4. Back to Menu{Colors.END}\n")
        
        choice = input(f"{Colors.BOLD}{Colors.MAGENTA}▶ Select option to configure: {Colors.END}").strip()
        
        if choice == '1':
            try:
                new_duration = int(input(f"{Colors.CYAN}Enter max duration in minutes (current: {self.max_duration}): {Colors.END}"))
                if new_duration > 0:
                    self.max_duration = new_duration
                    print(f"{Colors.GREEN}✓ Max duration updated to {self.max_duration} minutes{Colors.END}\n")
                else:
                    print(f"{Colors.RED}✗ Duration must be greater than 0{Colors.END}\n")
            except ValueError:
                print(f"{Colors.RED}✗ Invalid input{Colors.END}\n")
            time.sleep(1)
        
        elif choice == '2':
            try:
                new_threads = int(input(f"{Colors.CYAN}Enter default threads (current: {self.default_threads}): {Colors.END}"))
                if new_threads > 0 and new_threads <= 10:
                    self.default_threads = new_threads
                    print(f"{Colors.GREEN}✓ Default threads updated to {self.default_threads}{Colors.END}\n")
                else:
                    print(f"{Colors.RED}✗ Threads must be between 1 and 10{Colors.END}\n")
            except ValueError:
                print(f"{Colors.RED}✗ Invalid input{Colors.END}\n")
            time.sleep(1)
        
        elif choice == '3':
            try:
                new_concurrent = int(input(f"{Colors.CYAN}Enter max concurrent tasks (current: {self.max_concurrent_tasks}): {Colors.END}"))
                if new_concurrent > 0 and new_concurrent <= 5:
                    self.max_concurrent_tasks = new_concurrent
                    print(f"{Colors.GREEN}✓ Max concurrent tasks updated to {self.max_concurrent_tasks}{Colors.END}\n")
                else:
                    print(f"{Colors.RED}✗ Concurrent tasks must be between 1 and 5{Colors.END}\n")
            except ValueError:
                print(f"{Colors.RED}✗ Invalid input{Colors.END}\n")
            time.sleep(1)
        
        elif choice == '4':
            return
        
        else:
            print(f"{Colors.RED}✗ Invalid option{Colors.END}\n")
            time.sleep(1)

    def run(self):
        while True:
            try:
                self.print_header()
                self.display_status()
                self.show_menu()
                
                choice = input(f"{Colors.BOLD}{Colors.MAGENTA}▶ Select option: {Colors.END}").strip()
                
                if choice == '1':
                    self.start_spam()
                
                elif choice == '2':
                    self.reload_messages()
                
                elif choice == '3':
                    self.load_proxies_menu()
                
                elif choice == '4':
                    self.show_active_sessions()
                
                elif choice == '5':
                    self.toggle_proxy()
                
                elif choice == '6':
                    self.show_help()
                
                elif choice == '7':
                    self.config_settings()
                
                elif choice == '8':
                    print(f"\n{Colors.MAGENTA}Goodbye!{Colors.END}\n")
                    sys.exit(0)
                
                else:
                    print(f"{Colors.RED}✗ Invalid option{Colors.END}\n")
                    time.sleep(1)
            
            except KeyboardInterrupt:
                print(f"\n{Colors.MAGENTA}Goodbye!{Colors.END}\n")
                sys.exit(0)
            except Exception as e:
                print(f"{Colors.RED}✗ Error: {e}{Colors.END}\n")
                time.sleep(2)

if __name__ == '__main__':
    tool = NGLSpamTool()
    tool.run()
