import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import sys
import ctypes
import os
import webbrowser 

class IranDNSSwitcher:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Iran DNS Switcher v1.0")
        self.root.geometry("600x550")
        self.root.resizable(False, False)
        
        try:
            icon_path = os.path.join(os.path.dirname(__file__), "Logo-IranDnsSwitcher.ico")
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
            else:
                print(f"Warning: Icon file not found at {icon_path}")
        except tk.TclError as e:
            print(f"Error setting iconbitmap: {e}. This might happen on non-Windows systems or if the .ico file is invalid.")

        # Modern color scheme
        self.colors = {
            'bg': '#1e1e2e',
            'surface': '#313244',
            'primary': '#89b4fa',
            'secondary': '#a6e3a1',
            'accent': '#f38ba8',
            'text': '#cdd6f4',
            'text_dim': '#9399b2',
            'success': '#a6e3a1',
            'error': '#f38ba8',
            'warning': '#fab387'
        }
        
        self.root.configure(bg=self.colors['bg'])
        
        # DNS servers dictionary
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
        
    def setup_ui(self):
        # Main container
        main_container = tk.Frame(self.root, bg=self.colors['bg'])
        main_container.pack(fill='both', expand=True, padx=30, pady=20)
        
        # Header section
        header_frame = tk.Frame(main_container, bg=self.colors['bg'])
        header_frame.pack(fill='x', pady=(0, 30))
        
        # Title
        title_label = tk.Label(
            header_frame,
            text="Iran DNS Switcher",
            font=("Segoe UI", 24, "bold"),
            bg=self.colors['bg'],
            fg=self.colors['primary']
        )
        title_label.pack()
        
        # Version and Developer info in one line
        info_frame = tk.Frame(header_frame, bg=self.colors['bg'])
        info_frame.pack(pady=(5, 0))
        
        # Modified: Separating developer info and GitHub link for clickability
        dev_label = tk.Label(
            info_frame,
            text="v1.0 | Developed by Mehrshad | ", # Developer info
            font=("Segoe UI", 10),
            bg=self.colors['bg'],
            fg=self.colors['text_dim']
        )
        dev_label.pack(side=tk.LEFT) # Pack to the left
        
        # GitHub Link Label
        github_link = tk.Label(
            info_frame,
            text="github.com/mehrshadasgary", # GitHub URL
            font=("Segoe UI", 10, "underline"), # Underline for link appearance
            bg=self.colors['bg'],
            fg=self.colors['primary'], # A different color to indicate it's a link
            cursor="hand2" # Change cursor to hand when hovering
        )
        github_link.pack(side=tk.LEFT) # Pack to the left, next to the dev_label
        
        # Bind the click event to the GitHub link label
        # When clicked, it will call open_github_profile with your GitHub URL
        github_link.bind("<Button-1>", lambda e: self.open_github_profile("https://github.com/mehrshadasgary"))
        
        # Subtitle
        subtitle_label = tk.Label(
            header_frame,
            text="Fast & Easy DNS Configuration for Iran",
            font=("Segoe UI", 11),
            bg=self.colors['bg'],
            fg=self.colors['text_dim']
        )
        subtitle_label.pack(pady=(5, 0))
        
        # DNS Grid section
        dns_section = tk.Frame(main_container, bg=self.colors['bg'])
        dns_section.pack(fill='x', pady=(0, 20))
        
        # Section title
        section_title = tk.Label(
            dns_section,
            text="Select DNS Provider:",
            font=("Segoe UI", 12, "bold"),
            bg=self.colors['bg'],
            fg=self.colors['text']
        )
        section_title.pack(anchor='w', pady=(0, 15))
        
        # DNS buttons grid
        dns_grid = tk.Frame(dns_section, bg=self.colors['bg'])
        dns_grid.pack(fill='x')
        
        # Configure grid weights
        for i in range(3):
            dns_grid.columnconfigure(i, weight=1)
        
        # Create DNS buttons with modern styling
        self.create_dns_buttons(dns_grid)
        
        # Control section
        control_frame = tk.Frame(main_container, bg=self.colors['bg'])
        control_frame.pack(fill='x', pady=(20, 15))
        
        # Current DNS button
        current_dns_btn = tk.Button(
            control_frame,
            text="Show Current DNS",
            font=("Segoe UI", 10),
            bg=self.colors['surface'],
            fg=self.colors['text'],
            activebackground=self.colors['primary'],
            activeforeground=self.colors['bg'],
            relief='flat',
            bd=0,
            padx=20,
            pady=8,
            cursor='hand2',
            command=self.show_current_dns
        )
        current_dns_btn.pack()
        
        # Status section
        status_frame = tk.Frame(main_container, bg=self.colors['bg'])
        status_frame.pack(fill='x', pady=(10, 20))
        
        # Status label
        self.status_label = tk.Label(
            status_frame,
            text="Ready to change DNS",
            font=("Segoe UI", 10),
            bg=self.colors['bg'],
            fg=self.colors['success']
        )
        self.status_label.pack()
        
        # Footer (can be removed since info is now in header)
        footer_frame = tk.Frame(main_container, bg=self.colors['bg'])
        footer_frame.pack(fill='x', pady=(20, 0))
        
        # Just a simple line or empty space
        footer_spacer = tk.Label(
            footer_frame,
            text="",
            bg=self.colors['bg']
        )
        footer_spacer.pack()
        
    def create_dns_buttons(self, parent):
        """Create modern DNS buttons"""
        dns_colors = {
            "Shecan": "#e74c3c",
            "Radar": "#3498db", 
            "Electro": "#9b59b6",
            "Begzar": "#e67e22",
            "403": "#34495e",
            "Google": "#4285f4",
            "Cloudflare": "#f38020",
            "Auto (DHCP)": "#27ae60"
        }
        
        row = 0
        col = 0
        
        for dns_name, dns_values in self.dns_servers.items():
            # Create button frame for hover effects
            btn_frame = tk.Frame(parent, bg=self.colors['bg'])
            btn_frame.grid(row=row, column=col, padx=8, pady=8, sticky='ew')
            
            # DNS button
            color = dns_colors.get(dns_name, self.colors['primary'])
            
            btn = tk.Button(
                btn_frame,
                text=f"{dns_name}\n{dns_values[0]} | {dns_values[1]}" if dns_values[0] != "auto" else f"{dns_name}\nAutomatic Configuration",
                font=("Segoe UI", 9, "bold"),
                bg=color,
                fg='white',
                activebackground=self.lighten_color(color),
                activeforeground='white',
                relief='flat',
                bd=0,
                width=18,
                height=4,
                cursor='hand2',
                command=lambda name=dns_name: self.change_dns(name)
            )
            btn.pack(fill='both', expand=True)
            
            # Hover effects
            self.add_hover_effect(btn, color)
            
            col += 1
            if col > 2:
                col = 0
                row += 1
    
    def lighten_color(self, color):
        """Lighten a hex color"""
        color = color.lstrip('#')
        rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        rgb = tuple(min(255, int(c * 1.2)) for c in rgb)
        return '#{:02x}{:02x}{:02x}'.format(*rgb)
    
    def add_hover_effect(self, button, original_color):
        """Add hover effects to buttons"""
        hover_color = self.lighten_color(original_color)
        
        def on_enter(e):
            button.config(bg=hover_color)
        
        def on_leave(e):
            button.config(bg=original_color)
        
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)

    def open_github_profile(self, url):
        """Opens the given URL in the default web browser."""
        try:
            webbrowser.open_new(url)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open link:\n{str(e)}")
    
    def is_admin(self):
        """Check if running with admin privileges"""
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    
    def run_as_admin(self):
        """Run program with admin privileges"""
        try:
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, " ".join(sys.argv), None, 1
            )
        except:
            messagebox.showerror("Error", "Failed to run as administrator")
    
    def get_network_interface(self):
        """Get active network interface name"""
        try:
            cmd = 'netsh interface show interface'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding='utf-8')
            
            lines = result.stdout.split('\n')
            for line in lines:
                if 'Connected' in line and 'Dedicated' in line:
                    parts = line.split()
                    if len(parts) >= 4:
                        return ' '.join(parts[3:])
            
            # Fallback method
            cmd = 'wmic path win32_networkadapter where NetEnabled=true get NetConnectionID /value'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding='utf-8')
            
            for line in result.stdout.split('\n'):
                if line.startswith('NetConnectionID=') and line.strip() != 'NetConnectionID=':
                    return line.split('=')[1].strip()
            
            return "Wi-Fi"  # Default
            
        except Exception as e:
            return "Wi-Fi"  # Default fallback
    
    def change_dns(self, dns_name):
        """Change DNS settings"""
        if not self.is_admin():
            response = messagebox.askyesno(
                "Administrator Access Required",
                "This application needs administrator privileges to change DNS settings.\n\nWould you like to restart as administrator?"
            )
            if response:
                self.run_as_admin()
                self.root.quit()
            return
        
        try:
            interface_name = self.get_network_interface()
            dns_servers = self.dns_servers[dns_name]
            
            self.status_label.config(
                text=f"Changing to {dns_name}...", 
                fg=self.colors['warning']
            )
            self.root.update()
            
            if dns_servers[0] == "auto":
                # Set automatic DNS
                cmd1 = f'netsh interface ip set dns "{interface_name}" dhcp'
                subprocess.run(cmd1, shell=True, check=True)
                
                self.status_label.config(
                    text=f"✓ Successfully changed to Automatic DNS", 
                    fg=self.colors['success']
                )
                messagebox.showinfo(
                    "Success", 
                    f"DNS successfully changed to Automatic (DHCP)"
                )
            else:
                # Set manual DNS
                cmd1 = f'netsh interface ip set dns "{interface_name}" static {dns_servers[0]}'
                cmd2 = f'netsh interface ip add dns "{interface_name}" {dns_servers[1]} index=2'
                
                subprocess.run(cmd1, shell=True, check=True)
                subprocess.run(cmd2, shell=True, check=True)
                
                # Flush DNS cache
                subprocess.run('ipconfig /flushdns', shell=True)
                
                self.status_label.config(
                    text=f"✓ Successfully changed to {dns_name}", 
                    fg=self.colors['success']
                )
                messagebox.showinfo(
                    "Success", 
                    f"DNS successfully changed to {dns_name}\n\nPrimary: {dns_servers[0]}\nSecondary: {dns_servers[1]}"
                )
                
        except subprocess.CalledProcessError as e:
            self.status_label.config(
                text="✗ Error changing DNS", 
                fg=self.colors['error']
            )
            messagebox.showerror("Error", f"Failed to change DNS:\n{str(e)}")
        except Exception as e:
            self.status_label.config(
                text="✗ Unexpected error", 
                fg=self.colors['error']
            )
            messagebox.showerror("Error", f"Unexpected error:\n{str(e)}")
    
    def show_current_dns(self):
        """Show current DNS configuration"""
        try:
            interface_name = self.get_network_interface()
            cmd = f'netsh interface ip show config "{interface_name}"'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding='utf-8')
            
            dns_info = "Current DNS Configuration:\n\n"
            lines = result.stdout.split('\n')
            
            for line in lines:
                if 'DNS servers configured through DHCP' in line or 'Statically Configured DNS Servers' in line:
                    dns_info += line.strip() + "\n"
                elif line.strip() and (line.strip().replace('.', '').replace(':', '').isdigit() or 'None' in line):
                    if not any(x in line for x in ['Configuration', 'DHCP enabled', 'IP Address']):
                        dns_info += "    " + line.strip() + "\n"
            
            if len(dns_info.strip()) <= len("Current DNS Configuration:"):
                dns_info += "No DNS information found"
            
            messagebox.showinfo("Current DNS", dns_info)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to get DNS information:\n{str(e)}")
    
    def run(self):
        """Run the application"""
        self.root.mainloop()

if __name__ == "__main__":
    # Check Windows OS
    if os.name != 'nt':
        print("This application is designed for Windows only")
        sys.exit(1)
    
    app = IranDNSSwitcher()
    app.run()
