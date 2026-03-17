# SPDX-FileCopyrightText: 2026 5wHN28Dg
# SPDX-License-Identifier: GPL-3.0-or-later

import asyncio
import gettext
import os

# import gi
# gi.require_version("Gtk", "4.0")
# gi.require_version("Adw", "1")
from gi.events import GLibEventLoopPolicy

from .ui import DirectShareApp

_localedir = os.path.join(os.path.dirname(__file__), "..", "po")
gettext.bindtextdomain("direct-share", _localedir)
gettext.textdomain("direct-share")


def run():
    asyncio.set_event_loop_policy(GLibEventLoopPolicy())
    app = DirectShareApp(application_id="io.directshare.App")
    app.run(None)
