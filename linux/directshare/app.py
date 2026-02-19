import asyncio

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.events import GLibEventLoopPolicy
from gi.repository import Adw

from .ui import DirectShareApp


def run():
    asyncio.set_event_loop_policy(GLibEventLoopPolicy())
    app = DirectShareApp(application_id="io.directshare.App")
    app.run(None)
