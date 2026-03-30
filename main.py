from pawpal_system import Owner, Pet, Task, Scheduler
from datetime import datetime, timedelta

# Create an Owner
owner = Owner(name="John Doe")

# Create two Pets
pet1 = Pet(id=1, name="Buddy", species="Dog", age=3)
pet2 = Pet(id=2, name="Whiskers", species="Cat", age=2)

# Add pets to owner
owner.add_pet(pet1)
owner.add_pet(pet2)

# Create Tasks out of order (different due times)
now = datetime.now()
task1 = Task(
    id=1,
    description="Evening play",
    duration_mins=45,
    priority="Low",
    due_time=now.replace(hour=18, minute=0, second=0, microsecond=0),
    frequency="Once"
)
task2 = Task(
    id=2,
    description="Morning walk",
    duration_mins=30,
    priority="High",
    due_time=now.replace(hour=9, minute=0, second=0, microsecond=0),
    frequency="Daily"
)
task3 = Task(
    id=3,
    description="Feed pet",
    duration_mins=15,
    priority="Medium",
    due_time=now.replace(hour=14, minute=0, second=0, microsecond=0),
    frequency="Daily"
)
task4 = Task(
    id=4,
    description="Afternoon nap",
    duration_mins=60,
    priority="Low",
    due_time=None,  # No due time
    frequency="Once"
)
task5 = Task(
    id=5,
    description="Morning grooming",
    duration_mins=30,
    priority="Medium",
    due_time=now.replace(hour=9, minute=0, second=0, microsecond=0),  # Same as task2
    frequency="Once"
)

# Add tasks to pets (out of order)
pet1.add_task(task1)  # Evening
pet2.add_task(task2)  # Morning
pet1.add_task(task3)  # Afternoon
pet2.add_task(task4)  # No time
pet1.add_task(task5)  # Morning, same time as task2

# Create Scheduler
scheduler = Scheduler(owner)

# Demonstrate sorting and filtering
print("All Tasks (unsorted):")
for pet_name, task in scheduler.get_all_tasks():
    due = task.due_time.strftime('%H:%M') if task.due_time else 'No time'
    print(f"- {pet_name}: {task.description} at {due}")

print("\nTasks Sorted by Time:")
for pet_name, task in scheduler.get_tasks_sorted_by_time():
    due = task.due_time.strftime('%H:%M') if task.due_time else 'No time'
    print(f"- {pet_name}: {task.description} at {due}")

print("\nTasks Filtered by Pet (Buddy):")
for task in scheduler.get_tasks_filtered_by_pet("Buddy"):
    due = task.due_time.strftime('%H:%M') if task.due_time else 'No time'
    print(f"- {task.description} at {due}")

print("\nTasks Filtered by Status (Pending):")
for pet_name, task in scheduler.get_tasks_filtered_by_status(False):
    due = task.due_time.strftime('%H:%M') if task.due_time else 'No time'
    print(f"- {pet_name}: {task.description} at {due}")

print("\nRecurring Tasks Instances (next 2 days):")
start = now.replace(hour=0, minute=0, second=0, microsecond=0)
end = start + timedelta(days=2)
for pet_name, task, occ_time in scheduler.handle_recurring_tasks(start, end):
    print(f"- {pet_name}: {task.description} on {occ_time.strftime('%Y-%m-%d %H:%M')}")

# Generate schedule to add some scheduled tasks for conflict detection
schedule = scheduler.generate_daily_schedule(now.replace(hour=8, minute=0, second=0, microsecond=0))
print("\nBasic Conflicts Detected:")
conflicts = scheduler.detect_basic_conflicts()
if conflicts:
    for t1, t2 in conflicts:
        print(f"WARNING: Conflict detected - '{t1.description}' overlaps with '{t2.description}'")
else:
    print("- No conflicts detected.")

print("\nToday's Schedule:")
if not schedule:
    print("No tasks scheduled for today.")
else:
    for pet_name, task, start_time in schedule:
        end_time = start_time + timedelta(minutes=task.duration_mins)
        print(f"- {start_time.strftime('%H:%M')} - {end_time.strftime('%H:%M')}: {task.description} for {pet_name} (Priority: {task.priority})")
