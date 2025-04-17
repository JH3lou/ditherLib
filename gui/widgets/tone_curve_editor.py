## gui/widgets/tone_curve_editor.py

import customtkinter as ctk
from tkinter import Canvas
import numpy as np


class ToneCurveEditor(ctk.CTkFrame):
    def __init__(self, master, width=256, height=200, **kwargs):
        super().__init__(master, **kwargs)
        self.width = width
        self.height = height
        self.lut = np.arange(256, dtype=np.uint8)  # Identity LUT
        self.hist_data = None

        self.canvas = Canvas(self, width=self.width, height=self.height, bg="white", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self._draw_curve()

    def _draw_curve(self):
        """Draws the tone curve and optionally a faint histogram background."""
        self.canvas.delete("curve")
        self.canvas.delete("hist")

        if self.hist_data is not None:
            hist_norm = self.hist_data / max(self.hist_data)
            for i, value in enumerate(hist_norm):
                x = i
                y = self.height
                bar_height = value * self.height
                self.canvas.create_line(x, y, x, y - bar_height, fill="#cccccc", tags="hist")

        for i in range(255):
            x0, y0 = i, self.height - (self.lut[i] / 255 * self.height)
            x1, y1 = i + 1, self.height - (self.lut[i + 1] / 255 * self.height)
            self.canvas.create_line(x0, y0, x1, y1, fill="black", width=2, tags="curve")

    def get_lut(self):
        return self.lut

    def update_with_histogram(self, image_array):
        """Overlay histogram background using a grayscale image array."""
        flat = image_array.flatten()
        self.hist_data, _ = np.histogram(flat, bins=256, range=(0, 255))
        self._draw_curve()
