# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```
# e.g.:
# Daily plan for Biscuit (Golden Retriever):
#   08:00 — Morning walk (30 min) [priority: high]
#   09:00 — Feeding (10 min) [priority: high]
#   ...
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:
  TODAY'S SCHEDULE — 2026-07-05
  Owner: Bill

  MOCHI
  Note: Allergic to chicken
  ------------------------------------
  [PENDING] Morning walk at 07:00 (priority 1)
  [PENDING] Breakfast feeding at 07:30 (priority 1)
  [PENDING] Allergy medication at 08:00 (priority 2)

  LUNA
  Note: Takes joint supplement
  ------------------------------------
  [PENDING] Joint supplement at 11:00 (priority 1)
  [PENDING] Evening walk at 18:30 (priority 2)
  [PENDING] Dinner feeding at 20:00 (priority 1)
======================================
  SORTED BY TIME 

  MOCHI
  ----------------------------------------
  [PENDING] Morning walk at 07:00 (priority 1)
  [PENDING] Breakfast feeding at 07:30 (priority 1)
  [PENDING] Allergy medication at 08:00 (priority 2)

  LUNA
  ----------------------------------------
  [PENDING] Morning weigh-in at 06:30 (priority 1)
  [PENDING] Joint supplement at 11:00 (priority 1)
  [PENDING] Noon play session at 12:30 (priority 2)
  [PENDING] Evening walk at 18:30 (priority 2)
  [PENDING] Dinner feeding at 20:00 (priority 1)
======================================
  PENDING TASKS ONLY

  Mochi (3 pending)
  ----------------------------------------
  [PENDING] Morning walk at 07:00 (priority 1)
  [PENDING] Breakfast feeding at 07:30 (priority 1)
  [PENDING] Allergy medication at 08:00 (priority 2)

  Luna (5 pending)
  ----------------------------------------
  [PENDING] Morning weigh-in at 06:30 (priority 1)
  [PENDING] Joint supplement at 11:00 (priority 1)
  [PENDING] Noon play session at 12:30 (priority 2)
  [PENDING] Evening walk at 18:30 (priority 2)
  [PENDING] Dinner feeding at 20:00 (priority 1)
======================================
  FILTER BY PET: Luna
  [PENDING] Morning weigh-in at 06:30 (priority 1)
  [PENDING] Joint supplement at 11:00 (priority 1)
  [PENDING] Noon play session at 12:30 (priority 2)
  [PENDING] Evening walk at 18:30 (priority 2)
  [PENDING] Dinner feeding at 20:00 (priority 1)
======================================
  RECURRING TASKS 
  Completing daily task -> should schedule for tomorrow:
  [SCHEDULED] 'Morning medication' auto-scheduled for 2026-07-06

  Completing weekly task -> should schedule for next week:
  [SCHEDULED] 'Bath time' auto-scheduled for 2026-07-12

  Mochi's schedule for tomorrow (2026-07-06):
  ----------------------------------------
  [PENDING] Morning medication at 08:00 (priority 1) [daily]

  Mochi's schedule for next week (2026-07-12):
  ----------------------------------------
  [PENDING] Bath time at 10:00 (priority 2) [weekly]
======================================
  CONFLICT DETECTION 
  [WARNING] Conflict at 08:00: 'Morning medication' (Mochi) vs 'Allergy medication' (Mochi)
  [WARNING] Conflict at 17:00: 'Vet call' (Mochi) vs 'Grooming brush' (Luna)
```

# Paste your pytest output here
================================================================== test session starts ===================================================================
platform win32 -- Python 3.13.9, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Users\wendy2.0\Documents\GitHub\M2PawPal
plugins: anyio-4.14.1
collected 5 items                                                                                                                                         

tests\test_pawpal.py .....                                                                                                                          [100%]

=================================================================== 5 passed in 0.18s ====================================================================

```


## 📐 Smarter Scheduling

> Fill in once you've implemented scheduling logic.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | getTasksByTime() | sorts based on the time a task is scheduled (task happening sooner appear frist) |
| Filtering | getTasksByPet(), getPendingTasks() | takes in the name of a Pet, filters tasks belonging to inputed Pet |
| Conflict handling | checkConflicts() | overlapping time slots for one pet across pets belonging to same owner |
| Recurring tasks | completeTask() | marks a task as complete, then checks if it recurs, and updates schedule for tasks recurring weekly and monthly |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. Enter the owner name. Then enter the pet name, and pet species, and click the Add Pet button to add the pet to the owner. 
2. Select the current pet from the Active Pet dropdown.
3. Enter the details of the 1st task (title, time of day in hours and minutes, priority level, and recurrence). Click the add task button to check for scheduling conflicts and add the task to the list of tasks displayed in a table view. Repeat for all tasks.
4. Click the Generate Schedule button to display the list of sorted tasks based on the time they are scheduled, and based on priority if tasks are scheduled for the same time.
5. Go to the Task Completion Update section to update the status of tasks. Select a task from the dropdown and click the Mark as Complete button.
6. Click the Generate Schedule to rebuid the schedule with the updated task completion progress, and an updated task list with the task scheduled for the next day/week, if the task is a recurring task.

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->