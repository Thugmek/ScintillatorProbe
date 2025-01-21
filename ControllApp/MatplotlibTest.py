import gi
from matplotlib.artist import Artist

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib

import numpy as np
import random
from matplotlib.backends.backend_gtk3agg import \
    FigureCanvasGTK3Agg as FigureCanvas
from matplotlib.figure import Figure

DATA_LEN = 1000
data = [0]*DATA_LEN

data[3] = 1
data[5] = 2

print(data)

win = Gtk.Window()
win.connect("delete-event", Gtk.main_quit)
win.set_default_size(1000, 700)
win.set_title("Embedded in GTK3")

fig = Figure(figsize=(5, 4), dpi=100)
ax = fig.add_subplot()
t = np.arange(DATA_LEN)
ax.bar(t,data,width=1, edgecolor="white", linewidth=0.7)

sw = Gtk.ScrolledWindow()
win.add(sw)
# A scrolled window border goes outside the scrollbars and viewport
sw.set_border_width(10)

canvas = FigureCanvas(fig)  # a Gtk.DrawingArea
canvas.set_size_request(800, 600)

box = Gtk.Box(spacing=6)
sw.add(box)
box.add(canvas)
#sw.add(canvas)

def add_data(arg):
    for i in range(10000):
        r = random.randint(0,DATA_LEN-1)
        data[r] += 1
    fig.clf()
    ax = fig.add_subplot()
    ax.bar(t,data,width=1, edgecolor="white", linewidth=0)
    canvas.draw()
    return True

button = Gtk.Button(label="Click Here")
button.connect("clicked", add_data)
box.add(button)

GLib.timeout_add(2000, add_data, None)

win.show_all()
Gtk.main()