import threading

import gi
from serial.rfc2217 import Serial

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib
from matplotlib.backends.backend_gtk3agg import \
    FigureCanvasGTK3Agg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
import random

from SerialHandler import SerialHandler, SerialCallback

class MeasurementPage(Gtk.Box):
    def __init__(self):
        super().__init__()

        page_hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        self.add(page_hbox)

        listbox = Gtk.ListBox()
        listbox.set_selection_mode(Gtk.SelectionMode.NONE)
        page_hbox.add(listbox)

        self.bins = [0] * 4096

        fig = Figure(figsize=(5, 4), dpi=100)
        self.ax = fig.add_subplot()
        self.ax.set_ylim([0, 1])
        self.t = list(range(len(self.bins)))
        self.plot = self.ax.plot(self.t, self.bins)[0]

        self.max = 1

        self.canvas = FigureCanvas(fig)
        self.canvas.set_hexpand(True)
        self.canvas.set_vexpand(True)

        page_hbox.add(self.canvas)

        self.data_lock = threading.Lock()
        SerialHandler.add_callback(SerialCallback(b"R2:", self.serial_callback))

        GLib.timeout_add(300, self.redraw_chart)

    def redraw_chart(self):
        with self.data_lock:
            self.plot.set_ydata(self.bins)
        #self.ax.relim()
        # self.ax.autoscale_view()
        self.canvas.draw()
        return True

    def serial_callback(self, line, serial):
        print(line)
        val = int(line[3:])
        self.bins[val] += 1
        if self.bins[val] > self.max:
            self.max = self.bins[val]
            self.ax.set_ylim([0,self.max+1])



