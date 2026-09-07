"""
Calendar business logic service.
This module manages calendar scheduling operations, including finding available time slots
and scoring or ranking the best slots for meetings.
"""
from datetime import datetime, timedelta
from typing import List, Optional

from models.person import Person
from models.event import Event
from models.time_slot import TimeSlot
from models.room import Room
from services.room_service import RoomService
from config import Config
from interfaces.repository_protocols import CalendarRepositoryProtocol


class CalendarService:
    """Service for calculating available meeting time slots and ranking preferred meeting times."""
    def __init__(self, repository: CalendarRepositoryProtocol, room_service: Optional[RoomService] = None):
        self.repository = repository
        self.room_service = room_service

    def find_available_slots(
            self,
            people: List[Person],
            events: List[Event],
            duration_minutes: int,
            work_start_hour: str = Config.WORK_START_HOUR,
            work_end_hour: str = Config.WORK_END_HOUR,
            rooms: Optional[List[Room]] = None,
            number_of_people: int = 0
    ) -> List[TimeSlot]:
        """
                Finds available time slots for a given group of people within the working hours,
                accounting for existing events and room availability.

                :param people: List of participants required for the meeting.
                :param events: List of existing events to check for schedule conflicts.
                :param duration_minutes: Required duration of the meeting in minutes.
                :param work_start_hour: Start time of the workday (format "HH:MM").
                :param work_end_hour: End time of the workday (format "HH:MM").
                :param rooms: Optional list of rooms to check for availability during slots.
                :param number_of_people: Number of attendees requiring a room.
                :return: A list of available TimeSlot objects.
                """

        if not people:
            return []
        start_work = datetime.strptime(work_start_hour, "%H:%M")
        end_work = datetime.strptime(work_end_hour, "%H:%M")

        target_people_names = {person.name for person in people}


        busy_intervals = []
        for event in events:
            if any(p.name in target_people_names for p in event.participants):
                busy_intervals.append((event.start_time, event.end_time))

        busy_intervals.sort(key=lambda interval: interval[0])

        available_slots = []
        current_time = start_work
        step = timedelta(minutes=duration_minutes)


        def generate_slots_in_gap(gap_start: datetime, gap_end: datetime):
            slot_start = gap_start
            while slot_start + step <= gap_end:
                slot_end = slot_start + step

                available_rooms = []
                if rooms is not None:
                    # שימוש ב-RoomService לבדיקת חדרים פנויים
                    available_rooms = self.room_service.find_available_rooms(
                        rooms=rooms,
                        number_of_people=number_of_people,
                        start_time=slot_start,
                        end_time=slot_end,
                        events=events
                    )

                available_slots.append(
                    TimeSlot(
                        start_time=slot_start,
                        end_time=slot_end,
                        available_rooms=available_rooms
                    )
                )
                slot_start = slot_end


        for busy_start, busy_end in busy_intervals:
            if current_time < busy_start:
                generate_slots_in_gap(current_time, busy_start)
            if current_time < busy_end:
                current_time = busy_end


        if current_time < end_work:
            generate_slots_in_gap(current_time, end_work)

        return available_slots

    def get_top_slots(
            self,
            available_slots: List[TimeSlot],
            events: List[Event],
            limit: int = 4
    ) -> List[TimeSlot]:
        """
                Ranks and returns the top preferred available time slots based on heuristics
                such as adjacency to existing meetings, round hours, and proximity to mid-day.

                :param available_slots: List of available time slots to rank.
                :param events: List of existing events used for adjacency scoring.
                :param limit: Maximum number of top slots to return.
                :return: A sorted list of top-ranked TimeSlot objects.
                """
        if not available_slots:
            return []

        work_start = datetime.strptime(Config.WORK_START_HOUR, "%H:%M")
        work_end = datetime.strptime(Config.WORK_END_HOUR, "%H:%M")
        middle_of_day = work_start + (work_end - work_start) / 2

        busy_boundaries = set()
        for event in events:
            busy_boundaries.add(event.start_time)
            busy_boundaries.add(event.end_time)

        def calculate_score(slot: TimeSlot):
            is_adjacent = (slot.start_time in busy_boundaries) or (slot.end_time in busy_boundaries)
            is_nice_time = 1 if slot.start_time.minute in (0, 30) else 0
            slot_middle = slot.start_time + (slot.end_time - slot.start_time) / 2
            distance_from_middle = abs(slot_middle - middle_of_day).total_seconds()
            early_score = (slot.start_time - work_start).total_seconds()

            return (
                is_nice_time,
                0 if is_adjacent else 1,
                -distance_from_middle,
                -early_score
            )

        sorted_slots = sorted(available_slots, key=calculate_score, reverse=True)
        return sorted_slots[:limit]

