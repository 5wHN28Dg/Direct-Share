import asyncio

from dbus_fast import BusType, Variant
from dbus_fast.aio import MessageBus


async def main():
    bus = await MessageBus(bus_type=BusType.SYSTEM).connect()
    # the introspection xml would normally be included in your project, but
    # this is convenient for development
    introspection = await bus.introspect(
        "org.freedesktop.NetworkManager", "/org/freedesktop/NetworkManager"
    )

    service_obj = bus.get_proxy_object(
        "org.freedesktop.NetworkManager",
        "/org/freedesktop/NetworkManager",
        introspection,
    )
    interface = service_obj.get_interface("org.freedesktop.NetworkManager")
    # properties = service_obj.get_interface("org.freedesktop.DBus.Properties")

    devices = await interface.get_devices()

    for device in devices:
        device_obj = bus.get_proxy_object(
            "org.freedesktop.NetworkManager",
            device,
            await bus.introspect("org.freedesktop.NetworkManager", device),
        )
        device_interface = device_obj.get_interface(
            "org.freedesktop.NetworkManager.Device"
        )
        if await device_interface.get_device_type() == 30:
            print("Found WiFiP2P device, it is:", device)
            break


asyncio.run(main())
