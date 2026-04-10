# SPDX-FileCopyrightText: 2026 5wHN28Dg
# SPDX-License-Identifier: GPL-3.0-or-later


import asyncio

from gi.events import GLibEventLoopPolicy

from . import i18n
from .ui import DirectShareApp


def run():
    asyncio.set_event_loop_policy(GLibEventLoopPolicy())
    app = DirectShareApp(application_id="io.directshare.App")
    app.run(None)
