import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler
from datetime import datetime, timedelta

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to **PawPal+**, a pet care planning assistant built with Python and Streamlit.

This app helps you organize and schedule care tasks for your pets with intelligent conflict detection, task sorting, and automatic recurring task management.
"""
)

with st.expander("Features", expanded=False):
    st.markdown(
        """
- **Smart Scheduling**: Greedy algorithm that assigns tasks based on priority and time constraints
- **Recurring Tasks**: Automatic next-occurrence generation for daily and weekly tasks
- **Conflict Detection**: Real-time warnings for overlapping schedules
- **Task Management**: Sort, filter, and complete tasks with automatic next-instance creation
- **Interactive UI**: Manage owners, pets, tasks, and generate daily schedules
"""
    )

with st.expander("How to Use", expanded=False):
    st.markdown(
        """
1. **Add an Owner** and update your name
2. **Add Pets** with their basic information
3. **Add Tasks** with duration, priority, and frequency (once/daily/weekly)
4. **View Tasks** - sort by time or filter by status
5. **Generate Schedule** - creates a daily plan with conflict warnings
"""
    )

st.divider()

# Step 2: Manage Application Memory with st.session_state
if 'owner' not in st.session_state:
    st.session_state.owner = Owner(name="Jordan")  # Default owner
if 'pet_id_counter' not in st.session_state:
    st.session_state.pet_id_counter = 1
if 'task_id_counter' not in st.session_state:
    st.session_state.task_id_counter = 1

st.subheader("Quick Demo Inputs")
owner_name = st.text_input("Owner name", value=st.session_state.owner.name)
if st.button("Update Owner Name"):
    st.session_state.owner.name = owner_name
    st.success("Owner name updated!")

pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])
age = st.number_input("Pet age", min_value=0, max_value=30, value=2)

if st.button("Add Pet"):
    pet_id = st.session_state.pet_id_counter
    new_pet = Pet(id=pet_id, name=pet_name, species=species, age=age)
    try:
        st.session_state.owner.add_pet(new_pet)
        st.session_state.pet_id_counter += 1
        st.success(f"Pet {pet_name} added!")
    except ValueError as e:
        st.error(str(e))

st.markdown("### Current Pets")
if st.session_state.owner.pets:
    for pet in st.session_state.owner.pets:
        st.write(f"- {pet.name} ({pet.species}, age {pet.age})")
else:
    st.info("No pets added yet.")

st.markdown("### Tasks")
st.caption("Add tasks to the selected pet.")

selected_pet = st.selectbox("Select Pet", [pet.name for pet in st.session_state.owner.pets]) if st.session_state.owner.pets else None

if selected_pet:
    pet = next(p for p in st.session_state.owner.pets if p.name == selected_pet)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk")
    with col2:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    with col3:
        priority = st.selectbox("Priority", ["Low", "Medium", "High"], index=2)
    with col4:
        frequency = st.selectbox("Frequency", ["Once", "Daily"], index=0)
    
    due_time = st.time_input("Due time (optional)", value=None)
    due_datetime = datetime.combine(datetime.today(), due_time) if due_time else None
    
    if st.button("Add Task"):
        task_id = st.session_state.task_id_counter
        new_task = Task(
            id=task_id,
            description=task_title,
            duration_mins=duration,
            priority=priority,
            due_time=due_datetime,
            frequency=frequency
        )
        try:
            pet.add_task(new_task)
            st.session_state.task_id_counter += 1
            st.success(f"Task '{task_title}' added to {pet.name}!")
        except ValueError as e:
            st.error(str(e))
    
    st.markdown("#### Tasks for this Pet")
    if pet.tasks:
        for task in pet.tasks:
            status = "Completed" if task.is_completed else "Pending"
            st.write(f"- {task.description} ({task.duration_mins} min, {task.priority}, {status})")
    else:
        st.info("No tasks for this pet.")

st.subheader("Task Management")
if st.session_state.owner.pets:
    selected_pet_for_tasks = st.selectbox("Select Pet for Tasks", [pet.name for pet in st.session_state.owner.pets], key="task_pet")
    pet_for_tasks = next(p for p in st.session_state.owner.pets if p.name == selected_pet_for_tasks)
    
    if pet_for_tasks.tasks:
        st.write("#### All Tasks for Selected Pet")
        tasks_data = [{"Description": t.description, "Due Time": t.due_time.strftime('%H:%M') if t.due_time else 'None', "Priority": t.priority, "Completed": "Yes" if t.is_completed else "No"} for t in pet_for_tasks.tasks]
        st.table(tasks_data)
        
        if st.button("Show Sorted Tasks by Time"):
            scheduler = Scheduler(st.session_state.owner)
            sorted_tasks = scheduler.get_tasks_sorted_by_time()
            pet_sorted = [t for name, t in sorted_tasks if name == selected_pet_for_tasks]
            if pet_sorted:
                sorted_data = [{"Description": t.description, "Due Time": t.due_time.strftime('%H:%M') if t.due_time else 'None', "Priority": t.priority} for t in pet_sorted]
                st.success("Tasks sorted by time:")
                st.table(sorted_data)
            else:
                st.info("No tasks to sort.")
        
        status_filter = st.selectbox("Filter by Status", ["All", "Pending", "Completed"])
        if st.button("Apply Filter"):
            scheduler = Scheduler(st.session_state.owner)
            if status_filter == "Pending":
                filtered = scheduler.get_tasks_filtered_by_status(False)
            elif status_filter == "Completed":
                filtered = scheduler.get_tasks_filtered_by_status(True)
            else:
                filtered = scheduler.get_all_tasks()
            pet_filtered = [t for name, t in filtered if name == selected_pet_for_tasks]
            if pet_filtered:
                filter_data = [{"Description": t.description, "Due Time": t.due_time.strftime('%H:%M') if t.due_time else 'None', "Priority": t.priority, "Completed": "Yes" if t.is_completed else "No"} for t in pet_filtered]
                st.success(f"Filtered tasks ({status_filter}):")
                st.table(filter_data)
            else:
                st.info("No tasks match the filter.")
    else:
        st.info("No tasks for this pet.")
else:
    st.info("Add pets first.")

st.divider()

st.subheader("Build Schedule")
st.caption("Generate a daily schedule for today.")

if st.button("Generate Schedule"):
    if not st.session_state.owner.pets:
        st.error("Add at least one pet first.")
    else:
        scheduler = Scheduler(st.session_state.owner)
        start_time = datetime.now().replace(hour=8, minute=0, second=0, microsecond=0)
        schedule = scheduler.generate_daily_schedule(start_time)
        
        # Check for conflicts
        conflicts = scheduler.detect_basic_conflicts()
        if conflicts:
            conflict_details = []
            for t1, t2 in conflicts:
                conflict_details.append(f"'{t1.description}' overlaps with '{t2.description}'")
            st.warning("⚠️ Schedule Conflicts Detected: " + "; ".join(conflict_details) + ". Consider adjusting task times or priorities.")
        
        if schedule:
            st.success("Schedule generated!")
            schedule_data = [{"Pet": pet_name, "Task": task.description, "Start Time": start_time.strftime('%H:%M'), "End Time": (start_time + timedelta(minutes=task.duration_mins)).strftime('%H:%M'), "Priority": task.priority} for pet_name, task, start_time in schedule]
            st.table(schedule_data)
        else:
            st.info("No tasks to schedule for today.")
