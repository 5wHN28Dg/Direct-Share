import asyncio

import dearpygui.dearpygui as dpg
from dbus_fast import BusType, Variant
from dbus_fast.aio import MessageBus


async def main():
    global bus
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
        global device_obj
        device_obj = bus.get_proxy_object(
            "org.freedesktop.NetworkManager",
            device,
            await bus.introspect("org.freedesktop.NetworkManager", device),
        )
        device_interface = device_obj.get_interface(
            "org.freedesktop.NetworkManager.Device"
        )
        if await device_interface.get_device_type() == 30:
            print("Found WiFiP2P device, it is:", device, "you are good to go")
            break


async def find_wifi_p2p_peers():
    device_interface = device_obj.get_interface(
        "org.freedesktop.NetworkManager.Device.WifiP2P"
    )
    await device_interface.call_start_find({})
    # print("Found WiFiP2P peers:", await device_interface.get_peers())


asyncio.run(main())
dpg.create_context()

# add a font registry
with dpg.font_registry():
    # first argument ids the path to the .ttf or .otf file
    default_font = dpg.add_font("font/ProggyVector-Regular.otf", 75)

dpg.create_viewport(title="Direct Share", width=1280, height=720)

with dpg.window(label="Example Window", no_title_bar=True, tag="fullscreen"):
    dpg.bind_font(default_font)
    dpg.add_text("Hello, world")
    dpg.add_button(label="search for peers", callback=find_wifi_p2p_peers)
    dpg.add_input_text(label="string", default_value="Quick brown fox")
    dpg.add_slider_float(label="float", default_value=0.273, max_value=1)

dpg.setup_dearpygui()
dpg.set_primary_window("fullscreen", True)
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
