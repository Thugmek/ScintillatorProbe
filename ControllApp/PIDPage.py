import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class ParametersPage(Gtk.Box):
    def __init__(self):
        super().__init__()

        listbox = Gtk.ListBox()
        listbox.set_selection_mode(Gtk.SelectionMode.NONE)
        self.add(listbox)

        row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        row.add(hbox)
        label1 = Gtk.Label("PID P", xalign=0)
        hbox.pack_start(label1, True, True, 0)
        spin_button = Gtk.SpinButton()
        spin_button.props.valign = Gtk.Align.CENTER
        spin_button.set_range(0,10.5)
        spin_button.set_increments(0.1,5)
        spin_button.set_digits(2)
        hbox.pack_start(spin_button, False, True, 0)
        listbox.add(row)

        row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        row.add(hbox)
        label1 = Gtk.Label("PID I", xalign=0)
        hbox.pack_start(label1, True, True, 0)
        spin_button = Gtk.SpinButton()
        spin_button.props.valign = Gtk.Align.CENTER
        spin_button.set_range(0, 1)
        spin_button.set_increments(0.000_000_001, 0.000_000_1)
        spin_button.set_digits(9)
        hbox.pack_start(spin_button, False, True, 0)
        listbox.add(row)

        row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        row.add(hbox)
        label1 = Gtk.Label("PID D", xalign=0)
        hbox.pack_start(label1, True, True, 0)
        spin_button = Gtk.SpinButton()
        spin_button.props.valign = Gtk.Align.CENTER
        spin_button.set_range(0, 2000)
        spin_button.set_increments(1, 25)
        spin_button.set_digits(2)
        hbox.pack_start(spin_button, False, True, 0)
        listbox.add(row)

        row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        row.add(hbox)
        label1 = Gtk.Label("PID Max ΔOut", xalign=0)
        hbox.pack_start(label1, True, True, 0)
        spin_button = Gtk.SpinButton()
        spin_button.props.valign = Gtk.Align.CENTER
        spin_button.set_range(0, 1)
        spin_button.set_increments(0.00001, 0.001)
        spin_button.set_digits(5)
        hbox.pack_start(spin_button, False, True, 0)
        listbox.add(row)


