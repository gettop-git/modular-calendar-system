from datetime import datetime
from unittest.mock import MagicMock
import pytest

from models.person import Person
from models.room import Room
from models.event import Event
from services.calendar_service import CalendarService
from services.room_service import RoomService


def test_find_available_slots_basic_success():
    # Arrange
    mock_repo = MagicMock()
    service = CalendarService(repository=mock_repo)
    person = Person(name="Alice")
    events = [
        Event(
            title="Meeting 1",
            start_time=datetime.strptime("09:00", "%H:%M"),
            end_time=datetime.strptime("10:00", "%H:%M"),
            participants=[person]
        )
    ]

    # Act
    slots = service.find_available_slots(
        people=[person],
        events=events,
        duration_minutes=60,
        work_start_hour="08:00",
        work_end_hour="11:00"
    )

    # Assert
    slot_times = [(s.start_time.strftime("%H:%M"), s.end_time.strftime("%H:%M")) for s in slots]
    assert ("08:00", "09:00") in slot_times
    assert ("10:00", "11:00") in slot_times
    assert len(slots) == 2


def test_find_available_slots_no_time_available():
    # Arrange
    mock_repo = MagicMock()
    service = CalendarService(repository=mock_repo)
    person = Person(name="Bob")
    events = [
        Event(
            title="All Day Meeting",
            start_time=datetime.strptime("07:00", "%H:%M"),
            end_time=datetime.strptime("19:00", "%H:%M"),
            participants=[person]
        )
    ]

    # Act
    slots = service.find_available_slots(
        people=[person],
        events=events,
        duration_minutes=60,
        work_start_hour="07:00",
        work_end_hour="19:00"
    )

    # Assert
    assert len(slots) == 0


def test_find_available_slots_single_person_no_events():
    # Arrange
    mock_repo = MagicMock()
    service = CalendarService(repository=mock_repo)
    person = Person(name="Charlie")
    events = []

    # Act
    slots = service.find_available_slots(
        people=[person],
        events=events,
        duration_minutes=120,
        work_start_hour="08:00",
        work_end_hour="12:00"
    )

    # Assert
    assert len(slots) == 2
    assert slots[0].start_time.strftime("%H:%M") == "08:00"
    assert slots[0].end_time.strftime("%H:%M") == "10:00"
    assert slots[1].start_time.strftime("%H:%M") == "10:00"
    assert slots[1].end_time.strftime("%H:%M") == "12:00"


def test_find_available_rooms_capacity_and_availability():
    # Arrange
    mock_repo = MagicMock()
    room_service = RoomService(repository=mock_repo)
    room_small = Room(room_id="R1", capacity=2)
    room_large = Room(room_id="R2", capacity=10)
    rooms = [room_small, room_large]

    person = Person(name="Dave")
    event = Event(
        title="Blocked Room",
        start_time=datetime.strptime("10:00", "%H:%M"),
        end_time=datetime.strptime("11:00", "%H:%M"),
        participants=[person],
        room=room_large
    )

    # Act - Requesting room for 5 people during the blocked time
    available = room_service.find_available_rooms(
        rooms=rooms,
        number_of_people=5,
        start_time=datetime.strptime("10:30", "%H:%M"),
        end_time=datetime.strptime("11:30", "%H:%M"),
        events=[event]
    )

    # Assert - room_small capacity is too low (2 < 5), room_large is busy during this time
    assert len(available) == 0


def test_get_best_room_selects_smallest_suitable():
    # Arrange
    mock_repo = MagicMock()
    room_service = RoomService(repository=mock_repo)
    room_a = Room(room_id="A", capacity=5)
    room_b = Room(room_id="B", capacity=20)
    room_c = Room(room_id="C", capacity=50)
    rooms = [room_c, room_a, room_b]

    # Act
    best_room = room_service.get_best_room(available_rooms=rooms, number_of_people=10)

    # Assert
    assert best_room is not None
    assert best_room.room_id == "B"
    assert best_room.capacity == 20


def test_get_top_slots_ranking():
    # Arrange
    mock_repo = MagicMock()
    service = CalendarService(repository=mock_repo)
    person = Person(name="Eve")
    # Event at 09:00 - 10:00 creates a boundary
    events = [
        Event(
            title="Meeting",
            start_time=datetime.strptime("09:00", "%H:%M"),
            end_time=datetime.strptime("10:00", "%H:%M"),
            participants=[person]
        )
    ]

    # Let's generate slots manually or via service
    slots = service.find_available_slots(
        people=[person],
        events=events,
        duration_minutes=30,
        work_start_hour="08:00",
        work_end_hour="12:00"
    )

    # Act
    top_slots = service.get_top_slots(available_slots=slots, events=events, limit=2)

    # Assert
    assert len(top_slots) == 2