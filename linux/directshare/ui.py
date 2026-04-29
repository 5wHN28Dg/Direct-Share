# SPDX-FileCopyrightText: 2026 5wHN28Dg
# SPDX-License-Identifier: GPL-3.0-or-later

"""
UI layer for Direct Share built with GTK4 and Libadwaita.

Responsibilities:
- Define the main application window and navigation structure
- Construct primary views (main, trusted devices, settings)
- Handle user-driven UI state changes (theme, language, layout direction)
- Integrate with i18n for dynamic language switching

Architecture:
- Single Adw.Application subclass managing all UI state
- ViewStack-based navigation with adaptive layout (top/bottom switcher)
- UI is rebuilt on language switch

Assumptions / Constraints:
- Relies on environment variable LANGUAGE for language selection
- RTL/LTR direction is set globally via Gtk.Widget.set_default_direction
- Theme handling uses Adw.StyleManager with optional custom CSS override

Notes:
- UI is constructed programmatically (no .ui files / GtkBuilder)
"""

import os
from gettext import gettext as _

import gi

from . import i18n

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Adw, Gtk


class DirectShareApp(Adw.Application):
    def __init__(self, application_id: str):
        super().__init__(application_id=application_id)
        self.css_provider = None
        self.connect("activate", self.on_activate)

    def build_main_page(self):
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        box.append(Gtk.Label(label=_("Direct-Share is running ✅")))
        # will add widgets here
        return box

    def build_trusted_page(self):
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        box.append(Gtk.Label(label=_("Trusted Devices")))
        return box

    def build_settings_page(self):
        preferences_page = Adw.PreferencesPage()

        theme_toggle = Adw.ToggleGroup(margin_bottom=12, margin_top=12)
        theme_toggle.add(Adw.Toggle(label=_("Light"), name="Light"))
        theme_toggle.add(Adw.Toggle(label=_("Dark"), name="Dark"))
        theme_toggle.add(Adw.Toggle(label=_("Black"), name="Black"))
        theme_toggle.add(Adw.Toggle(label=_("System"), name="System"))
        self.scheme = {
            "Light": Adw.ColorScheme.FORCE_LIGHT,
            "Dark": Adw.ColorScheme.FORCE_DARK,
            "Black": Adw.ColorScheme.FORCE_DARK,
            "System": Adw.ColorScheme.DEFAULT,
        }
        current_scheme = Adw.StyleManager.get_default().get_color_scheme()

        if (
            current_scheme == Adw.ColorScheme.FORCE_DARK
            and "black-theme" in self.win.get_css_classes()
        ):
            selected_name = "Black"
        else:
            selected_name = next(
                name
                for name, value in self.scheme.items()
                if value == current_scheme and name != "Black"
            )

        theme_toggle.set_active_name(selected_name)
        theme_toggle.connect(
            "notify::active-name",
            lambda _toggle, _name: self.on_theme_changed(theme_toggle),
        )

        theme_row = Adw.ActionRow(title=_("Theme"))
        theme_row.add_suffix(theme_toggle)

        self.language_row = Adw.ComboRow(title=_("Language"))
        self.languages = i18n.get_available_languages()
        self.lang_names = list(self.languages.keys())
        self.language_row.set_model(Gtk.StringList.new(self.lang_names))
        for index, lang in enumerate(self.languages.values()):
            if os.getenv("LANGUAGE", os.getenv("LANG", "")).startswith(lang):
                self.language_row.set_selected(index)
                break
        self.language_row.connect("notify::selected-item", self.on_language_changed)

        device_name_row = Adw.EntryRow(title=_("Device Name"))

        general_group = Adw.PreferencesGroup(title=_("General"))
        general_group.add(theme_row)
        general_group.add(self.language_row)
        general_group.add(device_name_row)

        startup_row = Adw.SwitchRow(title=_("Start at OS startup"))
        quick_settings_row = Adw.SwitchRow(title=_("Add to Quick Settings Panel"))
        system_tray_row = Adw.SwitchRow(title=_("Add to system tray"))

        startup_access_group = Adw.PreferencesGroup(title=_("Startup and Access"))
        startup_access_group.add(startup_row)
        startup_access_group.add(quick_settings_row)
        startup_access_group.add(system_tray_row)

        awake_row = Adw.SwitchRow(title=_("Keep device awake during transfers"))

        power_behavior_group = Adw.PreferencesGroup(title=_("Power and Behavior"))
        power_behavior_group.add(awake_row)

        default_folder_row = Adw.ActionRow(title=_("Default Save Folder"))
        default_folder_row.add_suffix(
            Gtk.Button(
                child=Adw.ButtonContent(
                    label=_("Select"), icon_name="folder-open-symbolic"
                ),
                margin_top=8,
                margin_bottom=8,
                valign=Gtk.Align.CENTER,
            )
        )

        restore_backup_row = Adw.ActionRow(title=_("App Data"))
        restore_backup_row.add_suffix(
            Gtk.Button(
                child=Adw.ButtonContent(
                    label=_("Restore"), icon_name="document-open-symbolic"
                ),
                margin_top=8,
                margin_bottom=8,
                valign=Gtk.Align.CENTER,
            )
        )
        restore_backup_row.add_suffix(
            Gtk.Button(
                child=Adw.ButtonContent(
                    label=_("Backup"), icon_name="document-save-symbolic"
                ),
                margin_top=8,
                margin_bottom=8,
                valign=Gtk.Align.CENTER,
            )
        )

        files_storage_group = Adw.PreferencesGroup(title=_("Files and Storage"))
        files_storage_group.add(default_folder_row)
        files_storage_group.add(restore_backup_row)

        interface_row = Adw.ExpanderRow(title=_("Wi-Fi Direct Interface"))

        network_group = Adw.PreferencesGroup(title=_("Network"))
        network_group.add(interface_row)

        preferences_page.add(general_group)
        preferences_page.add(startup_access_group)
        preferences_page.add(files_storage_group)
        preferences_page.add(power_behavior_group)
        preferences_page.add(network_group)

        return preferences_page

    def build_about_dialog(self):
        about_dialog = Adw.AboutDialog(
            application_name="Direct Share",
            developer_name="5wHN28Dg",
            issue_url="https://github.com/5wHN28Dg/Direct-Share/issues/new/choose",
            support_url="https://github.com/5wHN28Dg/Direct-Share/discussions/10",
            website="https://github.com/5wHN28Dg/Direct-Share",
            copyright="© 2025-2026 5wHN28Dg",
            license_type=Gtk.License.GPL_3_0,
            version="0.0.1",
        )
        about_dialog.add_acknowledgement_section(
            _("UI/UX Inspiration"), ["Blip https://blip.net/"]
        )
        return about_dialog

    def apply_black_theme(self):
        self.css_provider = Gtk.CssProvider()
        self.css_provider.load_from_string("""
            window, .view {
                background-color: #000000;
            }
            dialog.about.scrolledwindow, dialog.about sheet {
                background-color: #1a1a1a;
            }
        """)
        Gtk.StyleContext.add_provider_for_display(
            self.win.get_display(),
            self.css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
        )
        self.win.add_css_class("black-theme")

    def on_theme_changed(self, toggle_group):
        active_scheme = self.scheme.get(
            toggle_group.get_active_name(), Adw.ColorScheme.DEFAULT
        )

        Adw.StyleManager.get_default().set_color_scheme(active_scheme)

        if (
            active_scheme == Adw.ColorScheme.FORCE_DARK
            and toggle_group.get_active_name() == "Black"
        ):
            self.apply_black_theme()
        elif self.css_provider is not None:
            self.win.remove_css_class("black-theme")
            Gtk.StyleContext.remove_provider_for_display(
                self.win.get_display(), self.css_provider
            )
            self.css_provider = None

    def on_language_changed(self, row, _name):
        current_lang = row.get_selected_item().get_string()
        current_page = self.stack.get_visible_child_name()

        direction = (
            Gtk.TextDirection.RTL
            if self.languages[current_lang] in i18n.RTL_LANGUAGES
            else Gtk.TextDirection.LTR
        )
        Gtk.Widget.set_default_direction(direction)
        os.environ["LANGUAGE"] = self.languages[current_lang]

        i18n.invalidate_gettext_cache("libadwaita", "/usr/share/locale")

        self.build_widgets()
        self.win.set_content(self.view)

        assert current_page is not None
        self.stack.set_visible_child_name(current_page)

    def build_widgets(self):
        header = Adw.HeaderBar()
        self.view = Adw.ToolbarView()
        self.stack = Adw.ViewStack(vexpand=True)

        main_page = self.build_main_page()
        trusted_page = self.build_trusted_page()
        settings_page = self.build_settings_page()
        about_dialog = self.build_about_dialog()

        self.stack.add_titled_with_icon(
            main_page, "main", _("Transfer Files"), "mail-send-receive-symbolic"
        )
        self.stack.add_titled_with_icon(
            trusted_page, "trusted", _("Trusted Devices"), "computer-symbolic"
        )
        self.stack.add_titled_with_icon(
            settings_page, "settings", _("Settings"), "applications-system-symbolic"
        )

        self.top_switcher = Adw.ViewSwitcher(
            stack=self.stack, policy=Adw.ViewSwitcherPolicy.WIDE
        )

        self.window_title = Adw.WindowTitle(title="Direct Share", visible=False)

        about_button = Gtk.Button(icon_name="help-about-symbolic")
        about_button.connect("clicked", lambda _: about_dialog.present(self.win))

        title_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        title_box.append(self.window_title)
        title_box.append(self.top_switcher)

        header.set_title_widget(title_box)
        header.pack_end(about_button)

        self.switcher = Adw.ViewSwitcherBar(stack=self.stack)

        self.view.add_top_bar(header)
        self.view.add_bottom_bar(self.switcher)
        self.view.set_content(self.stack)

        # Break point fires to switch between top and bottom switcher bars based on window width
        bp = Adw.Breakpoint.new(Adw.BreakpointCondition.parse("max-width: 550sp"))
        bp.add_setter(self.top_switcher, "visible", False)
        bp.add_setter(self.window_title, "visible", True)
        bp.add_setter(self.switcher, "reveal", True)
        self.win.add_breakpoint(bp)

    def on_activate(self, app: "DirectShareApp"):
        # Set up main app window
        self.win = Adw.ApplicationWindow(
            application=app,
            resizable=True,
            title="Direct Share",
            default_width=900,
            default_height=600,
        )

        self.build_widgets()
        self.win.set_content(self.view)

        self.win.present()
