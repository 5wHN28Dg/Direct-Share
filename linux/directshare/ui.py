# SPDX-FileCopyrightText: 2026 5wHN28Dg
# SPDX-License-Identifier: GPL-3.0-or-later

"""Handles All the UI components of the application."""

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
        box.append(Gtk.Label(label="Direct-Share is running ✅"))
        # will add widgets here
        return box

    def build_trusted_page(self):
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        box.append(Gtk.Label(label="Trusted Devices"))
        return box

    def build_settings_page(self):
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        box.append(Gtk.Label(label="Settings"))
        return box

    def on_activate(self, app: "DirectShareApp"):
        win = Adw.ApplicationWindow(application=app, resizable=True)
        win.set_title("Direct Share")
        win.set_default_size(900, 600)

        header = Adw.HeaderBar()

        view = Adw.ToolbarView()
        self.stack = Adw.ViewStack()
        self.stack.set_vexpand(True)

        # Build pages
        main_page = self.build_main_page()
        trusted_page = self.build_trusted_page()
        settings_page = self.build_settings_page()

        self.stack.add_titled(main_page, "main", "Transfer Files")
        self.stack.add_titled(trusted_page, "trusted", "Trusted Devices")
        self.stack.add_titled(settings_page, "settings", "Settings")

        top_switcher = Adw.ViewSwitcher()
        top_switcher.set_stack(self.stack)
        top_switcher.set_policy(Adw.ViewSwitcherPolicy.WIDE)

        window_title = Adw.WindowTitle(title="Direct Share")
        window_title.set_visible(False)

        title_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        title_box.append(window_title)
        title_box.append(top_switcher)

        header.set_title_widget(title_box)

        switcher = Adw.ViewSwitcherBar()
        switcher.set_stack(self.stack)

        view.add_top_bar(header)
        view.add_bottom_bar(switcher)
        view.set_content(self.stack)
        win.set_content(view)

        # Break point fires when window width drops below 550sp
        bp = Adw.Breakpoint.new(Adw.BreakpointCondition.parse("max-width: 550sp"))
        bp.add_setter(top_switcher, "visible", False)
        bp.add_setter(window_title, "visible", True)
        bp.add_setter(switcher, "reveal", True)
        win.add_breakpoint(bp)

        win.present()
