import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from MainWindow import MainWindow
from SerialHandler import SerialHandler

mw = MainWindow()
mw.show_all()
SerialHandler.start_handler()
Gtk.main()