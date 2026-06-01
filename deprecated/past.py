import asyncio
import threading
import uuid

import dearpygui.dearpygui as dpg
from dbus_fast import BusType, Variant
from dbus_fast.aio import MessageBus

async_loop = asyncio.new_event_loop()


def start_async_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()


threading.Thread(target=start_async_loop, args=(async_loop,), daemon=True).start()

peer = ""


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
    global interface
    interface = service_obj.get_interface("org.freedesktop.NetworkManager")

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


def search_callback():
    async def find_wifi_p2p_peers():
        global device_interface
        device_interface = device_obj.get_interface(
            "org.freedesktop.NetworkManager.Device.WifiP2P"
        )
        device_interface.on_peer_added(changed_notify)
        device_interface.on_peer_removed(changed_notify)
        await device_interface.call_start_find({})

    asyncio.run_coroutine_threadsafe(find_wifi_p2p_peers(), async_loop)


def peers_list_callback():
    async def update_peers_list():
        peers = await device_interface.get_peers()
        dpg.configure_item("Peer List", items=peers, show=True)

    asyncio.run_coroutine_threadsafe(update_peers_list(), async_loop)


def connect_callback(sender, app_data):
    async def connect_to_peer(peer_path):
        """Asynchronously initiates a Wi-Fi P2P connection to a selected peer."""
        # For AddAndActivateConnection2, we need to create a transient connection
        # profile. This dictionary defines the new connection.
        connection_settings = {
            "connection": {
                "id": Variant("s", "Direct Share P2P"),
                "uuid": Variant("s", str(uuid.uuid4())),
                "type": Variant("s", "wifi-p2p"),
            }
        }

        try:
            print(f"Attempting to connect to peer: {peer_path}")
            # The call requires the connection settings, the object path of the
            # P2P-capable device, the object path of the peer, and any options.
            (
                path,
                active_connection,
                result,
            ) = await interface.call_add_and_activate_connection2(
                connection_settings,
                device_obj.path,
                peer_path,
                {"persist": Variant("s", "volatile")},
            )
            print("Successfully initiated connection.")
            print(f"  Connection Path: {path}")
            print(f"  Active Connection: {active_connection}")
            print(f"  Result: {result}")
        except Exception as e:
            # Catch and print any exceptions during the connection attempt.
            print(f"Error connecting to peer: {e}")

    # Ensure a peer is selected before trying to connect.
    if peer:
        asyncio.run_coroutine_threadsafe(connect_to_peer(peer), async_loop)
    else:
        print("No peer selected.")


def callback(sender, app_data):
    print("OK was clicked.")
    print("Sender: ", sender)
    print("App Data: ", app_data)

    if sender == "Peer List":
        global peer
        peer = app_data


def cancel_callback(sender, app_data):
    print("Cancel was clicked.")
    print("Sender: ", sender)
    print("App Data: ", app_data)


def changed_notify(new_value):
    print(f"The new peer: {new_value}")
    peers_list_callback()


asyncio.run_coroutine_threadsafe(main(), async_loop)
dpg.create_context()

# add a font registry
with dpg.font_registry():
    # first argument ids the path to the .ttf or .otf file
    default_font = dpg.add_font("font/ProggyVector-Regular.otf", 75)

dpg.create_viewport(title="Direct Share", width=1280, height=720)

with dpg.window(label="Example Window", no_title_bar=True, tag="Main Window"):
    dpg.bind_font(default_font)
    dpg.add_button(label="search for peers", callback=search_callback)
    dpg.add_listbox(items=[], callback=callback, tag="Peer List", show=False)

    with dpg.file_dialog(
        show=False,
        callback=callback,
        tag="file_dialog_id",
        cancel_callback=cancel_callback,
        width=1280,
        height=720,
    ):
        dpg.add_file_extension(".*")
        dpg.add_file_extension("", color=(150, 255, 150, 255))
        dpg.add_file_extension(
            "Source files (*.cpp *.h *.hpp){.cpp,.h,.hpp}", color=(0, 255, 255, 255)
        )
        dpg.add_file_extension(".h", color=(255, 0, 255, 255), custom_text="[header]")
        dpg.add_file_extension(".py", color=(0, 255, 0, 255), custom_text="[Python]")
    dpg.add_button(
        label="file Selector", callback=lambda: dpg.show_item("file_dialog_id")
    )
    dpg.add_button(label="connect", callback=connect_callback)
    dpg.add_button(label="send")
dpg.setup_dearpygui()
dpg.set_primary_window("Main Window", True)
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
