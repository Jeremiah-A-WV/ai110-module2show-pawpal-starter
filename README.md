# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

## Smarter Scheduling

The PawPal+ system now includes advanced scheduling features for better pet care management:

- **Task Sorting and Filtering**: Tasks can be sorted by due time and filtered by pet or completion status for easy viewing.
- **Recurring Tasks**: Support for daily and weekly recurring tasks, with automatic generation of next instances when completed.
- **Conflict Detection**: Lightweight detection of overlapping scheduled tasks, providing warnings to avoid double-booking.
- **Intelligent Completion**: Marking a recurring task as complete automatically creates the next occurrence, keeping schedules up-to-date.
- **Calendar Management**: A dedicated Calendar class handles time-based operations, ensuring efficient scheduling and conflict checks.

These features make the app more robust and user-friendly, handling real-world pet care complexities without overwhelming the interface.

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.
