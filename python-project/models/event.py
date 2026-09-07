from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional
from .person import Person
from .room import Room

@dataclass(frozen=True)
class Event:
    title: str
    start_time: datetime
    end_time: datetime
    participants: List[Person]
    room: Optional[Room] = None
