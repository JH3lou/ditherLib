import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import customtkinter as ctk
from customtkinter import CTkImage
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np
from ditherlib.config import get_ditherer

class DitherApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("DitherLib GUI")
        self.geometry("1200x900")
        self.grid_columnconfigure(1, weight=1)

        self.image_path = None
        self.original_image_array = None
        self.processed_image_array = None
        self.live_preview_enabled = True

        self._build_sidebar()
        self._build_preview_panel()

    def _build_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=300)
        self.sidebar.grid(row=0, column=0, sticky="ns", padx=10, pady=10)

        self.load_btn = ctk.CTkButton(self.sidebar, text="Load Image", command=self.load_image)
        self.load_btn.pack(pady=(10, 5), padx=10)

        self.save_btn = ctk.CTkButton(self.sidebar, text="Save Image", command=self.save_image)
        self.save_btn.pack(pady=(0, 20), padx=10)

        ctk.CTkLabel(self.sidebar, text="Algorithm:").pack()
        self.algo_var = ctk.StringVar(value="adaptive")
        self.algo_menu = ctk.CTkOptionMenu(
            self.sidebar,
            variable=self.algo_var,
            values=[
                "floyd-steinberg", "burkes", "stucki",
                "sierra-3", "sierra-2", "sierra-lite",
                "atkinson", "adaptive"
            ],
            command=lambda val: self._maybe_process()
        )
        self.algo_menu.pack(padx=10, pady=5)

        ctk.CTkLabel(self.sidebar, text="Threshold").pack()
        self.threshold = ctk.IntVar(value=128)
        self.threshold_slider = ctk.CTkSlider(
            self.sidebar, from_=0, to=255, variable=self.threshold,
            command=lambda val: self._maybe_process()
        )
        self.threshold_slider.pack(padx=10, pady=5)

        ctk.CTkLabel(self.sidebar, text="Gamma").pack()
        self.gamma = ctk.DoubleVar(value=1.0)
        self.gamma_slider = ctk.CTkSlider(
            self.sidebar, from_=0.1, to=3.0, variable=self.gamma,
            command=lambda val: self._maybe_process()
        )
        self.gamma_slider.pack(padx=10, pady=5)

        ctk.CTkLabel(self.sidebar, text="Downscale %").pack()
        self.downscale = ctk.IntVar(value=100)
        self.downscale_slider = ctk.CTkSlider(
            self.sidebar, from_=25, to=100, variable=self.downscale,
            command=lambda val: self._maybe_process()
        )
        self.downscale_slider.pack(padx=10, pady=5)

        self.serpentine_var = ctk.BooleanVar(value=True)
        self.serpentine_switch = ctk.CTkSwitch(
            self.sidebar, text="Serpentine Scan", variable=self.serpentine_var,
            command=self._maybe_process
        )
        self.serpentine_switch.pack(pady=5)

        self.live_preview_var = ctk.BooleanVar(value=True)
        self.live_toggle = ctk.CTkSwitch(
            self.sidebar, text="Live Preview", variable=self.live_preview_var
        )
        self.live_toggle.pack(pady=(0, 10))

        self.apply_btn = ctk.CTkButton(self.sidebar, text="Apply Dither", command=self.process_and_preview)
        self.apply_btn.pack(pady=5, padx=10)

        self.status_label = ctk.CTkLabel(self.sidebar, text="Status: Idle")
        self.status_label.pack(pady=10)

    def _build_preview_panel(self):
        self.preview_frame = ctk.CTkFrame(self)
        self.preview_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.preview_frame.grid_rowconfigure(0, weight=1)
        self.preview_frame.grid_columnconfigure(0, weight=1)
        self.image_label = ctk.CTkLabel(self.preview_frame, text="No image loaded", fg_color="transparent")
        self.image_label.grid(row=0, column=0, sticky="nsew")
        self.loading_overlay = ctk.CTkFrame(self.preview_frame, corner_radius=0, fg_color="black", width=800, height=800)
        self.loading_label = ctk.CTkLabel(self.loading_overlay, text="Processing...", font=("Arial", 18))
        self.loading_label.place(relx=0.5, rely=0.5, anchor="center")
        self.loading_overlay.grid(row=0, column=0, sticky="nsew")
        self.loading_overlay.lower()  # Start hidden

    def load_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.bmp *.tiff *.webp"),
                ("All files", "*.*"),
            ]
        )
        if file_path:
            try:
                img = Image.open(file_path)
                img = img.convert("L")
                self.image_path = file_path
                self.original_image_array = np.array(img)
                self.status_label.configure(text=f"Loaded: {os.path.basename(file_path)}")
                self.process_and_preview()
            except Exception as e:
                self.status_label.configure(text=f"Failed to load: {e}")

    def save_image(self):
        if self.processed_image_array is not None:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png")]
            )
            if file_path:
                try:
                    Image.fromarray(self.processed_image_array).save(file_path)
                    self.status_label.configure(text=f"Saved to {os.path.basename(file_path)}")
                except Exception as e:
                    self.status_label.configure(text=f"Save failed: {e}")

    def _maybe_process(self, *args):
        if self.live_preview_var.get():
            self.process_and_preview()


    def process_and_preview(self):
        if self.original_image_array is None:
            return

        self.loading_overlay.lift()  # Show loading overlay
        self.status_label.configure(text="Processing...")
        self.update()  # Force redraw before starting work

        # Schedule the heavy lifting after the UI has had time to update
        self.after(50, self._run_dither_process)

    def _run_dither_process(self):
        algo = self.algo_var.get()
        try:
            ditherer = get_ditherer(
                algo,
                threshold=self.threshold.get(),
                serpentine=self.serpentine_var.get()
            )
            img = Image.fromarray(self.original_image_array)
            result_img = ditherer.dither(img)
            self.processed_image_array = np.array(result_img)
            self.display_image(self.processed_image_array)
            self.status_label.configure(text=f"Dithered using {algo}")
        except Exception as e:
            self.status_label.configure(text=f"Error: {e}")
        finally:
            self.loading_overlay.lower()  # Hide overlay no matter what




    def display_image(self, img_array):
        try:
            img = Image.fromarray(img_array)
            img.thumbnail((800, 800))
            ctk_img = CTkImage(light_image=img, size=img.size)
            self.image_label.configure(image=ctk_img, text="")
            self.image_label.image = ctk_img  # Keep a reference
        except Exception as e:
            self.status_label.configure(text=f"Display error: {e}")

    

if __name__ == "__main__":
    app = DitherApp()
    app.mainloop()