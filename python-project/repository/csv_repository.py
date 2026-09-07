
"""
CSV Repository implementation for calendar data persistence.
This module handles reading and writing people and events data using CSV file storage,
fulfilling the CalendarRepositoryProtocol.
"""
import csv
from datetime import datetime
from pathlib import Path
from typing import List

from models.person import Person
from models.event import Event
from models.room import Room
from interfaces.repository_protocols import CalendarRepositoryProtocol

class CsvRepository(CalendarRepositoryProtocol):
    
    def __init__(self, file_path: Path, rooms: List[Room]):
        """
                Initializes the CsvRepository with a target file path and a list of rooms.

                :param file_path: Path to the CSV file containing calendar data.
                :param rooms: List of rooms available for event assignment.
                """
        self.file_path = file_path
        self.rooms = rooms

    def load_people(self) -> List[Person]:
        people = []

        with open(self.file_path, mode="r", encoding="utf-8") as f:
            """
                    Loads and extracts unique people from the CSV file.

                    :return: A list of Person objects.
                    """
            reader = csv.DictReader(f)

            for row in reader:
                person = Person(name=row["name"])
                people.append(person)

        return people

    def load_events(self) -> List[Event]:
        """
                Loads scheduled events along with their participants and rooms from the CSV file.

                :return: A list of Event objects.
                """
        events = []
        people = {}

        rooms_dict = {room.room_id: room for room in self.rooms}

        with open(self.file_path, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            for row in reader:
                name = row["name"]

                if name not in people:
                    people[name] = Person(name=name)

                person = people[name]

                room_id = row.get("room_id")
                room = rooms_dict.get(room_id)

                start_time = datetime.strptime(row["start"], "%H:%M")
                end_time = datetime.strptime(row["end"], "%H:%M")

                event = Event(
                    title=row["event"],
                    start_time=start_time,
                    end_time=end_time,
                    participants=[person],
                    room=room
                )

                events.append(event)

        return events

    def save_event(self, event: Event):
        """
                Appends a new event record to the CSV file.

                :param event: The Event object to save.
                """
        with open(self.file_path, mode="a", encoding="utf-8", newline="") as f:
            room_id = event.room.room_id if event.room else ""
            start_str = event.start_time.strftime("%H:%M")
            end_str = event.end_time.strftime("%H:%M")

            seen_names = set()
            for person in event.participants:
                if person.name not in seen_names:
                    seen_names.add(person.name)

                    f.write(f"{person.name},{event.title},{start_str},{end_str},{room_id}\n")
