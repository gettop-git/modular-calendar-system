# Comp Calendar Scheduler

A Python calendar scheduling application designed with a robust, decoupled architecture adhering to SOLID principles and Dependency Injection. It finds suitable meeting times for multiple participants and selects an available meeting room efficiently.

## Features

The application can:

* Load calendar events and room data from CSV files using a decoupled Repository Pattern.
* Find time slots in which all requested participants are available.
* Support a customizable meeting duration.
* Check room availability during the requested time.
* Check whether a room has sufficient capacity for all participants.
* Select the most suitable available meeting time.
* Select the smallest suitable available room.
* Handle edge cases using clean Early Exit (Guard Clauses) patterns.
* Run automated unit tests with isolated mocks using `pytest`.

## Requirements

* Python 3.8 or higher
* pytest

## Project Structure

```text
python-project/
├── io_comp/
│   ├── __init__.py
│   └── app.py
│
├── models/
│   ├── __init__.py
│   ├── person.py
│   ├── event.py
│   ├── room.py
│   └── time_slot.py
│
├── interfaces/
│   ├── __init__.py
│   └── repository_protocols.py
│
├── repository/
│   ├── __init__.py
│   ├── csv_repository.py
│   └── room_repository.py
│
├── services/
│   ├── __init__.py
│   ├── calendar_service.py
│   └── room_service.py
│
├── resources/
│   ├── calendar.csv
│   └── rooms.csv
│
├── tests/
│   ├── __init__.py
│   └── test_app.py
│
├── requirements.txt
├── setup.py
└── README.md
```

## Data

### Calendar

The file `resources/calendar.csv` contains existing calendar events.

Each event contains:

* Person name
* Event name
* Start time
* End time
* Room ID

Example:

```csv
name,event,start,end,room_id
Alice,Morning meeting,8:00,9:30,Room A
```

### Rooms

The file `resources/rooms.csv` contains the available rooms and their capacities.

Example:

```csv
room_id,capacity
Room A,4
Room B,10
Room C,2
Room D,20
```

## Running the Application

From the project root, run:

```bash
python -m io_comp.app
```

The application asks the user to enter the meeting participants and the desired meeting duration.

Example:

```text
הכנס שמות משתתפים, מופרדים בפסיק: Alice, Jack, Bob
הכנס אורך פגישה בדקות: 30

הפגישה המומלצת:
זמן: 12:00 - 12:30
חדר: Room A, קיבולת: 4
```

The default working hours are **07:00–19:00**.

## Architecture & Design Patterns

The project is structured following professional software engineering standards:

* **Dependency Injection (DI)**: Services (`CalendarService`, `RoomService`) receive their data repositories via constructor injection, ensuring complete decoupling and high testability.
* **Repository Pattern & Protocols**: Data access is abstracted using Python `Protocols` (`interfaces/repository_protocols.py`), allowing seamless substitution between real data sources and mocks.
* **Early Exit**: Functions incorporate Guard Clauses at the entry points to handle edge cases immediately, improving code readability and performance.
* **Layered Architecture**:
  * **Models** — represent people, events, rooms, and time slots.
  * **Interfaces** — define contracts (Protocols) for data repositories.
  * **Repositories** — handle data loading from CSV files.
  * **Services** — contain business logic for scheduling (`CalendarService`) and room management (`RoomService`).
  * **Application** — orchestrates configuration and dependency wiring in `app.py`.
  * **Tests** — verify behavior using isolated `MagicMock` dependencies.

## Running Tests

The tests are located in:

```text
tests/test_app.py
```

To run all tests:

```bash
pytest
```

For detailed output:

```bash
pytest -v
```

The current test suite checks, among other things:

* Finding available time slots.
* Handling cases with no available time.
* Meeting duration and boundary conditions.
* Room capacity and occupancy checks.
* Selecting the best (smallest suitable) room.

## Testing Result

The test suite runs fully isolated with mock repositories.

Expected result:

```text
All tests passed successfully.
```