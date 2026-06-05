# SPDX-FileCopyrightText: 2026 5wHN28Dg
# SPDX-License-Identifier: GPL-3.0-or-later

from abc import ABC, abstractmethod
from typing import Any, Callable, List


class BackendInterface(ABC):
    """
    The unified contract for Wi-Fi Direct operations.
    CoreApp depends ONLY on this interface.
    """

    @abstractmethod
    async def initialize(self) -> None:
        """Set up necessary D-Bus connections or background services."""
        pass

    @abstractmethod
    async def find_peers(self) -> None:
        pass

    @abstractmethod
    async def get_peers(self) -> List[Any]:
        pass

    @abstractmethod
    async def connect_to_peer(self, peer_identifier: str) -> None:
        pass

    @abstractmethod
    def on_peer_added(self, callback: Callable[[Any], None]) -> None:
        pass

    @abstractmethod
    def on_peer_removed(self, callback: Callable[[Any], None]) -> None:
        pass

    @abstractmethod
    def on_connection_requested(self, callback: Callable[[str, str], None]) -> None:
        """Fired when another device tries to connect to us (handled by helper)."""
        pass
