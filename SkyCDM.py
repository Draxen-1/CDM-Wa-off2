#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
CDM TECH - CDM 503 NEO ULTRA X100
Version: 4.0.0
Developer: SKY PLUG CDM
Description: WhatsApp Message Automation Tool - 100 THREADS ULTRA POWER
"""

import subprocess
import time
import random
import os
import sys
import json
import threading
import signal
from datetime import datetime
from threading import Thread, Lock, Semaphore
from typing import List, Tuple, Dict, Optional
from dataclasses import dataclass
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import queue
import psutil 
 # Pour monitoring des performances

# ==================== CONFIGURATION ULTRA POWER ====================

@dataclass
class Config:
    """Configuration class for the tool - 100 THREADS"""
    version: str = "4.0.0"
    developer: str = "SKY PLUG CDM"
    tool_name: str = "CDM 503 NEO ULTRA X100"
    
    # Default file paths
    messages_file: str = "spam.txt"
    config_file: str = "config.json"
    log_file: str = "logs.txt"
    
    # Performance settings - 100 THREADS
    default_spam_count: int = 1000
    max_threads: int = 100  # 🔥 100 THREADS SIMULTANÉS
    batch_size: int = 20     # 20 messages par batch
    ultra_mode: bool = True
    turbo_boost: bool = True  # Nouveau mode turbo
    
    # Queue settings
    max_queue_size: int = 500
    queue_timeout: float = 0.1
    
    # UI settings
    enable_logging: bool = True
    enable_animation: bool = True
    typing_speed: float = 0.005  # Plus rapide
    show_system_stats: bool = True  # Afficher les stats système

# ==================== COLOR SYSTEM ULTRA ====================

class Colors:
    """ANSI color codes for terminal output"""
    BLACK = '\033[30m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    
    BOLD = '\033[1m'
    DIM = '\033[2m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'
    BLINK = '\033[5m'
    REVERSE = '\033[7m'
    RESET = '\033[0m'
    
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_PURPLE = '\033[45m'
    BG_CYAN = '\033[46m'
    
    @classmethod
    def gradient(cls, text: str, speed: str = "fast") -> str:
        """Gradient text effect"""
        colors = [cls.RED, cls.YELLOW, cls.GREEN, cls.CYAN, cls.BLUE, cls.PURPLE]
        result = ""
        for i, char in enumerate(text):
            if speed == "fast":
                result += f"{colors[i % len(colors)]}{char}"
            else:
                result += f"{colors[i % len(colors)]}{cls.BOLD}{char}"
        return f"{result}{cls.RESET}"

# ==================== SYSTEM MONITOR ====================

class SystemMonitor:
    """Monitor system performance"""
    
    def __init__(self):
        self.cpu_percent = 0
        self.ram_percent = 0
        self.thread_count = 0
        
    def update(self):
        """Update system stats"""
        try:
            self.cpu_percent = psutil.cpu_percent(interval=0.1)
            self.ram_percent = psutil.virtual_memory().percent
            self.thread_count = threading.active_count()
        except:
            self.cpu_percent = 0
            self.ram_percent = 0
            self.thread_count = 0
    
    def get_display(self) -> str:
        """Get formatted system stats"""
        self.update()
        return f"💻 CPU:{self.cpu_percent:.0f}% | 🧠 RAM:{self.ram_percent:.0f}% | 🧵 THREADS:{self.thread_count}"

# ==================== ULTRA PROGRESS BAR ====================

class UltraProgressBar:
    """Advanced progress bar with system stats"""
    
    def __init__(self, total: int, width: int = 70, monitor: SystemMonitor = None):
        self.total = total
        self.width = width
        self.start_time = time.time()
        self.last_update = 0
        self.monitor = monitor
        self.speeds = []
    
    def update(self, current: int, message: str = "", speed: float = 0):
        progress = current / self.total
        filled = int(self.width * progress)
        
        # Ultra gradient bar
        bar = ''
        for i in range(filled):
            if i < self.width // 4:
                bar += f"{Colors.RED}█"
            elif i < self.width // 2:
                bar += f"{Colors.YELLOW}█"
            elif i < 3 * self.width // 4:
                bar += f"{Colors.GREEN}█"
            else:
                bar += f"{Colors.CYAN}█"
        bar += '░' * (self.width - filled)
        
        elapsed = time.time() - self.start_time
        if current > 0 and current != self.last_update:
            eta = (elapsed / current) * (self.total - current)
            eta_str = f"ETA: {eta:.1f}s"
            self.last_update = current
            
            # Store speed for average
            if speed > 0:
                self.speeds.append(speed)
                if len(self.speeds) > 10:
                    self.speeds.pop(0)
        else:
            eta_str = "ETA: ---"
        
        percent = progress * 100
        avg_speed = sum(self.speeds) / len(self.speeds) if self.speeds else speed
        
        # System stats
        sys_stats = ""
        if self.monitor:
            sys_stats = f" | {self.monitor.get_display()}"
        
        sys.stdout.write(f'\r{Colors.BOLD}{bar}{Colors.RESET} {percent:5.1f}% | {eta_str} | ⚡ {speed:.1f} msg/s | 📊 AVG:{avg_speed:.1f}{sys_stats} | {message}')
        sys.stdout.flush()
    
    def finish(self, message: str = "COMPLETE"):
        self.update(self.total, message)
        print()

# ==================== ULTRA ENGINE 100 THREADS ====================

class UltraEngineX100:
    """100 THREADS High-performance engine"""
    
    def __init__(self, max_workers: int = Config.max_threads):
        self.max_workers = min(max_workers, 100)  # Max 100 threads
        self.executor = ThreadPoolExecutor(max_workers=self.max_workers)
        self.semaphore = Semaphore(self.max_workers)
        self.task_queue = queue.Queue(maxsize=Config.max_queue_size)
        self.results = []
        self.lock = Lock()
        self.active_tasks = 0
        
    def execute_batch(self, tasks: List[callable]) -> List:
        """Execute a batch of tasks in parallel - 100 threads"""
        futures = []
        
        # Submit all tasks
        for task in tasks:
            with self.semaphore:
                future = self.executor.submit(task)
                futures.append(future)
                with self.lock:
                    self.active_tasks += 1
        
        # Collect results with timeout
        results = []
        for future in as_completed(futures, timeout=10):
            try:
                result = future.result(timeout=2)
                results.append(result)
            except Exception:
                results.append(False)
            finally:
                with self.lock:
                    self.active_tasks -= 1
        
        return results
    
    def execute_stream(self, task_generator, max_tasks: int):
        """Stream execution for large batches"""
        results = []
        batch = []
        
        for i, task in enumerate(task_generator):
            if i >= max_tasks:
                break
            batch.append(task)
            
            if len(batch) >= Config.batch_size:
                batch_results = self.execute_batch(batch)
                results.extend(batch_results)
                batch = []
                
                # Small delay between batches for stability
                time.sleep(0.05)
        
        # Process remaining
        if batch:
            batch_results = self.execute_batch(batch)
            results.extend(batch_results)
        
        return results
    
    def shutdown(self):
        """Shutdown the executor"""
        self.executor.shutdown(wait=True, cancel_futures=False)

# ==================== ULTRA SPAM ENGINE X100 ====================

class UltraSpamEngineX100:
    """100 THREADS Ultra high-performance spam engine"""
    
    def __init__(self, config: Config, logger, message_manager, whatsapp):
        self.config = config
        self.logger = logger
        self.message_manager = message_manager
        self.whatsapp = whatsapp
        self.is_running = False
        self.ultra_engine = UltraEngineX100(max_workers=config.max_threads)
        self.monitor = SystemMonitor()
        self.stats = {
            'sent': 0,
            'failed': 0,
            'start_time': None,
            'end_time': None,
            'peak_speed': 0,
            'speeds': []
        }
        self.lock = Lock()
    
    def send_message_task(self, phone: str, message: str) -> bool:
        """Single message task for threading"""
        if not self.is_running:
            return False
        
        success = self.whatsapp.open_whatsapp(phone, message)
        
        with self.lock:
            if success:
                self.stats['sent'] += 1
            else:
                self.stats['failed'] += 1
        
        return success
    
    def generate_tasks(self, phone: str, count: int):
        """Generate tasks for streaming"""
        for _ in range(count):
            if not self.is_running:
                break
            message = self.message_manager.get_random_message()
            yield lambda p=phone, m=message: self.send_message_task(p, m)
    
    def run_ultra_x100(self, phone: str, count: int, min_delay: float, max_delay: float, 
                       show_progress: bool = True) -> Dict:
        """Run 100 THREADS ultra-fast parallel attack"""
        self.is_running = True
        self.stats['start_time'] = datetime.now()
        self.stats['sent'] = 0
        self.stats['failed'] = 0
        self.stats['peak_speed'] = 0
        self.stats['speeds'] = []
        
        self.logger.ultra(f"🚀 100 THREADS ULTRA MODE ACTIVATED - Power: {self.config.max_threads} threads")
        self.logger.ultra(f"🔥 TURBO BOOST: {'ENABLED' if self.config.turbo_boost else 'DISABLED'}")
        self.logger.info(f"Target: {phone}")
        self.logger.info(f"Messages: {count} | Delay: {min_delay}-{max_delay}s | Parallel: 100x")
        
        progress = UltraProgressBar(count, monitor=self.monitor) if show_progress else None
        start_time = time.time()
        last_update_time = start_time
        last_sent = 0
        
        try:
            # Generate and execute tasks stream
            task_gen = self.generate_tasks(phone, count)
            
            # Process in batches
            batch = []
            for i, task in enumerate(task_gen):
                if not self.is_running:
                    break
                    
                batch.append(task)
                
                if len(batch) >= self.config.batch_size:
                    # Execute batch with 100 threads
                    batch_results = self.ultra_engine.execute_batch(batch)
                    batch = []
                    
                    # Apply delay between batches (reduced for turbo mode)
                    if self.config.turbo_boost:
                        delay = random.uniform(min_delay * 0.5, max_delay * 0.8)
                    else:
                        delay = random.uniform(min_delay, max_delay)
                    time.sleep(delay)
                    
                    # Update progress and speed
                    if progress and time.time() - last_update_time > 0.5:
                        current_time = time.time()
                        elapsed = current_time - start_time
                        current_speed = self.stats['sent'] / elapsed if elapsed > 0 else 0
                        
                        # Calculate instant speed
                        time_diff = current_time - last_update_time
                        sent_diff = self.stats['sent'] - last_sent
                        instant_speed = sent_diff / time_diff if time_diff > 0 else 0
                        
                        if current_speed > self.stats['peak_speed']:
                            self.stats['peak_speed'] = current_speed
                        
                        self.stats['speeds'].append(instant_speed)
                        if len(self.stats['speeds']) > 20:
                            self.stats['speeds'].pop(0)
                        
                        avg_instant = sum(self.stats['speeds']) / len(self.stats['speeds']) if self.stats['speeds'] else 0
                        
                        progress.update(self.stats['sent'], 
                                      f"⚡ {instant_speed:.1f} msg/s | 🚀 Peak: {self.stats['peak_speed']:.1f} | 🔥 100T",
                                      instant_speed)
                        
                        last_update_time = current_time
                        last_sent = self.stats['sent']
            
            # Process remaining batch
            if batch:
                self.ultra_engine.execute_batch(batch)
        
        except KeyboardInterrupt:
            self.logger.warning("Attack interrupted by user")
        except Exception as e:
            self.logger.error(f"Error during attack: {e}")
        finally:
            self.stop()
        
        if progress:
            progress.finish()
        
        return self.get_stats()
    
    def stop(self):
        """Stop the attack"""
        self.is_running = False
        self.stats['end_time'] = datetime.now()
        self.ultra_engine.shutdown()
        
        duration = (self.stats['end_time'] - self.stats['start_time']).total_seconds() if self.stats['start_time'] else 0
        avg_speed = self.stats['sent'] / duration if duration > 0 else 0
        
        self.logger.success(f"Attack completed: {self.stats['sent']} sent, {self.stats['failed']} failed")
        self.logger.ultra(f"⚡ Average Speed: {avg_speed:.2f} msg/s | Peak: {self.stats['peak_speed']:.2f} msg/s")
        self.logger.ultra(f"🔥 100 THREADS PERFORMANCE: {self.stats['sent']} messages in {duration:.1f}s")
    
    def get_stats(self) -> Dict:
        """Get attack statistics"""
        duration = None
        if self.stats['start_time'] and self.stats['end_time']:
            duration = (self.stats['end_time'] - self.stats['start_time']).total_seconds()
        
        total_attempts = self.stats['sent'] + self.stats['failed']
        success_rate = (self.stats['sent'] / total_attempts * 100) if total_attempts > 0 else 0
        avg_speed = self.stats['sent'] / duration if duration and duration > 0 else 0
        
        return {
            'sent': self.stats['sent'],
            'failed': self.stats['failed'],
            'total': total_attempts,
            'duration': duration,
            'success_rate': success_rate,
            'peak_speed': self.stats['peak_speed'],
            'avg_speed': avg_speed,
            'threads_used': self.config.max_threads
        }

# ==================== BANNER X100 ====================

class Banner:
    """Ultra banner with 100 threads display"""
    
    @staticmethod
    def display():
        """Display main banner"""
        os.system('cls' if os.name == 'nt' else 'clear')
        
        banner = f"""
{Colors.RED}{Colors.BOLD}╔══════════════════════════════════════════════════════════════════════════════════════════════╗
║{Colors.gradient("  ██████╗██████╗ ███╗   ███╗    ███████╗ ██████╗ ██████╗     ██╗   ██╗██╗  ████████╗██████╗  █████╗ ", "fast")}{Colors.RED}║
║{Colors.gradient(" ██╔════╝██╔══██╗████╗ ████║    ██╔════╝██╔════╝██╔════╝     ██║   ██║██║  ╚══██╔══╝██╔══██╗██╔══██╗", "fast")}{Colors.RED}║
║{Colors.gradient(" ██║     ██║  ██║██╔████╔██║    ███████╗██║     ██║  ███╗    ██║   ██║██║     ██║   ██████╔╝███████║", "fast")}{Colors.RED}║
║{Colors.gradient(" ██║     ██║  ██║██║╚██╔╝██║    ╚════██║██║     ██║   ██║    ██║   ██║██║     ██║   ██╔══██╗██╔══██║", "fast")}{Colors.RED}║
║{Colors.gradient(" ╚██████╗██████╔╝██║ ╚═╝ ██║    ███████║╚██████╗╚██████╔╝    ╚██████╔╝███████╗██║   ██║  ██║██║  ██║", "fast")}{Colors.RED}║
║{Colors.gradient("  ╚═════╝╚═════╝ ╚═╝     ╚═╝    ╚══════╝ ╚═════╝ ╚═════╝      ╚═════╝ ╚══════╝╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝", "fast")}{Colors.RED}║
║                                                                                                      ║
║{Colors.YELLOW}{Colors.BOLD}                         ⚡ CDM TECH NEO ULTRA X100 v{Config.version} ⚡{Colors.RED}                         ║
║{Colors.CYAN}{Colors.BOLD}                         👑 DEVELOPER: {Config.developer} 👑{Colors.RED}                                  ║
║{Colors.GREEN}{Colors.BOLD}                         🚀 100 THREADS ULTRA POWER MODE 🚀{Colors.RED}                                 ║
║{Colors.PURPLE}{Colors.BOLD}                         🔥 TURBO BOOST ACTIVATED 🔥{Colors.RED}                                        ║
╚══════════════════════════════════════════════════════════════════════════════════════════════╝{Colors.RESET}
"""
        print(banner)
    
    @staticmethod
    def info_section(title: str, content: str, color: str = Colors.CYAN):
        """Display info section"""
        print(f"{color}┌─────────────────────────────────────────────────────────────────────────────────┐{Colors.RESET}")
        print(f"{color}│ {Colors.BOLD}{title}{Colors.RESET}{color}{' ' * (81 - len(title))}│{Colors.RESET}")
        print(f"{color}├─────────────────────────────────────────────────────────────────────────────────┤{Colors.RESET}")
        print(f"{color}│ {content}{' ' * (81 - len(content))}{color}│{Colors.RESET}")
        print(f"{color}└─────────────────────────────────────────────────────────────────────────────────┘{Colors.RESET}")

# ==================== WHATSAPP CONTROLLER ====================

class WhatsAppController:
    """Handle WhatsApp interactions with ultra speed"""
    
    def __init__(self, logger):
        self.logger = logger
        self.success_count = 0
        self.fail_count = 0
        self.lock = Lock()
    
    @staticmethod
    def clean_phone_number(phone: str) -> str:
        """Clean and validate phone number"""
        cleaned = ''.join(filter(str.isdigit, phone))
        if len(cleaned) < 10 or len(cleaned) > 15:
            raise ValueError(f"Invalid phone number length: {len(cleaned)} digits")
        return cleaned
    
    def open_whatsapp(self, phone_number: str, message: str) -> bool:
        """Open WhatsApp with pre-filled message - Ultra fast"""
        try:
            cleaned_number = self.clean_phone_number(phone_number)
            encoded_message = message.replace(' ', '%20').replace('\n', '%0A').replace('#', '%23')
            url = f"https://wa.me/{cleaned_number}?text={encoded_message}"
            
            # Ultra-fast opening without waiting
            if sys.platform == 'win32':
                os.startfile(url)
            elif sys.platform == 'darwin':
                subprocess.Popen(['open', url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            else:
                subprocess.Popen(['xdg-open', url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            with self.lock:
                self.success_count += 1
            return True
        except Exception:
            with self.lock:
                self.fail_count += 1
            return False

# ==================== MESSAGE MANAGER ====================

class MessageManager:
    """Handle message loading and management"""
    
    def __init__(self, filename: str = Config.messages_file):
        self.filename = Path(filename)
        self.messages: List[str] = []
        self.load_messages()
    
    def load_messages(self) -> List[str]:
        """Load messages from file"""
        if not self.filename.exists():
            self.create_default_messages()
        
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                self.messages = [line.strip() for line in f.readlines() if line.strip()]
            
            if not self.messages:
                self.create_default_messages()
            
            return self.messages
        except Exception:
            self.create_default_messages()
            return self.messages
    
    def create_default_messages(self):
        """Create default messages file"""
        default_messages = [
            "🔥 CDM503 🔥",
            "⚡ CDM Tech ⚡",
            "💀 Sky Plug CDM 💀",
            "👑 Le Génie Des Codes 👑",
            "🚀 CDM503 X100 🚀",
            "💎 SKY PLUG - MASTER 💎",
            "🎯 100 THREADS POWER 🎯",
            "🌟 TURBO MODE ACTIVE 🌟",
            "⚡ ULTRA SPEED ⚡",
            "🔥 X100 PERFORMANCE 🔥"
        ]
        
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                f.write('\n'.join(default_messages))
            self.messages = default_messages
        except Exception:
            self.messages = default_messages
    
    def get_random_message(self) -> str:
        """Get random message"""
        return random.choice(self.messages)

# ==================== LOGGER ====================

class Logger:
    """Professional logging system"""
    
    def __init__(self, log_file: str = Config.log_file):
        self.log_file = Path(log_file)
        self.lock = Lock()
        self.enabled = Config.enable_logging
    
    def log(self, level: str, message: str, color: str = Colors.WHITE):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        log_entry = f"[{timestamp}] [{level}] {message}"
        
        with self.lock:
            if self.enabled:
                try:
                    with open(self.log_file, 'a', encoding='utf-8') as f:
                        f.write(log_entry + '\n')
                except Exception:
                    pass
            
            level_colors = {
                'INFO': Colors.GREEN,
                'WARNING': Colors.YELLOW,
                'ERROR': Colors.RED,
                'SUCCESS': Colors.CYAN,
                'ULTRA': Colors.RED + Colors.BOLD
            }
            level_color = level_colors.get(level, Colors.WHITE)
            print(f"{level_color}[{level}]{Colors.RESET} {message}")
    
    def info(self, message: str):
        self.log('INFO', message)
    
    def warning(self, message: str):
        self.log('WARNING', message, Colors.YELLOW)
    
    def error(self, message: str):
        self.log('ERROR', message, Colors.RED)
    
    def success(self, message: str):
        self.log('SUCCESS', message, Colors.CYAN)
    
    def ultra(self, message: str):
        self.log('ULTRA', message, Colors.RED)

# ==================== MAIN APPLICATION ====================

class CDMApplication:
    """Main application class - 100 THREADS"""
    
    def __init__(self):
        self.config = Config()
        self.logger = Logger()
        self.message_manager = MessageManager()
        self.whatsapp = WhatsAppController(self.logger)
        self.spam_engine = UltraSpamEngineX100(self.config, self.logger, self.message_manager, self.whatsapp)
        
        signal.signal(signal.SIGINT, self.signal_handler)
    
    def signal_handler(self, sig, frame):
        print(f"\n{Colors.RED}{Colors.BOLD}⚠️ INTERRUPT SIGNAL{Colors.RESET}")
        self.spam_engine.stop()
        self.clean_exit()
    
    def clean_exit(self):
        print(f"\n{Colors.PURPLE}{Colors.BOLD}CDM TECH X100 SYSTEM DISCONNECTED{Colors.RESET}")
        print(f"{Colors.CYAN}{Colors.BOLD}SKY PLUG CDM - SIGNING OFF 👑{Colors.RESET}")
        sys.exit(0)
    
    def get_user_input(self):
        """Get and validate user inputs"""
        Banner.display()
        
        print(f"{Colors.GREEN}{Colors.BOLD}⚡ INITIALIZING 100 THREADS ULTRA SYSTEM...{Colors.RESET}")
        print(f"{Colors.CYAN}👑 DEVELOPER: {self.config.developer}{Colors.RESET}")
        print(f"{Colors.RED}{Colors.BOLD}🔥 100 THREADS MODE: ACTIVATED 🔥{Colors.RESET}")
        print()
        
        # Phone input
        phone = input(f"{Colors.PURPLE}╠══[CDM503-X100]> {Colors.RED}📱 PHONE: {Colors.RESET}").strip()
        
        # Count input
        while True:
            count_input = input(f"{Colors.PURPLE}╠══[CDM503-X100]> {Colors.RED}💥 COUNT (max 20000): {Colors.RESET}")
            try:
                count = int(count_input)
                if 1 <= count <= 20000:
                    break
                print(f"{Colors.RED}✗ Count must be between 1 and 20000{Colors.RESET}")
            except ValueError:
                print(f"{Colors.RED}✗ Invalid number{Colors.RESET}")
        
        # Delay inputs
        min_delay = float(input(f"{Colors.PURPLE}╠══[CDM503-X100]> {Colors.RED}⏱️ MIN DELAY (0-5s): {Colors.RESET}"))
        max_delay = float(input(f"{Colors.PURPLE}╠══[CDM503-X100]> {Colors.RED}⏱️ MAX DELAY (0-5s): {Colors.RESET}"))
        
        return phone, count, min_delay, max_delay
    
    def run(self):
        """Main application loop"""
        try:
            while True:
                phone, count, min_delay, max_delay = self.get_user_input()
                
                print(f"\n{Colors.YELLOW}🔥 READY FOR 100 THREADS ULTRA ATTACK?{Colors.RESET}")
                confirm = input(f"{Colors.PURPLE}╠══[CDM503-X100]> {Colors.RED}🚀 LAUNCH X100 (Y/N): {Colors.RESET}").lower()
                
                if confirm != 'y':
                    print(f"{Colors.RED}OPERATION CANCELLED{Colors.RESET}")
                    continue
                
                # Run attack
                Banner.display()
                print(f"{Colors.GREEN}{Colors.BOLD}🔥 100 THREADS ULTRA SEQUENCE ACTIVE 🔥{Colors.RESET}")
                print(f"{Colors.RED}{Colors.BOLD}⚡ PARALLEL PROCESSING: 100 THREADS ⚡{Colors.RESET}\n")
                
                stats = self.spam_engine.run_ultra_x100(phone, count, min_delay, max_delay, show_progress=True)
                
                # Results
                print(f"\n{Colors.CYAN}{'═'*90}{Colors.RESET}")
                print(f"{Colors.RAINBOW}{Colors.BOLD}🏆 100 THREADS ULTRA STATISTICS 🏆{Colors.RESET}")
                print(f"{Colors.CYAN}{'═'*90}{Colors.RESET}")
                print(f"{Colors.GREEN}{Colors.BOLD}✓ Messages Sent:     {stats['sent']}{Colors.RESET}")
                print(f"{Colors.RED}{Colors.BOLD}✗ Failed:            {stats['failed']}{Colors.RESET}")
                print(f"{Colors.BLUE}{Colors.BOLD}📊 Success Rate:     {stats['success_rate']:.1f}%{Colors.RESET}")
                print(f"{Colors.YELLOW}{Colors.BOLD}⏱️  Duration:          {stats['duration']:.2f} seconds{Colors.RESET}")
                print(f"{Colors.PURPLE}{Colors.BOLD}⚡ Average Speed:    {stats['avg_speed']:.2f} msg/s{Colors.RESET}")
                print(f"{Colors.RED}{Colors.BOLD}🚀 Peak Speed:       {stats['peak_speed']:.2f} msg/s{Colors.RESET}")
                print(f"{Colors.CYAN}{Colors.BOLD}🧵 Threads Used:     {stats['threads_used']}{Colors.RESET}")
                print(f"{Colors.CYAN}{'═'*90}{Colors.RESET}")
                
                again = input(f"\n{Colors.PURPLE}🔥 Start new X100 attack? (Y/N): {Colors.RESET}").lower()
                if again != 'y':
                    break
                
        except KeyboardInterrupt:
            pass
        finally:
            self.clean_exit()

# ==================== ENTRY POINT ====================

def main():
    """Main entry point"""
    if sys.version_info < (3, 6):
        print(f"{Colors.RED}Error: Python 3.6 or higher required{Colors.RESET}")
        sys.exit(1)
    
    # Check for psutil (optional)
    try:
        import psutil
    except ImportError:
        print(f"{Colors.YELLOW}⚠️ For system stats, install: pip install psutil{Colors.RESET}")
    
    app = CDMApplication()
    app.run()

if __name__ == "__main__":
    main()
