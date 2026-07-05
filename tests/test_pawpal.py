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
