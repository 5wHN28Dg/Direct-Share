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

import asyncio
import os
from gettext import gettext as _

import gi

from . import i18n

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Adw, Gdk, Gtk


class DirectShareApp(Adw.Application):
    def __init__(self, application_id: str):
        super().__init__(application_id=application_id)
        self.core = None
        self.peer_cards = {}
        self.css_provider = None
        self.connect("activate", self.on_activate)

    def set_core(self, core):
        self.core = core
        self.core.add_peer_added_callback(self.add_peer_card)
        self.core.add_peer_removed_callback(self.remove_peer_card)

    def build_main_page(self):
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)

        self.peers_flow_box = Gtk.FlowBox(
            orientation=Gtk.Orientation.HORIZONTAL,
            column_spacing=6,
            row_spacing=6,
            hexpand=True,
            selection_mode=Gtk.SelectionMode.MULTIPLE,
        )

        scroll_win = Gtk.ScrolledWindow(
            child=self.peers_flow_box,
            vscrollbar_policy=Gtk.PolicyType.NEVER,
            min_content_height=72,
            max_content_height=72,
        )

        search_button = Gtk.Button(
            icon_name="edit-find-symbolic",
            tooltip_text=_("Search for Peers"),
        )
        search_button.connect("clicked", self.on_search_clicked)

        self.header.pack_start(search_button)

        files_stack = Adw.ViewStack(enable_transitions=True)

        selected_files_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        queue_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)

        files_stack.add_titled(selected_files_box, "selected", _("Selected Files"))
        files_stack.add_titled(queue_box, "queue", _("Queue"))

        files_stack_switcher = Adw.InlineViewSwitcher(
            stack=files_stack, margin_bottom=12, margin_top=12, halign=Gtk.Align.CENTER
        )

        main_box.append(scroll_win)
        main_box.append(files_stack_switcher)
        main_box.append(files_stack)
        return main_box

    def add_peer_card(self, peer: dict[str, str | int]):
        peer_key = peer["path"]
        peer_label = peer.get("Name", peer["HwAddress"])

        if peer_key in self.peer_cards:
            return

        box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=6,
            margin_top=8,
            margin_bottom=8,
            margin_start=8,
            margin_end=8,
        )

        icon = Gtk.Image(icon_name="computer-symbolic", pixel_size=36)
        label = Gtk.Label(label=peer_label, wrap=True)
        signal_strength = Gtk.Label(
            label=f"{peer['Strength']}%",
            halign=Gtk.Align.END,
            tooltip_text="Signal Strength",
        )

        box.append(icon)
        box.append(label)
        box.append(signal_strength)

        card = Adw.Bin(
            child=box,
            css_classes=["card"],
            margin_top=4,
            margin_bottom=4,
            margin_start=4,
            margin_end=4,
        )

        child = Gtk.FlowBoxChild(child=card)

        gesture = Gtk.GestureClick(button=3)
        gesture.connect("pressed", self.on_peer_card_right_clicked, child, peer)
        child.add_controller(gesture)

        self.peer_cards[peer_key] = child
        self.peers_flow_box.insert(child, -1)

    def remove_peer_card(self, peer_path):
        child = self.peer_cards.pop(peer_path, None)

        if child is not None:
            self.peers_flow_box.remove(child)

    def on_peer_card_right_clicked(self, gesture, n_press, x, y, child, peer):
        popover = self.build_context_menu(peer)
        popover.set_parent(child)
        popover.popup()

    def build_context_menu(self, peer):
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        select_button = Gtk.Button(label=_("Select"), margin_bottom=6)
        trust_device_button = Gtk.Button(label=_("Trust this Device"), margin_bottom=6)
        device_info_button = Gtk.Button(label=_("Device Info"))

        device_info_button.connect(
            "clicked", lambda _: self.build_device_info_dialog(peer)
        )

        box.append(select_button)
        box.append(trust_device_button)
        box.append(device_info_button)

        return Gtk.Popover(child=box)

    def build_device_info_dialog(self, peer):
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        inner_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        left_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        right_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        flags = {
            0: "Peer has no special capabilities",
            1: "Peer requires authentication and encryption (usually means WEP)",
            2: "Peer supports some WPS method",
            4: "Peer supports push-button WPS",
            8: "Peer supports PIN-based WPS",
        }

        counter = 0
        for k, v in peer.items():
            if len(str(v)) > 0 and k not in ["LastSeen", "Strength", "WfdIEs", "path"]:
                k = (
                    "Model Number"
                    if k == "ModelNumber"
                    else "HW Address"
                    if k == "HwAddress"
                    else k
                )
                v = flags[v] if k == "Flags" else v

                left_box.append(
                    Gtk.Label(label=k)
                ) if counter < 4 else right_box.append(Gtk.Label(label=k))
                left_box.append(
                    Gtk.Label(label=str(v), selectable=True)
                ) if counter < 4 else right_box.append(
                    Gtk.Label(label=str(v), selectable=True)
                )
                counter += 1

        box.append(Adw.HeaderBar())
        box.append(inner_box)
        inner_box.append(left_box)
        inner_box.append(right_box)

        device_info_dialog = Adw.Dialog(title="Peer Info", child=box)
        device_info_dialog.present(self.win)

    def on_search_clicked(self, button):
        if self.core is None:
            print("CRITICAL: Core not ready yet")
            return

        async def run_scan():
            try:
                button.set_sensitive(False)
                print("Sending scan request to NetworkManager...")

                await self.core.find_peers()

                print("Scan request successful! Waiting for peers...")

            except Exception as e:
                print(f"CRITICAL: Failed to start scan: {e}")
            finally:
                await asyncio.sleep(30)
                button.set_sensitive(True)

        self.scan_task = asyncio.create_task(run_scan())

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

        self.languages = i18n.get_available_languages()
        self.lang_names = list(self.languages.keys())
        self.language_row = Adw.ComboRow(
            title=_("Language"), model=Gtk.StringList.new(self.lang_names)
        )
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
            preferencesgroup listview.inline {
                background-color: #00000000;
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
        self.header = Adw.HeaderBar()
        self.view = Adw.ToolbarView()
        self.stack = Adw.ViewStack(enable_transitions=True, vexpand=True)

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

        self.header.set_title_widget(title_box)
        self.header.pack_end(about_button)

        self.switcher = Adw.ViewSwitcherBar(stack=self.stack)

        self.view.add_top_bar(self.header)
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
