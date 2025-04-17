import sys
import os
import threading
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import customtkinter as ctk
from customtkinter import CTkImage
from tkinter import filedialog
from PIL import Image, ImageEnhance
import numpy as np
from ditherlib.config import get_ditherer
from gui.widgets.histogram_viewer import HistogramViewer
from gui.widgets.tone_curve_editor import ToneCurveEditor



class DitherApp(ctk.CTk):
    DEBOUNCE_DELAY_MS = 250

    def __init__(self):
        super().__init__()
        self.grid_rowconfigure(1, weight=1)
        self.title("DitherLib GUI")
        self.geometry("1200x900")
        self.grid_columnconfigure(1, weight=1)

        self.image_path = None
        self.original_image_array = None
        self.processed_image_array = None
        self.live_preview_enabled = True
        self._debounce_after_id = None

        self._build_sidebar()
        self._build_main_scroll_area()


    def _build_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=300) ##Non scrollable sidebar in mainwindow
        ## self.sidebar = ctk.CTkScrollableFrame(self, width=300) ##Scrollable sidebar in main window
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

        ctk.CTkLabel(self.sidebar, text="Brightness").pack()
        self.brightness = ctk.IntVar(value=0)
        self.brightness_slider = ctk.CTkSlider(
            self.sidebar, from_=-100, to=100, variable=self.brightness,
            command=lambda val: self._maybe_process()
        )
        self.brightness_slider.pack(padx=10, pady=5) ## Brightness Slider

        ctk.CTkLabel(self.sidebar, text="Contrast").pack()
        self.contrast = ctk.DoubleVar(value=1.0)
        self.contrast_slider = ctk.CTkSlider(
            self.sidebar, from_=0.5, to=2.0, variable=self.contrast,
            command=lambda val: self._maybe_process()
        )
        self.contrast_slider.pack(padx=10, pady=5) ## Contrast Slider

        ctk.CTkLabel(self.sidebar, text="Downscale %").pack()
        self.downscale = ctk.IntVar(value=100)
        self.downscale_slider = ctk.CTkSlider(
            self.sidebar, from_=25, to=100, variable=self.downscale,
            command=lambda val: self._maybe_process()
        )
        self.downscale_slider.pack(padx=10, pady=5) ## Downscale Slider

        self.serpentine_var = ctk.BooleanVar(value=True)
        self.serpentine_switch = ctk.CTkSwitch(
            self.sidebar, text="Serpentine Scan", variable=self.serpentine_var,
            command=self._maybe_process
        )
        self.serpentine_switch.pack(pady=5) ## Serpentine Toggle Switch

        self.live_preview_var = ctk.BooleanVar(value=True)
        self.live_toggle = ctk.CTkSwitch(
            self.sidebar, text="Live Preview", variable=self.live_preview_var
        )
        self.live_toggle.pack(pady=(0, 10))

        self.show_histogram_var = ctk.BooleanVar(value=True) ## Histogram Toggle
        self.histogram_toggle = ctk.CTkSwitch(
            self.sidebar,
            text="Show Histogram",
            variable=self.show_histogram_var,
            command=self._toggle_histogram
        )
        self.histogram_toggle.pack(pady=(0, 10))

        self.show_tone_curve_var = ctk.BooleanVar(value=True) ## Tone Curve Toggle
        self.tone_curve_toggle = ctk.CTkSwitch(
            self.sidebar,
            text="Show Tone Curve",
            variable=self.show_tone_curve_var,
            command=self._toggle_tone_curve
        )
        self.tone_curve_toggle.pack(pady=(0, 10))


        self.apply_btn = ctk.CTkButton(self.sidebar, text="Apply Dither", command=self.process_and_preview)
        self.apply_btn.pack(pady=5, padx=10)

        self.status_label = ctk.CTkLabel(self.sidebar, text="Status: Idle")
        self.status_label.pack(pady=10)

    def _build_main_scroll_area(self):
        self.scroll_area = ctk.CTkScrollableFrame(self)
        self.scroll_area.grid(row=0, column=1, rowspan=3, sticky="nsew", padx=10, pady=10)

        self._build_preview_panel()
        self._build_histogram_panel()
        self._build_tone_curve_panel()

    
    def _build_preview_panel(self):
        self.preview_frame = ctk.CTkFrame(self.scroll_area)
        self.preview_frame.pack(fill="both", expand=True, pady=(0, 10))
        self.preview_frame.grid_rowconfigure(0, weight=1)
        self.preview_frame.grid_columnconfigure(0, weight=1)
        self.image_label = ctk.CTkLabel(self.preview_frame, text="No image loaded", fg_color="transparent")
        self.image_label.grid(row=0, column=0, sticky="nsew")
        self.loading_overlay = ctk.CTkFrame(self.preview_frame, corner_radius=0, fg_color="black", width=800, height=800)
        self.loading_label = ctk.CTkLabel(self.loading_overlay, text="Processing...", font=("Arial", 18))
        self.loading_label.place(relx=0.5, rely=0.5, anchor="center")
        self.loading_overlay.grid(row=0, column=0, sticky="nsew")
        self.loading_overlay.lower()

    def _build_histogram_panel(self):
        self.histogram_frame = ctk.CTkFrame(self.scroll_area)
        self.histogram_frame.pack(fill="x", expand=True, pady=(0, 10))
        self.histogram_frame.grid_columnconfigure(0, weight=1)

        self.histogram_viewer = HistogramViewer(self.histogram_frame)
        self.histogram_viewer.pack(fill="both", expand=True)

        if not self.show_histogram_var.get():
            self.histogram_frame.grid_remove()

    def _toggle_histogram(self):
        if self.show_histogram_var.get():
            self.histogram_frame.pack(fill="x", expand=True, pady=(0, 10))
        else:
            self.histogram_frame.pack_forget()

    def _build_tone_curve_panel(self):
        self.tone_curve_frame = ctk.CTkFrame(self.scroll_area)
        self.tone_curve_frame.pack(fill="x", expand=True, pady=(0, 10))
        self.tone_curve_frame.grid_columnconfigure(0, weight=1)

        self.tone_curve_editor = ToneCurveEditor(self.tone_curve_frame)
        self.tone_curve_editor.pack(fill="both", expand=True)
        self.tone_curve_editor.on_curve_changed = self._maybe_process

    def _toggle_tone_curve(self):
        if self.show_tone_curve_var.get():
            self.tone_curve_frame.pack(fill="x", expand=True, pady=(0, 10))
        else:
            self.tone_curve_frame.pack_forget()

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[
            ("Image files", "*.png *.jpg *.jpeg *.bmp *.tiff *.webp"),
            ("All files", "*.*"),
        ])
        if file_path:
            try:
                img = Image.open(file_path).convert("L")
                self.image_path = file_path
                self.original_image_array = np.array(img)
                self.status_label.configure(text=f"Loaded: {os.path.basename(file_path)}")
                self.process_and_preview()
            except Exception as e:
                self.status_label.configure(text=f"Failed to load: {e}")

    def save_image(self):
        if self.processed_image_array is not None:
            file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
            if file_path:
                try:
                    Image.fromarray(self.processed_image_array).save(file_path)
                    self.status_label.configure(text=f"Saved to {os.path.basename(file_path)}")
                except Exception as e:
                    self.status_label.configure(text=f"Save failed: {e}")

    def _maybe_process(self, *args):
        if not self.live_preview_var.get():
            return

        if self._debounce_after_id:
            self.after_cancel(self._debounce_after_id)

        self._debounce_after_id = self.after(self.DEBOUNCE_DELAY_MS, self.process_and_preview)

    def _preprocess_image(self):
        img = Image.fromarray(self.original_image_array)

        if self.brightness.get() != 0:
            brightness_enhancer = ImageEnhance.Brightness(img)
            img = brightness_enhancer.enhance(1 + self.brightness.get() / 100)

        if self.contrast.get() != 1.0:
            contrast_enhancer = ImageEnhance.Contrast(img)
            img = contrast_enhancer.enhance(self.contrast.get())

        if hasattr(self, "tone_curve_editor"):
            lut = self.tone_curve_editor.get_lut()
            if lut is not None and isinstance(lut, np.ndarray) and lut.size == 256:
                img = img.point(lut.tolist())  # Apply LUT as tone curve

        return img

    def process_and_preview(self):
        if self.original_image_array is None:
            return

        self.loading_overlay.lift()
        self.status_label.configure(text="Processing...")
        self._disable_controls()
        self.update()

        thread = threading.Thread(target=self._run_dither_process_thread)
        thread.start()

    def _run_dither_process_thread(self):
        algo = self.algo_var.get()
        try:
            pre_img = self._preprocess_image()
            ditherer = get_ditherer(algo, threshold=self.threshold.get(), serpentine=self.serpentine_var.get())
            result_img = ditherer.dither(pre_img)
            self.processed_image_array = np.array(result_img)
            self.after(0, lambda: self._post_process_success(np.array(pre_img), np.array(result_img), algo))
        except Exception as e:
            self.after(0, lambda: self.status_label.configure(text=f"Error: {e}"))
        finally:
            self.after(0, self._finalize_processing)

    def _post_process_success(self, input_array, result_array, algo):
        self.display_image(result_array)
        if self.show_histogram_var.get():
            self.histogram_viewer.update_histogram(input_array)
        if self.show_tone_curve_var.get(): # Optionally refresh/redraw tone curve background to reflect histogram
            self.tone_curve_editor.update_with_histogram(input_array)

        self.status_label.configure(text=f"Dithered using {algo}")

    def _finalize_processing(self):
        self.loading_overlay.lower()
        self._enable_controls()

    def _disable_controls(self):
        for widget in [
            self.apply_btn, self.load_btn, self.save_btn, self.algo_menu,
            self.threshold_slider, self.gamma_slider, self.downscale_slider,
            self.brightness_slider, self.contrast_slider,
            self.serpentine_switch, self.live_toggle, self.histogram_toggle, self.tone_curve_toggle
        ]:
            widget.configure(state="disabled")

    def _enable_controls(self):
        for widget in [
            self.apply_btn, self.load_btn, self.save_btn, self.algo_menu,
            self.threshold_slider, self.gamma_slider, self.downscale_slider,
            self.brightness_slider, self.contrast_slider,
            self.serpentine_switch, self.live_toggle, self.histogram_toggle, self.tone_curve_toggle
        ]:
            widget.configure(state="normal")

    def display_image(self, img_array):
        try:
            img = Image.fromarray(img_array)
            img.thumbnail((800, 800))
            ctk_img = CTkImage(light_image=img, size=img.size)
            self.image_label.configure(image=ctk_img, text="")
            self.image_label.image = ctk_img
        except Exception as e:
            self.status_label.configure(text=f"Display error: {e}")

if __name__ == "__main__":
    app = DitherApp()
    app.mainloop()
