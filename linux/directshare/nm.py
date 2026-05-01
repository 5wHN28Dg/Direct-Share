# SPDX-FileCopyrightText: 2026 5wHN28Dg
# SPDX-License-Identifier: GPL-3.0-or-later

import asyncio
import uuid

from dbus_fast import BusType, Variant
from dbus_fast.aio import MessageBus


class NMClient:
    async def __init__(self):
        self.bus = await MessageBus(bus_type=BusType.SYSTEM).connect()

        login1 = self.bus.get_proxy_object(
            "org.freedesktop.login1",
            "/org/freedesktop/login1",
            await self.bus.introspect(
                "org.freedesktop.login1", "/org/freedesktop/login1"
            ),
        )
        manager = login1.get_interface("org.freedesktop.login1.Manager")
        manager.on_prepare_for_sleep(self._on_prepare_for_sleep)

        introspection = await self.bus.introspect(
            "org.freedesktop.NetworkManager", "/org/freedesktop/NetworkManager"
        )

        nm_service_obj = self.bus.get_proxy_object(
            "org.freedesktop.NetworkManager",
            "/org/freedesktop/NetworkManager",
            introspection,
        )

        self.nm_interface = nm_service_obj.get_interface(
            "org.freedesktop.NetworkManager"
        )
        await self.discover_wifi_p2p_device()

    async def discover_wifi_p2p_device(self):
        devices = await self.nm_interface.get_devices()
        wifi_p2p_devices = []
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
                wifi_p2p_devices.append(device)

        self.wifi_p2p_device = (
            wifi_p2p_devices[0] if len(wifi_p2p_devices) >= 1 else None
        )

    async def _on_prepare_for_sleep(self, sleeping: bool):
        if not sleeping:  # waking up
            await asyncio.sleep(2)
            await self.discover_wifi_p2p_device()

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
            ) = await self.nm_interface.call_add_and_activate_connection2(
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
