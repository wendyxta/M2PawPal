from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date, time, timedelta

from rich.console import Console

_console = Console()


# ── Task ──────────────────────────────────────────────────────────────────────

@dataclass
class Task:
    title: str
    time: time
    priority: int
    status: str = "pending"
    recurrence: str = "none"  # "none" | "daily" | "weekly"

    def complete(self) -> None:
        """Mark this task as completed."""
        self.status = "completed"

    def isComplete(self) -> bool:
        """Return True if the task has been completed."""
        return self.status == "completed"

    def __str__(self) -> str:
        """Return a human-readable summary of the task."""
        recur = f" [{self.recurrence}]" if self.recurrence != "none" else ""
        return f"[{self.status.upper()}] {self.title} at {self.time.strftime('%H:%M')} (priority {self.priority}){recur}"


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

    def getTasksByPet(self, date: str, pet_name: str) -> list[Task]:
        """Return time-sorted tasks for a single named pet on the given date."""
        for pet in self.pets:
            if pet.name.lower() == pet_name.lower():
                return pet.getSchedule(date).getTasksByTime()
        return []

    def getAllTasksForDate(self, date: str) -> list[tuple]:
        """Return (pet, task) pairs for all pets on a date, sorted by time then priority."""
        pairs = [
            (pet, task)
            for pet in self.pets
            for task in pet.getSchedule(date).getTasksByTime()
        ]
        return sorted(pairs, key=lambda pt: (pt[1].time, pt[1].priority))

    def checkConflicts(self, date: str) -> list[str]:
        """Return warning messages for any two tasks (same or different pet) at the same time."""
        warnings = []
        all_tasks = self.getAllTasksForDate(date)  # already sorted by time
        for i in range(len(all_tasks) - 1):
            pet_a, task_a = all_tasks[i]
            pet_b, task_b = all_tasks[i + 1]
            if task_a.time == task_b.time:
                warnings.append(
                    f"Conflict at {task_a.time.strftime('%H:%M')}: "
                    f"'{task_a.title}' ({pet_a.name}) vs '{task_b.title}' ({pet_b.name})"
                )
        return warnings


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

    def completeTask(self, task: Task) -> None:
        """Mark a task complete. If it recurs, schedule a fresh copy on the next due date."""
        task.complete()

        if task.recurrence == "daily":
            delta = timedelta(days=1)
        elif task.recurrence == "weekly":
            delta = timedelta(weeks=1)
        else:
            return

        next_date = str(date.fromisoformat(self.date) + delta)
        next_task = Task(
            title=task.title,
            time=task.time,
            priority=task.priority,
            recurrence=task.recurrence,
        )
        self.pet.getSchedule(next_date).addTask(next_task)
        _console.print(f"  [bold green]📅 Scheduled[/]  '{next_task.title}' → {next_date}")

    def getTasksByTime(self) -> list[Task]:
        """Return all tasks sorted by time, then priority."""
        by_time_then_priority = lambda t: (t.time, t.priority)
        return sorted(self.tasks, key=by_time_then_priority)

    def getPendingTasks(self) -> list[Task]:
        """Return only pending tasks, sorted by time then priority."""
        pending_tasks = []
        for task in self.tasks:
            if task.status == "pending":
                pending_tasks.append(task)
        by_time_then_priority = lambda task: (task.time, task.priority)
        return sorted(pending_tasks, key=by_time_then_priority)
