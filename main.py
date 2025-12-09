import asyncio

from dbus_fast import BusType, Variant
from dbus_fast.aio import MessageBus


async def main():
    bus = await MessageBus(bus_type=BusType.SYSTEM).connect()
    # the introspection xml would normally be included in your project, but
    # this is convenient for development

    introspection = await bus.introspect(
        "org.freedesktop.NetworkManager",
        "/org/freedesktop/NetworkManager/Devices/5",
    )
    print(introspection)

    obj = bus.get_proxy_object(
        "org.freedesktop.NetworkManager",
        "/org/freedesktop/NetworkManager/Devices/5",
        introspection,
    )
    interface = obj.get_interface("org.freedesktop.NetworkManager.Device")
    properties = obj.get_interface("org.freedesktop.DBus.Properties")

    var = await properties.call_get(
        "org.freedesktop.NetworkManager.Device", "Interface"
    )
    print(var.value)


asyncio.run(main())
