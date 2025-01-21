import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from PIDPage import PIDPage


class MainWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="GammaScintillator")
        self.connect("destroy", Gtk.main_quit)
        self.set_size_request(600,400)

        self.notebook = Gtk.Notebook()
        self.add(self.notebook)

        self.notebook.append_page(PIDPage(), Gtk.Label(label="PID"))

        self.page2 = Gtk.Box()
        self.page2.set_border_width(10)
        self.page2.add(Gtk.Label(label="A page with an image for a Title."))
        self.notebook.append_page(
            self.page2, Gtk.Image.new_from_icon_name("help-about", Gtk.IconSize.MENU)
        )

    def on_button_clicked(self, widget):
        print("Hello World")