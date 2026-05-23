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
        self.peers.append(peer)
        print(f"Peer added: {peer}")
        print(self.peers)

    def on_peer_removed(self, peer):
        self.peers = [p for p in self.peers if p != peer]
