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
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.live import Live
from rich.align import Align
from rich.progress import Progress, SpinnerColumn, TextColumn
from pysocks import ProxyError
import socks
import socket

class NGLSpamTool:
    def __init__(self):
        self.console = Console()
        self.active_sessions = {}
        self.bot_enabled = True
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

    def load_custom_messages(self):
        try:
            if os.path.exists('messages.txt'):
                with open('messages.txt', 'r') as f:
                    messages = [line.strip() for line in f if line.strip()]
                if messages:
                    self.custom_messages = messages
                    self.console.print(f"[cyan]✓ Loaded {len(self.custom_messages)} custom messages[/cyan]")
                    return True
                else:
                    self.custom_messages = self.default_messages
                    self.console.print("[yellow]⚠ messages.txt is empty, using defaults[/yellow]")
                    return False
            else:
                self.custom_messages = self.default_messages
                self.console.print("[yellow]⚠ messages.txt not found, using defaults[/yellow]")
                return False
        except Exception as e:
            self.console.print(f"[red]✗ Error loading messages: {e}[/red]")
            self.custom_messages = self.default_messages
            return False

    def get_random_message(self):
        messages = self.custom_messages if self.custom_messages else self.default_messages
        return random.choice(messages)

    def load_proxies(self):
        try:
            self.console.print("[cyan]⟳ Fetching proxies from GitHub...[/cyan]")
            
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
                    self.console.print(f"[cyan]✓ Loaded {len(socks5_proxies)} SOCKS5 proxies[/cyan]")
            except:
                pass
            
            try:
                response = requests.get(socks4_url, timeout=10)
                if response.status_code == 200:
                    socks4_proxies = [{'proxy': line.strip(), 'type': 'socks4'} 
                                     for line in response.text.split('\n') 
                                     if ':' in line.strip()]
                    all_proxies.extend(socks4_proxies)
                    self.console.print(f"[cyan]✓ Loaded {len(socks4_proxies)} SOCKS4 proxies[/cyan]")
            except:
                pass
            
            random.shuffle(all_proxies)
            self.proxies = all_proxies
            self.console.print(f"[cyan]✓ Total proxies: {len(self.proxies)}[/cyan]")
            
            if len(self.proxies) == 0 and os.path.exists('proxies.txt'):
                with open('proxies.txt', 'r') as f:
                    local_proxies = [{'proxy': line.strip(), 'type': 'auto'} 
                                    for line in f if ':' in line.strip()]
                self.proxies = local_proxies
                self.console.print(f"[cyan]✓ Loaded {len(self.proxies)} proxies from local file[/cyan]")
        
        except Exception as e:
            self.console.print(f"[red]✗ Error loading proxies: {e}[/red]")
            if os.path.exists('proxies.txt'):
                with open('proxies.txt', 'r') as f:
                    local_proxies = [{'proxy': line.strip(), 'type': 'auto'} 
                                    for line in f if ':' in line.strip()]
                self.proxies = local_proxies
                self.console.print(f"[cyan]✓ Fallback: Loaded {len(self.proxies)} proxies from local file[/cyan]")

    def get_next_proxy(self):
        if not self.proxies:
            return None
        proxy_obj = self.proxies[self.current_proxy_index]
        self.current_proxy_index = (self.current_proxy_index + 1) % len(self.proxies)
        return proxy_obj

    def create_proxy_session(self, proxy_obj):
        try:
            proxy, ptype = proxy_obj['proxy'], proxy_obj['type']
            session = requests.Session()
            
            if ptype == 'socks5':
                session.proxies = {'http': f'socks5://{proxy}', 'https': f'socks5://{proxy}'}
            else:
                session.proxies = {'http': f'socks4://{proxy}', 'https': f'socks4://{proxy}'}
            
            return session
        except Exception as e:
            return None

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
                
                if self.use_proxy and self.proxies:
                    proxy_obj = self.get_next_proxy()
                    session = self.create_proxy_session(proxy_obj)
                    if session:
                        response = session.post(url, headers=headers, data=data, timeout=10)
                    else:
                        response = requests.post(url, headers=headers, data=data, timeout=10)
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
            
            except Exception as e:
                session_data['errors'] += 1
                session_data['last_error'] = str(e)[:50]
                time.sleep(5)

        session_data['threads_completed'] += 1
        if session_data['threads_completed'] >= session_data['threads']:
            session_data['active'] = False

    def generate_status_table(self):
        table = Table(title="[bold magenta]HYCRON NGL SPAM DASHBOARD[/bold magenta]", show_header=False, box=None)
        
        if not self.active_sessions:
            table.add_row("[yellow]No active sessions[/yellow]")
            return table
        
        for session_id, session_data in list(self.active_sessions.items()):
            if not session_data['active'] and session_data['threads_completed'] >= session_data['threads']:
                continue
            
            elapsed = time.time() - session_data['start_time']
            remaining = max(0, session_data['end_time'] - time.time())
            
            minutes = int(remaining // 60)
            seconds = int(remaining % 60)
            
            rate = (session_data['sent'] / elapsed * 60) if elapsed > 0 else 0
            proxy_status = f"Enabled ({len(self.proxies)})" if self.use_proxy else "Disabled"
            status = "🔴 Spamming" if session_data['active'] else "🟢 Completed"
            
            content = f"""
[bold cyan]Target:[/bold cyan] {session_data['username']}
[bold cyan]Duration:[/bold cyan] {session_data['duration']}m | [bold cyan]Threads:[/bold cyan] {session_data['threads']}
[bold green]Sent:[/bold green] {session_data['sent']} | [bold red]Errors:[/bold red] {session_data['errors']}
[bold yellow]Time Left:[/bold yellow] {minutes}m {seconds}s | [bold magenta]Rate:[/bold magenta] {rate:.1f}/min
[bold blue]Proxy:[/bold blue] {proxy_status} | [bold cyan]Status:[/bold cyan] {status}
"""
            if session_data['last_error']:
                content += f"[bold red]Last Error:[/bold red] {session_data['last_error']}\n"
            
            table.add_row(Panel(content, border_style="cyan", padding=(1, 2)))
        
        return table

    def show_dashboard(self):
        while True:
            try:
                os.system('clear' if os.name == 'posix' else 'cls')
                
                self.console.print("\n")
                self.console.print(Panel(
                    "[bold magenta]╔═══════════════════════════════════╗\n"
                    "║  HYCRON NGL SPAM TOOL v1.0        ║\n"
                    "║  Advanced Message Delivery System  ║\n"
                    "╚═══════════════════════════════════╝[/bold magenta]",
                    border_style="magenta"
                ))
                
                self.console.print(self.generate_status_table())
                
                commands = """
[bold yellow]╔════════════════════════════════════════╗[/bold yellow]
[bold cyan]1.[/bold cyan] Start NGL Spam       [bold cyan]5.[/bold cyan] Toggle Proxy
[bold cyan]2.[/bold cyan] Load Messages      [bold cyan]6.[/bold cyan] Show Help
[bold cyan]3.[/bold cyan] Load Proxies       [bold cyan]7.[/bold cyan] Toggle Bot
[bold cyan]4.[/bold cyan] Active Sessions    [bold cyan]8.[/bold cyan] Exit
[bold yellow]╚════════════════════════════════════════╝[/bold yellow]
"""
                self.console.print(commands)
                
                break
            except KeyboardInterrupt:
                pass
            
            time.sleep(2)

    def start_spam(self):
        self.console.print("\n[bold cyan]▶ Start NGL Spam[/bold cyan]\n")
        
        username = self.console.input("[cyan]Target username:[/cyan] ").strip()
        if not username:
            self.console.print("[red]✗ Username cannot be empty[/red]")
            return
        
        try:
            duration = int(self.console.input(f"[cyan]Duration in minutes (max {self.max_duration}):[/cyan] ").strip())
        except ValueError:
            self.console.print("[red]✗ Duration must be a number[/red]")
            return
        
        if duration <= 0 or duration > self.max_duration:
            self.console.print(f"[red]✗ Duration must be between 1 and {self.max_duration} minutes[/red]")
            return
        
        user_active = [s for s in self.active_sessions.values() if s['active']]
        if len(user_active) >= self.max_concurrent_tasks:
            self.console.print(f"[red]✗ Maximum {self.max_concurrent_tasks} concurrent task(s) allowed[/red]")
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
        
        self.console.print(f"\n[green]✓ Starting spam on @{username}[/green]")
        self.console.print(f"[cyan]Duration: {duration}m | Threads: {self.default_threads}[/cyan]\n")
        
        for i in range(self.default_threads):
            thread = threading.Thread(target=self.send_ngl_message, args=(username, session_id, i), daemon=True)
            thread.start()
        
        time.sleep(1)

    def reload_messages(self):
        self.load_custom_messages()
        self.console.print("[green]✓ Messages reloaded[/green]\n")
        time.sleep(1)

    def load_proxies_menu(self):
        self.load_proxies()
        if self.proxies:
            self.console.print(f"[green]✓ Proxies loaded: {len(self.proxies)}[/green]\n")
        else:
            self.console.print("[red]✗ Failed to load proxies[/red]\n")
        time.sleep(2)

    def show_active_sessions(self):
        if not self.active_sessions:
            self.console.print("\n[yellow]No active sessions[/yellow]\n")
            time.sleep(1)
            return
        
        table = Table(title="[bold cyan]Active Sessions[/bold cyan]")
        table.add_column("Username", style="cyan")
        table.add_column("Sent", style="green")
        table.add_column("Errors", style="red")
        table.add_column("Status", style="yellow")
        
        for session_data in self.active_sessions.values():
            status = "🔴 Active" if session_data['active'] else "🟢 Done"
            table.add_row(
                session_data['username'],
                str(session_data['sent']),
                str(session_data['errors']),
                status
            )
        
        self.console.print("\n")
        self.console.print(table)
        self.console.print()
        time.sleep(2)

    def show_help(self):
        help_text = """
[bold cyan]╔════════════════════════════════════════╗[/bold cyan]
[bold yellow]HYCRON NGL SPAM TOOL - HELP[/bold yellow]
[bold cyan]╠════════════════════════════════════════╣[/bold cyan]

[bold magenta]Commands:[/bold magenta]
  [cyan]1[/cyan] - Start spamming a target
  [cyan]2[/cyan] - Load custom messages from messages.txt
  [cyan]3[/cyan] - Load proxies (SOCKS4/SOCKS5)
  [cyan]4[/cyan] - View all active sessions
  [cyan]5[/cyan] - Toggle proxy usage on/off
  [cyan]6[/cyan] - Show this help menu
  [cyan]7[/cyan] - Toggle bot on/off
  [cyan]8[/cyan] - Exit application

[bold magenta]Files:[/bold magenta]
  [cyan]messages.txt[/cyan] - Add custom messages (one per line)
  [cyan]proxies.txt[/cyan] - Add local proxies (IP:PORT format)

[bold magenta]Requirements:[/bold magenta]
  [cyan]messages.txt[/cyan] - Optional (defaults provided)
  [cyan]proxies.txt[/cyan] - Optional (downloads from GitHub)

[bold cyan]╚════════════════════════════════════════╝[/bold cyan]
"""
        self.console.print(help_text)
        time.sleep(3)

    def toggle_proxy(self):
        self.use_proxy = not self.use_proxy
        status = "[green]ENABLED[/green]" if self.use_proxy else "[red]DISABLED[/red]"
        self.console.print(f"\n[cyan]Proxy Status: {status}[/cyan]\n")
        if self.use_proxy and not self.proxies:
            self.console.print("[yellow]Loading proxies...[/yellow]")
            self.load_proxies()
        time.sleep(2)

    def toggle_bot(self):
        self.bot_enabled = not self.bot_enabled
        status = "[green]ENABLED[/green]" if self.bot_enabled else "[red]DISABLED[/red]"
        self.console.print(f"\n[cyan]Bot Status: {status}[/cyan]\n")
        time.sleep(1)

    def run(self):
        while True:
            try:
                os.system('clear' if os.name == 'posix' else 'cls')
                
                self.console.print(Panel(
                    "[bold magenta]╔═══════════════════════════════════╗\n"
                    "║  HYCRON NGL SPAM TOOL v1.0        ║\n"
                    "║  Advanced Message Delivery System  ║\n"
                    "╚═══════════════════════════════════╝[/bold magenta]",
                    border_style="magenta"
                ))
                
                self.console.print(self.generate_status_table())
                
                commands = """
[bold yellow]╔════════════════════════════════════════╗[/bold yellow]
[bold cyan]1.[/bold cyan] Start NGL Spam       [bold cyan]5.[/bold cyan] Toggle Proxy
[bold cyan]2.[/bold cyan] Load Messages      [bold cyan]6.[/bold cyan] Show Help
[bold cyan]3.[/bold cyan] Load Proxies       [bold cyan]7.[/bold cyan] Toggle Bot
[bold cyan]4.[/bold cyan] Active Sessions    [bold cyan]8.[/bold cyan] Exit
[bold yellow]╚════════════════════════════════════════╝[/bold yellow]
"""
                self.console.print(commands)
                
                choice = self.console.input("[bold magenta]▶ Select option:[/bold magenta] ").strip()
                
                if choice == '1':
                    if not self.bot_enabled:
                        self.console.print("[red]✗ Bot is disabled[/red]\n")
                        time.sleep(2)
                        continue
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
                    self.toggle_bot()
                
                elif choice == '8':
                    self.console.print("\n[magenta]Goodbye![/magenta]\n")
                    sys.exit(0)
                
                else:
                    self.console.print("[red]✗ Invalid option[/red]\n")
                    time.sleep(1)
            
            except KeyboardInterrupt:
                self.console.print("\n[magenta]Goodbye![/magenta]\n")
                sys.exit(0)
            except Exception as e:
                self.console.print(f"[red]✗ Error: {e}[/red]\n")
                time.sleep(2)

if __name__ == '__main__':
    tool = NGLSpamTool()
    tool.run()
