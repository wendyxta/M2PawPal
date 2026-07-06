import streamlit as st
from datetime import time, date as date_type
from pawpal_system import Owner, Pet, Task

TODAY = str(date_type.today())

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

# st.markdown(
#     """
# Welcome to the PawPal+ starter app.

# This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
# but **it does not implement the project logic**. Your job is to design the system and build it.

# Use this app as your interactive demo once your backend classes/functions exist.
# """
# )

# with st.expander("Scenario", expanded=True):
#     st.markdown(
#         """
# **PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
# for their pet(s) based on constraints like time, priority, and preferences.

# You will design and implement the scheduling logic and connect it to this Streamlit UI.
# """
#     )

# with st.expander("What you need to build", expanded=True):
#     st.markdown(
#         """
# At minimum, your system should:
# - Represent pet care tasks (what needs to happen, how long it takes, priority)
# - Represent the pet and the owner (basic info and preferences)
# - Build a plan/schedule for a day that chooses and orders tasks based on constraints
# - Explain the plan (why each task was chosen and when it happens)
# """
#     )

# st.divider()

owner_name = st.text_input("Owner name", value="Jordan")

if "owner" not in st.session_state:
    st.session_state.owner = Owner(owner_name)

# ── Add pet ────────────────────────────────────────────────────────────────────
st.markdown("### Pets")
col_p1, col_p2, col_p3 = st.columns(3)
with col_p1:
    new_pet_name = st.text_input("Pet name", value="Mochi")
with col_p2:
    new_pet_species = st.selectbox("Species", ["dog", "cat", "other"])
with col_p3:
    st.write("")
    st.write("")
    if st.button("Add pet"):
        existing_names = [p.name.lower() for p in st.session_state.owner.getPets()]
        if new_pet_name.lower() in existing_names:
            st.warning(f"A pet named '{new_pet_name}' already exists.")
        else:
            new_pet = Pet(name=new_pet_name, owner=st.session_state.owner)
            st.session_state.owner.addPet(new_pet)
            st.session_state.pet = new_pet
            st.success(f"Pet '{new_pet_name}' added!")

# Seed a default pet if none exist yet
if not st.session_state.owner.getPets():
    default_pet = Pet(name="Mochi", owner=st.session_state.owner)
    st.session_state.owner.addPet(default_pet)

# Pet selector
pet_names = [p.name for p in st.session_state.owner.getPets()]
if "pet" not in st.session_state or st.session_state.pet not in st.session_state.owner.getPets():
    st.session_state.pet = st.session_state.owner.getPets()[0]

selected_pet_name = st.selectbox("Active pet", pet_names, index=pet_names.index(st.session_state.pet.name))
st.session_state.pet = next(p for p in st.session_state.owner.getPets() if p.name == selected_pet_name)

st.markdown("### Tasks")
col1, col2, col3, col4 = st.columns(4)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    task_hour = st.number_input("Hour (0-23)", min_value=0, max_value=23, value=8)
    task_minute = st.number_input("Minute (0-59)", min_value=0, max_value=59, value=0)
with col3:
    priority = st.number_input("Priority (1=highest)", min_value=1, max_value=10, value=1)
with col4:
    recurrence = st.selectbox("Recurrence", ["none", "daily", "weekly"])

if st.button("Add task"):
    new_task = Task(title=task_title, time=time(int(task_hour), int(task_minute)), priority=int(priority), recurrence=recurrence)
    st.session_state.pet.addTask(new_task)
    st.session_state.pet.getSchedule(TODAY).addTask(new_task)
    st.success(f"Task '{task_title}' added.")

current_tasks = st.session_state.pet.getTasks()
if current_tasks:
    st.write("Current tasks:")
    st.table([{"title": t.title, "time": str(t.time), "priority": t.priority, "recurrence": t.recurrence, "status": t.status} for t in current_tasks])
else:
    st.info("No tasks yet. Add one above.")

# Task Conflict warnings 
scheduler_now = st.session_state.pet.getSchedule(TODAY)
all_scheduled = scheduler_now.getTasksByTime()
time_counts = {}
for t in all_scheduled:
    time_counts[t.time] = time_counts.get(t.time, []) + [t.title]

conflict_times = {k: v for k, v in time_counts.items() if len(v) > 1}
if conflict_times:
    for conflict_time, titles in conflict_times.items():
        tasks_str = " vs ".join(f"'{t}'" for t in titles)
        st.warning(f"Conflict at {conflict_time.strftime('%H:%M')}: {tasks_str} are scheduled at the same time.")
elif current_tasks:
    st.success("No scheduling conflicts detected.")

st.divider()

st.subheader("Build Schedule")
# st.caption("This button should call your scheduling logic once you implement it.")

if st.button("Generate schedule"):
    scheduler = st.session_state.pet.getSchedule(TODAY)
    for task in st.session_state.pet.getTasks():
        scheduler.addTask(task)
    sorted_tasks = scheduler.getTasksByTime()   
    if sorted_tasks:
        st.caption(f"Sorted by time then priority — {len(sorted_tasks)} task(s)")
        st.table([
            {
                "Date": TODAY,
                "Time": t.time.strftime("%H:%M"),
                "Task": t.title,
                "Priority": t.priority,
                "Recurrence": t.recurrence,
                "Status": "✅ Done" if t.isComplete() else "🔲 Pending",
            }
            for t in sorted_tasks
        ])
    else:
        st.info("No tasks to schedule. Add tasks above first.")

st.divider()

# Task Completion Update 
st.subheader("Task Completion Update")

scheduler = st.session_state.pet.getSchedule(TODAY)
pending = scheduler.getPendingTasks() 
if pending:
    task_options = {f"{t.time.strftime('%H:%M')} — {t.title}": t for t in pending}
    chosen_label = st.selectbox("Select a pending task", list(task_options.keys()))
    if st.button("Mark complete"):
        chosen = task_options[chosen_label]
        scheduler.completeTask(chosen)
        if chosen.recurrence == "daily":
            from datetime import timedelta
            next_date = str(date_type.fromisoformat(TODAY) + timedelta(days=1))
            st.success(f"'{chosen.title}' marked complete. Next occurrence scheduled for {next_date} (daily).")
        elif chosen.recurrence == "weekly":
            from datetime import timedelta
            next_date = str(date_type.fromisoformat(TODAY) + timedelta(weeks=1))
            st.success(f"'{chosen.title}' marked complete. Next occurrence scheduled for {next_date} (weekly).")
        else:
            st.success(f"'{chosen.title}' marked complete.")
else:
    st.success("All tasks for today are complete!")

st.divider()

# ── Upcoming recurring tasks ───────────────────────────────────────────────────
st.subheader("Upcoming Scheduled Tasks")
st.caption("Tasks auto-scheduled from completed recurring tasks.")

pet = st.session_state.pet
upcoming_rows = []
for date_key, sched in sorted(pet.schedulers.items()):
    if date_key == TODAY:
        continue
    for t in sched.getTasksByTime():
        upcoming_rows.append({
            "Date": date_key,
            "Time": t.time.strftime("%H:%M"),
            "Task": t.title,
            "Priority": t.priority,
            "Recurrence": t.recurrence,
            "Status": "✅ Done" if t.isComplete() else "🔲 Pending",
        })

if upcoming_rows:
    st.table(upcoming_rows)
else:
    st.info("No upcoming recurring tasks yet. Mark a recurring task complete to see it here.")

