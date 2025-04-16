# gui/widgets/histogram_viewer.py

import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np

class HistogramViewer(ctk.CTkFrame):
    def __init__(self, parent, width=400, height=200):
        super().__init__(parent)
        self.width = width
        self.height = height

        # Setup Matplotlib figure
        self.fig, self.ax = plt.subplots(figsize=(width/100, height/100), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill="both", expand=True)

    def update_histogram(self, image_array: np.ndarray):
        """Update histogram with a new grayscale image array."""
        if image_array.ndim != 2:
            raise ValueError("Expected a 2D grayscale image array.")

        self.ax.clear()
        hist, bins = np.histogram(image_array, bins=256, range=(0, 255))
        self.ax.fill_between(bins[:-1], hist, step="mid", color="gray", alpha=0.8)
        self.ax.set_xlim(0, 255)
        self.ax.set_title("Luminance Histogram")
        self.canvas.draw_idle()
