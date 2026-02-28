# SPDX-FileCopyrightText: 2026 Hashim Al-Moussawi
# SPDX-License-Identifier: GPL-3.0-or-later

import asyncio

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.events import GLibEventLoopPolicy

from .ui import DirectShareApp


def run():
    asyncio.set_event_loop_policy(GLibEventLoopPolicy())
    app = DirectShareApp(application_id="io.directshare.App")
    app.run(None)
