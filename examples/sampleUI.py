import customtkinter as ctk
from tkinter import filedialog
from PIL import Image, ImageTk

class DitherApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("DitherLib GUI")
        self.geometry("1200x800")
        self.grid_columnconfigure(1, weight=1)
        self.create_sidebar()
        self.create_preview_panel()
        
    def create_sidebar(self):
        # Sidebar frame with fixed width
        self.sidebar = ctk.CTkFrame(self, width=300)
        self.sidebar.grid(row=0, column=0, sticky="ns", padx=10, pady=10)
        
        # File I/O Buttons
        self.load_btn = ctk.CTkButton(self.sidebar, text="Load Image", command=self.load_image)
        self.load_btn.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.save_btn = ctk.CTkButton(self.sidebar, text="Save Output", command=self.save_image)
        self.save_btn.grid(row=0, column=1, padx=20, pady=(20, 10))
        
        # Algorithm Selection
        ctk.CTkLabel(self.sidebar, text="Algorithm").grid(row=1, column=0, columnspan=2, padx=20, pady=(10, 0))
        self.algo_var = ctk.StringVar(value="FS")
        self.algo_menu = ctk.CTkOptionMenu(
            self.sidebar,
            variable=self.algo_var,
            values=["FS", "Burkes", "Stucki", "Sierra-3", "Two-row Sierra", "Sierra Lite", "Atkinson", "Ordered4x4", "BlueNoise", "Random"],
            width=250
        )
        self.algo_menu.grid(row=2, column=0, columnspan=2, padx=20, pady=(0, 10))
        
        # Basic Parameters
        ctk.CTkLabel(self.sidebar, text="Threshold").grid(row=3, column=0, padx=20, pady=(10, 0))
        self.thresh_var = ctk.IntVar(value=128)
        self.thresh_slider = ctk.CTkSlider(self.sidebar, variable=self.thresh_var, from_=0, to=255, width=250)
        self.thresh_slider.grid(row=4, column=0, columnspan=2, padx=20, pady=(0, 10))
        
        ctk.CTkLabel(self.sidebar, text="Gamma Correction").grid(row=5, column=0, padx=20, pady=(10, 0))
        self.gamma_var = ctk.DoubleVar(value=1.0)
        self.gamma_slider = ctk.CTkSlider(self.sidebar, variable=self.gamma_var, from_=0.1, to=3.0, width=250)
        self.gamma_slider.grid(row=6, column=0, columnspan=2, padx=20, pady=(0, 10))
        
        ctk.CTkLabel(self.sidebar, text="Downscale Factor (%)").grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scale_var = ctk.IntVar(value=100)
        self.scale_slider = ctk.CTkSlider(self.sidebar, variable=self.scale_var, from_=25, to=100, width=250)
        self.scale_slider.grid(row=8, column=0, columnspan=2, padx=20, pady=(0, 10))
        
        # Performance Mode Toggle
        self.perf_mode = ctk.CTkSwitch(self.sidebar, text="Fast Mode")
        self.perf_mode.grid(row=9, column=0, columnspan=2, padx=20, pady=(10, 10))
        
        # Advanced Settings (Collapsible)
        self.adv_toggle = ctk.CTkButton(self.sidebar, text="Advanced Settings ▼", command=self.toggle_advanced)
        self.adv_toggle.grid(row=10, column=0, columnspan=2, padx=20, pady=(10, 0))
        self.adv_frame = ctk.CTkFrame(self.sidebar)
        # Example advanced control: Serpentine scanning option
        self.serpentine_chk = ctk.CTkCheckBox(self.adv_frame, text="Serpentine Scanning")
        self.serpentine_chk.grid(row=0, column=0, padx=20, pady=5)
        ctk.CTkLabel(self.adv_frame, text="Error Diffusion Factor (%)").grid(row=1, column=0, padx=20, pady=(10, 0))
        self.error_factor = ctk.CTkSlider(self.adv_frame, variable=ctk.DoubleVar(value=100), from_=50, to=100, width=200)
        self.error_factor.grid(row=2, column=0, padx=20, pady=(0, 10))
        self.adv_frame.grid_forget()  # Hide advanced settings initially
        
        # Process Button
        self.process_btn = ctk.CTkButton(self.sidebar, text="Apply Dither", command=self.apply_dither)
        self.process_btn.grid(row=11, column=0, columnspan=2, padx=20, pady=(20, 10))
        
        # Status Bar
        self.status_label = ctk.CTkLabel(self.sidebar, text="Status: Idle", fg_color="transparent")
        self.status_label.grid(row=12, column=0, columnspan=2, padx=20, pady=10)
    
    def create_preview_panel(self):
        # Preview panel for showing images
        self.preview_frame = ctk.CTkFrame(self)
        self.preview_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.preview_frame.grid_rowconfigure(0, weight=1)
        self.preview_frame.grid_columnconfigure(0, weight=1)
        
        self.image_label = ctk.CTkLabel(self.preview_frame, text="No image loaded", fg_color="transparent")
        self.image_label.grid(row=0, column=0, sticky="nsew")
    
    def toggle_advanced(self):
        # Toggle visibility of the advanced settings panel.
        if self.adv_frame.winfo_ismapped():
            self.adv_frame.grid_forget()
            self.adv_toggle.configure(text="Advanced Settings ▼")
        else:
            self.adv_frame.grid(row=11, column=0, columnspan=2, padx=20, pady=(0, 10))
            self.adv_toggle.configure(text="Advanced Settings ▲")
    
    def load_image(self):
        # Dummy functionality: simply update the status label.
        self.status_label.configure(text="Status: Load Button Pressed")
    
    def save_image(self):
        # Dummy functionality: simply update the status label.
        self.status_label.configure(text="Status: Save Button Pressed")
    
    def apply_dither(self):
        # Dummy functionality: simply update the status label.
        self.status_label.configure(text="Status: Apply Dither Button Pressed")
    
if __name__ == "__main__":
    app = DitherApp()
    app.mainloop()
