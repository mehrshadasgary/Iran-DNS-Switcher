import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import sys
import ctypes
import os
import webbrowser # Import the webbrowser module

class IranDNSSwitcher:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Iran DNS Switcher v1.0")
        self.root.geometry("600x550")
        self.root.resizable(False, False)
        
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
            command=self.show_current_dns # This method will be implemented later
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
                activebackground=color, # Placeholder for active background before lighten_color
                activeforeground='white',
                relief='flat',
                bd=0,
                width=18,
                height=4,
                cursor='hand2',
                command=lambda name=dns_name: self.change_dns(name) # This method will be implemented later
            )
            btn.pack(fill='both', expand=True)
            
            # Hover effects will be added in a later commit
            # self.add_hover_effect(btn, color) 
            
            col += 1
            if col > 2:
                col = 0
                row += 1
    
    def open_github_profile(self, url):
        """Opens the given URL in the default web browser."""
        try:
            webbrowser.open_new(url)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open link:\n{str(e)}")

    # Placeholder methods for later commits
    def lighten_color(self, color):
        pass
    
    def add_hover_effect(self, button, original_color):
        pass
    
    def is_admin(self):
        pass
    
    def run_as_admin(self):
        pass
    
    def get_network_interface(self):
        pass
    
    def change_dns(self, dns_name):
        pass
    
    def show_current_dns(self):
        pass
    
    def run(self):
        pass

# Main execution block placeholder
if __name__ == "__main__":
    pass