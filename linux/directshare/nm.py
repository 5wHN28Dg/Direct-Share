import uuid

from dbus_fast import BusType, Variant
from dbus_fast.aio import MessageBus


class NMClient:
    async def __init__(self):
        self.bus = await MessageBus(bus_type=BusType.SYSTEM).connect()

        introspection = await self.bus.introspect(
            "org.freedesktop.NetworkManager", "/org/freedesktop/NetworkManager"
        )

        service_obj = self.bus.get_proxy_object(
            "org.freedesktop.NetworkManager",
            "/org/freedesktop/NetworkManager",
            introspection,
        )

        self.interface = service_obj.get_interface("org.freedesktop.NetworkManager")

        devices = await self.interface.get_devices()
        for device in devices:
            self.device_obj = self.bus.get_proxy_object(
                "org.freedesktop.NetworkManager",
                device,
                await self.bus.introspect("org.freedesktop.NetworkManager", device),
            )
            device_interface = self.device_obj.get_interface(
                "org.freedesktop.NetworkManager.Device"
            )
            if await device_interface.get_device_type() == 30:
                print("Found WiFiP2P device, it is:", device, "you are good to go")
                break

    async def find_wifi_p2p_peers(self):
        device_interface = self.device_obj.get_interface(
            "org.freedesktop.NetworkManager.Device.WifiP2P"
        )
        # device_interface.on_peer_added(self.changed_notify)
        # device_interface.on_peer_removed(self.changed_notify)
        await device_interface.call_start_find({})

    async def connect_to_peer(self, peer_path):
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
            ) = await self.interface.call_add_and_activate_connection2(
                connection_settings,
                self.device_obj.path,
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
    # if peer:
    #   asyncio.run_coroutine_threadsafe(connect_to_peer(peer), async_loop)
    # else:
    #   print("No peer selected.")
