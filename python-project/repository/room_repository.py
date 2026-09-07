"""
CSV Repository implementation for room data persistence.
This module handles loading room details from CSV storage, fulfilling the RoomRepositoryProtocol.
"""
import csv
from pathlib import Path
from typing import List

from models.room import Room
from interfaces.repository_protocols import RoomRepositoryProtocol

class RoomRepository(RoomRepositoryProtocol):

    def __init__(self, file_path: str):
        self.file_path = file_path

    def load_rooms(self) -> List[Room]:
        """
                Loads room data from the CSV file and constructs Room objects.

                :return: A list of Room objects.
                """
        rooms = []

        with open(self.file_path, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            for row in reader:
                room = Room(
                    room_id=row["room_id"],
                    capacity=int(row["capacity"])
                )

                rooms.append(room)

        return rooms