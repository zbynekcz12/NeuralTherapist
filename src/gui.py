import tkinter as tk
from tkinter import ttk
import threading
from config import config
from logger import logger

class GUI:
    def __init__(self, bci_reader, robot_controller, safety_monitor):
        self.root = tk.Tk()
        self.root.title("BCI Therapeutic Robot Control")
        self.root.geometry("800x600")
        
        self.bci_reader = bci_reader
        self.robot_controller = robot_controller
        self.safety_monitor = safety_monitor
        
        self.create_widgets()
        
    def create_widgets(self):
        # Status Frame
        status_frame = ttk.LabelFrame(self.root, text="System Status")
        status_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.bci_status = ttk.Label(status_frame, text="BCI: Disconnected")
        self.bci_status.pack(side=tk.LEFT, padx=5)
        
        self.robot_status = ttk.Label(status_frame, text="Robot: Disconnected")
        self.robot_status.pack(side=tk.LEFT, padx=5)
        
        # Control Frame
        control_frame = ttk.LabelFrame(self.root, text="Controls")
        control_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(control_frame, text="Connect BCI", 
                  command=self.connect_bci).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Connect Robot",
                  command=self.connect_robot).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Start System",
                  command=self.start_system).pack(side=tk.LEFT, padx=5)
        
        # Emergency Stop
        emergency_btn = ttk.Button(control_frame, text="EMERGENCY STOP",
                                 command=self.emergency_stop)
        emergency_btn.pack(side=tk.RIGHT, padx=5)
        emergency_btn.configure(style='Emergency.TButton')
        
        # Parameters Frame
        param_frame = ttk.LabelFrame(self.root, text="Parameters")
        param_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(param_frame, text="Max Speed:").grid(row=0, column=0, padx=5)
        self.speed_scale = ttk.Scale(param_frame, from_=0, to=1,
                                   orient=tk.HORIZONTAL)
        self.speed_scale.set(config.MAX_SPEED)
        self.speed_scale.grid(row=0, column=1, sticky='ew', padx=5)
        
        # Log Frame
        log_frame = ttk.LabelFrame(self.root, text="System Log")
        log_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.log_text = tk.Text(log_frame, height=10, wrap=tk.WORD)
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Style
        style = ttk.Style()
        style.configure('Emergency.TButton', 
                       background='red',
                       foreground='white',
                       font=('Arial', 12, 'bold'))

    def connect_bci(self):
        self.bci_reader.connect()
        if self.bci_reader.connected:
            self.bci_status.config(text="BCI: Connected")
            self.log_message("BCI connected successfully")
        else:
            self.log_message("Failed to connect BCI")

    def connect_robot(self):
        self.robot_controller.connect()
        if self.robot_controller.connected:
            self.robot_status.config(text="Robot: Connected")
            self.log_message("Robot connected successfully")
        else:
            self.log_message("Failed to connect robot")

    def start_system(self):
        if not (self.bci_reader.connected and self.robot_controller.connected):
            self.log_message("Please connect both BCI and robot first")
            return
        
        self.safety_monitor.start_monitoring()
        self.log_message("System started")

    def emergency_stop(self):
        self.safety_monitor.trigger_emergency_stop()
        self.log_message("EMERGENCY STOP ACTIVATED", "red")

    def log_message(self, message, color="black"):
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        
    def run(self):
        self.root.mainloop()
