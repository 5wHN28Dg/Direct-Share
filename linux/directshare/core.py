# SPDX-FileCopyrightText: 2026 5wHN28Dg
# SPDX-License-Identifier: GPL-3.0-or-later

"""
Represents:
**Application brain**

Responsibility:

* Decide what happens when user clicks
* Maintain state (peers list, selected peer, status)
* Coordinate between UI and backend

It represents:

> "What the app *means*"
"""

from .backend import BackendInterface


class CoreApp:
    def __init__(self, backend: BackendInterface):
        self.backend = backend
        self.helper = None
        self.selected_peer = None
        self.peers = []
        self.trusted_peers = []
        self.active_transfers = {}

        self._peer_added_callbacks = []
        self._peer_removed_callbacks = []

    @classmethod
    async def create(cls, backend: BackendInterface):
        instance = cls(backend)

        instance.backend.on_peer_added(instance.on_peer_added)
        instance.backend.on_peer_removed(instance.on_peer_removed)

        await instance.backend.initialize()
        await instance.update_peers_list()
        return instance

    async def find_peers(self):
        await self.backend.find_peers()

    async def update_peers_list(self):
        self.peers = await self.backend.get_peers()

    def on_peer_added(self, peer):
        peer_path = peer["path"]

        if any(existing["path"] == peer_path for existing in self.peers):
            return

        self.peers.append(peer)

        for callback in self._peer_added_callbacks:
            callback(peer)

    def on_peer_removed(self, peer_path):
        self.peers = [peer for peer in self.peers if peer["path"] != peer_path]

        for callback in self._peer_removed_callbacks:
            callback(peer_path)

    def add_peer_added_callback(self, callback):
        self._peer_added_callbacks.append(callback)

    def add_peer_removed_callback(self, callback):
        self._peer_removed_callbacks.append(callback)
