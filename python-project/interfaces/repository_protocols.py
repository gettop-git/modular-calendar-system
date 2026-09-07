"""
Repository protocols defining interfaces for data access.
This module establishes contracts for loading and saving entities like rooms, people, and events,
ensuring loose coupling between the business logic and data storage layers.
"""

from typing import List, Protocol
from models.person import Person
from models.event import Event
from models.room import Room


class RoomRepositoryProtocol(Protocol):
    """Protocol for loading room data from a storage source."""

    def load_rooms(self) -> List[Room]:
        """Loads and returns a list of all available rooms."""
        ...


class CalendarRepositoryProtocol(Protocol):
    """Protocol for loading and saving calendar data, including people and events."""

    def load_people(self) -> List[Person]:
        """Loads and returns a list of people."""
        ...

    def load_events(self) -> List[Event]:
        """Loads and returns a list of scheduled events."""
        ...

    def save_event(self, event: Event) -> None:
        """Saves a new event to the storage source."""
        ...