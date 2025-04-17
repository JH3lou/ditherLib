## gui/widgets/tone_curve_editor.py

import customtkinter as ctk
from tkinter import Canvas
import numpy as np

class ToneCurveEditor(ctk.CTkFrame):
    def __init__(self, master, width=256, height=200, **kwargs):
        super().__init__(master, **kwargs)
        self.width = width
        self.height = height
        self.canvas = Canvas(self, width=self.width, height=self.height, bg="white", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # Control points for the curve (x in 0-255, y in 0-255)
        self.points = [(0, 255), (64, 192), (128, 128), (192, 64), (255, 0)]
        self.dragging_point = None

        self.lut = np.arange(256, dtype=np.uint8)
        self.hist_overlay = None
        self.hist_array = None

        self._redraw_editor()

        self.canvas.bind("<Button-1>", self._on_click)
        self.canvas.bind("<B1-Motion>", self._on_drag)
        self.canvas.bind("<ButtonRelease-1>", self._on_release)

    def _redraw_editor(self):
        self.canvas.delete("all")
        self._draw_histogram_background()
        self._draw_curve()
        self._draw_points()

    def _draw_histogram_background(self):
        if self.hist_array is None:
            return
        hist = self.hist_array / self.hist_array.max()
        for i, val in enumerate(hist):
            x = i
            y = self.height
            h = val * self.height
            self.canvas.create_line(x, y, x, y - h, fill="#cccccc")

    def _draw_curve(self):
        xs, ys = zip(*self.points)
        xs = np.array(xs)
        ys = np.array(ys)

        interp_x = np.arange(256)
        interp_y = np.interp(interp_x, xs, ys)
        self.lut = np.clip(255 - interp_y, 0, 255).astype(np.uint8)

        for i in range(255):
            x0, y0 = i, self.height - self.lut[i]
            x1, y1 = i + 1, self.height - self.lut[i + 1]
            self.canvas.create_line(x0, y0, x1, y1, fill="black", width=2, tags="curve")

    def _draw_points(self):
        for x, y in self.points:
            cx = x
            cy = self.height - y
            self.canvas.create_oval(cx - 4, cy - 4, cx + 4, cy + 4, fill="red", outline="black", tags="point")

    def _on_click(self, event):
        for i, (x, y) in enumerate(self.points):
            cx, cy = x, self.height - y
            if abs(event.x - cx) < 6 and abs(event.y - cy) < 6:
                self.dragging_point = i
                break

    def _on_drag(self, event):
        if self.dragging_point is None:
            return
        x = max(0, min(255, event.x))
        y = max(0, min(255, self.height - event.y))
        self.points[self.dragging_point] = (x, y)
        self._redraw_editor()

    def _on_release(self, event):
        self.dragging_point = None
        if hasattr(self, "on_curve_changed"):
            self.on_curve_changed()

    def get_lut(self):
        return self.lut

    def update_with_histogram(self, array):
        hist, _ = np.histogram(array.flatten(), bins=256, range=(0, 256))
        self.hist_array = hist
        self._redraw_editor()