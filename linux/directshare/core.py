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

> “What the app *means*”
"""

device_interface.on_peer_added(self.changed_notify)
device_interface.on_peer_removed(self.changed_notify)


async def update_peers_list(self):
    peers = await self.device_interface.get_peers()
    dpg.configure_item("Peer List", items=peers, show=True)
