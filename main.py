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

# Create Tasks with different times
now = datetime.now()
task1 = Task(
    id=1,
    description="Morning walk",
    duration_mins=30,
    priority="High",
    due_time=now.replace(hour=9, minute=0, second=0, microsecond=0),
    frequency="Daily"
)
task2 = Task(
    id=2,
    description="Feed pet",
    duration_mins=15,
    priority="Medium",
    due_time=now.replace(hour=14, minute=0, second=0, microsecond=0),
    frequency="Daily"
)
task3 = Task(
    id=3,
    description="Evening play",
    duration_mins=45,
    priority="Low",
    due_time=now.replace(hour=18, minute=0, second=0, microsecond=0),
    frequency="Once"
)

# Add tasks to pets
pet1.add_task(task1)
pet2.add_task(task2)
pet1.add_task(task3)  # Assign to pet1 for variety

# Create Scheduler
scheduler = Scheduler(owner)

# Generate today's schedule
today = datetime.now().replace(hour=8, minute=0, second=0, microsecond=0)  # Start at 8am
schedule = scheduler.generate_daily_schedule(today)

# Print Today's Schedule
print("Today's Schedule:")
if not schedule:
    print("No tasks scheduled for today.")
else:
    for pet_name, task, start_time in schedule:
        end_time = start_time + timedelta(minutes=task.duration_mins)
        print(f"- {start_time.strftime('%H:%M')} - {end_time.strftime('%H:%M')}: {task.description} for {pet_name} (Priority: {task.priority})")
