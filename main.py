from datetime import date, time
from pawpal_system import Task, Pet, Owner, TaskScheduler

TODAY = str(date.today())

# Create an Owner and at least two Pets
owner = Owner(name="Bill")

mochi = Pet(name="Mochi", owner=owner, healthNotes="Allergic to chicken")
luna  = Pet(name="Luna",  owner=owner, healthNotes="Takes joint supplement")

owner.addPet(mochi)
owner.addPet(luna)

# Add at least three Tasks with different times to those pets:
# Mochi's tasks
mochi_schedule = mochi.getSchedule(TODAY)
mochi_schedule.addTask(Task(title="Morning walk", time=time(7, 0),  priority=1))
mochi_schedule.addTask(Task(title="Breakfast feeding", time=time(7, 30), priority=1))
mochi_schedule.addTask(Task(title="Allergy medication",time=time(8, 0),  priority=2))

# Luna's tasks
luna_schedule = luna.getSchedule(TODAY)
luna_schedule.addTask(Task(title="Joint supplement", time=time(7, 0),  priority=1))
luna_schedule.addTask(Task(title="Dinner feeding", time=time(17, 0), priority=1))
luna_schedule.addTask(Task(title="Evening walk", time=time(18, 30),priority=2))

# Prints a "Today's Schedule" to the terminal
print(f"  TODAY'S SCHEDULE — {TODAY}")
print(f"  Owner: {owner.name}")

for pet in owner.getPets():
    schedule = pet.getSchedule(TODAY)
    print(f"\n  {pet.name.upper()}")
    if pet.healthNotes:
        print(f"  Note: {pet.healthNotes}")
    print("  " + "-" * 36)
    for task in schedule.getTasksByTime():
        print(f"  {task}")
