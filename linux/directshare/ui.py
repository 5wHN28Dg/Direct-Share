import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Adw, Gtk


class DirectShareApp(Adw.Application):
    def __init__(self, application_id: str):
        super().__init__(application_id=application_id)
        self.connect("activate", self.on_activate)

    def on_activate(self, app: "DirectShareApp"):
        win = Adw.ApplicationWindow(application=app)
        win.set_title("DirectShare")
        win.set_default_size(900, 600)

        header = Adw.HeaderBar()
        # win.set_titlebar(header)

        # Just a placeholder so you see something
        label = Gtk.Label(label="DirectShare is running ✅")
        win.set_content(label)

        win.present()
