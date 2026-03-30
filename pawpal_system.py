from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List, Tuple, Optional, Dict
import heapq

@dataclass
class Task:
    id: int
    description: str
    duration_mins: int
    priority: str
    due_time: Optional[datetime] = None
    frequency: str = "Once"
    is_completed: bool = False
    pet_id: Optional[int] = None  # Back-reference to pet
    start_time: Optional[datetime] = None  # Scheduled start time

    def mark_complete(self):
        """Marks the task as completed."""
        self.is_completed = True

    def is_recurring(self) -> bool:
        """Checks if the task is recurring."""
        return self.frequency != "Once"

    def next_occurrence(self, after: datetime) -> Optional[datetime]:
        """Returns the next occurrence of the task after the given time."""
        if not self.is_recurring():
            return self.due_time if self.due_time and self.due_time > after else None
        # Simple recurring logic: assume daily for now
        if self.frequency == "Daily":
            next_time = self.due_time
            while next_time and next_time <= after:
                next_time += timedelta(days=1)
            return next_time
        return self.due_time

@dataclass
class Pet:
    id: int  # Add unique ID
    name: str
    species: str
    age: int
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task):
        """Adds a task to the pet if it doesn't already exist."""
        if task.id in [t.id for t in self.tasks]:
            raise ValueError(f"Task with id {task.id} already exists for pet {self.name}")
        task.pet_id = self.id
        self.tasks.append(task)

@dataclass
class Owner:
    name: str
    pets: List[Pet] = field(default_factory=list)
    _next_pet_id: int = field(default=1, init=False)

    def add_pet(self, pet: Pet):
        """Adds a pet to the owner if it doesn't already exist."""
        if pet.id in [p.id for p in self.pets]:
            raise ValueError(f"Pet with id {pet.id} already exists for owner {self.name}")
        self.pets.append(pet)

    def get_all_tasks(self) -> List[Task]:
        """Returns all tasks across all pets."""
        return [task for pet in self.pets for task in pet.tasks]

class Calendar:
    def __init__(self):
        self.scheduled: List[Tuple[datetime, Task]] = []  # Min-heap for start times

    def add_scheduled_task(self, task: Task):
        """Adds a scheduled task to the calendar."""
        if task.start_time:
            heapq.heappush(self.scheduled, (task.start_time, task))

    def get_conflicts(self, new_task: Task) -> List[Task]:
        """Returns a list of tasks that conflict with the given new task."""
        if not new_task.start_time:
            return []
        end_time = new_task.start_time + timedelta(minutes=new_task.duration_mins)
        conflicts = []
        for start, task in self.scheduled:
            if task.start_time < end_time and start < (new_task.start_time + timedelta(minutes=new_task.duration_mins)):
                conflicts.append(task)
        return conflicts

    def get_schedule_for_day(self, date: datetime) -> List[Tuple[datetime, Task]]:
        """Returns the schedule for the given day."""
        start_of_day = date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = start_of_day + timedelta(days=1)
        return [(start, task) for start, task in self.scheduled if start_of_day <= start < end_of_day]

class Scheduler:
    
    def __init__(self, owner: Owner):
        """Initializes the scheduler with an owner."""
        self.owner = owner
        self.calendar = Calendar()
        self._task_id_counter = max((t.id for p in owner.pets for t in p.tasks), default=0) + 1

    def get_all_tasks(self) -> List[Tuple[str, Task]]:
        """Returns all tasks with their pet names."""
        tasks = []
        for pet in self.owner.pets:
            for task in pet.tasks:
                tasks.append((pet.name, task))
        return tasks

    def get_upcoming_tasks(self, within_hours: int = 24) -> List[Tuple[str, Task]]:
        """Returns upcoming tasks within the next 24 hours."""
        now = datetime.now()
        cutoff = now + timedelta(hours=within_hours)
        upcoming = []
        for pet in self.owner.pets:
            for task in pet.tasks:
                if task.due_time and now <= task.due_time <= cutoff and not task.is_completed:
                    upcoming.append((pet.name, task))
                elif task.is_recurring():
                    next_occ = task.next_occurrence(now)
                    if next_occ and next_occ <= cutoff:
                        upcoming.append((pet.name, task))
        return sorted(upcoming, key=lambda x: x[1].due_time or datetime.max)

    def check_conflicts(self, new_task: Task) -> bool:
        """Checks if the new task conflicts with existing scheduled tasks."""
        return len(self.calendar.get_conflicts(new_task)) > 0

    def generate_daily_schedule(self, start_time: datetime) -> List[Tuple[str, Task, datetime]]:
        """Generates a daily schedule starting from the given time."""
        # Simple greedy scheduler: sort by priority and due time, assign sequentially
        day_start = start_time.replace(hour=0, minute=0, second=0, microsecond=0)
        day_end = day_start + timedelta(days=1)
        available_tasks = []
        for pet in self.owner.pets:
            for task in pet.tasks:
                if not task.is_completed and task.due_time and day_start <= task.due_time < day_end:
                    available_tasks.append((pet.name, task))
                elif task.is_recurring():
                    next_occ = task.next_occurrence(day_start)
                    if next_occ and day_start <= next_occ < day_end:
                        # Create a temporary instance
                        instance = Task(
                            id=self._task_id_counter,
                            description=task.description,
                            duration_mins=task.duration_mins,
                            priority=task.priority,
                            due_time=next_occ,
                            frequency="Once",  # Instance is once
                            pet_id=task.pet_id
                        )
                        self._task_id_counter += 1
                        available_tasks.append((pet.name, instance))

        # Sort by priority (assume High > Medium > Low) and due time
        priority_order = {"High": 0, "Medium": 1, "Low": 2}
        available_tasks.sort(key=lambda x: (priority_order.get(x[1].priority, 3), x[1].due_time or datetime.max))

        schedule = []
        current_time = start_time
        for pet_name, task in available_tasks:
            if current_time + timedelta(minutes=task.duration_mins) > day_end:
                continue  # Skip if doesn't fit
            task.start_time = current_time
            schedule.append((pet_name, task, current_time))
            self.calendar.add_scheduled_task(task)
            current_time += timedelta(minutes=task.duration_mins)

        return schedule