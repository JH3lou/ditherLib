import customtkinter as ctk
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# Dummy image processing functions for demonstration.
def process_image_with_threshold(image_array, threshold):
    processed = np.where(image_array > threshold, 255, 0)
    return processed

def process_image_with_rgb_clipping(image, low_clip, high_clip):
    clipped = np.clip(image, low_clip, high_clip)
    return clipped

def process_image_with_gamma(image_array, gamma):
    corrected = 255 * ((image_array / 255) ** (1 / gamma))
    return np.clip(corrected, 0, 255)

class AdvancedHistogramControl(ctk.CTkFrame):
    def __init__(self, parent, update_callback, image_array, rgb_image_array):
        """
        :param parent: parent widget
        :param update_callback: a callback function that takes current advanced parameter settings
               and updates the main image preview.
        :param image_array: grayscale image data (numpy array)
        :param rgb_image_array: color (RGB) image data (numpy array)
        """
        super().__init__(parent)
        self.update_callback = update_callback
        self.image_array = image_array
        self.rgb_image_array = rgb_image_array

        # Create a Tabview inside this frame.
        self.tabview = ctk.CTkTabview(self, width=800, height=250)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)
        # Add tabs:
        self.tabview.add("Luminance")
        self.tabview.add("RGB")
        self.tabview.add("Clipping & Gamma")

        self._setup_luminance_tab()
        self._setup_rgb_tab()
        self._setup_clipping_gamma_tab()

    def _setup_luminance_tab(self):
        tab = self.tabview.tab("Luminance")
        self.fig_lum, self.ax_lum = plt.subplots(figsize=(5, 2), dpi=100)
        self.canvas_lum = FigureCanvasTkAgg(self.fig_lum, master=tab)
        self.canvas_lum.get_tk_widget().pack(side="top", fill="both", expand=True)
        self.hist_lum, self.bins_lum = np.histogram(self.image_array, bins=256, range=(0, 255))
        self.ax_lum.clear()
        self.ax_lum.fill_between(np.arange(256), self.hist_lum, color='gray')
        self.ax_lum.set_xlim(0, 255)
        self.ax_lum.set_title("Luminance Histogram")
        self.lum_threshold = 128
        self.threshold_line = self.ax_lum.axvline(self.lum_threshold, color='red', linewidth=2)
        self.canvas_lum.draw()
        self.lum_thresh_slider = ctk.CTkSlider(tab, from_=0, to=255, number_of_steps=255,
                                               command=self._on_lum_thresh_change)
        self.lum_thresh_slider.set(self.lum_threshold)
        self.lum_thresh_slider.pack(padx=10, pady=(5, 10))

    def _on_lum_thresh_change(self, value):
        self.lum_threshold = float(value)
        self.threshold_line.set_xdata([self.lum_threshold, self.lum_threshold])
        self.canvas_lum.draw_idle()
        self.update_callback(threshold=self.lum_threshold)

    def _setup_rgb_tab(self):
        tab = self.tabview.tab("RGB")
        self.fig_rgb, self.ax_rgb = plt.subplots(figsize=(5, 2), dpi=100)
        self.canvas_rgb = FigureCanvasTkAgg(self.fig_rgb, master=tab)
        self.canvas_rgb.get_tk_widget().pack(side="top", fill="both", expand=True)
        r = self.rgb_image_array[:, :, 0].flatten()
        g = self.rgb_image_array[:, :, 1].flatten()
        b = self.rgb_image_array[:, :, 2].flatten()
        self.hist_r, _ = np.histogram(r, bins=256, range=(0, 255))
        self.hist_g, _ = np.histogram(g, bins=256, range=(0, 255))
        self.hist_b, _ = np.histogram(b, bins=256, range=(0, 255))
        self.ax_rgb.clear()
        self.ax_rgb.fill_between(np.arange(256), self.hist_r, color='red', alpha=0.5, label="Red")
        self.ax_rgb.fill_between(np.arange(256), self.hist_g, color='green', alpha=0.5, label="Green")
        self.ax_rgb.fill_between(np.arange(256), self.hist_b, color='blue', alpha=0.5, label="Blue")
        self.ax_rgb.set_xlim(0, 255)
        self.ax_rgb.set_title("RGB Histograms")
        self.ax_rgb.legend()
        self.canvas_rgb.draw()

    def _setup_clipping_gamma_tab(self):
        tab = self.tabview.tab("Clipping & Gamma")
        self.fig_clip, self.ax_clip = plt.subplots(figsize=(5, 2), dpi=100)
        self.canvas_clip = FigureCanvasTkAgg(self.fig_clip, master=tab)
        self.canvas_clip.get_tk_widget().pack(side="top", fill="both", expand=True)
        self.hist_clip, self.bins_clip = np.histogram(self.image_array, bins=256, range=(0, 255))
        self.ax_clip.clear()
        self.ax_clip.fill_between(np.arange(256), self.hist_clip, color='gray')
        self.ax_clip.set_xlim(0, 255)
        self.ax_clip.set_title("Clipping & Gamma Histogram")
        self.canvas_clip.draw()
        slider_frame = ctk.CTkFrame(tab)
        slider_frame.pack(pady=10, padx=10, fill="x")
        ctk.CTkLabel(slider_frame, text="Black Point").grid(row=0, column=0, padx=5, pady=5)
        self.black_point = ctk.IntVar(value=0)
        self.black_slider = ctk.CTkSlider(slider_frame, variable=self.black_point,
                                          from_=0, to=127, command=self._on_clipping_change)
        self.black_slider.grid(row=0, column=1, padx=5, pady=5)
        ctk.CTkLabel(slider_frame, text="White Point").grid(row=1, column=0, padx=5, pady=5)
        self.white_point = ctk.IntVar(value=255)
        self.white_slider = ctk.CTkSlider(slider_frame, variable=self.white_point,
                                          from_=128, to=255, command=self._on_clipping_change)
        self.white_slider.grid(row=1, column=1, padx=5, pady=5)
        ctk.CTkLabel(slider_frame, text="Gamma").grid(row=2, column=0, padx=5, pady=5)
        self.gamma_adv = ctk.DoubleVar(value=1.0)
        self.gamma_adv_slider = ctk.CTkSlider(slider_frame, variable=self.gamma_adv,
                                              from_=0.1, to=3.0, command=self._on_clipping_change)
        self.gamma_adv_slider.grid(row=2, column=1, padx=5, pady=5)

    def _on_clipping_change(self, value):
        low = self.black_point.get()
        high = self.white_point.get()
        gamma_val = self.gamma_adv.get()
        self.update_callback(low_clip=low, high_clip=high, gamma=gamma_val)
        self.ax_clip.set_title(f"Clip: {low} / {high}, Gamma: {gamma_val:.2f}")
        self.canvas_clip.draw_idle()

class DitherApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("DitherLib GUI with Advanced Histogram Controls")
        self.geometry("1200x900")
        self.grid_columnconfigure(1, weight=1)
        self.create_sidebar()
        self.create_preview_panel()
        
        # Initialize dummy image arrays for demonstration before creating advanced controls.
        self.original_image_array = (np.random.rand(300, 400) * 255).astype(np.uint8)
        self.rgb_image_array = np.stack([
            (np.random.rand(300, 400) * 255).astype(np.uint8),
            (np.random.rand(300, 400) * 255).astype(np.uint8),
            (np.random.rand(300, 400) * 255).astype(np.uint8)
        ], axis=-1)
        
        self.create_advanced_controls()
        self.update_preview(self.original_image_array)
    
    def create_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=300)
        self.sidebar.grid(row=0, column=0, sticky="ns", padx=10, pady=10)
        
        self.load_btn = ctk.CTkButton(self.sidebar, text="Load Image", command=self.load_image)
        self.load_btn.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.save_btn = ctk.CTkButton(self.sidebar, text="Save Output", command=self.save_image)
        self.save_btn.grid(row=0, column=1, padx=20, pady=(20, 10))
        
        ctk.CTkLabel(self.sidebar, text="Algorithm").grid(row=1, column=0, columnspan=2, padx=20, pady=(10, 0))
        self.algo_var = ctk.StringVar(value="FS")
        self.algo_menu = ctk.CTkOptionMenu(
            self.sidebar,
            variable=self.algo_var,
            values=["FS", "Burkes", "Stucki", "Sierra-3", "Two-row Sierra", "Sierra Lite", "Atkinson", "Ordered4x4", "BlueNoise", "Random"],
            width=250
        )
        self.algo_menu.grid(row=2, column=0, columnspan=2, padx=20, pady=(0, 10))
        
        ctk.CTkLabel(self.sidebar, text="Threshold").grid(row=3, column=0, padx=20, pady=(10, 0))
        self.thresh_var = ctk.IntVar(value=128)
        self.thresh_slider = ctk.CTkSlider(self.sidebar, variable=self.thresh_var, from_=0, to=255, width=250,
                                           command=self.basic_update_callback)
        self.thresh_slider.grid(row=4, column=0, columnspan=2, padx=20, pady=(0, 10))
        
        ctk.CTkLabel(self.sidebar, text="Gamma Correction").grid(row=5, column=0, padx=20, pady=(10, 0))
        self.gamma_var = ctk.DoubleVar(value=1.0)
        self.gamma_slider = ctk.CTkSlider(self.sidebar, variable=self.gamma_var, from_=0.1, to=3.0, width=250,
                                          command=self.basic_update_callback)
        self.gamma_slider.grid(row=6, column=0, columnspan=2, padx=20, pady=(0, 10))
        
        ctk.CTkLabel(self.sidebar, text="Downscale Factor (%)").grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scale_var = ctk.IntVar(value=100)
        self.scale_slider = ctk.CTkSlider(self.sidebar, variable=self.scale_var, from_=25, to=100, width=250)
        self.scale_slider.grid(row=8, column=0, columnspan=2, padx=20, pady=(0, 10))
        
        self.perf_mode = ctk.CTkSwitch(self.sidebar, text="Fast Mode")
        self.perf_mode.grid(row=9, column=0, columnspan=2, padx=20, pady=(10, 10))
        
        self.status_label = ctk.CTkLabel(self.sidebar, text="Status: Idle", fg_color="transparent")
        self.status_label.grid(row=10, column=0, columnspan=2, padx=20, pady=10)
    
    def create_preview_panel(self):
        self.preview_frame = ctk.CTkFrame(self)
        self.preview_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.preview_frame.grid_rowconfigure(0, weight=1)
        self.preview_frame.grid_columnconfigure(0, weight=1)
        self.image_label = ctk.CTkLabel(self.preview_frame, text="No image loaded", fg_color="transparent")
        self.image_label.grid(row=0, column=0, sticky="nsew")
    
    def create_advanced_controls(self):
        self.adv_controls_frame = ctk.CTkFrame(self)
        self.adv_controls_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10, pady=10)
        self.adv_controls_frame.grid_columnconfigure(0, weight=1)
        self.adv_hist_control = AdvancedHistogramControl(
            self.adv_controls_frame,
            update_callback=self.advanced_update_callback,
            image_array=self.original_image_array,
            rgb_image_array=self.rgb_image_array
        )
        self.adv_hist_control.pack(fill="both", expand=True)
    
    def basic_update_callback(self, value):
        thresh = self.thresh_var.get()
        gamma = self.gamma_var.get()
        self.status_label.configure(text=f"Basic: Thresh {thresh} Gamma {gamma:.2f}")
        processed = process_image_with_threshold(self.original_image_array, thresh)
        self.update_preview(processed)
    
    def advanced_update_callback(self, **kwargs):
        msg = ", ".join([f"{k}: {v}" for k, v in kwargs.items()])
        self.status_label.configure(text=f"Advanced: {msg}")
        thresh = kwargs.get("threshold", self.thresh_var.get())
        processed = process_image_with_threshold(self.original_image_array, thresh)
        self.update_preview(processed)
    
    def update_preview(self, img_array):
        if len(img_array.shape) == 2:
            mode = "L"
        else:
            mode = "RGB"
        pil_img = Image.fromarray(img_array.astype(np.uint8), mode=mode)
        max_dim = 500
        pil_img.thumbnail((max_dim, max_dim))
        tk_img = ImageTk.PhotoImage(pil_img)
        self.image_label.configure(image=tk_img, text="")
        self.image_label.image = tk_img
    
    def load_image(self):
        self.status_label.configure(text="Status: Load Button Pressed")
        self.update_preview(self.original_image_array)
    
    def save_image(self):
        self.status_label.configure(text="Status: Save Button Pressed")
    
if __name__ == "__main__":
    app = DitherApp()
    app.mainloop()
