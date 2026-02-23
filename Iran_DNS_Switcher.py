# Iran DNS Changer version 2.6

# --- Imports ---
import customtkinter as ctk
from tkinter import messagebox 
import tkinter 

import subprocess
import sys
import ctypes
import os
import webbrowser
import re
import requests
import threading
import json
from datetime import datetime
import concurrent.futures

import winreg
from PIL import Image
import pystray

class IranDNSSwitcher:
    def __init__(self):
        # --- Logging ---
        self.log_messages = []
        self.log("Application started")

        # --- Theme and Appearance ---
        ctk.set_appearance_mode("dark")  
        ctk.set_default_color_theme("blue") 

        self.root = ctk.CTk()
        # Name
        self.root.title("Iran DNS Switcher")
        self.root.resizable(False, False)

        # --- Version and GitHub Info for Update Check ---
        self.current_version = "v2.6"
        self.github_repo = "mehrshadasgary/Iran-DNS-Switcher"
        
        # --- File for storing custom DNS ---
        app_data_path = os.getenv('LOCALAPPDATA')
        app_folder = os.path.join(app_data_path, "IranDNSSwitcher")
        if not os.path.exists(app_folder):
            os.makedirs(app_folder)
            self.log(f"Created application data folder at: {app_folder}")
        self.save_file = os.path.join(app_folder, "custom_dns.json")
        self.dns_list_file = os.path.join(app_folder, "dns_list.json") # File for storing fetched DNS
        
        # --- Settings File & Variables ---
        self.settings_file = os.path.join(app_folder, "settings.json")
        self.startup_var = ctk.BooleanVar(value=False)
        self.tray_var = ctk.BooleanVar(value=False)
        self.tray_icon = None
        self.icon_path = None

        # --- Center Window ---
        self.center_window(700, 650)

        # --- Icon ---
        try:
            base_dir = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
            icon_path = os.path.join(base_dir, "Logo-IranDnsSwitcher.ico")

            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
                self.icon_path = icon_path # Save for tray icon
                self.log("Application icon loaded successfully.")
            else:
                self.log(f"Warning: Icon file not found at {icon_path}")
                
        except Exception as e:
            self.log(f"Error setting iconbitmap: {e}. This might happen on non-Windows systems or if the .ico file is invalid.")

        # --- Color ---
        self.colors = {
            'app_bg': '#242424',
            'frame_bg': '#2E2E2E',
            'menu_bar_bg': '#3A3A3A',
            
            'primary_accent_main_red': '#D32F2F',
            'primary_accent_hover_red': '#E57373',
            'primary_accent_pressed_red': '#B71C1C',

            'secondary_accent_gray': '#757575',
            'secondary_accent_gray_hover': '#9E9E9E',
            
            'text_primary': '#F5F5F5',      
            'text_secondary': '#BDBDBD',
            
            'success': '#4CAF50',
            'error': '#FF5252',
            'warning': '#FFC107',
            
            "dns_foreign_purple": "#8E44AD",
            "dns_auto": "#757575",
            "custom_dns_blue": "#2980B9",
            "custom_dns_blue_hover": "#3498DB",
        }

        # --- Fonts ---
        self.font_title = ctk.CTkFont(family="Segoe UI",
                                       size=36,
                                         weight="bold")
        
        self.font_subtitle = ctk.CTkFont(family="Segoe UI",
                                          size=12)
        
        self.font_info_text = ctk.CTkFont(family="Segoe UI",
                                           size=11)
        
        self.font_info_link = ctk.CTkFont(family="Segoe UI",
                                           size=11,
                                             underline=True)
        
        self.font_section_title = ctk.CTkFont(family="Segoe UI",
                                               size=16,
                                                 weight="bold")
        
        self.font_button_main = ctk.CTkFont(family="Segoe UI",
                                             size=12,
                                               weight="bold")
        
        self.font_category_button = ctk.CTkFont(family="Segoe UI",
                                                 size=13,
                                                   weight="bold") 
        
        self.font_status_label = ctk.CTkFont(family="Segoe UI",
                                              size=11)
        
        self.font_dns_button_name = ctk.CTkFont(family="Segoe UI",
                                                 size=12,
                                                   weight="bold")
        
        self.font_delete_button = ctk.CTkFont(family="Segoe UI",
                                               size=10,
                                                 weight="bold")


        # --- DNS Servers with Categories ---
        self.DEFAULT_DNS_SERVERS = {
            "Iranian": {
                "Shecan": ["178.22.122.100",
                            "185.51.200.2"],

                "Radar": ["10.202.10.10",
                           "10.202.10.11"],

                "Electro": ["78.157.42.100",
                             "78.157.42.101"],

                "Begzar": ["185.55.225.25",
                            "185.55.226.26"],

                "403": ["10.202.10.202",
                         "10.202.10.102"],

                "Shatel": ["85.15.1.14",
                            "85.15.1.15"],

                "Shelter": ["78.157.60.6",
                             "78.157.60.242"],

                "Beshkan": ["181.41.194.177",
                             "181.41.194.186"],
                             
                "Shecan 2": ["178.22.122.101",
                              "185.51.200.1"],
                              
                "Begzar 2": ["185.55.224.24",
                              ""],
                              
                "Shelter 2": ["91.92.250.185",
                               "91.92.244.233"],
                               
                "Hamrah Aval": ["208.67.220.200",
                                 "208.67.222.222"],
                                 
                "Irancell": ["74.82.42.42",
                              "0.0.0.0"],
                              
                "Rightel": ["91.239.100.100",
                             "89.223.43.71"],
                             
                "NobarCloud": ["78.110.120.220",
                                "78.110.120.200"],
                                
                "DynX": ["193.24.103.1",
                          "193.24.103.2"],

            },
            "Foreign": {
                "Google": ["8.8.8.8",
                            "8.8.4.4"],

                "Cloudflare": ["1.1.1.1",
                                "1.0.0.1"],

                "OpenDNS": ["208.67.222.222",
                             "208.67.220.220"],

                "Comodo": ["8.26.56.26",
                            "8.20.247.20"],

                "Quad9": ["9.9.9.9",
                           "49.112.112.112"],

                "AlternateDNS": ["76.76.19.19",
                                  "76.223.122.150"],

                "Control D": ["76.76.2.0",
                               "76.76.10.0"],

                "Yandex": ["77.88.8.8",
                            "77.88.8.1"],
                            
                "Cisco": ["208.67.222.222",
                           "208.67.222.20"],
                           
                "Verisign": ["64.6.64.6",
                              "64.6.65.6"],

            },
            "Custom": {}
        }
        self.dns_servers = {}
        
        # --- State for the current category ---
        self.current_category = "Iranian"

        # --- Live Ping State ---
        self.ping_generation = 0
        self.active_ping_buttons = {}

        # --- Variable to store selected network interface ---
        self.selected_interface_var = ctk.StringVar(value="auto")

        # --- Load DNS lists from files or defaults ---
        self.load_main_dns_list()
        self.load_custom_dns()
        
        self.setup_ui()
        self.apply_initial_settings()
        
        # Handle window close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # --- Start Update Check in a Background Thread ---
        update_thread = threading.Thread(target=self.check_for_updates,
                                          daemon=True)
        
        update_thread.start()
        # --- End of Update Check Start ---

    # --- Centralized logging function ---
    def log(self, message):
        """Adds a message to the log list with a timestamp."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        self.log_messages.append(log_entry)
        print(log_entry) 

    def center_window(self, width, height):
        self.root.update_idletasks() 
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # --- Adaptive Height Logic ---
        # If the screen is not tall enough for the default height plus a margin, adjust the height.
        app_height = height
        if screen_height < (height + 100):
            # Leave some space for taskbar and window decorations
            new_height = screen_height - 120 
            # Ensure the window doesn't become impractically small
            app_height = max(600, new_height) 
            self.log(f"Screen height ({screen_height}px) is small. Adjusting window height from {height}px to {app_height}px.")
        
        app_width = width

        x = int((screen_width / 2) - (app_width / 2))
        # Nudge up a bit from the absolute center
        y = int((screen_height / 2) - (app_height / 2) - 40) 
        
        self.root.geometry(f'{app_width}x{app_height}+{x}+{y}')
        
    def setup_ui(self):
        # --- Setup the custom menu bar ---
        self.setup_custom_menu()

        main_container = ctk.CTkFrame(self.root, fg_color=self.colors['app_bg']) 
        main_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # --- Header ---
        header_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        header_frame.pack(fill='x', pady=(0, 15), side='top')
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="Iran DNS Switcher",
            font=self.font_title,
            text_color=self.colors['text_primary'] 
        )
        title_label.pack(pady=(0,5))
        
        info_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        info_frame.pack(pady=(0, 10))
        
        dev_label = ctk.CTkLabel(
            info_frame,
            text=f"{self.current_version} | Developed by Mehrshad Asgary | ",
            font=self.font_info_text,
            text_color=self.colors['text_secondary']
        )

        dev_label.pack(side=ctk.LEFT)
        
        contact_link = ctk.CTkLabel(
            info_frame,
            text="Contact Me",
            font=self.font_info_link,
            text_color=self.colors['primary_accent_hover_red'],
            cursor="hand2"
        )

        # Contact Me
        contact_link.pack(side=ctk.LEFT)
        contact_link.bind("<Button-1>",
                           lambda e: self.open_link("https://mehrshadasgary.ir"))
        
        subtitle_label = ctk.CTkLabel(
            header_frame,
            text="Fast & Easy DNS Configuration for Iran",
            font=self.font_subtitle,
            text_color=self.colors['text_secondary']
        )

        subtitle_label.pack()
        
        # --- Status  ---
        status_frame = ctk.CTkFrame(main_container, fg_color="transparent") 
        status_frame.pack(fill='x', pady=(5, 0), side='bottom')
        
        self.status_label = ctk.CTkLabel(
            status_frame,
            text="Ready to change DNS",
            font=self.font_status_label,
            text_color=self.colors['success']
        )

        self.status_label.pack()

        # --- Control ---
        control_frame = ctk.CTkFrame(main_container,
                                      fg_color="transparent")
        
        control_frame.pack(fill='x',
                            pady=(10, 5),
                              side='bottom')

        button_holder_frame = ctk.CTkFrame(control_frame,
                                            fg_color="transparent")
        
        button_holder_frame.pack()
        
        btn_width = 155
        btn_height = 40
        
        current_dns_btn = ctk.CTkButton(
            button_holder_frame, text="Show Current DNS", font=self.font_button_main,
            fg_color=self.colors['secondary_accent_gray'],
              hover_color=self.colors['secondary_accent_gray_hover'],
            text_color=self.colors['text_primary'],
              command=self.show_current_dns,
            height=btn_height, width=btn_width, corner_radius=8
        )

        current_dns_btn.pack(side=ctk.LEFT, padx=(0, 10))

        ping_current_btn = ctk.CTkButton(
            button_holder_frame, text="Ping Current DNS",
              font=self.font_button_main,
            fg_color=self.colors['secondary_accent_gray'],
              hover_color=self.colors['secondary_accent_gray_hover'],
            text_color=self.colors['text_primary'],
              command=self.ping_current_dns,
            height=btn_height, width=btn_width,
              corner_radius=8
        )

        ping_current_btn.pack(side=ctk.LEFT, padx=(0, 10))

        ping_all_btn = ctk.CTkButton(
            button_holder_frame, text="Ping All DNS",
              font=self.font_button_main,
            fg_color=self.colors['secondary_accent_gray'],
              hover_color=self.colors['secondary_accent_gray_hover'],
            text_color=self.colors['text_primary'],
              command=self.ping_all_dns,
            height=btn_height, width=btn_width,
              corner_radius=8
        )

        ping_all_btn.pack(side=ctk.LEFT, padx=(0, 10))

        add_custom_dns_btn = ctk.CTkButton(
            button_holder_frame, text="Add Custom DNS",
              font=self.font_button_main,
            fg_color=self.colors['secondary_accent_gray'],
              hover_color=self.colors['secondary_accent_gray_hover'],
            text_color=self.colors['text_primary'],
              command=self.open_add_custom_dns_window,
            height=btn_height,
              width=btn_width,
                corner_radius=8
        )

        add_custom_dns_btn.pack(side=ctk.LEFT)
        
        # --- DNS Section ---
        dns_section_frame = ctk.CTkFrame(main_container,
                                          fg_color=self.colors['frame_bg'],
                                            corner_radius=10)
        dns_section_frame.pack(fill='x', side='top', pady=(0, 15))

        section_title = ctk.CTkLabel(
            dns_section_frame,
            text="Select DNS Provider:",
            font=self.font_section_title,
            text_color=self.colors['text_primary']
        )
        section_title.pack(anchor='w', pady=(10, 5), padx=15)

        # --- Category Buttons Frame ---
        category_frame = ctk.CTkFrame(dns_section_frame, fg_color="transparent")
        category_frame.pack(fill='x', padx=15, pady=(0, 10))

        self.category_buttons = {}
        categories = ["Iranian", "Foreign", "Custom"]
        for i, cat_name in enumerate(categories):
            cat_btn = ctk.CTkButton(category_frame, text=cat_name, font=self.font_category_button, command=lambda c=cat_name: self.display_dns_for_category(c))
            cat_btn.pack(side='left', padx=(0, 5))
            self.category_buttons[cat_name] = cat_btn
        
        # --- Default DNS Button ---
        default_btn = ctk.CTkButton(category_frame, text="Default DNS", font=self.font_category_button, command=lambda: self.change_dns("auto", "Default (DHCP)"), fg_color=self.colors['dns_auto'], hover_color=self.colors['secondary_accent_gray_hover'])
        default_btn.pack(side='right', padx=(5, 0))
        
        self.dns_scroll_frame = ctk.CTkScrollableFrame(dns_section_frame,
                                                        fg_color="transparent",
                                                          height=245) 
        
        self.dns_scroll_frame.pack(fill='x', padx=10, pady=(0, 10))
        
        for i in range(3):
            self.dns_scroll_frame.columnconfigure(i, weight=1, minsize=180)
        
        self.display_dns_for_category(self.current_category) # Display initial category

    def setup_custom_menu(self):
        """Creates a custom, theme-able menu bar."""
        self.menu_bar_frame = ctk.CTkFrame(self.root, height=30, fg_color=self.colors['menu_bar_bg'], corner_radius=0)
        self.menu_bar_frame.pack(side="top", fill="x")

        # Network Button
        self.network_btn = ctk.CTkButton(
            self.menu_bar_frame, text="Network",
            font=self.font_button_main,
            fg_color="transparent",
            hover_color=self.colors['secondary_accent_gray'],
            width=80,
            corner_radius=0,
            command=self.toggle_network_menu
        )
        self.network_btn.pack(side="left", padx=(5,0))

        # --- Settings Menu Button ---
        self.settings_menubutton = ctk.CTkButton(
            self.menu_bar_frame, text="Settings",
            font=self.font_button_main,
            fg_color="transparent",
            hover_color=self.colors['secondary_accent_gray'],
            width=80, corner_radius=0
        )
        self.settings_menubutton.pack(side="left")

        # Standard Tkinter Menu for Dropdown
        self.settings_menu = tkinter.Menu(self.menu_bar_frame, tearoff=0,
                                           background=self.colors['frame_bg'],
                                           foreground=self.colors['text_primary'],
                                           activebackground=self.colors['secondary_accent_gray'],
                                           activeforeground=self.colors['text_primary'],
                                           bd=1, relief="solid")
        
        self.settings_menu.add_checkbutton(label="Run on Windows Startup",
                                           variable=self.startup_var,
                                           command=self.toggle_startup)
        
        self.settings_menu.add_checkbutton(label="Minimize to System Tray",
                                           variable=self.tray_var,
                                           command=self.save_settings)

        self.settings_menubutton.bind("<Button-1>", self.show_settings_menu)

        # Log Button
        log_btn = ctk.CTkButton(
            self.menu_bar_frame, text="Log",
            font=self.font_button_main,
            fg_color="transparent",
            hover_color=self.colors['secondary_accent_gray'],
            width=50,
            corner_radius=0,
            command=self.show_log_window
        )
        log_btn.pack(side="left")

        # Update DNS Button
        update_dns_btn = ctk.CTkButton(
            self.menu_bar_frame, text="Update DNS List",
            font=self.font_button_main,
            fg_color="transparent",
            hover_color=self.colors['secondary_accent_gray'],
            width=120,
            corner_radius=0,
            command=self.update_dns_list_from_github
        )
        update_dns_btn.pack(side="left")
        
        self.network_menu_window = None

    def show_settings_menu(self, event):
        """Displays the settings menu at the button's position."""
        x = self.settings_menubutton.winfo_rootx()
        y = self.settings_menubutton.winfo_rooty() + self.settings_menubutton.winfo_height()
        self.settings_menu.tk_popup(x, y)

    def toggle_network_menu(self):
        """Creates and shows or hides the network dropdown menu."""
        if self.network_menu_window is not None and self.network_menu_window.winfo_exists():
            self.network_menu_window.destroy()
            self.network_menu_window = None
            return

        self.network_menu_window = ctk.CTkToplevel(self.root)
        self.network_menu_window.overrideredirect(True)

        x = self.network_btn.winfo_rootx()
        y = self.network_btn.winfo_rooty() + self.network_btn.winfo_height()
        self.network_menu_window.geometry(f"+{x}+{y}")

        menu_frame = ctk.CTkFrame(self.network_menu_window, fg_color=self.colors['frame_bg'], corner_radius=6, border_width=1, border_color=self.colors['secondary_accent_gray'])
        menu_frame.pack()

        auto_rb = ctk.CTkRadioButton(
            menu_frame, text="Auto-detect (Default)",
            variable=self.selected_interface_var,
            value="auto",
            command=lambda: self.select_interface_from_menu("Auto-detect (Default)")
        )
        auto_rb.pack(anchor="w", padx=10, pady=5)

        sep = ctk.CTkFrame(menu_frame, height=1, fg_color=self.colors['secondary_accent_gray'])
        sep.pack(fill="x", padx=10, pady=5)

        interfaces = self.get_all_network_interfaces()
        if not interfaces:
            no_if_label = ctk.CTkLabel(menu_frame, text="No interfaces found", text_color=self.colors['text_secondary'])
            no_if_label.pack(anchor="w", padx=10, pady=5)
        else:
            for interface in interfaces:
                rb = ctk.CTkRadioButton(
                    menu_frame, text=interface,
                    variable=self.selected_interface_var,
                    value=interface,
                    command=lambda i=interface: self.select_interface_from_menu(i)
                )
                rb.pack(anchor="w", padx=10, pady=5)

        self.network_menu_window.bind("<FocusOut>", lambda e: self.network_menu_window.destroy())
        self.network_menu_window.focus_set()

    def select_interface_from_menu(self, interface_name):
        """Handles selection from the custom dropdown menu."""
        self.select_interface(interface_name)
        if self.network_menu_window is not None and self.network_menu_window.winfo_exists():
            self.network_menu_window.destroy()
            self.network_menu_window = None

    def display_dns_for_category(self, category_name):
        self.log(f"Displaying DNS category: {category_name}")
        self.current_category = category_name
        
        category_colors = {
            "Iranian": self.colors['primary_accent_main_red'],
            "Foreign": self.colors['dns_foreign_purple'],
            "Custom": self.colors['custom_dns_blue']
        }

        for name, button in self.category_buttons.items():
            if name == category_name:
                button.configure(fg_color=category_colors.get(name))
            else:
                button.configure(fg_color=self.colors['secondary_accent_gray'])

        for widget in self.dns_scroll_frame.winfo_children():
            widget.destroy()

        dns_list = self.dns_servers.get(category_name, {})
        
        if not dns_list:
            no_dns_label = ctk.CTkLabel(self.dns_scroll_frame, text=f"No DNS servers in '{category_name}' category.", font=self.font_info_text, text_color=self.colors['text_secondary'])
            no_dns_label.pack(pady=20)
            return

        row, col = 0, 0
        button_height = 70

        self.ping_generation += 1
        current_gen = self.ping_generation
        self.active_ping_buttons.clear()

        for dns_name, dns_values in dns_list.items():
            base_color = category_colors.get(category_name)
            hover_color = self.lighten_hex_color(base_color, 0.15)
            
            button_text = f"{dns_name} | ...\n{dns_values[0]}"
            if len(dns_values) > 1 and dns_values[1]:
                button_text += f" | {dns_values[1]}"

            btn = ctk.CTkButton(
                self.dns_scroll_frame, text=button_text, font=self.font_dns_button_name, 
                fg_color=base_color, hover_color=hover_color,
                text_color=self.colors['text_primary'],
                command=lambda cat=category_name, name=dns_name: self.change_dns(cat, name),
                height=button_height, corner_radius=8,
            )
            btn.grid(row=row, column=col, padx=5, pady=5, sticky='nsew')
            
            self.active_ping_buttons[dns_name] = btn

            if category_name == "Custom":
                btn.bind("<Button-3>", lambda event, name=dns_name: self.show_delete_menu(event, name))

            col += 1
            if col > 2:
                col = 0
                row += 1
                
        threading.Thread(target=self._run_live_pings, args=(dns_list, current_gen), daemon=True).start()

    def _run_live_pings(self, dns_list, generation):
        """Runs ping for the currently displayed category in the background."""
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            futures = {}
            for dns_name, dns_values in dns_list.items():
                primary_ip = dns_values[0]
                futures[executor.submit(self.ping_dns_server, primary_ip)] = (dns_name, dns_values)

            for future in concurrent.futures.as_completed(futures):
                if self.ping_generation != generation:
                    break 

                dns_name, dns_values = futures[future]
                try:
                    latency, display_string = future.result()
                    self.root.after(0, self._update_button_ping_text, dns_name, dns_values, display_string, generation)
                except Exception as e:
                    self.log(f"Live ping failed for {dns_name}: {e}")

    def _update_button_ping_text(self, dns_name, dns_values, ping_str, generation):
        """Updates the button text with the live ping result."""
        if self.ping_generation != generation:
            return
        
        if dns_name in self.active_ping_buttons:
            btn = self.active_ping_buttons[dns_name]
            
            new_text = f"{dns_name} | {ping_str}\n{dns_values[0]}"
            if len(dns_values) > 1 and dns_values[1]:
                new_text += f" | {dns_values[1]}"
            btn.configure(text=new_text)

    def get_all_network_interfaces(self):
        self.log("Attempting to get all network interfaces...")
        interfaces = []
        try:
            cmd_config = 'netsh interface ip show config'
            config_result = subprocess.run(cmd_config, shell=True, capture_output=True, text=True, encoding='oem', errors='ignore', timeout=10, creationflags=subprocess.CREATE_NO_WINDOW)
            if config_result.returncode == 0 and config_result.stdout:
                self.log("'netsh interface ip show config' executed successfully.")
                interface_configs = config_result.stdout.strip().split('\n\n')
                for config in interface_configs:
                    match = re.search(r'Configuration for interface "(.+?)"', config, re.IGNORECASE)
                    if match:
                        interfaces.append(match.group(1).strip())
                self.log(f"Found interfaces: {interfaces}")
            else:
                self.log(f"Error executing 'netsh interface ip show config'. Return code: {config_result.returncode}")
                self.log(f"STDOUT: {config_result.stdout}")
                self.log(f"STDERR: {config_result.stderr}")
            return interfaces
        except Exception as e:
            self.log(f"An exception occurred in get_all_network_interfaces: {e}")
            return []

    def select_interface(self, interface_name):
        self.log(f"User selected network interface: {interface_name}")
        self.status_label.configure(text=f"Network interface set to: {interface_name}", text_color=self.colors['text_secondary'])

    def show_log_window(self):
        if hasattr(self, 'log_window') and self.log_window.winfo_exists():
            self.log_window.focus()
            return

        self.log_window = ctk.CTkToplevel(self.root)
        self.log_window.title("Application Log")
        self.log_window.geometry("700x500")
        self.log_window.attributes("-topmost", True)
        self.log_window.transient(self.root)

        dialog_frame = ctk.CTkFrame(self.log_window, fg_color=self.colors['frame_bg'])
        dialog_frame.pack(expand=True, fill="both", padx=10, pady=10)
        
        dialog_frame.rowconfigure(0, weight=1)
        dialog_frame.columnconfigure(0, weight=1)

        log_textbox = ctk.CTkTextbox(dialog_frame, wrap="word", font=self.font_info_text)
        log_textbox.grid(row=0, column=0, columnspan=2, sticky="nsew", pady=(0, 10))
        
        log_content = "\n".join(self.log_messages)
        log_textbox.insert("1.0", log_content)
        log_textbox.configure(state="disabled")

        def copy_log():
            self.log("Log content copied to clipboard.")
            self.root.clipboard_clear()
            self.root.clipboard_append(log_textbox.get("1.0", "end"))
            messagebox.showinfo("Copied", "Log content has been copied to the clipboard.", parent=self.log_window)

        copy_btn = ctk.CTkButton(dialog_frame, text="Copy to Clipboard", command=copy_log, font=self.font_button_main, fg_color=self.colors['secondary_accent_gray'], hover_color=self.colors['secondary_accent_gray_hover'])
        copy_btn.grid(row=1, column=0, padx=5, pady=5)
        
        close_btn = ctk.CTkButton(dialog_frame, text="Close", command=self.log_window.destroy, font=self.font_button_main, fg_color=self.colors['secondary_accent_gray'], hover_color=self.colors['secondary_accent_gray_hover'])
        close_btn.grid(row=1, column=1, padx=5, pady=5)

    def check_for_updates(self):
        self.log("Checking for updates...")
        try:
            api_url = f"https://api.github.com/repos/{self.github_repo}/releases/latest"
            response = requests.get(api_url, timeout=5)
            response.raise_for_status()

            latest_release_data = response.json()
            latest_version = latest_release_data.get("tag_name")
            release_url = latest_release_data.get("html_url")
            self.log(f"Found latest version: {latest_version}. Current version: {self.current_version}")

            if latest_version and latest_version > self.current_version:
                self.log("New update is available.")
                message = (f"A new version ({latest_version}) is available!\n\n" f"You are currently using version {self.current_version}.\n\n" "Would you like to go to the download page?")
                if messagebox.askyesno("Update Available", message):
                    self.open_link(release_url)
            else:
                self.log("Application is up to date.")
        except requests.exceptions.RequestException as e:
            self.log(f"Could not check for updates (RequestException): {e}")
        except Exception as e:
            self.log(f"An unexpected error occurred during update check: {e}")

    def update_dns_list_from_github(self):
        """Starts the process of updating the DNS list from GitHub in a new thread."""
        if messagebox.askyesno("Update DNS List", "This will fetch the latest DNS list from GitHub. Your custom DNS entries will not be affected.\n\nDo you want to continue?"):
            self.status_label.configure(text="Updating DNS list from GitHub...", text_color=self.colors['warning'])
            self.root.update_idletasks()
            update_thread = threading.Thread(target=self._update_dns_list_threaded, daemon=True)
            update_thread.start()

    def _update_dns_list_threaded(self):
        """Fetches and processes the DNS list from GitHub using a plain text file."""
        self.log("Attempting to update DNS list from GitHub...")
        try:
            headers = {'Cache-Control': 'no-cache', 'Pragma': 'no-cache'}
            dns_list_url = f"https://raw.githubusercontent.com/{self.github_repo}/main/dns_servers.txt"
            response = requests.get(dns_list_url, timeout=10, headers=headers)
            response.raise_for_status()

            file_content = response.text
            if file_content.startswith('\ufeff'):
                self.log("Detected and stripped UTF-8 BOM from the beginning of the file.")
                file_content = file_content.lstrip('\ufeff')

            new_iranian_dns = {}
            new_foreign_dns = {}
            current_category = None

            lines = file_content.splitlines()
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                if line.lower().startswith("category: iranian"):
                    current_category = "Iranian"
                elif line.lower().startswith("category: foreign"):
                    current_category = "Foreign"
                elif ":" in line and current_category:
                    try:
                        name, ips_str = line.split(":", 1)
                        ips = [ip.strip() for ip in ips_str.split(",")]
                        
                        if current_category == "Iranian":
                            new_iranian_dns[name.strip()] = ips
                        elif current_category == "Foreign":
                            new_foreign_dns[name.strip()] = ips
                    except ValueError:
                        self.log(f"Skipping malformed line in DNS list: {line}")
                        continue

            if new_iranian_dns or new_foreign_dns:
                self.dns_servers["Iranian"] = new_iranian_dns
                self.dns_servers["Foreign"] = new_foreign_dns
                
                self.save_main_dns_list()
                
                self.log("Successfully fetched and updated DNS list from GitHub.")
                self.root.after(0, self.refresh_dns_display_after_update)
            else:
                self.log("Error: Fetched DNS list appears to be empty or in an invalid format.")
                self.root.after(0, lambda: messagebox.showerror("Update Error", "The fetched DNS list from GitHub is empty or has an invalid format."))
                self.root.after(0, lambda: self.status_label.configure(text="✗ Error: Invalid DNS list format", text_color=self.colors['error']))

        except requests.exceptions.RequestException as e:
            self.log(f"Could not update DNS list (RequestException): {e}")
            self.root.after(0, lambda: messagebox.showerror("Update Error", f"A network error occurred while fetching the DNS list:\n\n{e}"))
            self.root.after(0, lambda: self.status_label.configure(text="✗ Error: Failed to fetch DNS list", text_color=self.colors['error']))
        except Exception as e:
            self.log(f"An unexpected error occurred during DNS list update: {e}")
            self.root.after(0, lambda: messagebox.showerror("Update Error", f"An unexpected error occurred:\n\n{e}"))
            self.root.after(0, lambda: self.status_label.configure(text="✗ Error: Unexpected update failure", text_color=self.colors['error']))
            
    def refresh_dns_display_after_update(self):
        """Refreshes the UI after a successful DNS list update."""
        self.display_dns_for_category(self.current_category)
        self.status_label.configure(text="✓ DNS list updated successfully!", text_color=self.colors['success'])
        messagebox.showinfo("Update Complete", "The DNS list has been successfully updated from GitHub.")

    def show_delete_menu(self, event, dns_name):
        """Creates and displays a right-click context menu to delete a custom DNS."""

        menu = tkinter.Menu(self.root, tearoff=0, bg=self.colors['frame_bg'],
                             fg=self.colors['text_primary'])
        
        menu.add_command(label=f"Delete '{dns_name}'",
                          command=lambda: self.delete_custom_dns(dns_name))
        
        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            menu.grab_release()

    def ping_dns_server(self, ip_address):
        if sys.platform == "win32":
            command = ["ping", "-n", "1", "-w", "1000", ip_address]
        else:
            command = ["ping", "-c", "1", "-W", "1", ip_address]

        try:
            startupinfo = None
            if sys.platform == "win32":
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                startupinfo.wShowWindow = subprocess.SW_HIDE

            result = subprocess.run(
                command, capture_output=True, text=True, encoding='oem', 
                errors='ignore', timeout=2, startupinfo=startupinfo
            )

            output = result.stdout

            if result.returncode == 0:
                match = re.search(r"time(?:<|=)(\d+(?:\.\d+)?)ms", output)
                if match:
                    latency = float(match.group(1))
                    return latency, f"{int(latency)} ms"
            
            if "Request timed out" in output or "Destination host unreachable" in output:
                return float('inf'), "Timeout"

            return float('inf'), "Failed"

        except subprocess.TimeoutExpired:
            return float('inf'), "Timeout"
        except Exception as e:
            self.log(f"Ping error for {ip_address}: {e}")
            return float('inf'), "Error"

    def ping_all_dns(self):
        self.status_label.configure(text="Pinging all DNS servers...",
                                     text_color=self.colors['warning'])
        self.root.update_idletasks()
        ping_all_thread = threading.Thread(target=self._ping_all_dns_threaded,
                                            daemon=True)
        ping_all_thread.start()

    def _ping_all_dns_threaded(self):
        ping_results = []
        # Iterate through all categories and their DNS servers
        for category, dns_list in self.dns_servers.items():
            for name, ips in dns_list.items():
                primary_ip = ips[0]
                self.root.after(0, lambda n=name: self.status_label.configure(text=f"Pinging {n}..."))
                latency, display_string = self.ping_dns_server(primary_ip)
                ping_results.append({
                    'name': name, 'ip': primary_ip,
                    'latency': latency, 'display': display_string
                })
        
        sorted_results = sorted(ping_results, key=lambda x: x['latency'])
        self.root.after(0, lambda: self._update_all_ping_results_ui(sorted_results))

    def _update_all_ping_results_ui(self, results):
        if hasattr(self, 'all_ping_window') and self.all_ping_window.winfo_exists():
            self.all_ping_window.destroy()

        self.all_ping_window = ctk.CTkToplevel(self.root)
        self.all_ping_window.title("All DNS Ping Results")
        self.all_ping_window.geometry("450x450") # Increased height for the new button
        self.all_ping_window.resizable(False, False)
        self.all_ping_window.attributes("-topmost", True)
        self.all_ping_window.transient(self.root)

        dialog_frame = ctk.CTkFrame(self.all_ping_window, fg_color=self.colors['frame_bg'])
        dialog_frame.pack(expand=True, fill="both", padx=20, pady=20)

        ctk.CTkLabel(dialog_frame, text="Ping Results (Sorted by Latency):", 
                     font=self.font_section_title,
                       text_color=self.colors['text_primary']).pack(anchor='w', pady=(0,10))

        results_frame = ctk.CTkScrollableFrame(dialog_frame,
                                                fg_color="transparent")
        results_frame.pack(fill='both', expand=True,
                            pady=(0, 10))

        header_font = ctk.CTkFont(family="Segoe UI", size=12, weight="bold")

        results_frame.columnconfigure(0, weight=2)
        results_frame.columnconfigure(1, weight=1)
        results_frame.columnconfigure(2, weight=1)

        ctk.CTkLabel(results_frame, text="DNS Name",
                      font=header_font,
                        text_color=self.colors['text_secondary']).grid(row=0, column=0, padx=5, pady=2, sticky='w')
        
        ctk.CTkLabel(results_frame, text="Primary IP",
                      font=header_font,
                        text_color=self.colors['text_secondary']).grid(row=0, column=1, padx=5, pady=2, sticky='w')
        
        ctk.CTkLabel(results_frame,
                      text="Latency",
                      font=header_font,
                        text_color=self.colors['text_secondary']).grid(row=0, column=2, padx=5, pady=2, sticky='w')

        for i, res in enumerate(results):
            row_num = i + 1
            text_color = self.colors['success'] if "ms" in res['display'] else self.colors['error']
            
            ctk.CTkLabel(results_frame,
                          text=res['name'], font=self.font_info_text,
                            text_color=self.colors['text_primary']).grid(row=row_num, column=0, padx=5, pady=1, sticky='w')
            
            ctk.CTkLabel(results_frame,
                          text=res['ip'], font=self.font_info_text,
                            text_color=self.colors['text_primary']).grid(row=row_num, column=1, padx=5, pady=1, sticky='w')
            
            ctk.CTkLabel(results_frame,
                          text=res['display'],
                            font=self.font_info_text,
                              text_color=text_color).grid(row=row_num, column=2, padx=5, pady=1, sticky='w')
        
        button_frame = ctk.CTkFrame(dialog_frame, fg_color="transparent")
        button_frame.pack(pady=(10,0))
        
        if results and results[0]['latency'] != float('inf'):
            fastest_dns = results[0]
            connect_btn = ctk.CTkButton(
                button_frame,
                text=f"Connect to Fastest: {fastest_dns['name']}",
                command=lambda: self.connect_to_fastest_dns(fastest_dns),
                font=self.font_button_main,
                fg_color=self.colors['success'],
                hover_color=self.lighten_hex_color(self.colors['success'], 0.15)
            )
            connect_btn.pack(side="left", padx=(0, 10))

        close_btn = ctk.CTkButton(
            button_frame, text="Close",
              command=self.all_ping_window.destroy,
            font=self.font_button_main,
              fg_color=self.colors['secondary_accent_gray'],
            hover_color=self.colors['secondary_accent_gray_hover']
        )
        close_btn.pack(side="left")

        self.status_label.configure(text="Ping test complete. Results are ready.",
                                     text_color=self.colors['success'])

    def connect_to_fastest_dns(self, fastest_dns_info):
        """Finds the full DNS info and applies the settings for the fastest DNS."""
        dns_name = fastest_dns_info['name']
        self.log(f"User requested to connect to the fastest DNS: {dns_name}")

        dns_servers_list = None
        found_category = None

        for category, dns_list in self.dns_servers.items():
            if dns_name in dns_list:
                dns_servers_list = dns_list[dns_name]
                found_category = category
                break
        
        if dns_servers_list:
            self.log(f"Found '{dns_name}' in category '{found_category}' with IPs: {dns_servers_list}")
            
            if hasattr(self, 'all_ping_window') and self.all_ping_window.winfo_exists():
                self.all_ping_window.destroy()
            
            self._apply_dns_settings(dns_name, dns_servers_list)
        else:
            self.log(f"Error: Could not find the DNS server details for '{dns_name}' in self.dns_servers dictionary.")
            messagebox.showerror("Error", f"An error occurred. Could not find the details for '{dns_name}' to apply the settings.", parent=self.root)

    def ping_current_dns(self):
        self.status_label.configure(text="Pinging current DNS...",
                                     text_color=self.colors['warning'])
        self.root.update_idletasks()
        ping_thread = threading.Thread(target=self._ping_current_dns_threaded, daemon=True)
        ping_thread.start()

    def _get_current_dns_ips(self):
        try:
            interface_name = self.get_network_interface()
            if not interface_name: return []

            cmd = f'netsh interface ip show dns name="{interface_name}"'
            result = subprocess.run(cmd, shell=True,
                                     capture_output=True,
                                       text=True,
                                         encoding='oem',
                                           errors='ignore',
                                             timeout=5)
            
            dns_servers_found = []
            for line in result.stdout.split('\n'):
                stripped_line = line.strip()
                if "Statically Configured DNS Servers" in line or "DNS servers configured through DHCP" in line:
                    continue
                parts = stripped_line.split()
                if len(parts) > 0 and (parts[-1].count('.') == 3):
                     if not any(x in stripped_line.lower() for x in ['configuration for interface',
                                                                      'dhcp enabled',
                                                                        'register with suffix']):
                         dns_servers_found.append(parts[-1])
            return dns_servers_found
        except Exception as e:
            self.log(f"Error getting current DNS IPs: {e}")
            return []

    def _ping_current_dns_threaded(self):
        current_dns_ips = self._get_current_dns_ips()
        
        if not current_dns_ips:
            self.root.after(0, lambda: messagebox.showwarning("Ping Failed",
                                                               "Could not determine the current DNS server to ping."))
            self.root.after(0, lambda: self.status_label.configure(text="Ping failed: No current DNS found.",
                                                                    text_color=self.colors['error']))
            return

        primary_dns = current_dns_ips[0]
        latency, display_string = self.ping_dns_server(primary_dns)
        
        message = f"Ping result for {primary_dns}:\n\n{display_string}"
        self.root.after(0, lambda: messagebox.showinfo("Current DNS Ping", message))
        
        status_color = self.colors['success'] if "ms" in display_string else self.colors['error']
        status_text = f"Ping for {primary_dns}: {display_string}"
        self.root.after(0, lambda: self.status_label.configure(text=status_text, text_color=status_color))

    def lighten_hex_color(self, hex_color, factor=0.2):
        if not hex_color.startswith('#'): return hex_color
        
        hex_color = hex_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
        new_rgb = [min(255, max(0, int(val + (255 - val) * factor))) for val in rgb]
            
        return '#{:02x}{:02x}{:02x}'.format(*new_rgb)

    def open_link(self, url):
        try:
            self.log(f"Opening link: {url}")
            webbrowser.open_new(url)
        except Exception as e:
            self.log(f"Failed to open link {url}: {e}")
            messagebox.showerror("Error",
                                  f"Failed to open link:\n{str(e)}")

    def is_admin(self):
        try:
            is_admin = ctypes.windll.shell32.IsUserAnAdmin()
            self.log(f"Administrator check: IsUserAnAdmin() -> {is_admin}")
            return is_admin
        except:
            self.log("Administrator check failed.")
            return False
    
    def run_as_admin(self):
        self.log("Attempting to restart with administrator privileges.")
        try:
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, " ".join(sys.argv), None, 1
            )
        except Exception as e:
            self.log(f"Failed to run as administrator: {e}")
            messagebox.showerror("Error",
                                  "Failed to run as administrator")
    
    def get_network_interface(self):
        selected_interface = self.selected_interface_var.get()
        if selected_interface and selected_interface != "auto":
            self.log(f"Using user-selected interface: '{selected_interface}'")
            return selected_interface

        self.log("Auto-detecting active network interface...")
        try:
            cmd_route = 'route print -4 0.0.0.0'
            self.log(f"Executing command: {cmd_route}")
            route_result = subprocess.run(cmd_route, shell=True,
                                           capture_output=True,
                                             text=True, encoding='utf-8',
                                               errors='ignore',
                                                 timeout=5)
            
            active_interface_ip = None
            if route_result.returncode == 0:
                self.log("'route print' executed successfully.")
                for line in route_result.stdout.split('\n'):
                    if line.strip().startswith('0.0.0.0'):
                        parts = line.strip().split()
                        if len(parts) >= 4:
                            active_interface_ip = parts[3]  
                            self.log(f"Found active route IP: {active_interface_ip}")
                            break
            else:
                self.log(f"Error executing 'route print'. Return code: {route_result.returncode}\nSTDOUT: {route_result.stdout}\nSTDERR: {route_result.stderr}")
            
            if not active_interface_ip:
                self.log("Could not determine the default route interface.")
                messagebox.showwarning("Network Error",
                                        "Could not determine the default route interface. Please check your internet connection.")
                return None

            cmd_config = 'netsh interface ip show config'
            self.log(f"Executing command: {cmd_config}")
            config_result = subprocess.run(cmd_config, shell=True,
                                            capture_output=True,
                                              text=True,
                                                encoding='oem',
                                                errors='ignore',
                                                  timeout=10)

            if config_result.returncode == 0 and config_result.stdout:
                self.log("'netsh show config' executed successfully.")
                interface_configs = config_result.stdout.strip().split('\n\n')
                for config in interface_configs:
                    if active_interface_ip in config:
                        match = re.search(r'Configuration for interface "(.+?)"', config, re.IGNORECASE)
                        if match:
                            interface_name = match.group(1).strip()
                            self.log(f"Found active interface name: '{interface_name}' with IP {active_interface_ip}")
                            return interface_name
            
            self.log(f"Could not match the active route IP {active_interface_ip} to a network interface.")
            messagebox.showwarning("Network Interface", "Could not match the active route to a network interface.")
            return None

        except subprocess.TimeoutExpired as e:
            self.log(f"A network command timed out: {e}")
            messagebox.showerror("Timeout",
                                  "A network command timed out. Please try again.")
            return None
        except Exception as e:
            self.log(f"An unexpected error occurred while detecting the network interface: {e}")
            messagebox.showerror("Network Interface Error",
                                  f"An unexpected error occurred while detecting the network interface: {e}")
            return None
    
    
    def is_valid_ip(self, ip):
        """Checks if the provided string is a valid IPv4 address."""
        pattern = r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"
        if re.match(pattern, ip):
            parts = ip.split('.')
            if all(0 <= int(part) <= 255 for part in parts):
                return True
        return False


    def open_add_custom_dns_window(self):
        """Opens a new window to add a custom DNS."""
        if hasattr(self, 'add_dns_window') and self.add_dns_window.winfo_exists():
            self.add_dns_window.focus()
            return

        self.add_dns_window = ctk.CTkToplevel(self.root)
        self.add_dns_window.title("Add Custom DNS")
        self.add_dns_window.geometry("400x300")
        self.add_dns_window.resizable(False, False)
        self.add_dns_window.attributes("-topmost", True)
        self.add_dns_window.transient(self.root)

        dialog_frame = ctk.CTkFrame(self.add_dns_window,
                                     fg_color=self.colors['frame_bg'])
        dialog_frame.pack(expand=True,
                           fill="both",
                             padx=20,
                               pady=20)

        ctk.CTkLabel(dialog_frame, text="Enter Custom DNS Servers:", 
                     font=self.font_section_title,
                       text_color=self.colors['text_primary']).pack(anchor='w', pady=(0,15))

        name_entry = ctk.CTkEntry(
            dialog_frame,
            placeholder_text="Custom DNS Name (e.g., My DNS)",
            font=self.font_info_text,
            height=35
        )
        name_entry.pack(fill='x', pady=(0,10))

        primary_entry = ctk.CTkEntry(
            dialog_frame,
            placeholder_text="Primary DNS (e.g., 8.8.8.8)",
            font=self.font_info_text,
            height=35
        )
        primary_entry.pack(fill='x', pady=(0,10))

        secondary_entry = ctk.CTkEntry(
            dialog_frame,
            placeholder_text="Secondary DNS (Optional)",
            font=self.font_info_text,
            height=35
        )
        secondary_entry.pack(fill='x', pady=(0,20))

        save_btn = ctk.CTkButton(
            dialog_frame, text="Save DNS",
            command=lambda: self.add_custom_dns(name_entry.get(),
                                                 primary_entry.get(),
                                                   secondary_entry.get()),
            font=self.font_button_main, fg_color=self.colors['secondary_accent_gray'],
            hover_color=self.colors['secondary_accent_gray_hover']
        )
        save_btn.pack()

    def add_custom_dns(self, custom_name, primary_dns, secondary_dns):
        """Validates and adds the new custom DNS to the list."""
        custom_name = custom_name.strip()
        primary_dns = primary_dns.strip()
        secondary_dns = secondary_dns.strip()

        if not primary_dns:
            messagebox.showerror("Input Error",
                                  "Primary DNS field cannot be empty.",
                                    parent=self.add_dns_window)
            return

        if not self.is_valid_ip(primary_dns):
            messagebox.showerror("Invalid IP",
                                  f"The primary DNS address '{primary_dns}' is not a valid IP address.",
                                    parent=self.add_dns_window)
            return
        
        if secondary_dns and not self.is_valid_ip(secondary_dns):
            messagebox.showerror("Invalid IP",
                                  f"The secondary DNS address '{secondary_dns}' is not a valid IP address.",
                                    parent=self.add_dns_window)
            return
        
        if not custom_name:
            custom_name = f"Custom ({primary_dns})"

        if custom_name in self.dns_servers["Custom"]:
            messagebox.showwarning("DNS Exists",
                                    f"A DNS with the name '{custom_name}' already exists in Custom DNS.",
                                      parent=self.add_dns_window)
            return

        self.dns_servers["Custom"][custom_name] = [primary_dns, secondary_dns]
        self.save_custom_dns()
        self.display_dns_for_category("Custom")
        self.log(f"Custom DNS '{custom_name}' added with values: {primary_dns}, {secondary_dns}")
        
        self.add_dns_window.destroy()
        messagebox.showinfo("Success",
                             f"DNS '{custom_name}' has been added to the list.")

    def delete_custom_dns(self, dns_name):
        """Deletes a custom DNS entry."""
        if messagebox.askyesno("Confirm Deletion",
                                f"Are you sure you want to delete '{dns_name}'?"):
            if dns_name in self.dns_servers["Custom"]:
                del self.dns_servers["Custom"][dns_name]
                self.save_custom_dns()
                self.display_dns_for_category("Custom")
                self.log(f"Custom DNS '{dns_name}' has been deleted.")

    def load_main_dns_list(self):
        """Loads the main DNS list from a local file, or uses defaults if not found."""
        self.log("Loading main DNS list...")
        try:
            if os.path.exists(self.dns_list_file):
                with open(self.dns_list_file, 'r') as f:
                    loaded_dns = json.load(f)
                    if "Iranian" in loaded_dns and "Foreign" in loaded_dns:
                        self.dns_servers["Iranian"] = loaded_dns["Iranian"]
                        self.dns_servers["Foreign"] = loaded_dns["Foreign"]
                        self.log(f"Successfully loaded main DNS list from {self.dns_list_file}")
                        return
            
            self.log("Main DNS list file not found or invalid. Using default list.")
            self.dns_servers["Iranian"] = self.DEFAULT_DNS_SERVERS["Iranian"]
            self.dns_servers["Foreign"] = self.DEFAULT_DNS_SERVERS["Foreign"]

        except (json.JSONDecodeError, IOError) as e:
            self.log(f"Could not load main DNS file, using defaults: {e}")
            self.dns_servers["Iranian"] = self.DEFAULT_DNS_SERVERS["Iranian"]
            self.dns_servers["Foreign"] = self.DEFAULT_DNS_SERVERS["Foreign"]

    def load_custom_dns(self):
        """Loads custom DNS entries from the save file."""
        self.log("Loading custom DNS from file...")
        self.dns_servers["Custom"] = {}
        try:
            if os.path.exists(self.save_file):
                with open(self.save_file, 'r') as f:
                    custom_dns = json.load(f)
                    self.dns_servers["Custom"] = custom_dns
                    self.log(f"Successfully loaded {len(custom_dns)} custom DNS entries.")
            else:
                self.log("Custom DNS file does not exist. No entries loaded.")
        except (json.JSONDecodeError, IOError) as e:
            self.log(f"Could not load custom DNS file: {e}")

    def save_main_dns_list(self):
        """Saves the current Iranian and Foreign DNS lists to a local file."""
        self.log("Saving main DNS list to file...")
        try:
            data_to_save = {
                "Iranian": self.dns_servers.get("Iranian", {}),
                "Foreign": self.dns_servers.get("Foreign", {})
            }
            with open(self.dns_list_file, 'w') as f:
                json.dump(data_to_save, f, indent=4)
            self.log("Successfully saved main DNS list.")
        except IOError as e:
            self.log(f"Could not save main DNS list file: {e}")

    def save_custom_dns(self):
        """Saves custom DNS entries to the save file."""
        self.log("Saving custom DNS entries to file...")
        try:
            with open(self.save_file, 'w') as f:
                json.dump(self.dns_servers["Custom"], f, indent=4)
            self.log(f"Successfully saved {len(self.dns_servers['Custom'])} custom DNS entries.")
        except IOError as e:
            self.log(f"Could not save custom DNS file: {e}")

    def change_dns(self, category, dns_name):
        if category == "auto":
            dns_servers_list = ["auto", "auto"]
        else:
            dns_servers_list = self.dns_servers[category][dns_name]
        
        self._apply_dns_settings(dns_name, dns_servers_list)

    def _apply_dns_settings(self, dns_name, dns_servers_list):
        """Core logic to apply DNS settings for both predefined and custom DNS."""
        if not self.is_admin():
            response = messagebox.askyesno(
                "Administrator Access Required",
                "This application needs administrator privileges to change DNS settings.\n\nWould you like to restart as administrator?"
            )

            if response:
                self.run_as_admin()
                if hasattr(self.root, 'destroy'): self.root.destroy()
                else: sys.exit()
            return
        
        try:
            interface_name = self.get_network_interface()
            if not interface_name:
                self.status_label.configure(text="✗ Error: No active network interface found",
                                             text_color=self.colors['error'])
                return

            self.log(f"Attempting to change DNS to '{dns_name}' for interface '{interface_name}'")
            self.status_label.configure(
                text=f"Changing to {dns_name} for '{interface_name}'...",
                text_color=self.colors['warning']
            )

            self.root.update_idletasks()
            
            cli_encoding = 'oem'

            if dns_servers_list[0] == "auto":
                cmd_clear_static = f'netsh interface ipv4 delete dnsserver "{interface_name}" all'
                cmd_set_dhcp = f'netsh interface ip set dns name="{interface_name}" source=dhcp'
                
                self.log(f"Executing command: {cmd_clear_static}")
                subprocess.run(cmd_clear_static,
                                shell=True,
                                  check=False,
                                    capture_output=True,
                                      text=True,
                                        encoding=cli_encoding,
                                          errors='ignore')
                
                self.log(f"Executing command: {cmd_set_dhcp}")
                subprocess.run(cmd_set_dhcp,
                                shell=True, 
                                check=True,
                                  capture_output=True,
                                    text=True,
                                      encoding=cli_encoding,
                                        errors='ignore')
                
                self.status_label.configure(
                    text=f"✓ DNS for '{interface_name}' set to Default (DHCP)", 
                    text_color=self.colors['success']
                )
                self.log(f"DNS for '{interface_name}' successfully set to Default (DHCP).")
                messagebox.showinfo(
                    "Success", 
                    f"DNS successfully set to Default (DHCP) for interface '{interface_name}'"
                )

            else:
                primary_dns = dns_servers_list[0]
                secondary_dns = dns_servers_list[1] if len(dns_servers_list) > 1 and dns_servers_list[1] else ""

                cmd_set_primary = f'netsh interface ip set dns name="{interface_name}" static {primary_dns}'
                cmd_flush_dns = 'ipconfig /flushdns'
                
                self.log(f"Executing command: {cmd_set_primary}")
                subprocess.run(cmd_set_primary, shell=True, check=True, capture_output=True, text=True, encoding=cli_encoding, errors='ignore')
                
                if secondary_dns:
                    cmd_add_secondary = f'netsh interface ip add dns name="{interface_name}" addr={secondary_dns} index=2'
                    self.log(f"Executing command: {cmd_add_secondary}")
                    subprocess.run(cmd_add_secondary,
                                    shell=True,
                                      check=True,
                                        capture_output=True,
                                          text=True,
                                            encoding=cli_encoding,
                                              errors='ignore')
                else:
                    pass

                self.log(f"Executing command: {cmd_flush_dns}")
                subprocess.run(cmd_flush_dns,
                                shell=True,
                                  check=False,
                                    capture_output=True,
                                      text=True,
                                        encoding=cli_encoding,
                                          errors='ignore')
                
                self.status_label.configure(
                    text=f"✓ DNS for '{interface_name}' changed to {dns_name}", 
                    text_color=self.colors['success']
                )
                self.log(f"DNS for '{interface_name}' successfully changed to {dns_name}.")
                success_message = f"DNS successfully changed to {dns_name} for interface '{interface_name}'\n\nPrimary: {primary_dns}"
                if secondary_dns:
                    success_message += f"\nSecondary: {secondary_dns}"
                messagebox.showinfo("Success", success_message)
                
        except subprocess.CalledProcessError as e:
            error_details = f"Command:\n{e.cmd}\n\nReturn Code: {e.returncode}\n\nSTDOUT:\n{e.stdout}\n\nSTDERR:\n{e.stderr}"
            full_error_message = f"A command failed to execute properly.\n\n{error_details}"
            self.log(f"Command Execution Error: {full_error_message}")
            messagebox.showerror("Command Execution Error",
                                  full_error_message)
            
            self.status_label.configure(text="✗ Error changing DNS (command failed)",
                                         text_color=self.colors['error'])
            
        except Exception as e:
            self.log(f"An unexpected error occurred during DNS change: {e}")
            messagebox.showerror("Error", f"An unexpected error occurred during DNS change:\n{str(e)}")
            self.status_label.configure(text="✗ Unexpected error during DNS change",
                                         text_color=self.colors['error'])
    
    def show_current_dns(self):
        try:
            interface_name = self.get_network_interface()
            if not interface_name:
                return

            cmd = f'netsh interface ip show dns name="{interface_name}"'
            self.log(f"Executing command: {cmd}")
            cli_encoding = 'oem'
            try:
                result = subprocess.run(
                    cmd,
                    shell=True,
                    capture_output=True,
                    text=True,
                    encoding=cli_encoding,
                    errors='ignore',
                    timeout=5
                )
            except UnicodeDecodeError:
                # Fallback encoding if 'oem' fails
                result = subprocess.run(
                    cmd,
                    shell=True,
                    capture_output=True,
                    text=True,
                    encoding='latin-1',
                    errors='ignore',
                    timeout=5
                )
            except subprocess.TimeoutExpired:
                self.log(f"Command to show DNS for '{interface_name}' timed out.")
                messagebox.showerror("Timeout", f"Command to show DNS for '{interface_name}' timed out.")
                return

            dns_info = f"Current DNS Servers for '{interface_name}':\n\n"
            
            # --- START OF CHANGE ---
            # Regex to find all valid IPv4 addresses in the output
            ip_pattern = r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b"
            
            # Find all IPs in the entire output string
            dns_servers_found = re.findall(ip_pattern, result.stdout)
            # --- END OF CHANGE ---

            if dns_servers_found:
                # Join all found DNS servers with a new line
                dns_info += "\n".join(dns_servers_found)
            elif 'dhcp' in result.stdout.lower():
                dns_info += "DNS servers configured automatically through DHCP."
            else:
                dns_info += "No static DNS servers specified."
            
            self.log(f"Showing current DNS info: {dns_info.replace(chr(10), ' ')}")
            messagebox.showinfo("Current DNS", dns_info)
            
        except Exception as e:
            self.log(f"Failed to get DNS information: {e}")
            messagebox.showerror("Error", f"Failed to get DNS information:\n{str(e)}")


    # ==========================================
    # --- SETTINGS, STARTUP, AND TRAY ---
    # ==========================================

    def on_closing(self):
        """Handles the window close event based on settings."""
        if self.tray_var.get():
            self.hide_window_to_tray()
        else:
            if messagebox.askyesno("Confirm Exit", "Are you sure you want to exit?"):
                if self.tray_icon:
                    self.tray_icon.stop()
                    self.tray_icon = None
                self.root.destroy()
                self.log("Application closing normally.")
            else:
                self.log("Exit cancelled by user.")

    def load_settings(self):
        """Loads settings from the settings file."""
        self.log("Loading application settings...")
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r') as f:
                    settings = json.load(f)
                    self.startup_var.set(settings.get("run_on_startup", False))
                    self.tray_var.set(settings.get("minimize_to_tray", False))
                    self.log("Settings loaded successfully.")
            else:
                self.log("Settings file not found, using default settings (False).")
        except (json.JSONDecodeError, IOError) as e:
            self.log(f"Could not load settings file, using defaults: {e}")

    def save_settings(self):
        """Saves current settings to the file."""
        self.log("Saving application settings...")
        try:
            settings = {
                "run_on_startup": self.startup_var.get(),
                "minimize_to_tray": self.tray_var.get()
            }
            with open(self.settings_file, 'w') as f:
                json.dump(settings, f, indent=4)
            self.log("Settings saved successfully.")
        except IOError as e:
            self.log(f"Could not save settings file: {e}")

    def apply_initial_settings(self):
        """Syncs settings on application start."""
        self.log("Applying initial settings...")
        self.load_settings()
        
        is_in_registry = self._is_in_startup()
        self.startup_var.set(is_in_registry)
        self.save_settings() 

        self.log(f"Startup (from registry): {'Enabled' if is_in_registry else 'Disabled'}")
        self.log(f"Minimize to Tray (from file): {'Enabled' if self.tray_var.get() else 'Disabled'}")

    def _get_app_path(self):
        """Gets the correct path for the executable, works for frozen (.exe) and scripts (.py)."""
        if getattr(sys, 'frozen', False):
            # If the application is run as a bundle by PyInstaller
            return f'"{sys.executable}"'
        else:
            # If the application is run as a python script
            return f'"{sys.executable}" "{os.path.abspath(sys.argv[0])}"'

    def add_to_startup(self):
        """Adds the application to Windows startup via registry. No admin required for HKCU."""
        app_name = "IranDNSSwitcher"
        app_path = self._get_app_path()
        try:
            key = winreg.HKEY_CURRENT_USER
            key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
            with winreg.OpenKey(key, key_path, 0, winreg.KEY_SET_VALUE) as registry_key:
                winreg.SetValueEx(registry_key, app_name, 0, winreg.REG_SZ, app_path)
            self.log(f"Application added to startup: {app_path}")
            return True
        except Exception as e:
            self.log(f"Error adding to startup: {e}")
            messagebox.showerror("Registry Error", f"Failed to add to startup:\n{e}")
            return False

    def remove_from_startup(self):
        """Removes the application from Windows startup. No admin required for HKCU."""
        app_name = "IranDNSSwitcher"
        try:
            key = winreg.HKEY_CURRENT_USER
            key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
            with winreg.OpenKey(key, key_path, 0, winreg.KEY_SET_VALUE) as registry_key:
                winreg.DeleteValue(registry_key, app_name)
            self.log("Application removed from startup.")
            return True
        except FileNotFoundError:
            self.log("Startup entry not found, nothing to remove.")
            return True 
        except Exception as e:
            self.log(f"Error removing from startup: {e}")
            messagebox.showerror("Registry Error", f"Failed to remove from startup:\n{e}")
            return False

    def _is_in_startup(self):
        """Checks if the application is already in Windows startup."""
        app_name = "IranDNSSwitcher"
        try:
            key = winreg.HKEY_CURRENT_USER
            key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
            with winreg.OpenKey(key, key_path, 0, winreg.KEY_READ) as registry_key:
                winreg.QueryValueEx(registry_key, app_name)
            return True
        except FileNotFoundError:
            return False
        except Exception as e:
            self.log(f"Error checking startup status: {e}")
            return False

    def toggle_startup(self):
        """Toggles the application's presence in Windows startup."""
        is_enabled = self.startup_var.get()
        success = False

        if is_enabled:
            self.log("User wants to enable startup.")
            success = self.add_to_startup()
        else:
            self.log("User wants to disable startup.")
            success = self.remove_from_startup()
        
        if success:
            self.save_settings()
        else:
            self.log("Startup toggle failed, reverting checkbox state.")
            self.startup_var.set(not is_enabled)

    def hide_window_to_tray(self):
        """Hides the main window and shows the system tray icon."""
        self.root.withdraw()
        self.log("Window hidden to system tray.")
        
        if self.tray_icon is not None:
            return 
        
        threading.Thread(target=self._create_tray_icon, daemon=True).start()

    def _create_tray_icon(self):
        """Creates and runs the pystray icon."""
        image = None
        if self.icon_path:
            try:
                image = Image.open(self.icon_path)
            except Exception as e:
                self.log(f"Failed to load icon for tray from path '{self.icon_path}': {e}")
        
        if not image:
            self.log("Creating fallback image for tray icon.")
            width, height = 64, 64
            color1 = (211, 47, 47) 
            image = Image.new('RGB', (width, height), color1)

        menu = (pystray.MenuItem('Show App', self.show_window_from_tray, default=True),
                pystray.MenuItem('Exit', self.exit_app_from_tray))
        
        self.tray_icon = pystray.Icon("Iran DNS Switcher", image, "Iran DNS Switcher", menu)
        self.log("System tray icon started.")
        self.tray_icon.run()

    def show_window_from_tray(self, icon=None, item=None):
        """Shows the main window and stops the tray icon."""
        self.log("Showing window from tray.")
        if self.tray_icon:
            self.tray_icon.stop()
            self.tray_icon = None  
        self.root.after(0, self.root.deiconify)

    def exit_app_from_tray(self, icon=None, item=None):
        """Exits the application from the tray menu safely."""
        self.log("Exit command received from tray icon.")
        if self.tray_icon:
            self.tray_icon.stop()
            self.tray_icon = None  
        self.root.after(0, self.root.destroy)


    def run(self):
        self.root.mainloop()
        self.log("Application closing.")

if __name__ == "__main__":
    if os.name != 'nt':
        # error and exit.
        messagebox.showerror("Compatibility Error",
                              "This application is designed for Windows only.")
        sys.exit(1)
    
    # Run
    app = IranDNSSwitcher()
    app.run()