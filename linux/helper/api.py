# SPDX-FileCopyrightText: 2026 5wHN28Dg
# SPDX-License-Identifier: GPL-3.0-or-later

from dbus_fast.annotations import DBusSignature, DBusBool, DBusByte, DBusInt32, DBusStr
from dbus_fast.aio import MessageBus
from dbus_fast.service import ServiceInterface, dbus_method, dbus_property, dbus_signal
from dbus_fast import Variant, DBusError

import asyncio
from typing import Annotated

FrobateReturnDBusType = Annotated[dict[int, str], DBusSignature("a{us}")]
BazifyBarDBusType = Annotated[tuple[int, int, int], DBusSignature("(iiu)")]
BazifyReturnDBusType = Annotated[tuple[Variant, Variant], DBusSignature("vv")]
MorgifyBarDBusType = Annotated[tuple[int, int, list[Variant]], DBusSignature("(iiav)")]


class ExampleInterface(ServiceInterface):
    def __init__(self):
        super().__init__("com.example.SampleInterface0")
        self._bar = 105

    @dbus_method()
    def Frobate(self, foo: DBusInt32, bar: DBusStr) -> FrobateReturnDBusType:
        print(f"called Frobate with foo={foo} and bar={bar}")

        return {1: "one", 2: "two"}

    @dbus_method()
    async def Bazify(self, bar: BazifyBarDBusType) -> BazifyReturnDBusType:
        print(f"called Bazify with bar={bar}")

        return Variant("s", "example"), Variant("s", "bazify")

    @dbus_method()
    def Mogrify(self, bar: MorgifyBarDBusType):
        raise DBusError(
            "com.example.error.CannotMogrify", "it is not possible to mogrify"
        )

    @dbus_signal()
    def Changed(self) -> DBusBool:
        return True

    @dbus_property()
    def Bar(self) -> DBusByte:
        return self._bar

    @Bar.setter
    def Bar(self, val: DBusByte):
        if self._bar == val:
            return

        self._bar = val

        self.emit_properties_changed({"Bar": self._bar})


async def main():
    bus = await MessageBus().connect()
    interface = ExampleInterface()
    bus.export("/com/example/sample0", interface)
    await bus.request_name("com.example.name")

    # emit the changed signal after two seconds.
    await asyncio.sleep(2)

    interface.changed()

    await bus.wait_for_disconnect()


asyncio.run(main())
