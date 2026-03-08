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

    def build_about_dialog(self):
        about_dialog = Adw.AboutDialog(
            application_name="Direct Share",
            developer_name="5wHN28Dg",
            issue_url="https://github.com/5wHN28Dg/Direct-Share/issues/new/choose",
            support_url="https://github.com/5wHN28Dg/Direct-Share/discussions",
            website="https://github.com/5wHN28Dg/Direct-Share",
            copyright="© 2024 5wHN28Dg",
            license_type=Gtk.License.GPL_3_0,
            version="0.0.1",
        )
        return about_dialog

    def on_activate(self, app: "DirectShareApp"):
        # Set up main app window
        win = Adw.ApplicationWindow(
            application=app,
            resizable=True,
            title="Direct Share",
            default_width=900,
            default_height=600,
        )

        header = Adw.HeaderBar()
        view = Adw.ToolbarView()
        self.stack = Adw.ViewStack(vexpand=True)

        main_page = self.build_main_page()
        trusted_page = self.build_trusted_page()
        settings_page = self.build_settings_page()
        about_dialog = self.build_about_dialog()

        self.stack.add_titled_with_icon(
            main_page, "main", "Transfer Files", "mail-send-receive-symbolic"
        )
        self.stack.add_titled_with_icon(
            trusted_page, "trusted", "Trusted Devices", "computer-symbolic"
        )
        self.stack.add_titled_with_icon(
            settings_page, "settings", "Settings", "applications-system-symbolic"
        )

        top_switcher = Adw.ViewSwitcher(
            stack=self.stack, policy=Adw.ViewSwitcherPolicy.WIDE
        )

        window_title = Adw.WindowTitle(title="Direct Share", visible=False)

        about_button = Gtk.Button(icon_name="help-about-symbolic")
        about_button.connect("clicked", lambda _: about_dialog.present(win))

        title_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        title_box.append(window_title)
        title_box.append(top_switcher)
        title_box.append(about_button)

        header.set_title_widget(title_box)

        switcher = Adw.ViewSwitcherBar(stack=self.stack)

        view.add_top_bar(header)
        view.add_bottom_bar(switcher)
        view.set_content(self.stack)

        win.set_content(view)

        # Break point fires to switch between top and bottom switcher bars based on window width
        bp = Adw.Breakpoint.new(Adw.BreakpointCondition.parse("max-width: 550sp"))
        bp.add_setter(top_switcher, "visible", False)
        bp.add_setter(window_title, "visible", True)
        bp.add_setter(switcher, "reveal", True)
        win.add_breakpoint(bp)

        win.present()
