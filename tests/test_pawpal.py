import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from datetime import time
from pawpal_system import Task, Pet, Owner


def test_task_completion():
    task = Task(title="Morning walk", time=time(7, 0), priority=1)
    assert task.status == "pending"
    task.complete()
    assert task.status == "completed"


def test_add_task_increases_pet_task_count():
    owner = Owner(name="Bill")
    pet = Pet(name="Mochi", owner=owner)
    task = Task(title="Breakfast feeding", time=time(7, 30), priority=1)

    assert len(pet.getTasks()) == 0
    pet.addTask(task)
    assert len(pet.getTasks()) == 1


def test_tasks_sorted_chronologically():
    owner = Owner(name="Bill")
    pet = Pet(name="Mochi", owner=owner)
    scheduler = pet.getSchedule("2025-07-05")

    scheduler.addTask(Task(title="Evening walk",  time=time(18, 0), priority=1))
    scheduler.addTask(Task(title="Lunch feeding", time=time(12, 0), priority=1))
    scheduler.addTask(Task(title="Morning walk",  time=time(7,  0), priority=1))

    sorted_tasks = scheduler.getTasksByTime()
    times = [t.time for t in sorted_tasks]
    assert times == sorted(times)


def test_daily_recurrence_schedules_next_day():
    owner = Owner(name="Bill")
    pet = Pet(name="Mochi", owner=owner)
    scheduler = pet.getSchedule("2025-07-05")

    task = Task(title="Morning walk", time=time(7, 0), priority=1, recurrence="daily")
    scheduler.addTask(task)
    scheduler.completeTask(task)

    next_scheduler = pet.getSchedule("2025-07-06")
    assert len(next_scheduler.tasks) == 1
    next_task = next_scheduler.tasks[0]
    assert next_task.title == "Morning walk"
    assert next_task.status == "pending"
    assert next_task.recurrence == "daily"


def test_conflict_detection_flags_same_time():
    owner = Owner(name="Bill")
    pet_a = Pet(name="Mochi", owner=owner)
    pet_b = Pet(name="Noodle", owner=owner)
    owner.addPet(pet_a)
    owner.addPet(pet_b)

    pet_a.getSchedule("2025-07-05").addTask(Task(title="Morning walk",    time=time(8, 0), priority=1))
    pet_b.getSchedule("2025-07-05").addTask(Task(title="Breakfast feeding", time=time(8, 0), priority=2))

    conflicts = owner.checkConflicts("2025-07-05")
    assert len(conflicts) == 1
    assert "08:00" in conflicts[0]
