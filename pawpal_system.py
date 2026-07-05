from __future__ import annotations
from dataclasses import dataclass, field
from datetime import time


# ── Task ──────────────────────────────────────────────────────────────────────

@dataclass
class Task:
    title: str
    time: time
    priority: int
    status: str = "pending"

    def complete(self) -> None:
        """Mark this task as completed."""
        self.status = "completed"

    def isComplete(self) -> bool:
        """Return True if the task has been completed."""
        return self.status == "completed"

    def __str__(self) -> str:
        """Return a human-readable summary of the task."""
        return f"[{self.status.upper()}] {self.title} at {self.time} (priority {self.priority})"


# ── Owner ─────────────────────────────────────────────────────────────────────

@dataclass
class Owner:
    name: str
    pets: list[Pet] = field(default_factory=list)

    def addPet(self, pet: Pet) -> None:
        """Add a pet to this owner's list, ignoring duplicates."""
        if pet not in self.pets:
            self.pets.append(pet)

    def removePet(self, pet: Pet) -> None:
        """Remove a pet from this owner's list."""
        self.pets.remove(pet)

    def getPets(self) -> list[Pet]:
        """Return all pets belonging to this owner."""
        return self.pets


# ── Pet ───────────────────────────────────────────────────────────────────────

@dataclass
class Pet:
    name: str
    owner: Owner
    healthNotes: str = ""
    tasks: list[Task] = field(default_factory=list)
    schedulers: dict[str, TaskScheduler] = field(default_factory=dict)

    def getOwner(self) -> Owner:
        """Return the owner of this pet."""
        return self.owner

    def getTasks(self) -> list[Task]:
        """Return all tasks assigned to this pet."""
        return self.tasks

    def addTask(self, task: Task) -> None:
        """Add a task to this pet, ignoring duplicates."""
        if task not in self.tasks:
            self.tasks.append(task)

    def removeTask(self, task: Task) -> None:
        """Remove a task from this pet."""
        self.tasks.remove(task)

    def getSchedule(self, date: str) -> TaskScheduler:
        """Return the scheduler for the given date, creating one if it doesn't exist."""
        if date not in self.schedulers:
            self.schedulers[date] = TaskScheduler(pet=self, date=date)
        return self.schedulers[date]


# ── TaskScheduler ─────────────────────────────────────────────────────────────

@dataclass
class TaskScheduler:
    pet: Pet
    date: str
    tasks: list[Task] = field(default_factory=list)

    def addTask(self, task: Task) -> None:
        """Add a task to this day's schedule, ignoring duplicates."""
        if task not in self.tasks:
            self.tasks.append(task)

    def getTasksByTime(self) -> list[Task]:
        """Return all tasks sorted by scheduled time."""
        return sorted(self.tasks, key=lambda t: t.time)
