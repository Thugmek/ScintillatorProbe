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

        self.data_lock = threading.Lock()

        page_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=50)
        self.add(page_vbox)

        self.decimation = 1
        self.bins = [0] * 4096
        self.bins_decimated = self.bins[:]

        fig = Figure(figsize=(5, 4), dpi=100)
        self.ax = fig.add_subplot()
        self.ax.set_ylim([0, 1])
        self.t = list(range(len(self.bins)))
        self.plot = self.ax.plot(self.t, self.bins)[0]
        fig.tight_layout()

        self.max = 1

        self.canvas = FigureCanvas(fig)
        self.canvas.set_hexpand(True)
        self.canvas.set_vexpand(True)

        fig.canvas.mpl_connect('motion_notify_event', self.update)

        page_vbox.add(self.canvas)

        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        page_vbox.add(hbox)

        lbl = Gtk.Label("Display decimation: ")
        hbox.add(lbl)
        name_store = Gtk.ListStore(int, str)
        name_store.append([1,'1x'])
        name_store.append([2, '2x'])
        name_store.append([4, '4x'])
        name_store.append([8, '8x'])
        name_store.append([16, '16x'])
        name_store.append([32, '32x'])
        name_store.append([64, '64x'])
        name_store.append([128, '128x'])
        name_store.append([256, '256x'])
        name_store.append([512, '512x'])
        combo = Gtk.ComboBox.new_with_model_and_entry(name_store)
        combo.connect("changed", self.update_decimation)
        combo.set_entry_text_column(1)
        combo.set_active(0)
        hbox.add(combo)

        SerialHandler.add_callback(SerialCallback(b"R2:", self.serial_callback))
        GLib.timeout_add(2000, self.redraw_chart)

    def update(self, event):
        if event.xdata is None:
            print('Drag mouse over axes for position')
        else:
            print(f'x,y=({event.xdata}, {event.ydata})')
            print(event)

    def update_decimation(self, combo):
        tree_iter = combo.get_active_iter()
        model = combo.get_model()
        decimation, name = model[tree_iter][:2]
        self.decimation = decimation
        self.redecimate()

    def redraw_chart(self):
        with self.data_lock:
            self.plot.set_ydata(self.bins_decimated)
            self.ax.set_ylim([0, self.max + 1])
        self.canvas.draw()
        return True

    def redecimate(self):
        with self.data_lock:
            l = int(len(self.bins) / self.decimation)
            self.bins_decimated = [0] * l
            self.max = 0
            for i, e in enumerate(self.bins):
                self.bins_decimated[int(i / self.decimation)] += e
                self.max = max(self.max, self.bins_decimated[int(i / self.decimation)])
            self.ax.set_xlim([0, l - 1])
            self.ax.set_ylim([0, self.max + 1])
            self.plot.set_xdata(list(range(l)))
            self.plot.set_ydata(self.bins_decimated)
        self.canvas.draw()

    def append_pulse(self, value):
        self.bins[value] += 1
        self.bins_decimated[int(value / self.decimation)] += 1
        self.max = max(self.max, self.bins_decimated[int(value / self.decimation)])

    def serial_callback(self, line, serial):
        print(line)
        val = int(line[3:])
        self.append_pulse(val)



