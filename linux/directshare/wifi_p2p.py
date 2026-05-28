# SPDX-FileCopyrightText: 2026 5wHN28Dg
# SPDX-License-Identifier: GPL-3.0-or-later

import asyncio

from .backend import BackendInterface
from .nm import NMClient


class WifiDirectBackend(BackendInterface):
    def __init__(self):
        self.nm = None

        self._core_peer_added_cb = None
        self._core_peer_removed_cb = None

        self._tasks = set()

    async def initialize(self):
        self.nm = await NMClient.create()

        self.nm.on_peer_added(self._handle_nm_peer_added)
        self.nm.on_peer_removed(self._handle_nm_peer_removed)

    async def find_peers(self):
        await self.nm.find_peers()

    async def get_peers(self):
        return await self.nm.get_peers()

    async def connect_to_peer(self, peer_identifier):
        await self.nm.connect_to_peer(peer_identifier)

    def on_peer_added(self, callback):
        self._core_peer_added_cb = callback

    def on_peer_removed(self, callback):
        self._core_peer_removed_cb = callback

    def on_connection_requested(self, callback):
        pass  # To be implemented when Helper is ready

    def _handle_nm_peer_added(self, peer_path):
        task = asyncio.create_task(self._emit_peer_added(peer_path))
        self._tasks.add(task)
        task.add_done_callback(self._tasks.discard)

    async def _emit_peer_added(self, peer_path):
        peer = await self.nm.get_peer_info(peer_path)
        peer["path"] = peer_path

        if self._core_peer_added_cb:
            self._core_peer_added_cb(peer)

    def _handle_nm_peer_removed(self, peer_path):
        if self._core_peer_removed_cb:
            self._core_peer_removed_cb(peer_path)
