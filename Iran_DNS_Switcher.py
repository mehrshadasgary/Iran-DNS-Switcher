                                           # Iran DNS Changer version 2.3

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

class IranDNSSwitcher:
    def __init__(self):
        # --- Theme and Appearance ---
        ctk.set_appearance_mode("dark")  
        ctk.set_default_color_theme("blue") 

        self.root = ctk.CTk()
        # Name
        self.root.title("Iran DNS Switcher")
        self.root.resizable(False, False)

        # --- Version and GitHub Info for Update Check ---
        self.current_version = "v2.3"
        self.github_repo = "mehrshadasgary/Iran-DNS-Switcher"
        
        # --- File for storing custom DNS ---
        app_data_path = os.getenv('LOCALAPPDATA')
        app_folder = os.path.join(app_data_path, "IranDNSSwitcher")
        if not os.path.exists(app_folder):
            os.makedirs(app_folder)
        self.save_file = os.path.join(app_folder, "custom_dns.json")

        # --- Center Window ---
        self.center_window(700, 600) 

        # --- Icon ---
        try:
            base_dir = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
            icon_path = os.path.join(base_dir, "Logo-IranDnsSwitcher.ico")

            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
                
            else:
                print(f"Warning: Icon file not found at {icon_path}")
                
        except Exception as e:
            print(f"Error setting iconbitmap: {e}. This might happen on non-Windows systems or if the .ico file is invalid.")

        # --- Color ---
        self.colors = {
            'app_bg': '#242424',
            'frame_bg': '#2E2E2E',
            
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
            
            # Google & Cloudflare
            "dns_foreign_purple": "#8E44AD",

            # auto
            "dns_auto": "#757575",

            # custom
            "custom_dns_blue": "#2980B9",
            "custom_dns_blue_hover": "#3498DB",
        }

        # --- Fonts ---
        self.font_title = ctk.CTkFont(family="Segoe UI", size=36, weight="bold")

        self.font_subtitle = ctk.CTkFont(family="Segoe UI", size=12)

        self.font_info_text = ctk.CTkFont(family="Segoe UI", size=11)

        self.font_info_link = ctk.CTkFont(family="Segoe UI", size=11, underline=True)

        self.font_section_title = ctk.CTkFont(family="Segoe UI", size=16, weight="bold")

        self.font_button_main = ctk.CTkFont(family="Segoe UI", size=12, weight="bold")

        self.font_status_label = ctk.CTkFont(family="Segoe UI", size=11)

        self.font_dns_button_name = ctk.CTkFont(family="Segoe UI", size=12, weight="bold")

        self.font_delete_button = ctk.CTkFont(family="Segoe UI", size=10, weight="bold")


        # --- DNS Servers ---
        self.dns_servers = {

            # irani
            "Shecan": ["178.22.122.100",
                        "185.51.200.2"],

            "Radar": ["10.202.10.10",
                       "10.202.10.11"],

            "Electro": ["78.157.42.100",
                         "78.157.42.101"],

            "Begzar": ["185.55.226.26",
                        "185.55.226.25"],

            "403": ["10.202.10.202",
                     "10.202.10.102"],
            
            # Google & Cloudflare
            "Google": ["8.8.8.8",
                        "8.8.4.4"],
                        
            "Cloudflare": ["1.1.1.1",
                            "1.0.0.1"],

            # auto
            "Auto (DHCP)": ["auto",
                             "auto"]
        }

        self.predefined_dns_keys = set(self.dns_servers.keys())
        
        # --- Load custom DNS from file ---
        self.load_custom_dns()
        
        self.setup_ui()

        # --- Start Update Check in a Background Thread ---
        update_thread = threading.Thread(target=self.check_for_updates,
                                          daemon=True)
        
        update_thread.start()
        # --- End of Update Check Start ---

    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()

        screen_height = self.root.winfo_screenheight()

        x = int((screen_width / 2) - (width / 2))

        y = int((screen_height / 2) - (height / 2) - 50)

        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def setup_ui(self):
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
        
        # --- DNS grade  ---
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
        
        self.dns_scroll_frame = ctk.CTkScrollableFrame(dns_section_frame,
                                                        fg_color="transparent",
                                                          height=245)
        self.dns_scroll_frame.pack(fill='x', padx=10, pady=(0, 10))
        
        for i in range(3):
            self.dns_scroll_frame.columnconfigure(i, weight=1, minsize=180)
        
        self.create_dns_buttons(self.dns_scroll_frame)

    def check_for_updates(self):
        try:
            api_url = f"https://api.github.com/repos/{self.github_repo}/releases/latest"
            response = requests.get(api_url, timeout=5)
            response.raise_for_status()

            latest_release_data = response.json()
            latest_version = latest_release_data.get("tag_name")
            release_url = latest_release_data.get("html_url")

            if latest_version and latest_version > self.current_version:
                message = (
                    f"A new version ({latest_version}) is available!\n\n"
                    f"You are currently using version {self.current_version}.\n\n"
                    "Would you like to go to the download page?"
                )
                if messagebox.askyesno("Update Available", message):
                    self.open_link(release_url)

        except requests.exceptions.RequestException as e:
            print(f"Could not check for updates: {e}")
        except Exception as e:
            print(f"An unexpected error occurred during update check: {e}")

    def create_dns_buttons(self, parent_frame):
        # Clear existing buttons before redrawing
        for widget in parent_frame.winfo_children():
            widget.destroy()

        custom_dns_color = self.colors['custom_dns_blue']

        row, col = 0, 0
        button_height = 70

        for i, (dns_name, dns_values) in enumerate(self.dns_servers.items()):
            is_custom = dns_name not in self.predefined_dns_keys
            
            # --- Main DNS Button ---
            if is_custom:
                base_color = custom_dns_color
            else:
                if dns_name == "Auto (DHCP)":
                    base_color = self.colors['dns_auto']
                elif dns_name in ["Google", "Cloudflare"]:
                    base_color = self.colors['dns_foreign_purple']
                else:
                    base_color = self.colors['primary_accent_main_red']
            
            hover_color = self.lighten_hex_color(base_color,
                                                  0.15) if dns_name != "Auto (DHCP)" else self.colors['secondary_accent_gray_hover']

            button_text = f"{dns_name}\n"
            if dns_values[0] != "auto":
                button_text += f"{dns_values[0]}"
                if len(dns_values) > 1 and dns_values[1]:
                    button_text += f" | {dns_values[1]}"
            else:
                button_text += "Automatic Configuration"

            btn = ctk.CTkButton(
                parent_frame, text=button_text, font=self.font_dns_button_name, 
                fg_color=base_color, hover_color=hover_color,
                  text_color=self.colors['text_primary'],
                command=lambda name=dns_name: self.change_dns(name),
                  height=button_height, corner_radius=8,
            )

            btn.grid(row=row, column=col, padx=5, pady=5, sticky='nsew')
            
            # --- Bind right-click menu for custom DNS ---
            if is_custom:
                btn.bind("<Button-3>", lambda event, name=dns_name: self.show_delete_menu(event, name))

            col += 1
            if col > 2:
                col = 0
                row += 1

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
            print(f"Ping error for {ip_address}: {e}")
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
        for name, ips in self.dns_servers.items():
            if ips[0] != "auto":
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
        self.all_ping_window.geometry("450x400")
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
        
        close_btn = ctk.CTkButton(
            dialog_frame, text="Close",
              command=self.all_ping_window.destroy,
            font=self.font_button_main,
              fg_color=self.colors['secondary_accent_gray'],
            hover_color=self.colors['secondary_accent_gray_hover']
        )
        close_btn.pack(pady=(10,0))

        self.status_label.configure(text="Ping test complete. Results are ready.",
                                     text_color=self.colors['success'])

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
            print(f"Error getting current DNS IPs: {e}")
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
            webbrowser.open_new(url)
        except Exception as e:
            messagebox.showerror("Error",
                                  f"Failed to open link:\n{str(e)}")

    def is_admin(self):
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    
    def run_as_admin(self):
        try:
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, " ".join(sys.argv), None, 1
            )
        except:
            messagebox.showerror("Error",
                                  "Failed to run as administrator")
    
    def get_network_interface(self):
        try:
            cmd = 'netsh interface ip show config'
            cli_encoding = 'oem' 
            
            try:
                result = subprocess.run(cmd,
                                         shell=True,
                                           capture_output=True,
                                             text=True,
                                               encoding=cli_encoding,
                                                 errors='ignore',
                                                   timeout=10)
                
            except UnicodeDecodeError:
                result = subprocess.run(cmd,
                                         shell=True,
                                           capture_output=True,
                                             text=True,
                                               encoding='latin-1',
                                                 errors='ignore',
                                                   timeout=10)

            if result.returncode == 0 and result.stdout:
                interface_configs = result.stdout.strip().split('\n\n')
                
                for config in interface_configs:
                    if 'Default Gateway' in config and '127.0.0.1' not in config:
                        gateway_line = [line for line in config.split('\n') if 'Default Gateway' in line]
                        if gateway_line:
                            gateway_ip = gateway_line[0].split(':')[-1].strip()
                            if gateway_ip and gateway_ip != '0.0.0.0':
                                match = re.search(r'Configuration for interface "(.+?)"',
                                                   config)
                                if match:
                                    interface_name = match.group(1)
                                    print(f"Found active interface: '{interface_name}' with gateway {gateway_ip}")
                                    return interface_name

            print("Warning: Could not determine active network interface with a gateway.")
            messagebox.showwarning("Network Interface",
                                    "Could not automatically determine the active network interface.\n"
                                    "Please ensure you are connected to the internet.")
            return None

        except subprocess.TimeoutExpired:
            print("Error: The command to find network interfaces timed out.")
            messagebox.showerror("Error",
                                  "The command to find network interfaces timed out. Please try again.")
            return None
        except Exception as e:
            print(f"Error getting network interface: {e}.")
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

        if custom_name in self.dns_servers:
            messagebox.showwarning("DNS Exists",
                                    f"A DNS with the name '{custom_name}' already exists.",
                                      parent=self.add_dns_window)
            return

        self.dns_servers[custom_name] = [primary_dns, secondary_dns]
        self.save_custom_dns()
        self.create_dns_buttons(self.dns_scroll_frame)
        
        self.add_dns_window.destroy()
        messagebox.showinfo("Success",
                             f"DNS '{custom_name}' has been added to the list.")

    def delete_custom_dns(self, dns_name):
        """Deletes a custom DNS entry."""
        if messagebox.askyesno("Confirm Deletion",
                                f"Are you sure you want to delete '{dns_name}'?"):
            if dns_name in self.dns_servers:
                del self.dns_servers[dns_name]
                self.save_custom_dns()
                self.create_dns_buttons(self.dns_scroll_frame)

    def load_custom_dns(self):
        """Loads custom DNS entries from the save file."""
        try:
            if os.path.exists(self.save_file):
                with open(self.save_file, 'r') as f:
                    custom_dns = json.load(f)
                    self.dns_servers.update(custom_dns)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Could not load custom DNS file: {e}")

    def save_custom_dns(self):
        """Saves custom DNS entries to the save file."""
        custom_dns_to_save = {k: v for k, v in self.dns_servers.items() if k not in self.predefined_dns_keys}
        try:
            with open(self.save_file, 'w') as f:
                json.dump(custom_dns_to_save, f, indent=4)
        except IOError as e:
            print(f"Could not save custom DNS file: {e}")

    def change_dns(self, dns_name):
        dns_servers_list = self.dns_servers[dns_name]
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

            self.status_label.configure(
                text=f"Changing to {dns_name} for '{interface_name}'...",
                text_color=self.colors['warning']
            )

            self.root.update_idletasks()
            
            cli_encoding = 'oem'

            if dns_servers_list[0] == "auto":
                cmd_clear_static = f'netsh interface ipv4 delete dnsserver "{interface_name}" all'
                cmd_set_dhcp = f'netsh interface ip set dns name="{interface_name}" source=dhcp'
                
                subprocess.run(cmd_clear_static,
                                shell=True,
                                  check=False,
                                    capture_output=True,
                                      text=True,
                                        encoding=cli_encoding,
                                          errors='ignore')
                
                subprocess.run(cmd_set_dhcp,
                                shell=True, 
                                check=True,
                                  capture_output=True,
                                    text=True,
                                      encoding=cli_encoding,
                                        errors='ignore')
                
                self.status_label.configure(
                    text=f"✓ DNS for '{interface_name}' set to Automatic (DHCP)", 
                    text_color=self.colors['success']
                )

                messagebox.showinfo(
                    "Success", 
                    f"DNS successfully set to Automatic (DHCP) for interface '{interface_name}'"
                )

            else:
                primary_dns = dns_servers_list[0]
                secondary_dns = dns_servers_list[1] if len(dns_servers_list) > 1 and dns_servers_list[1] else ""

                cmd_set_primary = f'netsh interface ip set dns name="{interface_name}" static {primary_dns}'
                cmd_flush_dns = 'ipconfig /flushdns'
                
                subprocess.run(cmd_set_primary, shell=True, check=True, capture_output=True, text=True, encoding=cli_encoding, errors='ignore')
                
                if secondary_dns:
                    cmd_add_secondary = f'netsh interface ip add dns name="{interface_name}" addr={secondary_dns} index=2'
                    subprocess.run(cmd_add_secondary,
                                    shell=True,
                                      check=True,
                                        capture_output=True,
                                          text=True,
                                            encoding=cli_encoding,
                                              errors='ignore')
                else:
                    pass

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
                
                success_message = f"DNS successfully changed to {dns_name} for interface '{interface_name}'\n\nPrimary: {primary_dns}"
                if secondary_dns:
                    success_message += f"\nSecondary: {secondary_dns}"
                messagebox.showinfo("Success", success_message)
                
        except subprocess.CalledProcessError as e:
            error_details = f"Command:\n{e.cmd}\n\nReturn Code: {e.returncode}\n\nSTDOUT:\n{e.stdout}\n\nSTDERR:\n{e.stderr}"
            full_error_message = f"A command failed to execute properly.\n\n{error_details}"

            messagebox.showerror("Command Execution Error",
                                  full_error_message)
            
            self.status_label.configure(text="✗ Error changing DNS (command failed)",
                                         text_color=self.colors['error'])
            
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred during DNS change:\n{str(e)}")
            self.status_label.configure(text="✗ Unexpected error during DNS change",
                                         text_color=self.colors['error'])
    
    def show_current_dns(self):
        try:
            interface_name = self.get_network_interface()
            if not interface_name:
                 return

            cmd = f'netsh interface ip show dns name="{interface_name}"'
            cli_encoding = 'oem'
            try:
                result = subprocess.run(cmd,
                                         shell=True,
                                           capture_output=True,
                                             text=True,
                                               encoding=cli_encoding,
                                                 errors='ignore',
                                                   timeout=5)
                
            except UnicodeDecodeError:
                result = subprocess.run(cmd,
                                         shell=True,
                                           capture_output=True,
                                             text=True,
                                               encoding='latin-1',
                                                 errors='ignore',
                                                   timeout=5)
                
            except subprocess.TimeoutExpired:
                messagebox.showerror("Timeout",
                                      f"Command to show DNS for '{interface_name}' timed out.")
                return

            dns_info = f"Current DNS Servers for '{interface_name}':\n\n"
            lines = result.stdout.split('\n')
            
            dns_servers_found = []
            for line in lines:
                stripped_line = line.strip()
                if "Statically Configured DNS Servers" in line or "DNS servers configured through DHCP" in line:
                    continue
                
                parts = stripped_line.split()
                if len(parts) > 0 and (parts[-1].count('.') == 3 or ':' in parts[-1]):
                     if not any(x in stripped_line.lower() for x in ['configuration for interface',
                                                                      'dhcp enabled', 'register with suffix']):
                         dns_servers_found.append(parts[-1])

            if dns_servers_found:
                 dns_info += "\n".join(dns_servers_found)
            elif 'dhcp' in result.stdout.lower():
                 dns_info += "DNS servers configured automatically through DHCP."
            else:
                 dns_info += "No static DNS servers specified."
            
            messagebox.showinfo("Current DNS", dns_info)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to get DNS information:\n{str(e)}")
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    if os.name != 'nt':
        messagebox.showerror("Compatibility Error",
                              "This application is designed for Windows only.")
        sys.exit(1)
    
    # Run
    app = IranDNSSwitcher()
    app.run()
