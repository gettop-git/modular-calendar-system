from pathlib import Path

from repository.csv_repository import CsvRepository
from repository.room_repository import RoomRepository
from services.calendar_service import CalendarService
from services.room_service import RoomService
from models.person import Person
from models.event import Event

def main():
    project_root = Path(__file__).resolve().parent.parent

    csv_path = project_root / "resources" / "calendar.csv"
    rooms_path = project_root / "resources" / "rooms.csv"

    room_repo = RoomRepository(str(rooms_path))
    rooms = room_repo.load_rooms()

    csv_repo = CsvRepository(
        file_path=str(csv_path),
        rooms=rooms
    )
    events = csv_repo.load_events()
    people = csv_repo.load_people()

    room_service = RoomService(repository=room_repo)
    calendar_service = CalendarService(repository=csv_repo, room_service=room_service)

    event_title = input("Enter the event title/purpose: ")
    duration = int(input("Enter meeting duration in minutes (e.g., 60): "))
    participant_names = input("Enter participant names (comma-separated): ").split(",")
    participant_names = [name.strip() for name in participant_names]

    selected_people = [p for p in people if p.name in participant_names]

    all_slots = calendar_service.find_available_slots(
        people=selected_people,
        events=events,
        duration_minutes=duration,
        rooms=rooms,
        number_of_people=len(selected_people)
    )

    top_slots = calendar_service.get_top_slots(all_slots, events, limit=4)

    if not top_slots:
        print("No suitable available time slots found.")
    else:
        print("\n--- Choose the most convenient time ---")
        for idx, slot in enumerate(top_slots, start=1):
            start_str = slot.start_time.strftime("%H:%M")
            end_str = slot.end_time.strftime("%H:%M")
            rooms_str = ", ".join([r.room_id for r in slot.available_rooms]) if slot.available_rooms else "No room"
            print(f"{idx}. Time: {start_str} - {end_str} | Available rooms: {rooms_str}")

        choice = int(input("\nEnter the number of the desired option (1-4): ")) - 1
        chosen_slot = top_slots[choice]

        available_rooms = room_service.find_available_rooms(
            rooms=chosen_slot.available_rooms,
            number_of_people=len(selected_people),
            start_time=chosen_slot.start_time,
            end_time=chosen_slot.end_time,
            events=events
        )
        chosen_room = room_service.get_best_room(
            available_rooms=available_rooms,
            number_of_people=len(selected_people)
        )

        new_event = Event(
            title=event_title,
            start_time=chosen_slot.start_time,
            end_time=chosen_slot.end_time,
            participants=selected_people,
            room=chosen_room
        )

        csv_repo.save_event(new_event)
        print(f"\nEvent '{event_title}' successfully saved to the calendar!")

if __name__ == "__main__":
    main()