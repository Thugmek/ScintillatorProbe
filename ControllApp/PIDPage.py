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

class PIDPage(Gtk.Box):
    def __init__(self):
        super().__init__()

        page_hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        self.add(page_hbox)

        listbox = Gtk.ListBox()
        listbox.set_selection_mode(Gtk.SelectionMode.NONE)
        page_hbox.add(listbox)

        # row = Gtk.ListBoxRow()
        # hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        # row.add(hbox)
        # label1 = Gtk.Label("PID P", xalign=0)
        # hbox.pack_start(label1, True, True, 0)
        # spin_button = Gtk.SpinButton()
        # spin_button.props.valign = Gtk.Align.CENTER
        # spin_button.set_range(0,10.5)
        # spin_button.set_increments(0.1,5)
        # spin_button.set_digits(2)
        # hbox.pack_start(spin_button, False, True, 0)
        # listbox.add(row)
        #
        # row = Gtk.ListBoxRow()
        # hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        # row.add(hbox)
        # label1 = Gtk.Label("PID I", xalign=0)
        # hbox.pack_start(label1, True, True, 0)
        # spin_button = Gtk.SpinButton()
        # spin_button.props.valign = Gtk.Align.CENTER
        # spin_button.set_range(0, 1)
        # spin_button.set_increments(0.000_000_001, 0.000_000_1)
        # spin_button.set_digits(9)
        # hbox.pack_start(spin_button, False, True, 0)
        # listbox.add(row)
        #
        # row = Gtk.ListBoxRow()
        # hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        # row.add(hbox)
        # label1 = Gtk.Label("PID D", xalign=0)
        # hbox.pack_start(label1, True, True, 0)
        # spin_button = Gtk.SpinButton()
        # spin_button.props.valign = Gtk.Align.CENTER
        # spin_button.set_range(0, 2000)
        # spin_button.set_increments(1, 25)
        # spin_button.set_digits(2)
        # hbox.pack_start(spin_button, False, True, 0)
        # listbox.add(row)
        #
        # row = Gtk.ListBoxRow()
        # hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        # row.add(hbox)
        # label1 = Gtk.Label("PID Max ΔOut", xalign=0)
        # hbox.pack_start(label1, True, True, 0)
        # spin_button = Gtk.SpinButton()
        # spin_button.props.valign = Gtk.Align.CENTER
        # spin_button.set_range(0, 1)
        # spin_button.set_increments(0.00001, 0.001)
        # spin_button.set_digits(5)
        # hbox.pack_start(spin_button, False, True, 0)
        # listbox.add(row)

        row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        row.add(hbox)
        label1 = Gtk.Label("Manual PWM", xalign=0)
        hbox.pack_start(label1, True, True, 0)
        self.spin_button = Gtk.SpinButton()
        self.spin_button.props.valign = Gtk.Align.CENTER
        self.spin_button.set_range(0, 1200)
        self.spin_button.set_increments(10, 100)
        self.spin_button.set_digits(0)
        hbox.pack_start(self.spin_button, False, True, 0)
        listbox.add(row)

        row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        row.add(hbox)
        button = Gtk.Button(label="Send")
        button.connect("clicked", self.send_params)
        hbox.pack_start(button, True, True, 0)
        listbox.add(row)

        fig = Figure(figsize=(5, 4), dpi=100)
        self.ax = fig.add_subplot()
        self.ax.set_ylim([0,3200])
        self.voltages = [0] * 200
        self.voltages_min = [0] * 200
        self.voltages_max = [0] * 200
        self.pwms = [0] * 200
        self.pwms_min = [0] * 200
        self.pwms_max = [0] * 200
        self.t = list(range(len(self.voltages)))
        self.plot_range = self.ax.fill_between(self.t, self.voltages_min, self.voltages_max)
        self.plot = self.ax.plot(self.t, self.voltages)[0]
        self.plot_range_pwm = self.ax.fill_between(self.t, self.pwms_min, self.pwms_max)
        self.plot_pwm = self.ax.plot(self.t, self.pwms)[0]
        fig.tight_layout()

        self.canvas = FigureCanvas(fig)
        self.canvas.set_hexpand(True)
        self.canvas.set_vexpand(True)

        page_hbox.add(self.canvas)

        self.data_lock = threading.Lock()
        SerialHandler.add_callback(SerialCallback(b"Temperature Report, data size", self.serial_callback))

        GLib.timeout_add(300,self.redraw_chart)

    def send_params(self, button):
        SerialHandler.send_command(f"P1 A{self.spin_button.get_value()}")

    def redraw_chart(self):
        with self.data_lock:
            self.plot.set_ydata(self.voltages)
            self.plot_pwm.set_ydata(self.pwms)
            self.plot_range.remove()
            self.plot_range_pwm.remove()
            self.plot_range = self.ax.fill_between(self.t, self.voltages_min, self.voltages_max, color='C0', alpha=0.5)
            self.plot_range_pwm = self.ax.fill_between(self.t, self.pwms_min, self.pwms_max, color='C1', alpha=0.5)
        self.ax.relim()
        #self.ax.autoscale_view()
        self.canvas.draw()
        return True

    def serial_callback(self, line, serial):
        temperatures_bin = serial.read(200)
        pwms_bin = serial.read(200)
        voltages = []
        pwms = []

        v_max = -1
        v_min = 10000
        p_max = -1
        p_min = 10000
        v_avg = 0
        p_avg = 0
        for i in range(100):
            b = temperatures_bin[0:2]
            temperatures_bin = temperatures_bin[2:]
            p = pwms_bin[0:2]
            pwms_bin = pwms_bin[2:]

            volt = int.from_bytes(b, "little")
            pwm = int.from_bytes(p, "little")

            v_avg += volt/100
            p_avg += pwm/100

            if volt > v_max:
                v_max = volt
            if volt < v_min:
                v_min = volt
            if pwm > p_max:
                p_max = pwm
            if pwm < p_min:
                p_min = pwm

        with self.data_lock:
            self.voltages.append(v_avg)
            self.voltages = self.voltages[-200:]
            self.voltages_min.append(v_min)
            self.voltages_min = self.voltages_min[-200:]
            self.voltages_max.append(v_max)
            self.voltages_max = self.voltages_max[-200:]
            self.pwms.append(p_avg)
            self.pwms = self.pwms[-200:]
            self.pwms_min.append(p_min)
            self.pwms_min = self.pwms_min[-200:]
            self.pwms_max.append(p_max)
            self.pwms_max = self.pwms_max[-200:]




