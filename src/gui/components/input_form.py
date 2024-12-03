"""Input form component for the GUI."""
import customtkinter as ctk
from typing import Callable, Dict, Any

class InputForm:
    def __init__(self, parent, on_submit: Callable[[Dict[str, Any]], None]):
        self.frame = ctk.CTkFrame(parent)
        self.frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)
        self.on_submit = on_submit
        
        # Configure grid columns to be responsive
        self.frame.grid_columnconfigure(1, weight=1)
        
        # Animation state
        self.animation_after_id = None
        
        self.create_widgets()
        self.running = False
        
    def create_widgets(self):
        # Container for smooth animations
        self.container = ctk.CTkFrame(self.frame, fg_color="transparent")
        self.container.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=10, pady=5)
        self.container.grid_columnconfigure(1, weight=1)
        
        # Keyword input
        self.keyword_label = ctk.CTkLabel(self.container, text="Search Keyword:")
        self.keyword_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.keyword_entry = ctk.CTkEntry(self.container)
        self.keyword_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
        
        # Target site input
        self.target_label = ctk.CTkLabel(self.container, text="Target Site URL:")
        self.target_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.target_entry = ctk.CTkEntry(self.container)
        self.target_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        
        # Number of bots
        self.bots_label = ctk.CTkLabel(self.container, text="Number of Bots:")
        self.bots_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.bots_slider = ctk.CTkSlider(self.container, from_=1, to=10, number_of_steps=9)
        self.bots_slider.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
        self.bots_slider.set(1)  # Set default value
        
        # Pages to visit on target site
        self.pages_label = ctk.CTkLabel(self.container, text="Pages to Visit:")
        self.pages_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.pages_slider = ctk.CTkSlider(self.container, from_=1, to=10, number_of_steps=9)
        self.pages_slider.grid(row=3, column=1, padx=10, pady=5, sticky="ew")
        self.pages_slider.set(3)  # Default value
        
        # Time on target site (seconds)
        self.time_label = ctk.CTkLabel(self.container, text="Time on Site (sec):")
        self.time_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.time_slider = ctk.CTkSlider(self.container, from_=10, to=60, number_of_steps=50)
        self.time_slider.grid(row=4, column=1, padx=10, pady=5, sticky="ew")
        self.time_slider.set(30)  # Default value
        
        # Visit competitors
        self.competitors_var = ctk.BooleanVar()
        self.competitors_check = ctk.CTkCheckBox(
            self.container,
            text="Visit Competitors",
            variable=self.competitors_var,
            command=self.toggle_competitors_input
        )
        self.competitors_check.grid(row=5, column=0, columnspan=2, padx=10, pady=5, sticky="w")
        
        # Number of competitors
        self.competitors_label = ctk.CTkLabel(self.container, text="Number of Competitors:")
        self.competitors_label.grid(row=6, column=0, padx=10, pady=5, sticky="w")
        self.competitors_combobox = ctk.CTkComboBox(
            self.container,
            values=[str(i) for i in range(1, 6)],
            state="disabled"
        )
        self.competitors_combobox.grid(row=6, column=1, padx=10, pady=5, sticky="ew")
        self.competitors_combobox.set("1")
        
        # Use France GPS
        self.gps_var = ctk.BooleanVar()
        self.gps_check = ctk.CTkCheckBox(
            self.container,
            text="Use France GPS",
            variable=self.gps_var
        )
        self.gps_check.grid(row=7, column=0, columnspan=2, padx=10, pady=5, sticky="w")
        
        # Google Domain selector
        self.domain_label = ctk.CTkLabel(self.container, text="Domaine Google:")
        self.domain_label.grid(row=8, column=0, padx=10, pady=5, sticky="w")
        self.domain_combobox = ctk.CTkComboBox(
            self.container,
            values=["google.fr", "google.de"],
            state="normal"
        )
        self.domain_combobox.grid(row=8, column=1, padx=10, pady=5, sticky="ew")
        self.domain_combobox.set("google.fr")
        
        # Use proxies
        self.proxies_var = ctk.BooleanVar()
        self.proxies_check = ctk.CTkCheckBox(
            self.container,
            text="Use Proxies",
            variable=self.proxies_var,
            command=self.toggle_proxy_input
        )
        self.proxies_check.grid(row=9, column=0, columnspan=2, padx=10, pady=5, sticky="w")
        
        # Proxy input
        self.proxy_label = ctk.CTkLabel(self.container, text="Proxy List (space separated):")
        self.proxy_label.grid(row=10, column=0, padx=10, pady=5, sticky="w")
        self.proxy_entry = ctk.CTkEntry(self.container)
        self.proxy_entry.grid(row=10, column=1, padx=10, pady=5, sticky="ew")
        self.proxy_entry.configure(state="disabled")
        
        # Submit button - Now in its own frame for better centering
        button_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        button_frame.grid(row=11, column=0, columnspan=2, pady=20, sticky="ew")
        button_frame.grid_columnconfigure(0, weight=1)  # Center the button
        
        # Buttons container for side-by-side layout
        buttons_container = ctk.CTkFrame(button_frame, fg_color="transparent")
        buttons_container.grid(row=0, column=0)
        
        self.submit_btn = ctk.CTkButton(
            buttons_container,
            text="Start Bots",
            command=self.submit,
            fg_color=["#2B87D3", "#1B77C3"],
            hover_color=["#1B77C3", "#0B67B3"],
            height=40,
            width=150,
            font=("Roboto", 14, "bold")
        )
        self.submit_btn.grid(row=0, column=0, padx=10)
        
        self.stop_btn = ctk.CTkButton(
            buttons_container,
            text="Stop Bots",
            command=self.stop_bots,
            fg_color=["#D32B2B", "#C31B1B"],
            hover_color=["#C31B1B", "#B30B0B"],
            height=40,
            width=150,
            font=("Roboto", 14, "bold"),
            state="disabled"
        )
        self.stop_btn.grid(row=0, column=1, padx=10)
        
    def toggle_proxy_input(self):
        """Enable/disable proxy input based on checkbox."""
        state = "normal" if self.proxies_var.get() else "disabled"
        self.proxy_entry.configure(state=state)

    def toggle_competitors_input(self):
        """Enable/disable competitors input based on checkbox."""
        state = "normal" if self.competitors_var.get() else "disabled"
        self.competitors_combobox.configure(state=state)
        
    def get_config(self) -> Dict[str, Any]:
        """Get configuration from form inputs."""
        config = {
            'keyword': self.keyword_entry.get(),
            'target_site': self.target_entry.get(),
            'bot_count': int(self.bots_slider.get()),
            'pages_to_visit': int(self.pages_slider.get()),
            'time_on_site': int(self.time_slider.get()),
            'use_france_gps': self.gps_var.get(),
            'use_proxies': self.proxies_var.get(),
            'google_domain': self.domain_combobox.get(),
            'visit_competitors': self.competitors_var.get(),
            'competitors_count': int(self.competitors_combobox.get()) if self.competitors_var.get() else 0
        }
        
        if config['use_proxies']:
            config['proxies'] = self.proxy_entry.get().split()
            
        return config
        
    def submit(self):
        """Validate and submit form data."""
        config = self.get_config()
        
        # Basic validation
        if not config['keyword']:
            self.show_error("Please enter a search keyword")
            return
            
        if not config['target_site']:
            self.show_error("Please enter a target site URL")
            return
            
        if config['use_proxies'] and not config['proxies']:
            self.show_error("Please enter proxy list or disable proxy usage")
            return
            
        self.running = True
        self.submit_btn.configure(state="disabled")
        self.stop_btn.configure(state="normal")
        self.start_loading_animation()
        self.on_submit(config)
        
    def stop_bots(self):
        """Stop running bots."""
        if self.running:
            self.running = False
            self.submit_btn.configure(state="normal")
            self.stop_btn.configure(state="disabled")
            self.stop_loading_animation()
            # Signal bot manager to stop
            if hasattr(self, 'on_stop'):
                self.on_stop()
                
    def start_loading_animation(self):
        """Start loading animation on buttons."""
        def animate():
            if self.running:
                current_text = self.submit_btn.cget("text")
                dots = current_text.count(".")
                new_text = "Running" + "." * ((dots + 1) % 4)
                self.submit_btn.configure(text=new_text)
                self.animation_after_id = self.frame.after(500, animate)
                
        animate()
        
    def stop_loading_animation(self):
        """Stop loading animation."""
        if self.animation_after_id:
            self.frame.after_cancel(self.animation_after_id)
            self.animation_after_id = None
        self.submit_btn.configure(text="Start Bots")
        
    def show_error(self, message: str):
        """Show error message."""
        ctk.CTkMessagebox(
            title="Error",
            message=message,
            icon="cancel"
        )

def create_input_form(parent, on_submit: Callable[[Dict[str, Any]], None]) -> InputForm:
    return InputForm(parent, on_submit)