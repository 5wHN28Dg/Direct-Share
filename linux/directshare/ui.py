# SPDX-FileCopyrightText: 2026 5wHN28Dg
# SPDX-License-Identifier: GPL-3.0-or-later

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Adw, Gtk


class DirectShareApp(Adw.Application):
    def __init__(self, application_id: str):
        super().__init__(application_id=application_id)
        self.connect("activate", self.on_activate)

    def build_main_page(self):
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        # will add widgets here
        return box

    def build_trusted_page(self):
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        return box

    def build_settings_page(self):
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        return box

    def on_activate(self, app: "DirectShareApp"):
        win = Adw.ApplicationWindow(application=app, resizable=True)
        win.set_title("Direct-Share")
        win.set_default_size(900, 600)

        header = Adw.HeaderBar()

        view = Adw.ToolbarView()
        self.stack = Adw.ViewStack()
        self.stack.set_vexpand(True)

        # Build pages
        main_page = self.build_main_page()
        trusted_page = self.build_trusted_page()
        settings_page = self.build_settings_page()

        self.stack.add_titled(main_page, "main", "Main")
        self.stack.add_titled(trusted_page, "trusted", "Trusted")
        self.stack.add_titled(settings_page, "settings", "Settings")

        switcher = Adw.ViewSwitcherBar()
        switcher.set_stack(self.stack)

        view.add_top_bar(header)

        # view.set_content(Gtk.Label(label="Direct-Share is running ✅"))
        win.set_content(view)

        win.present()
