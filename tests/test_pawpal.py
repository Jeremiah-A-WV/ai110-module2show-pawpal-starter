import pytest
from datetime import datetime, timedelta
from pawpal_system import Task, Pet, Owner, Scheduler

def test_task_completion():
    """Verify that calling mark_complete() changes the task's status."""
    task = Task(
        id=1,
        description="Test task",
        duration_mins=30,
        priority="Medium",
        due_time=datetime.now(),
        frequency="Once",
        is_completed=False
    )
    assert not task.is_completed, "Task should not be completed initially"
    task.mark_complete()
    assert task.is_completed, "Task should be completed after calling mark_complete()"

def test_task_addition():
    """Verify that adding a task to a Pet increases that pet's task count."""
    pet = Pet(id=1, name="TestPet", species="Dog", age=2)
    initial_count = len(pet.tasks)
    assert initial_count == 0, "Pet should have no tasks initially"
    
    task = Task(
        id=1,
        description="Test task",
        duration_mins=15,
        priority="Low",
        due_time=datetime.now(),
        frequency="Once"
    )
    pet.add_task(task)
    assert len(pet.tasks) == initial_count + 1, "Pet's task count should increase by 1 after adding a task"
    assert pet.tasks[0].pet_id == pet.id, "Task should have the pet's ID set"

def test_task_sorting_by_time():
    """Verify tasks are sorted correctly by due time."""
    owner = Owner(name="TestOwner")
    pet = Pet(id=1, name="Buddy", species="Dog", age=3)
    owner.add_pet(pet)
    
    now = datetime.now()
    task1 = Task(id=1, description="Late task", duration_mins=30, priority="Low", due_time=now + timedelta(hours=2))
    task2 = Task(id=2, description="Early task", duration_mins=15, priority="High", due_time=now + timedelta(hours=1))
    task3 = Task(id=3, description="No time task", duration_mins=20, priority="Medium", due_time=None)
    
    pet.add_task(task1)
    pet.add_task(task2)
    pet.add_task(task3)
    
    scheduler = Scheduler(owner)
    sorted_tasks = scheduler.get_tasks_sorted_by_time()
    
    # Should be early, late, no time
    assert len(sorted_tasks) == 3
    assert sorted_tasks[0][1].description == "Early task"
    assert sorted_tasks[1][1].description == "Late task"
    assert sorted_tasks[2][1].description == "No time task"

def test_recurring_task_completion():
    """Verify marking a recurring task complete creates a new instance."""
    owner = Owner(name="TestOwner")
    pet = Pet(id=1, name="Buddy", species="Dog", age=3)
    owner.add_pet(pet)
    
    now = datetime.now()
    task = Task(id=1, description="Daily walk", duration_mins=30, priority="High", due_time=now.replace(hour=9, minute=0), frequency="Daily")
    pet.add_task(task)
    
    scheduler = Scheduler(owner)
    initial_task_count = len(pet.tasks)
    
    success = scheduler.mark_task_complete(1)
    assert success, "Marking complete should succeed"
    assert task.is_completed, "Task should be completed"
    assert len(pet.tasks) == initial_task_count + 1, "A new recurring instance should be added"
    
    new_task = pet.tasks[-1]
    assert new_task.description == task.description, "New task should have same description"
    assert new_task.frequency == "Daily", "New task should be recurring"
    assert new_task.due_time == task.next_occurrence(now), "New task should have next occurrence time"

def test_conflict_detection():
    """Verify Scheduler detects conflicts in scheduled tasks."""
    owner = Owner(name="TestOwner")
    pet = Pet(id=1, name="Buddy", species="Dog", age=3)
    owner.add_pet(pet)
    
    now = datetime.now()
    task1 = Task(id=1, description="Task 1", duration_mins=60, priority="High", due_time=now.replace(hour=9, minute=0))
    task2 = Task(id=2, description="Task 2", duration_mins=30, priority="Medium", due_time=now.replace(hour=9, minute=30))  # Overlaps
    
    pet.add_task(task1)
    pet.add_task(task2)
    
    scheduler = Scheduler(owner)
    schedule = scheduler.generate_daily_schedule(now.replace(hour=8, minute=0))
    
    conflicts = scheduler.detect_basic_conflicts()
    assert len(conflicts) > 0, "Conflicts should be detected for overlapping tasks"
    # Assuming the schedule assigns overlapping times
    found_conflict = any(t1.description in ["Task 1", "Task 2"] and t2.description in ["Task 1", "Task 2"] for t1, t2 in conflicts)
    assert found_conflict, "Specific tasks should be in conflicts"
