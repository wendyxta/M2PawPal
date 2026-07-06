from datetime import date, time, timedelta

import sys
import io

# Force UTF-8 so Windows console can render rich markup and emoji
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

from rich.console import Console
from rich.table import Table
from rich import box
from rich.panel import Panel

from pawpal_system import Task, Pet, Owner, TaskScheduler

console = Console()

# ── helpers ──────────────────────────────────────────────────────────────────

PRIORITY_LABEL = {1: "[bold red]★★ High[/]", 2: "[yellow]★☆ Med[/]", 3: "[dim]☆☆ Low[/]"}
RECUR_LABEL    = {"daily": "[cyan]↺ daily[/]", "weekly": "[blue]↻ weekly[/]", "none": ""}

STATUS_ICON = {
    "pending":   "[yellow]⏳ Pending[/]",
    "completed": "[green]✅ Done[/]",
}


def task_table(tasks: list[Task], title: str = "") -> Table:
    """Build a rich Table for a list of tasks."""
    tbl = Table(
        title=title,
        box=box.ROUNDED,
        header_style="bold cyan",
        show_lines=True,
        expand=False,
    )
    tbl.add_column("Time",       style="bold white",  width=7,  justify="center")
    tbl.add_column("Task",       style="white",        min_width=22)
    tbl.add_column("Priority",   justify="center",     width=12)
    tbl.add_column("Status",     justify="center",     width=14)
    tbl.add_column("Recurrence", justify="center",     width=12)

    for t in tasks:
        tbl.add_row(
            t.time.strftime("%H:%M"),
            t.title,
            PRIORITY_LABEL.get(t.priority, str(t.priority)),
            STATUS_ICON.get(t.status, t.status),
            RECUR_LABEL.get(t.recurrence, t.recurrence),
        )
    return tbl


def section(title: str) -> None:
    console.print()
    console.rule(f"[bold magenta]{title}[/]")


# ── setup data ────────────────────────────────────────────────────────────────

TODAY = str(date.today())

owner = Owner(name="Bill")

mochi = Pet(name="Mochi", owner=owner, healthNotes="Allergic to chicken")
luna  = Pet(name="Luna",  owner=owner, healthNotes="Takes joint supplement")

owner.addPet(mochi)
owner.addPet(luna)

mochi_schedule = mochi.getSchedule(TODAY)
mochi_schedule.addTask(Task(title="Morning walk",      time=time(7, 0),   priority=1))
mochi_schedule.addTask(Task(title="Breakfast feeding", time=time(7, 30),  priority=1))
mochi_schedule.addTask(Task(title="Allergy medication",time=time(8, 0),   priority=2))

luna_schedule = luna.getSchedule(TODAY)
luna_schedule.addTask(Task(title="Joint supplement",   time=time(11, 0),  priority=1))
luna_schedule.addTask(Task(title="Dinner feeding",     time=time(20, 0),  priority=1))
luna_schedule.addTask(Task(title="Evening walk",       time=time(18, 30), priority=2))

# ── Phase 2 · Today's Schedule ────────────────────────────────────────────────

console.print(Panel(
    f"[bold]Owner:[/] {owner.name}   [bold]Date:[/] {TODAY}",
    title="[bold green]🐾 PawPal — Today's Schedule[/]",
    border_style="green",
))

for pet in owner.getPets():
    schedule = pet.getSchedule(TODAY)
    note = f"  [dim italic]Note: {pet.healthNotes}[/]" if pet.healthNotes else ""
    console.print(f"\n[bold cyan]🐶 {pet.name}[/]{note}")
    console.print(task_table(schedule.getTasksByTime()))

# ── Phase 4 · Sorting & Filtering ─────────────────────────────────────────────

luna_schedule.addTask(Task(title="Noon play session", time=time(12, 30), priority=2))
luna_schedule.addTask(Task(title="Morning weigh-in",  time=time(6, 30),  priority=1))

section("Sorted by Time")
for pet in owner.getPets():
    console.print(f"\n[bold cyan]🐶 {pet.name}[/]")
    console.print(task_table(pet.getSchedule(TODAY).getTasksByTime()))

section("Pending Tasks Only")
for pet in owner.getPets():
    pending = pet.getSchedule(TODAY).getPendingTasks()
    console.print(f"\n[bold cyan]🐶 {pet.name}[/]  [dim]({len(pending)} pending)[/]")
    console.print(task_table(pending))

section("Filter by Pet: Luna")
luna_tasks = owner.getTasksByPet(TODAY, "Luna")
console.print(task_table(luna_tasks, title="Luna's Tasks"))

# ── Phase 5 · Recurring Tasks ─────────────────────────────────────────────────

section("Recurring Tasks")

TOMORROW  = str(date.today() + timedelta(days=1))
NEXT_WEEK = str(date.today() + timedelta(weeks=1))

daily_task  = Task(title="Morning medication", time=time(8, 0),  priority=1, recurrence="daily")
weekly_task = Task(title="Bath time",          time=time(10, 0), priority=2, recurrence="weekly")
mochi_schedule.addTask(daily_task)
mochi_schedule.addTask(weekly_task)

console.print("\n[bold]Completing daily task[/] → should auto-schedule for tomorrow:")
mochi_schedule.completeTask(daily_task)

console.print("\n[bold]Completing weekly task[/] → should auto-schedule for next week:")
mochi_schedule.completeTask(weekly_task)

console.print(f"\n[bold cyan]Mochi — Tomorrow ({TOMORROW}):[/]")
console.print(task_table(mochi.getSchedule(TOMORROW).getTasksByTime()))

console.print(f"\n[bold cyan]Mochi — Next Week ({NEXT_WEEK}):[/]")
console.print(task_table(mochi.getSchedule(NEXT_WEEK).getTasksByTime()))

# ── Phase 6 · Conflict Detection ──────────────────────────────────────────────

section("Conflict Detection")

mochi_schedule.addTask(Task(title="Vet call",       time=time(17, 0), priority=1))
luna_schedule.addTask( Task(title="Grooming brush", time=time(17, 0), priority=2))

conflicts = owner.checkConflicts(TODAY)
if conflicts:
    for warning in conflicts:
        console.print(f"[bold red]⚠️  {warning}[/]")
else:
    console.print("[green]✅ No conflicts found.[/]")

console.print()
