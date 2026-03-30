import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler
from datetime import datetime, timedelta

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
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
        
        if schedule:
            st.success("Schedule generated!")
            for pet_name, task, start_time in schedule:
                end_time = start_time + timedelta(minutes=task.duration_mins)
                st.write(f"- {start_time.strftime('%H:%M')} - {end_time.strftime('%H:%M')}: {task.description} for {pet_name} (Priority: {task.priority})")
        else:
            st.info("No tasks to schedule for today.")
