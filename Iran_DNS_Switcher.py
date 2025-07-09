import customtkinter as ctk
from tkinter import messagebox 
import subprocess
import sys
import ctypes
import os
import webbrowser
import re

class IranDNSSwitcher:
    def __init__(self):
        # --- Theme and Appearance ---
        ctk.set_appearance_mode("dark")  
        ctk.set_default_color_theme("blue") 

        self.root = ctk.CTk()
        self.root.title("Iran DNS Switcher")
        self.root.resizable(False, False)

        # --- Center Window ---
        self.center_window(700, 650)

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

            
            "dns_foreign_purple": "#8E44AD",
            "dns_auto": "#757575",
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

        # --- DNS Servers ---
        self.dns_servers = {
            "Shecan": ["178.22.122.100", "185.51.200.2"],
            "Radar": ["10.202.10.10", "10.202.10.11"],
            "Electro": ["78.157.42.100", "78.157.42.101"],
            "Begzar": ["185.55.226.26", "185.55.226.25"],
            "403": ["10.202.10.202", "10.202.10.102"],
            "Google": ["8.8.8.8", "8.8.4.4"],
            "Cloudflare": ["1.1.1.1", "1.0.0.1"],
            "Auto (DHCP)": ["auto", "auto"]
        }
        
        self.setup_ui()

    def center_window(self, width, height):
    
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = int((screen_width / 2) - (width / 2))
        # Center - Up
        y = int((screen_height / 2) - (height / 2) - 50)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def setup_ui(self):
        main_container = ctk.CTkFrame(self.root, fg_color=self.colors['app_bg']) 
        main_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # --- Header ---
        header_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        header_frame.pack(fill='x', pady=(0, 25))
        
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
            # Version
            text="v2.1 | Developed by Mehrshad Asgary | ",
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
        contact_link.pack(side=ctk.LEFT)
        # Contact me
        contact_link.bind("<Button-1>", lambda e: self.open_link("https://mehrshadasgary.ir"))
        
        subtitle_label = ctk.CTkLabel(
            header_frame,
            text="Fast & Easy DNS Configuration for Iran",
            font=self.font_subtitle,
            text_color=self.colors['text_secondary']
        )
        subtitle_label.pack()
        
        # --- DNS grade ---
        dns_section_frame = ctk.CTkFrame(main_container, fg_color=self.colors['frame_bg'], corner_radius=10)
        dns_section_frame.pack(fill='x', pady=(0, 25), ipady=10)

        section_title = ctk.CTkLabel(
            dns_section_frame,
            text="Select DNS Provider:",
            font=self.font_section_title,
            text_color=self.colors['text_primary']
        )
        section_title.pack(anchor='w', pady=(10, 15), padx=15)
        
        dns_grid = ctk.CTkFrame(dns_section_frame, fg_color="transparent")
        dns_grid.pack(fill='x', padx=15, pady=(0,10))
        
        for i in range(3):
            dns_grid.columnconfigure(i, weight=1, minsize=180)
        
        self.create_dns_buttons(dns_grid)
        
        # --- Control ---
        control_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        control_frame.pack(fill='x', pady=(0, 15))
        
        current_dns_btn = ctk.CTkButton(
            control_frame,
            text="Show Current DNS",
            font=self.font_button_main,
            fg_color=self.colors['secondary_accent_gray'],
            hover_color=self.colors['secondary_accent_gray_hover'],
            text_color=self.colors['text_primary'],
            command=self.show_current_dns,
            height=40,
            width=200,
            corner_radius=8
        )
        current_dns_btn.pack()
        
        # --- Status ---
        status_frame = ctk.CTkFrame(main_container, fg_color="transparent") 
        status_frame.pack(fill='x', pady=(0, 10))
        
        self.status_label = ctk.CTkLabel(
            status_frame,
            text="Ready to change DNS",
            font=self.font_status_label,
            text_color=self.colors['success']
        )
        self.status_label.pack()

    def create_dns_buttons(self, parent_frame):
        iranian_dns_color = self.colors['primary_accent_main_red']
        foreign_dns_color = self.colors['dns_foreign_purple']
        auto_dns_color = self.colors['dns_auto']

        dns_button_colors_map = {
            "Shecan": iranian_dns_color,
            "Radar": iranian_dns_color,
            "Electro": iranian_dns_color,
            "Begzar": iranian_dns_color,
            "403": iranian_dns_color,
            "Google": foreign_dns_color,
            "Cloudflare": foreign_dns_color,
            "Auto (DHCP)": auto_dns_color
        }

        row, col = 0, 0
        button_height = 70

        for i, (dns_name, dns_values) in enumerate(self.dns_servers.items()):
            base_color = dns_button_colors_map.get(dns_name, self.colors['primary_accent_main_red'])
            
            if dns_name == "Auto (DHCP)":
                 hover_color = self.colors['secondary_accent_gray_hover']
            else:
                hover_color = self.lighten_hex_color(base_color, 0.15)

            button_text = f"{dns_name}\n"
            if dns_values[0] != "auto":
                button_text += f"{dns_values[0]} | {dns_values[1]}"
            else:
                button_text += "Automatic Configuration"

            btn = ctk.CTkButton(
                parent_frame,
                text=button_text,
                font=self.font_dns_button_name, 
                fg_color=base_color,
                hover_color=hover_color,
                text_color=self.colors['text_primary'],
                command=lambda name=dns_name: self.change_dns(name),
                height=button_height,
                corner_radius=8,
            )
            btn.grid(row=row, column=col, padx=5, pady=5, sticky='ew')
            
            col += 1
            if col > 2:
                col = 0
                row += 1
        
        total_buttons = len(self.dns_servers)
        if total_buttons % 3 != 0:
            remaining_cols = 3 - (total_buttons % 3)
            for i in range(remaining_cols):
                empty_frame = ctk.CTkFrame(parent_frame, fg_color="transparent", width=10, height=10)
                empty_frame.grid(row=row, column=col + i, padx=5, pady=5, sticky='ew')

    def lighten_hex_color(self, hex_color, factor=0.2):
        if not hex_color.startswith('#'): return hex_color
        
        hex_color = hex_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
        new_rgb = []
        for val in rgb:
            new_val = int(val + (255 - val) * factor)
            new_rgb.append(min(255, max(0, new_val)))
            
        return '#{:02x}{:02x}{:02x}'.format(*new_rgb)

    def open_link(self, url):
        try:
            webbrowser.open_new(url)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open link:\n{str(e)}")

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
            messagebox.showerror("Error", "Failed to run as administrator")
    
    def get_network_interface(self):
        
        #  netsh interface ip show config
        try:
            # fibd Gateway
            cmd = 'netsh interface ip show config'
            cli_encoding = 'oem' 
            
            try:
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding=cli_encoding, errors='ignore', timeout=10)
            except UnicodeDecodeError:
                # if error
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding='latin-1', errors='ignore', timeout=10)

            if result.returncode == 0 and result.stdout:
                interface_configs = result.stdout.strip().split('\n\n')
                
                for config in interface_configs:
                    # Default Gateway
                    if 'Default Gateway' in config and '127.0.0.1' not in config:
                        gateway_line = [line for line in config.split('\n') if 'Default Gateway' in line]
                        if gateway_line:
                            gateway_ip = gateway_line[0].split(':')[-1].strip()
                            if gateway_ip and gateway_ip != '0.0.0.0':
                                match = re.search(r'Configuration for interface "(.+?)"', config)
                                if match:
                                    interface_name = match.group(1)
                                    print(f"Found active interface: '{interface_name}' with gateway {gateway_ip}")
                                    return interface_name

            # Error message if no active network card is found
            print("Warning: Could not determine active network interface with a gateway.")
            messagebox.showwarning("Network Interface",
                                    "Could not automatically determine the active network interface.\n"
                                    "Please ensure you are connected to the internet.")
            return None

        except subprocess.TimeoutExpired:
            print("Error: The command to find network interfaces timed out.")
            messagebox.showerror("Error", "The command to find network interfaces timed out. Please try again.")
            return None
        except Exception as e:
            print(f"Error getting network interface: {e}.")
            messagebox.showerror("Network Interface Error", f"An unexpected error occurred while detecting the network interface: {e}")
            return None
    
    def change_dns(self, dns_name):
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
                # The get_network_interface function now shows its own detailed error message.
                # So we can just update the status label and return.
                self.status_label.configure(text="✗ Error: No active network interface found", text_color=self.colors['error'])
                return

            dns_servers_list = self.dns_servers[dns_name]
            
            self.status_label.configure(
                text=f"Changing to {dns_name} for '{interface_name}'...",
                text_color=self.colors['warning']
            )
            self.root.update_idletasks()
            
            cli_encoding = 'oem'

            if dns_servers_list[0] == "auto":
                cmd_clear_static = f'netsh interface ipv4 delete dnsserver "{interface_name}" all'
                cmd_set_dhcp = f'netsh interface ip set dns name="{interface_name}" source=dhcp'
                
                subprocess.run(cmd_clear_static, shell=True, check=False, capture_output=True, text=True, encoding=cli_encoding, errors='ignore')
                subprocess.run(cmd_set_dhcp, shell=True, check=True, capture_output=True, text=True, encoding=cli_encoding, errors='ignore')
                
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
                secondary_dns = dns_servers_list[1]

                cmd_set_primary = f'netsh interface ip set dns name="{interface_name}" static {primary_dns}'
                cmd_add_secondary = f'netsh interface ip add dns name="{interface_name}" addr={secondary_dns} index=2'
                cmd_flush_dns = 'ipconfig /flushdns'
                
                subprocess.run(cmd_set_primary, shell=True, check=True, capture_output=True, text=True, encoding=cli_encoding, errors='ignore')
                subprocess.run(cmd_add_secondary, shell=True, check=True, capture_output=True, text=True, encoding=cli_encoding, errors='ignore')
                subprocess.run(cmd_flush_dns, shell=True, check=False, capture_output=True, text=True, encoding=cli_encoding, errors='ignore')
                
                self.status_label.configure(
                    text=f"✓ DNS for '{interface_name}' changed to {dns_name}", 
                    text_color=self.colors['success']
                )
                messagebox.showinfo(
                    "Success", 
                    f"DNS successfully changed to {dns_name} for interface '{interface_name}'\n\nPrimary: {primary_dns}\nSecondary: {secondary_dns}"
                )
                
        except subprocess.CalledProcessError as e:
            error_details = f"Command:\n{e.cmd}\n\nReturn Code: {e.returncode}\n\nSTDOUT:\n{e.stdout}\n\nSTDERR:\n{e.stderr}"
            full_error_message = f"A command failed to execute properly.\n\n{error_details}"
            messagebox.showerror("Command Execution Error", full_error_message)
            self.status_label.configure(text="✗ Error changing DNS (command failed)", text_color=self.colors['error'])
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred during DNS change:\n{str(e)}")
            self.status_label.configure(text="✗ Unexpected error during DNS change", text_color=self.colors['error'])
    
    def show_current_dns(self):
        try:
            interface_name = self.get_network_interface()
            if not interface_name:
                 # Error is already shown by get_network_interface
                 return

            cmd = f'netsh interface ip show dns name="{interface_name}"'
            cli_encoding = 'oem'
            try:
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding=cli_encoding, errors='ignore', timeout=5)
            except UnicodeDecodeError:
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding='latin-1', errors='ignore', timeout=5)
            except subprocess.TimeoutExpired:
                messagebox.showerror("Timeout", f"Command to show DNS for '{interface_name}' timed out.")
                return

            dns_info = f"Current DNS Servers for '{interface_name}':\n\n"
            lines = result.stdout.split('\n')
            
            dns_servers_found = []
            for line in lines:
                stripped_line = line.strip()
                # A more robust check for DNS server lines
                if "Statically Configured DNS Servers" in line or "DNS servers configured through DHCP" in line:
                    continue # Skip header lines
                
                # Check if the line seems to contain an IP address
                parts = stripped_line.split()
                if len(parts) > 0 and (parts[-1].count('.') == 3 or ':' in parts[-1]):
                     # Avoid other config lines that might end in an IP-like string
                     if not any(x in stripped_line.lower() for x in ['configuration for interface', 'dhcp enabled', 'register with suffix']):
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
        messagebox.showerror("Compatibility Error", "This application is designed for Windows only.")
        sys.exit(1)
    
    app = IranDNSSwitcher()
    app.run()
