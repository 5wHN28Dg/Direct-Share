import asyncio

import gi
from gi.events import GLibEventLoopPolicy
from gi.repository import Adw

from .ui import DirectShareApp

gi.require_version("Gtk", "4.2.3")
gi.require_version("Adw", "1.8.1")


def run():
    asyncio.set_event_loop_policy(GLibEventLoopPolicy())
    app = DirectShareApp(application_id="io.directshare.App")
    app.run(None)
