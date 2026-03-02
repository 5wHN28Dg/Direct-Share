# SPDX-FileCopyrightText: 2026 Hashim Al-Moussawi
# SPDX-License-Identifier: GPL-3.0-or-later

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Adw, Gtk


class DirectShareApp(Adw.Application):
    def __init__(self, application_id: str):
        super().__init__(application_id=application_id)
        self.connect("activate", self.on_activate)

    def on_activate(self, app: "DirectShareApp"):
        win = Adw.ApplicationWindow(application=app, resizable=True)
        win.set_title("Direct-Share")
        win.set_default_size(900, 600)

        header = Adw.HeaderBar()

        view = Adw.ToolbarView()
        view.add_top_bar(header)

        view.set_content(Gtk.Label(label="Direct-Share is running ✅"))
        win.set_content(view)

        win.present()
