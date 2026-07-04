from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field


# ── Abstract base task ────────────────────────────────────────────────────────

@dataclass
class Task(ABC):
    title: str
    time: str
    priority: str
    status: str = "pending"

    @abstractmethod
    def getPriority(self) -> str:
        pass

    @abstractmethod
    def getTime(self) -> str:
        pass


# ── Owner ─────────────────────────────────────────────────────────────────────

@dataclass
class Owner:
    name: str
    pets: list[Pet] = field(default_factory=list)

    def addPet(self, pet: Pet) -> None:
        pass

    def removePet(self, pet: Pet) -> None:
        pass

    def getPets(self) -> list[Pet]:
        pass


# ── Pet ───────────────────────────────────────────────────────────────────────

@dataclass
class Pet:
    name: str
    ownerId: str
    healthNotes: str = ""

    def updateInfo(self, name: str, healthNotes: str) -> None:
        pass

    def getOwner(self) -> Owner:
        pass

    def getTasks(self) -> list[Task]:
        pass

    def getSchedule(self) -> TaskScheduler:
        pass

    def addTask(self, task: Task) -> None:
        pass

    def removeTask(self, task: Task) -> None:
        pass


# ── TaskScheduler (merged with DailyView) ────────────────────────────────────

@dataclass
class TaskScheduler:
    pet: Pet
    date: str
    tasks: list[Task] = field(default_factory=list)
    priorityQueue: list[Task] = field(default_factory=list)

    def addTask(self, task: Task) -> None:
        pass

    def getDailyTasks(self) -> list[Task]:
        pass

    def prioritizeTasks(self) -> list[Task]:
        pass

    def rescheduleTasks(self) -> None:
        pass

    def getTasksByTime(self) -> list[Task]:
        pass

    def getTasksByPriority(self) -> list[Task]:
        pass