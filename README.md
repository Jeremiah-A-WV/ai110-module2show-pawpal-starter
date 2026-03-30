# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app includes:

- Owner and pet profiles with task management
- A daily schedule generator that respects priority and time constraints
- Interactive Streamlit UI for managing owners, pets, tasks, and viewing schedules

## Features

### Core Scheduling Algorithms

- **Priority-Based Greedy Scheduling**: Tasks are assigned to time slots based on priority (High → Medium → Low) and due time, ensuring important tasks are scheduled first without backtracking.

- **Sorting by Due Time**: Tasks can be sorted chronologically using built-in comparison operators (`__lt__`, `__le__`). Tasks without due times are automatically placed at the end.

- **Intelligent Filtering**: 
  - Filter tasks by pet for focused pet-specific planning
  - Filter tasks by completion status (pending or completed) for progress tracking
  - Retrieve only upcoming tasks within a specified timeframe

- **Recurring Task Management**: 
  - Support for "Daily" and "Weekly" recurring tasks
  - Automatic next-occurrence calculation using `next_occurrence()` method
  - When a recurring task is marked complete, a new instance is automatically created for the next occurrence

- **Conflict Detection**: Lightweight detection algorithm that scans scheduled tasks for time overlaps, returning warnings to prevent double-booking. Conflicts don't crash the app—they're displayed as helpful UI warnings.

- **Calendar-Based Time Management**: Dedicated Calendar class handles:
  - Efficient storage of scheduled tasks (using heaps for optimization)
  - Conflict lookups for new task assignments
  - Daily schedule retrieval and organization

### User Interface Features

- Add and manage multiple pets with basic profiles (name, species, age)
- Add tasks with customizable duration, priority, and frequency
- View tasks sorted by time or filtered by pet/status
- Generate and display daily schedules in readable table format
- See conflict warnings with actionable suggestions when overlaps occur

### Data Integrity

- Duplicate prevention: No duplicate task IDs within a pet, no duplicate pet IDs per owner
- Automatic ID management with internal counters
- Task-to-pet linking via `pet_id` back-references for reliable data retrieval

## 📸 Demo

Check out the PawPal+ Streamlit interface in action:

![PawPal+ Streamlit App](image%20copy.png)

The app features an intuitive interface for managing pets, adding tasks, sorting and filtering by various criteria, and generating intelligent daily schedules with real-time conflict detection.

## Testing PawPal+

Run the test suite with: `python -m pytest`

The tests cover core behaviors including task completion, addition, sorting by time, recurring task auto-generation, and conflict detection. They verify happy paths (e.g., successful sorting) and edge cases (e.g., no tasks, overlapping schedules).

**Confidence Level**: ⭐⭐⭐⭐ (4/5 stars) - The system handles basic scheduling reliably, but more edge cases (e.g., large pet/task counts) could be tested for production use.

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
