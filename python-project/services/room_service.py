from datetime import datetime
from typing import List, Optional

from models.event import Event
from models.room import Room


class RoomService:
    def __init__(self, repository):
        self.repository = repository
    """Service for managing, filtering, and finding available rooms for meetings."""
    def get_best_room(
            self,
            available_rooms: List[Room],
            number_of_people: int
    ) -> Optional[Room]:
        """
                Selects the optimal room from the list of available rooms.
                The selection prioritizes the smallest room that fits at least the required number of people.

                :param available_rooms: List of available rooms to check.
                :param number_of_people: Number of participants in the meeting.
                :return: The best matching Room object, or None if no suitable room is found.
                """
        suitable_rooms = [room for room in available_rooms if room.capacity >= number_of_people]

        if not suitable_rooms:
            return None


        best_room = min(
            suitable_rooms,
            key=lambda room: room.capacity
        )

        return best_room

    def find_available_rooms(
            self,
            rooms: List[Room],
            number_of_people: int,
            start_time: datetime,
            end_time: datetime,
            events: List[Event]
    ) -> List[Room]:
        """
                Finds all available rooms meeting the capacity requirement during the requested time slot.

                :param rooms: List of all rooms in the system.
                :param number_of_people: Required room capacity.
                :param start_time: Meeting start time.
                :param end_time: Meeting end time.
                :param events: List of existing events to check for conflicts.
                :return: List of available rooms meeting the conditions.
                """

        if not rooms:
            return []
        available_rooms = []

        for room in rooms:

            if room.capacity < number_of_people:
                continue

            room_is_available = True


            for event in events:
                if event.room == room:
                    if (
                            event.start_time < end_time
                            and event.end_time > start_time
                    ):
                        room_is_available = False
                        break

            if room_is_available:
                available_rooms.append(room)

        return available_rooms