import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog, simpledialog
import time
import datetime
import json
import os
import sys
import math
import random
import traceback
from threading import Thread
import queue
import platform

class MKSOperatingSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("MKS-OS v1.2 - Mini Operating System")
        self.root.geometry("1000x700")
        
        # Load settings
        self.settings = self.load_settings()
        self.current_language = "english"  # English by default
        
        # System information
        self.system_name = "MKS-OS"
        self.version = "1.2"
        self.username = self.settings.get('username', 'User')
        self.start_time = time.time()
        
        # Development variables
        self.output_queue = queue.Queue()
        
        # Create interface
        self.create_widgets()
        self.update_time()
        
    def load_settings(self):
        """Load settings from file"""
        default = {
            'language': 'english',
            'username': 'User',
            'theme': 'dark',
            'font_size': 12,
            'recent_files': []
        }
        
        try:
            if os.path.exists('mksos_settings.json'):
                with open('mksos_settings.json', 'r', encoding='utf-8') as f:
                    return json.load(f)
        except:
            pass
        return default
    
    def save_settings(self):
        """Save settings to file"""
        try:
            with open('mksos_settings.json', 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=4, ensure_ascii=False)
        except:
            pass
    
    def create_widgets(self):
        """Create user interface"""
        # Top panel
        self.create_top_panel()
        
        # Main tabs
        self.create_main_tabs()
        
        # Status bar
        self.create_status_bar()
        
        # Update system info
        self.update_system_info()
    
    def create_top_panel(self):
        """Create top panel"""
        top_frame = tk.Frame(self.root, bg='#2c3e50', height=60)
        top_frame.pack(fill=tk.X)
        top_frame.pack_propagate(False)
        
        # Logo
        tk.Label(top_frame, text="MKS-OS", font=("Arial", 22, "bold"),
                bg="#2c3e50", fg="white").pack(side=tk.LEFT, padx=20)
        
        tk.Label(top_frame, text=f"v{self.version}", font=("Arial", 10),
                bg="#2c3e50", fg="#bdc3c7").pack(side=tk.LEFT)
        
        # User info
        tk.Label(top_frame, text=f"User: {self.username}", font=("Arial", 10),
                bg="#2c3e50", fg="#bdc3c7").pack(side=tk.LEFT, padx=20)
        
        # Buttons
        button_frame = tk.Frame(top_frame, bg="#2c3e50")
        button_frame.pack(side=tk.RIGHT, padx=20)
        
        tk.Button(button_frame, text="⚙️", command=self.open_settings,
                 bg="#3498db", fg="white", width=3, height=1).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="ℹ️", command=self.show_system_info,
                 bg="#2ecc71", fg="white", width=3, height=1).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="🔄", command=self.restart_system,
                 bg="#e74c3c", fg="white", width=3, height=1).pack(side=tk.LEFT, padx=5)
    
    def create_main_tabs(self):
        """Create main tabs"""
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Home version
        self.home_frame = tk.Frame(self.notebook, bg='#ecf0f1')
        self.notebook.add(self.home_frame, text="🏠 Home")
        self.create_home_tab()
        
        # Development mode
        self.dev_frame = tk.Frame(self.notebook, bg='#ecf0f1')
        self.notebook.add(self.dev_frame, text="⚙️ Development")
        self.create_dev_tab()
        
        # Pro version
        self.pro_frame = tk.Frame(self.notebook, bg='#ecf0f1')
        self.notebook.add(self.pro_frame, text="🚀 Pro")
        self.create_pro_tab()
        
        # Education version
        self.edu_frame = tk.Frame(self.notebook, bg='#ecf0f1')
        self.notebook.add(self.edu_frame, text="🎓 Education")
        self.create_edu_tab()
        
        # Settings
        self.settings_frame = tk.Frame(self.notebook, bg='#ecf0f1')
        self.notebook.add(self.settings_frame, text="⚙️ Settings")
        self.create_settings_tab()
    
    def create_home_tab(self):
        """Create home tab"""
        frame = self.home_frame
        
        # Welcome
        tk.Label(frame, text="Welcome to MKS-OS", font=("Arial", 20, "bold"),
                bg="#ecf0f1").pack(pady=30)
        
        tk.Label(frame, text="Mini Operating System Simulation", font=("Arial", 14),
                bg="#ecf0f1", fg="#7f8c8d").pack(pady=5)
        
        # Quick access
        quick_frame = tk.LabelFrame(frame, text="Quick Access", font=("Arial", 14, "bold"),
                                   bg="#ecf0f1", padx=30, pady=30)
        quick_frame.pack(pady=20, padx=40, fill=tk.X)
        
        # Buttons
        buttons = [
            ("📁", "File Manager", self.open_file_manager, "#3498db"),
            ("📝", "Text Editor", self.open_text_editor, "#2ecc71"),
            ("🧮", "Calculator", self.open_calculator, "#9b59b6"),
            ("📊", "System Info", self.show_system_info, "#e67e22"),
            ("🎮", "Games", self.open_games, "#1abc9c"),
            ("🎵", "Media", self.open_media_player, "#f39c12")
        ]
        
        for i, (icon, text, command, color) in enumerate(buttons):
            btn = tk.Button(quick_frame, text=f"{icon}\n{text}", command=command,
                          bg=color, fg="white", font=("Arial", 10, "bold"),
                          width=12, height=3)
            btn.pack(side=tk.LEFT, padx=15, pady=10)
        
        # System information
        info_frame = tk.LabelFrame(frame, text="System Information", font=("Arial", 14, "bold"),
                                  bg="#ecf0f1", padx=30, pady=30)
        info_frame.pack(pady=20, padx=40, fill=tk.X)
        
        self.info_text = scrolledtext.ScrolledText(info_frame, height=12, width=70,
                                                  bg="#2c3e50", fg="white",
                                                  font=("Courier", 10))
        self.info_text.pack(fill=tk.BOTH, expand=True)
    
    def create_dev_tab(self):
        """Create development tab with full functionality"""
        frame = self.dev_frame
        
        # Development toolbar
        toolbar = tk.Frame(frame, bg='#34495e', height=50)
        toolbar.pack(fill=tk.X, padx=10, pady=5)
        toolbar.pack_propagate(False)
        
        # Tool buttons
        dev_buttons = [
            ("▶️ Run", self.run_code, "#2ecc71"),
            ("⏹️ Stop", self.stop_code, "#e74c3c"),
            ("🐛 Debug", self.debug_code, "#3498db"),
            ("📁 New File", self.new_code_file, "#9b59b6"),
            ("📂 Open File", self.open_code_file, "#1abc9c"),
            ("💾 Save File", self.save_code_file, "#f39c12"),
            ("🗑️ Clear", self.clear_console, "#95a5a6")
        ]
        
        for text, command, color in dev_buttons:
            btn = tk.Button(toolbar, text=text, command=command,
                          bg=color, fg="white", font=("Arial", 10),
                          padx=10, pady=5)
            btn.pack(side=tk.LEFT, padx=5)
        
        # Main area - split into editor and console
        paned = tk.PanedWindow(frame, orient=tk.HORIZONTAL, sashwidth=5, sashrelief=tk.RAISED)
        paned.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel - code editor
        left_frame = tk.Frame(paned, bg='#1e1e1e')
        
        # Editor tabs
        self.dev_notebook = ttk.Notebook(left_frame)
        self.dev_notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create first editor tab
        self.create_editor_tab("main.py")
        
        paned.add(left_frame, width=600)
        
        # Right panel - console and tools
        right_frame = tk.Frame(paned, bg='#2c3e50')
        
        # Right tabs
        right_notebook = ttk.Notebook(right_frame)
        right_notebook.pack(fill=tk.BOTH, expand=True)
        
        # Console output tab
        console_frame = tk.Frame(right_notebook, bg='#2c3e50')
        right_notebook.add(console_frame, text="📟 Console")
        
        # Console output
        self.console_output = scrolledtext.ScrolledText(console_frame,
                                                       bg="#1c2833", fg="#ecf0f1",
                                                       font=("Consolas", 10),
                                                       wrap=tk.WORD)
        self.console_output.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.console_output.insert(tk.END, "MKS-OS Development Console v1.2\n")
        self.console_output.insert(tk.END, "Python " + sys.version.split()[0] + "\n")
        self.console_output.insert(tk.END, "Type your code and press Run\n")
        self.console_output.insert(tk.END, "="*50 + "\n")
        
        # Terminal tab
        terminal_frame = tk.Frame(right_notebook, bg='#2c3e50')
        right_notebook.add(terminal_frame, text="💻 Terminal")
        
        self.terminal_output = scrolledtext.ScrolledText(terminal_frame,
                                                        bg="#1c2833", fg="#ecf0f1",
                                                        font=("Consolas", 10))
        self.terminal_output.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.terminal_output.insert(tk.END, "MKS-OS Terminal v1.2\n")
        self.terminal_output.insert(tk.END, "System terminal simulation\n")
        
        # Projects tab
        projects_frame = tk.Frame(right_notebook, bg='#2c3e50')
        right_notebook.add(projects_frame, text="📁 Projects")
        
        self.project_listbox = tk.Listbox(projects_frame, bg="#1c2833", fg="#ecf0f1",
                                         font=("Arial", 10))
        self.project_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Add example projects
        projects = ["Calculator App", "Text Editor", "File Manager", 
                   "Game: Snake", "Weather App", "Database Manager"]
        for project in projects:
            self.project_listbox.insert(tk.END, "📦 " + project)
        
        paned.add(right_frame, width=400)
    
    def create_editor_tab(self, filename):
        """Create editor tab"""
        editor_frame = tk.Frame(self.dev_notebook, bg='#1e1e1e')
        
        # Text area with scroll
        text_area = scrolledtext.ScrolledText(editor_frame,
                                             bg="#1e1e1e", fg="#d4d4d4",
                                             font=("Consolas", 12),
                                             insertbackground="white",
                                             undo=True)
        text_area.pack(fill=tk.BOTH, expand=True)
        
        # Sample code
        sample_code = '''# Welcome to MKS-OS Development Environment
print("Hello, MKS-OS v1.2!")

def fibonacci(n):
    """Calculate Fibonacci sequence"""
    if n <= 1:
        return n
    else:
        return fibonacci(n-1) + fibonacci(n-2)

# Example usage
if __name__ == "__main__":
    print("Fibonacci(10) =", fibonacci(10))
    
    # List comprehension example
    squares = [x**2 for x in range(10)]
    print("Squares:", squares)
    
    # Working with files
    try:
        with open("example.txt", "w") as f:
            f.write("Hello from MKS-OS v1.2!")
        print("File created successfully")
    except Exception as e:
        print(f"Error: {e}")'''
        
        text_area.insert(tk.END, sample_code)
        
        # Save reference to editor
        self.current_editor = text_area
        
        # Add tab
        self.dev_notebook.add(editor_frame, text=filename)
        self.dev_notebook.select(editor_frame)
    
    def create_pro_tab(self):
        """Create Pro tab"""
        frame = self.pro_frame
        
        # Title
        tk.Label(frame, text="Pro Version v1.2 - System Tools", font=("Arial", 20, "bold"),
                bg="#ecf0f1").pack(pady=20)
        
        # System monitoring
        monitor_frame = tk.LabelFrame(frame, text="System Monitoring", font=("Arial", 14, "bold"),
                                     bg="#ecf0f1", padx=30, pady=30)
        monitor_frame.pack(pady=10, padx=40, fill=tk.X)
        
        # System metrics
        metrics_frame = tk.Frame(monitor_frame, bg="#ecf0f1")
        metrics_frame.pack(fill=tk.X)
        
        self.metrics = {}
        metric_data = [
            ("CPU Usage", "75%", "#e74c3c"),
            ("Memory", "64%", "#3498db"),
            ("Disk", "42%", "#2ecc71"),
            ("Network", "1.2 MB/s", "#9b59b6"),
            ("Uptime", self.get_uptime(), "#f39c12"),
            ("Processes", "24", "#1abc9c")
        ]
        
        for i, (label, value, color) in enumerate(metric_data):
            metric_box = tk.Frame(metrics_frame, bg="#ecf0f1", relief=tk.RAISED, bd=2)
            metric_box.grid(row=0, column=i, padx=10, pady=10, sticky='nsew')
            
            tk.Label(metric_box, text=label, font=("Arial", 10), 
                    bg="#ecf0f1", fg="#7f8c8d").pack(pady=(10, 5))
            value_label = tk.Label(metric_box, text=value, font=("Arial", 16, "bold"),
                                  bg="#ecf0f1", fg=color)
            value_label.pack(pady=(5, 10))
            
            self.metrics[label] = value_label
            metrics_frame.grid_columnconfigure(i, weight=1)
        
        # Professional tools
        tools_frame = tk.LabelFrame(frame, text="Professional Tools", font=("Arial", 14, "bold"),
                                   bg="#ecf0f1", padx=30, pady=30)
        tools_frame.pack(pady=10, padx=40, fill=tk.X)
        
        pro_tools = [
            ("🚀 Turbo Mode", self.turbo_boost, "#e74c3c"),
            ("🔒 Security Scan", self.security_scan, "#2ecc71"),
            ("📊 System Analytics", self.system_analytics, "#3498db"),
            ("⚡ Performance Test", self.performance_test, "#9b59b6"),
            ("💾 Backup System", self.backup_system, "#f39c12"),
            ("🔧 System Diagnostics", self.system_diagnostics, "#1abc9c")
        ]
        
        row, col = 0, 0
        for text, command, color in pro_tools:
            btn = tk.Button(tools_frame, text=text, command=command,
                          bg=color, fg="white", font=("Arial", 11),
                          width=20, height=2)
            btn.grid(row=row, column=col, padx=10, pady=10)
            col += 1
            if col > 2:
                col = 0
                row += 1
        
        # System logs
        log_frame = tk.LabelFrame(frame, text="System Logs", font=("Arial", 14, "bold"),
                                 bg="#ecf0f1", padx=30, pady=30)
        log_frame.pack(pady=10, padx=40, fill=tk.BOTH, expand=True)
        
        self.system_logs = scrolledtext.ScrolledText(log_frame, height=8,
                                                    bg="#2c3e50", fg="#ecf0f1",
                                                    font=("Courier", 9))
        self.system_logs.pack(fill=tk.BOTH, expand=True)
        self.log_message("System started successfully")
        self.log_message(f"User: {self.username}")
        self.log_message(f"Python: {sys.version.split()[0]}")
    
    def create_edu_tab(self):
        """Create education tab"""
        frame = self.edu_frame
        
        # Title
        tk.Label(frame, text="Education Version v1.2", font=("Arial", 20, "bold"),
                bg="#ecf0f1").pack(pady=20)
        
        # Main panel
        main_paned = tk.PanedWindow(frame, orient=tk.HORIZONTAL, sashwidth=5)
        main_paned.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Left panel - courses
        left_frame = tk.Frame(main_paned, bg='#ecf0f1')
        
        tk.Label(left_frame, text="Learning Courses", font=("Arial", 16, "bold"),
                bg="#ecf0f1").pack(pady=20)
        
        # Courses list
        courses_listbox = tk.Listbox(left_frame, font=("Arial", 12), 
                                    selectmode=tk.SINGLE, height=15)
        courses_listbox.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        courses = [
            "1. Introduction to Operating Systems",
            "2. Python Programming Basics",
            "3. GUI Development with Tkinter",
            "4. System Architecture",
            "5. Process Management",
            "6. Memory Management",
            "7. File Systems",
            "8. Networking Basics",
            "9. Security Fundamentals",
            "10. System Administration"
        ]
        
        for course in courses:
            courses_listbox.insert(tk.END, course)
        
        main_paned.add(left_frame, width=300)
        
        # Right panel - content
        right_frame = tk.Frame(main_paned, bg='#ecf0f1')
        
        self.edu_content = scrolledtext.ScrolledText(right_frame,
                                                    font=("Arial", 12),
                                                    wrap=tk.WORD)
        self.edu_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Load demo content
        self.load_edu_content()
        
        main_paned.add(right_frame)
        
        # Practical exercises
        exercises_frame = tk.LabelFrame(frame, text="Practical Exercises", 
                                       font=("Arial", 14, "bold"),
                                       bg="#ecf0f1", padx=30, pady=30)
        exercises_frame.pack(fill=tk.X, padx=20, pady=10)
        
        exercises = [
            ("📝 Quiz: OS Basics", self.start_quiz),
            ("💻 Coding Challenge", self.coding_challenge),
            ("⚙️ System Simulation", self.system_simulation),
            ("🐛 Debug Practice", self.debug_practice)
        ]
        
        for text, command in exercises:
            tk.Button(exercises_frame, text=text, command=command,
                     bg="#3498db", fg="white", font=("Arial", 11),
                     width=20).pack(side=tk.LEFT, padx=10, pady=10)
    
    def create_settings_tab(self):
        """Create settings tab"""
        frame = self.settings_frame
        
        # Title
        tk.Label(frame, text="System Settings v1.2", font=("Arial", 20, "bold"),
                bg="#ecf0f1").pack(pady=20)
        
        # Main settings
        main_frame = tk.LabelFrame(frame, text="General Settings", font=("Arial", 14, "bold"),
                                  bg="#ecf0f1", padx=30, pady=30)
        main_frame.pack(pady=10, padx=40, fill=tk.X)
        
        # Username
        tk.Label(main_frame, text="Username:", font=("Arial", 12)).grid(row=0, column=0, sticky=tk.W, pady=15)
        self.user_var = tk.StringVar(value=self.username)
        user_entry = tk.Entry(main_frame, textvariable=self.user_var, width=28)
        user_entry.grid(row=0, column=1, pady=15, padx=20)
        
        # Font size
        tk.Label(main_frame, text="Font Size:", font=("Arial", 12)).grid(row=1, column=0, sticky=tk.W, pady=15)
        self.font_var = tk.StringVar(value=str(self.settings.get('font_size', 12)))
        font_combo = ttk.Combobox(main_frame, textvariable=self.font_var,
                                 values=['10', '11', '12', '13', '14', '16'], state='readonly', width=25)
        font_combo.grid(row=1, column=1, pady=15, padx=20)
        
        # Buttons
        button_frame = tk.Frame(main_frame, bg="#ecf0f1")
        button_frame.grid(row=2, column=0, columnspan=2, pady=30)
        
        tk.Button(button_frame, text="💾 Save", 
                 command=self.save_settings_changes,
                 bg="#2ecc71", fg="white", font=("Arial", 12),
                 width=15).pack(side=tk.LEFT, padx=10)
        
        tk.Button(button_frame, text="🔄 Defaults", 
                 command=self.restore_defaults,
                 bg="#3498db", fg="white", font=("Arial", 12),
                 width=15).pack(side=tk.LEFT, padx=10)
        
        tk.Button(button_frame, text="Cancel", 
                 command=self.cancel_settings,
                 bg="#e74c3c", fg="white", font=("Arial", 12),
                 width=15).pack(side=tk.LEFT, padx=10)
        
        # System information
        info_frame = tk.LabelFrame(frame, text="System Information", 
                                  font=("Arial", 14, "bold"),
                                  bg="#ecf0f1", padx=30, pady=30)
        info_frame.pack(pady=10, padx=40, fill=tk.X)
        
        sys_info = f"""
MKS-OS Version: {self.version}
Python Version: {sys.version.split()[0]}
Platform: {sys.platform}
Home Directory: {os.path.expanduser('~')}
System Uptime: {self.get_uptime()}
Current User: {self.username}
"""
        
        sys_text = scrolledtext.ScrolledText(info_frame, height=8, 
                                            font=("Courier", 10))
        sys_text.pack(fill=tk.BOTH, expand=True)
        sys_text.insert(tk.END, sys_info)
        sys_text.config(state=tk.DISABLED)
    
    def create_status_bar(self):
        """Create status bar"""
        self.status_bar = tk.Label(self.root, text="MKS-OS v1.2 Ready | Status: OK", 
                                  bd=1, relief=tk.SUNKEN, anchor=tk.W,
                                  font=("Arial", 9))
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def update_time(self):
        """Update time"""
        current_time = time.strftime("%H:%M:%S %d.%m.%Y")
        self.status_bar.config(text=f"MKS-OS v1.2 Ready | Time: {current_time} | Status: OK")
        self.root.after(1000, self.update_time)
    
    def update_system_info(self):
        """Update system information"""
        uptime = self.get_uptime()
        info = f"""
=== MKS-OS System Information ===
Version: {self.version}
User: {self.username}
System Uptime: {uptime}
Python Version: {sys.version.split()[0]}
Platform: {sys.platform}
Architecture: {platform.architecture()[0] if hasattr(platform, 'architecture') else 'Unknown'}

System Status: ✅ Operational
Virtual Environment: MKS-OS is running as an application

Memory Usage: 64% (Simulated)
CPU Usage: 75% (Simulated)
Disk Usage: 42% (Simulated)

Active Processes: 24 (Simulated)
Network Status: Connected (Simulated)

===================================
Note: MKS-OS v1.2 is a virtual operating system
running inside your main OS: {sys.platform}
"""
        if hasattr(self, 'info_text'):
            self.info_text.delete(1.0, tk.END)
            self.info_text.insert(tk.END, info)
    
    def get_uptime(self):
        """Get system uptime"""
        uptime = time.time() - self.start_time
        hours = int(uptime // 3600)
        minutes = int((uptime % 3600) // 60)
        seconds = int(uptime % 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    
    def log_message(self, message):
        """Log messages"""
        timestamp = time.strftime("%H:%M:%S")
        if hasattr(self, 'system_logs'):
            self.system_logs.insert(tk.END, f"[{timestamp}] {message}\n")
            self.system_logs.see(tk.END)
    
    def load_edu_content(self):
        """Load education content"""
        content = """
=== Welcome to MKS-OS v1.2 Educational System ===

This virtual operating system is designed to teach you 
the fundamental concepts of real operating systems.

📚 Available Courses:

1. Introduction to Operating Systems
   - What is an OS?
   - Types of operating systems
   - Key components and functions

2. Python Programming Basics
   - Python syntax and semantics
   - Data types and variables
   - Control structures and functions

3. GUI Development with Tkinter
   - Creating windows and widgets
   - Event handling
   - Layout management

4. System Architecture
   - Kernel and user space
   - Process management
   - Memory management

5. Process Management
   - Process scheduling algorithms
   - Inter-process communication
   - Threads and concurrency

6. Memory Management
   - Virtual memory
   - Paging and segmentation
   - Memory allocation algorithms

7. File Systems
   - File organization
   - Directory structures
   - File operations

8. Networking Basics
   - Network protocols
   - Socket programming
   - Client-server architecture

9. Security Fundamentals
   - Authentication and authorization
   - Encryption
   - Security protocols

10. System Administration
    - User management
    - System monitoring
    - Backup and recovery

Select a course from the left panel to begin learning!
"""
        self.edu_content.insert(tk.END, content)
    
    # ========== DEVELOPMENT MODE FUNCTIONS ==========
    
    def run_code(self):
        """Run Python code"""
        # Get code from current editor
        current_tab = self.dev_notebook.select()
        if current_tab:
            tab_widget = self.dev_notebook.nametowidget(current_tab)
            for child in tab_widget.winfo_children():
                if isinstance(child, scrolledtext.ScrolledText):
                    code = child.get("1.0", tk.END)
                    
                    # Clear console
                    self.console_output.delete(1.0, tk.END)
                    self.console_output.insert(tk.END, ">>> Running Python code...\n")
                    self.console_output.insert(tk.END, "="*50 + "\n")
                    
                    # Run in separate thread
                    thread = Thread(target=self.execute_python_code, args=(code,))
                    thread.daemon = True
                    thread.start()
                    break
    
    def execute_python_code(self, code):
        """Execute Python code"""
        try:
            # Create safe environment
            safe_builtins = {
                'print': print,
                'len': len,
                'range': range,
                'str': str,
                'int': int,
                'float': float,
                'list': list,
                'dict': dict,
                'tuple': tuple,
                'set': set,
                'bool': bool,
                'type': type,
                'abs': abs,
                'min': min,
                'max': max,
                'sum': sum,
                'sorted': sorted,
                'enumerate': enumerate,
                'zip': zip,
                'map': map,
                'filter': filter,
                'isinstance': isinstance,
                'issubclass': issubclass
            }
            
            # Add safe modules
            safe_globals = {
                '__builtins__': safe_builtins,
                'math': math,
                'random': random,
                'datetime': datetime,
                'time': time,
                'json': json
            }
            
            # Redirect output to console
            old_stdout = sys.stdout
            old_stderr = sys.stderr
            sys.stdout = self.ConsoleRedirector(self.console_output)
            sys.stderr = self.ConsoleRedirector(self.console_output)
            
            # Execute code
            exec(code, safe_globals, {})
            
            # Restore standard streams
            sys.stdout = old_stdout
            sys.stderr = old_stderr
            
            # Show success message
            self.console_output.insert(tk.END, "\n" + "="*50 + "\n")
            self.console_output.insert(tk.END, "✅ Code executed successfully!\n")
            self.console_output.see(tk.END)
            
        except Exception as e:
            # Restore standard streams
            sys.stdout = old_stdout
            sys.stderr = old_stderr
            
            # Show error
            error_msg = f"\n❌ Error: {str(e)}\n"
            error_msg += "Traceback:\n"
            error_msg += traceback.format_exc()
            self.console_output.insert(tk.END, error_msg)
            self.console_output.see(tk.END)
    
    class ConsoleRedirector:
        """Redirect output to console"""
        def __init__(self, text_widget):
            self.text_widget = text_widget
        
        def write(self, string):
            self.text_widget.insert(tk.END, string)
            self.text_widget.see(tk.END)
            self.text_widget.update()
        
        def flush(self):
            pass
    
    def stop_code(self):
        """Stop code execution"""
        self.console_output.insert(tk.END, "\n⏹️ Execution stopped\n")
    
    def debug_code(self):
        """Debug code"""
        self.console_output.insert(tk.END, "\n🔍 Starting debug mode...\n")
        self.console_output.insert(tk.END, "Debugger initialized\n")
        self.console_output.insert(tk.END, "Set breakpoints in the code editor\n")
        self.console_output.insert(tk.END, "Use 'Run' to execute with debugging\n")
        
        # Add debug info
        debug_info = """
Debug Commands Available:
• Step Over (F10) - Execute current line
• Step Into (F11) - Step into function
• Step Out (Shift+F11) - Step out of function
• Continue (F5) - Continue execution
• Breakpoint (F9) - Toggle breakpoint

Current Debug Status: Ready
"""
        self.console_output.insert(tk.END, debug_info)
        self.console_output.see(tk.END)
    
    def new_code_file(self):
        """Create new code file"""
        filename = simpledialog.askstring("New File", "Enter filename (e.g., script.py):")
        if filename:
            if not filename.endswith('.py'):
                filename += '.py'
            self.create_editor_tab(filename)
    
    def open_code_file(self):
        """Open code file"""
        filename = filedialog.askopenfilename(
            title="Open Python File",
            filetypes=[("Python files", "*.py"), ("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Create new tab with file content
                editor_frame = tk.Frame(self.dev_notebook, bg='#1e1e1e')
                
                text_area = scrolledtext.ScrolledText(editor_frame,
                                                     bg="#1e1e1e", fg="#d4d4d4",
                                                     font=("Consolas", 12),
                                                     insertbackground="white",
                                                     undo=True)
                text_area.pack(fill=tk.BOTH, expand=True)
                text_area.insert(tk.END, content)
                
                self.dev_notebook.add(editor_frame, text=os.path.basename(filename))
                self.dev_notebook.select(editor_frame)
                
                self.console_output.insert(tk.END, f"\n📂 Opened file: {filename}\n")
                
            except Exception as e:
                messagebox.showerror("Error", f"Could not open file: {str(e)}")
    
    def save_code_file(self):
        """Save code file"""
        current_tab = self.dev_notebook.select()
        if current_tab:
            tab_widget = self.dev_notebook.nametowidget(current_tab)
            for child in tab_widget.winfo_children():
                if isinstance(child, scrolledtext.ScrolledText):
                    code = child.get("1.0", tk.END)
                    
                    filename = filedialog.asksaveasfilename(
                        title="Save Python File",
                        defaultextension=".py",
                        filetypes=[("Python files", "*.py"), ("Text files", "*.txt"), ("All files", "*.*")]
                    )
                    
                    if filename:
                        try:
                            with open(filename, 'w', encoding='utf-8') as f:
                                f.write(code)
                            
                            # Update tab name
                            tab_name = os.path.basename(filename)
                            self.dev_notebook.tab(current_tab, text=tab_name)
                            
                            self.console_output.insert(tk.END, f"\n💾 Saved to: {filename}\n")
                            messagebox.showinfo("Success", f"File saved successfully!\n{filename}")
                            
                        except Exception as e:
                            messagebox.showerror("Error", f"Could not save file: {str(e)}")
                    break
    
    def clear_console(self):
        """Clear console"""
        self.console_output.delete(1.0, tk.END)
        self.console_output.insert(tk.END, "Console cleared\n")
        self.console_output.insert(tk.END, "="*50 + "\n")
    
    # ========== HOME VERSION FUNCTIONS ==========
    
    def open_file_manager(self):
        """Open file manager"""
        messagebox.showinfo("File Manager", "File Manager would open here\n(Simulated functionality in v1.2)")
    
    def open_text_editor(self):
        """Open text editor"""
        messagebox.showinfo("Text Editor", "Text Editor would open here\n(Simulated functionality in v1.2)")
    
    def open_calculator(self):
        """Open calculator"""
        calc_window = tk.Toplevel(self.root)
        calc_window.title("Calculator v1.2")
        calc_window.geometry("300x400")
        
        # Entry field
        entry_var = tk.StringVar()
        entry = tk.Entry(calc_window, textvariable=entry_var, font=("Arial", 20), justify='right')
        entry.grid(row=0, column=0, columnspan=4, sticky='nsew', padx=10, pady=10)
        
        # Buttons
        buttons = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            '0', '.', '=', '+',
            'C'
        ]
        
        row = 1
        col = 0
        for button in buttons:
            if button == '=':
                tk.Button(calc_window, text=button, font=("Arial", 14),
                         command=lambda: self.calculate(entry_var),
                         bg="#2ecc71", fg="white").grid(row=row, column=col, sticky='nsew', padx=2, pady=2)
            elif button == 'C':
                tk.Button(calc_window, text=button, font=("Arial", 14),
                         command=lambda: entry_var.set(''),
                         bg="#e74c3c", fg="white").grid(row=row, column=col, sticky='nsew', padx=2, pady=2)
            else:
                tk.Button(calc_window, text=button, font=("Arial", 14),
                         command=lambda b=button: entry_var.set(entry_var.get() + b)).grid(row=row, column=col, sticky='nsew', padx=2, pady=2)
            
            col += 1
            if col > 3:
                col = 0
                row += 1
        
        # Configure column weights
        for i in range(4):
            calc_window.grid_columnconfigure(i, weight=1)
        for i in range(6):
            calc_window.grid_rowconfigure(i, weight=1)
    
    def calculate(self, entry_var):
        """Perform calculation"""
        try:
            result = eval(entry_var.get())
            entry_var.set(str(result))
        except:
            entry_var.set("Error")
    
    def open_games(self):
        """Open games"""
        messagebox.showinfo("Games", "Games would open here\n(Simulated functionality in v1.2)")
    
    def open_media_player(self):
        """Open media player"""
        messagebox.showinfo("Media Player", "Media Player would open here\n(Simulated functionality in v1.2)")
    
    # ========== PRO VERSION FUNCTIONS ==========
    
    def turbo_boost(self):
        """Turbo mode"""
        self.log_message("Turbo Boost activated")
        messagebox.showinfo("Turbo Boost", "System performance optimized!\nTurbo mode activated in v1.2.")
    
    def security_scan(self):
        """Security scan"""
        self.log_message("Security scan started")
        messagebox.showinfo("Security Scan", "Security scan completed.\nNo threats found in v1.2.")
    
    def system_analytics(self):
        """System analytics"""
        analytics = f"""
=== System Analytics v1.2 ===
Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}

Performance Metrics:
• CPU Usage: 75%
• Memory Usage: 64%
• Disk Usage: 42%
• Network Activity: 1.2 MB/s

System Health:
• Uptime: {self.get_uptime()}
• Processes: 24
• Services: 8 running
• Updates: All current

Recommendations:
1. Clear temporary files
2. Update system drivers
3. Run disk cleanup
"""
        messagebox.showinfo("System Analytics", analytics)
    
    def performance_test(self):
        """Performance test"""
        self.log_message("Performance test started")
        
        # Simulate performance test
        start_time = time.time()
        result = 0
        for i in range(1000000):
            result += i * i
        end_time = time.time()
        
        score = int(1000000 / (end_time - start_time))
        
        messagebox.showinfo("Performance Test v1.2", 
                          f"Performance Test Completed!\n\n"
                          f"Score: {score} operations/sec\n"
                          f"Time: {end_time - start_time:.2f} seconds\n"
                          f"System Rating: {'Excellent' if score > 500000 else 'Good'}")
    
    def backup_system(self):
        """Backup system"""
        self.log_message("System backup initiated")
        messagebox.showinfo("Backup System v1.2", "System backup started...\nBackup will complete in background.")
    
    def system_diagnostics(self):
        """System diagnostics"""
        diagnostics = f"""
=== System Diagnostics v1.2 ===
Time: {time.strftime('%Y-%m-%d %H:%M:%S')}

Hardware Check:
• CPU: Virtual processor (OK)
• Memory: 8.0 GB simulated (OK)
• Storage: 256 GB simulated (OK)
• Network: Virtual adapter (OK)

Software Check:
• MKS-OS: v{self.version} (OK)
• Python: {sys.version.split()[0]} (OK)
• Dependencies: All satisfied (OK)

Security Check:
• Firewall: Active (OK)
• Antivirus: Enabled (OK)
• Updates: Current (OK)

Overall Status: ✅ All systems operational
"""
        messagebox.showinfo("System Diagnostics", diagnostics)
    
    # ========== EDU VERSION FUNCTIONS ==========
    
    def start_quiz(self):
        """Start quiz"""
        messagebox.showinfo("Quiz v1.2", "Starting OS Basics Quiz...\n(Simulated quiz interface)")
    
    def coding_challenge(self):
        """Coding challenge"""
        messagebox.showinfo("Coding Challenge v1.2", "Opening coding challenge...\nTry the Fibonacci sequence exercise!")
    
    def system_simulation(self):
        """System simulation"""
        messagebox.showinfo("System Simulation v1.2", "Starting process scheduling simulation...")
    
    def debug_practice(self):
        """Debug practice"""
        messagebox.showinfo("Debug Practice v1.2", "Opening debugging exercises...\nTry fixing the buggy code!")
    
    # ========== SETTINGS FUNCTIONS ==========
    
    def open_settings(self):
        """Open settings"""
        self.notebook.select(self.settings_frame)
    
    def save_settings_changes(self):
        """Save settings changes"""
        self.settings['username'] = self.user_var.get()
        self.settings['font_size'] = int(self.font_var.get())
        
        # Update variables
        self.username = self.settings['username']
        
        # Save settings
        self.save_settings()
        
        # Update interface
        self.update_ui()
        
        messagebox.showinfo("Settings v1.2", "Settings saved successfully!")
    
    def restore_defaults(self):
        """Restore defaults"""
        self.settings = {
            'language': 'english',
            'username': 'User',
            'theme': 'dark',
            'font_size': 12,
            'recent_files': []
        }
        
        self.user_var.set('User')
        self.font_var.set('12')
        
        messagebox.showinfo("Defaults", "Default settings restored in v1.2")
    
    def cancel_settings(self):
        """Cancel settings"""
        self.user_var.set(self.username)
        self.font_var.set(str(self.settings.get('font_size', 12)))
        messagebox.showinfo("Cancel", "Changes cancelled")
    
    def update_ui(self):
        """Update interface"""
        # Update system information
        self.update_system_info()
        
        # Update status bar
        self.status_bar.config(text=f"MKS-OS v{self.version} | User: {self.username}")
    
    # ========== SYSTEM FUNCTIONS ==========
    
    def show_system_info(self):
        """Show system information"""
        info = f"""
=== MKS-OS v{self.version} System Information ===
Version: {self.version}
Build: Stable Release
User: {self.username}
Uptime: {self.get_uptime()}
Python Version: {sys.version.split()[0]}
Platform: {sys.platform}

Development Features:
• Real Python code execution
• Interactive console output
• Debugging tools
• File management
• System monitoring

Note: This is a virtual OS running inside {sys.platform}
All operations are simulated for educational purposes.
"""
        messagebox.showinfo("System Information", info)
    
    def restart_system(self):
        """Restart system"""
        if messagebox.askyesno("Restart MKS-OS v1.2", "Restart MKS-OS?\nUnsaved changes will be lost."):
            # Close window
            self.root.destroy()
            
            # Restart application
            python = sys.executable
            os.execl(python, python, *sys.argv)
    
    def exit_system(self):
        """Exit system"""
        if messagebox.askyesno("Exit MKS-OS v1.2", "Exit MKS-OS?"):
            self.save_settings()
            self.root.quit()

def main():
    """Main function"""
    root = tk.Tk()
    app = MKSOperatingSystem(root)
    
    # Handle window closing
    root.protocol("WM_DELETE_WINDOW", app.exit_system)
    
    root.mainloop()

if __name__ == "__main__":
    main()