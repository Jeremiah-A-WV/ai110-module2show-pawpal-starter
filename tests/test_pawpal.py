import pytest
from datetime import datetime
from pawpal_system import Task, Pet

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
