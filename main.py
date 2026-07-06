from datetime import date, time, timedelta
from pawpal_system import Task, Pet, Owner, TaskScheduler

# Phase 2 ------------------------------------------------------
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
luna_schedule.addTask(Task(title="Joint supplement", time=time(11, 0),  priority=1))
luna_schedule.addTask(Task(title="Dinner feeding", time=time(20, 0), priority=1))
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

# Phase 4 ----------------------------------------------------
# Add tasks out of order to test sorting and filtering methods
luna_schedule.addTask(Task(title="Noon play session", time=time(12, 30), priority=2))
luna_schedule.addTask(Task(title="Morning weigh-in",  time=time(6, 30),  priority=1))

# ──  Sorted by time ────────────
print("======================================")
print("  SORTED BY TIME ")
for pet in owner.getPets():
    print(f"\n  {pet.name.upper()}")
    print("  " + "-" * 40)
    for task in pet.getSchedule(TODAY).getTasksByTime():
        print(f"  {task}")

# ── Filtered by pending tasks only  ────────────────────────────────────
print("======================================")
print("  PENDING TASKS ONLY")
for pet in owner.getPets():
    pending = pet.getSchedule(TODAY).getPendingTasks()
    print(f"\n  {pet.name} ({len(pending)} pending)")
    print("  " + "-" * 40)
    for task in pending:
        print(f"  {task}")

# ── Filtered by pet name ─────────────────────────────────────────────────────
print("======================================")
print("  FILTER BY PET: Luna")
for task in owner.getTasksByPet(TODAY, "Luna"):
    print(f"  {task}")

# ── Automate Recurring tasks  ────────────────────────────────────────────────────
print("======================================")
print("  RECURRING TASKS ")

TOMORROW = str(date.today() + timedelta(days=1))
NEXT_WEEK = str(date.today() + timedelta(weeks=1))

# Add a daily recurring task and a weekly recurring task for Mochi
daily_task  = Task(title="Morning medication",time=time(8, 0), priority=1, recurrence="daily")
weekly_task = Task(title="Bath time", time=time(10, 0), priority=2, recurrence="weekly")
mochi_schedule.addTask(daily_task)
mochi_schedule.addTask(weekly_task)

# Completing via completeTask() auto-schedules the next occurrence
print("  Completing daily task -> should schedule for tomorrow:")
mochi_schedule.completeTask(daily_task)

print("\n  Completing weekly task -> should schedule for next week:")
mochi_schedule.completeTask(weekly_task)

# Show tomorrow's auto-created schedule for Mochi
print(f"\n  Mochi's schedule for tomorrow ({TOMORROW}):")
print("  " + "-" * 40)
for task in mochi.getSchedule(TOMORROW).getTasksByTime():
    print(f"  {task}")

# Show next week's auto-created schedule for Mochi
print(f"\n  Mochi's schedule for next week ({NEXT_WEEK}):")
print("  " + "-" * 40)
for task in mochi.getSchedule(NEXT_WEEK).getTasksByTime():
    print(f"  {task}")

# ── Conflict detection  ───────────────────────────────────────────────
print("======================================")
print("  CONFLICT DETECTION ")

# Add two tasks at the same time to check task conflict detection
mochi_schedule.addTask(Task(title="Vet call", time=time(17, 0), priority=1))  # same as Luna's Dinner feeding
luna_schedule.addTask( Task(title="Grooming brush", time=time(17, 0), priority=2))  # same time, different pet

conflicts = owner.checkConflicts(TODAY)
if conflicts:
    for warning in conflicts:
        print(warning)
else:
    print("  No conflicts found.")
