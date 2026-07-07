# SPDX-FileCopyrightText: 2026 5wHN28Dg
# SPDX-License-Identifier: GPL-3.0-or-later

from dbus_fast import BusType
from dbus_fast.aio import MessageBus


class WpasBackend:
    def __init__(self, bus: MessageBus):
        self.bus = bus

    @classmethod
    async def create(cls):
        bus = await MessageBus(bus_type=BusType.SYSTEM).connect()
        instance = cls(bus)
        return instance
