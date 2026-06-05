# SPDX-FileCopyrightText: 2026 5wHN28Dg
# SPDX-License-Identifier: GPL-3.0-or-later

"""
Direct-Share composition + startup orchestration

Assumptions / Constraints:
- Relies on the deprecated `set_event_loop_policy` function due to GLib integration.
  GTK/PyGObject currently documents GLibEventLoopPolicy as the supported way
  to let asyncio tasks run while Gtk.Application.run() owns the main loop.

  Python 3.14 deprecates global event loop policies in favor of Runner/
  loop_factory, but Gtk.Application.run() is a blocking GLib call rather than
  an awaitable coroutine, so Runner does not currently fit this startup model.

  Revisit when PyGObject provides a Python-3.16-compatible replacement.
"""

import asyncio
import sys

from gi.events import GLibEventLoopPolicy

from . import i18n
from .core import CoreApp
from .ui import DirectShareApp
from .wifi_p2p import WifiDirectBackend


def run():
    policy = GLibEventLoopPolicy()
    asyncio.set_event_loop_policy(policy)

    app = DirectShareApp(application_id="io.directshare.App")

    async def startup():
        core = await CoreApp.create(WifiDirectBackend())
        app.set_core(core)

    app.startup_task = policy.get_event_loop().create_task(startup())

    sys.exit(app.run(sys.argv))
