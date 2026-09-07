from dataclasses import dataclass
from datetime import datetime
from typing import List
from .room import Room

@dataclass(frozen=True)
class TimeSlot:
    start_time: datetime
    end_time: datetime
    available_rooms: List[Room]