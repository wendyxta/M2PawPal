import streamlit as st
from datetime import time
from pawpal_system import Owner, Pet, Task

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

st.subheader("Quick Demo Inputs (UI only)")
owner_name = st.text_input("Owner name", value="Jordan")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

st.markdown("### Tasks")
st.caption("Add a few tasks. In your final version, these should feed into your scheduler.")

if "owner" not in st.session_state:
    st.session_state.owner = Owner(owner_name)

if "pet" not in st.session_state:
    st.session_state.pet = Pet(name=pet_name, owner=st.session_state.owner)
    st.session_state.owner.addPet(st.session_state.pet)

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    task_hour = st.number_input("Hour (0-23)", min_value=0, max_value=23, value=8)
    task_minute = st.number_input("Minute (0-59)", min_value=0, max_value=59, value=0)
with col3:
    priority = st.number_input("Priority (1=highest)", min_value=1, max_value=10, value=1)

if st.button("Add task"):
    new_task = Task(title=task_title, time=time(int(task_hour), int(task_minute)), priority=int(priority))
    st.session_state.pet.addTask(new_task)

current_tasks = st.session_state.pet.getTasks()
if current_tasks:
    st.write("Current tasks:")
    st.table([{"title": t.title, "time": str(t.time), "priority": t.priority, "status": t.status} for t in current_tasks])
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("This button should call your scheduling logic once you implement it.")

if st.button("Generate schedule"):
    scheduler = st.session_state.pet.getSchedule("today")
    for task in st.session_state.pet.getTasks():
        scheduler.addTask(task)
    sorted_tasks = scheduler.getTasksByTime()
    if sorted_tasks:
        for t in sorted_tasks:
            st.write(f"{'✅' if t.isComplete() else '🔲'} `{t.time}` — **{t.title}** (priority {t.priority})")
    else:
        st.info("No tasks to schedule. Add tasks above first.")
