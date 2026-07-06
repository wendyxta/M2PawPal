# PawPal+ Project Reflection

## 1. System Design

The 3 Core User Actions (Initial Plan)
1. Adding pets
2. Scheduling a walk
3. Viewing daily tasks (walks, feeding sessions, grooming sessions, medication)

Main objects (and attributes + methods) needed (Initial Plan)
- Owner
    - attributes: pets, name
    - methods: addPet(), removePets(), getPets()
- Pet
    - attributes: name, ownerId, healthNotes
    - methods: updateInfo(), getOwner(), getTasks(), getSchedule(), addTask(), removeTask()
- Task
    - attributes: title, time, priority, status
    - methods: getPriority(), getTime()
    - other subclasses of Task: WalkTask, FeedTask, GroomTask, AppointmentTask, MedicationTask
- TaskScheduler
    - attributes: tasks, pet, dates
    - methods: addTask(), getDailyTasks(), prioritizeTasks(), rescheduleTasks(), getTasksByTime(), getTasksByPriority()

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?
    - I chose a design with the 4 main classes being the Pet, Owner, Task, and TaskScheduler. The Pet has a name, owner, and notes about its health. It is responsible for updating its health info, getting its owner, schedule, and tasks. It will also add and remove tasks. The Owner has a name and a list of pets. It is responsible for adding, rmeoving, and retrieving pets. A task has a title, time, priority, and completion status. It is responsible for getting its time and priority. The TaskScheduler is for a specific pet with dates, and tasks. It is responsible for task and schedule retrieval base don task time and priority.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.
    - Yes, several design changes were made. One change was adding missing relationship between the Pet and the TaskScheduler. Each pet should have a task scheduler, along with a list of tasks, since there needs to be a way to keep track of when all the tasks are scheduled in a combined system.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?
    - My scheduler considered the constraints of the available time in a day, and the priority of the tasks. For example, it handles conflicts when two tasks are scheduled at the same time. I decided that this was the constraint that mattered the most since time is one of those things that we can't get back, and every task is time dependent. They all take time to do and need a time slot, and people can't efficiently do multiple things that the same time. Secondly, to handle time conflicts, I considered the constraint of priority. Tasks with higher urgency were scheduled first.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?
    - One tradeoff my scheduler makes is prioritizing the time a task is scheduled over the priority of a task. For example, if there is a lower urgency task such as feeding time, that occurs earlier in the day, and a more urgent task that occurs later in the day, such as a vet visit, the feeding task will still be prioritized and occur before the vet visit. This is reasonable because in real life, many tasks still need to routinely occur at set times, even though they may not be the most important tasks. In the scenario, it wouldn't make sense to starve the pet and skip the feeding task, just because the vet task is more urgent.
---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?
    - I used AI tools for design brainstorming, coming up with the structure including the classes, attributes, and methods for the project, and generating UML diagrams. I used AI for code generation of the main structure classes and algorithms for sorting and filtering tasks. Lastly, I used AI tools for testing to create test cases and documentation to write docstrings for my methods.
    - The most helpful prompts included context of the current situation, and specific questions that clearly mention specific blocks of code and different files.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?
    - One moment I didn't accept an AI suggestion as-is was when I used it to generate code for filtering tasks based on their completion status. I verified the AI suggested code by running the code myself to test fuctionality, and it seemed like it worked properly. However, the code was not very human readable, with the entire function logic in a one liner. So, I had to adjust my prompt to improve the AI suggestion to be more clear and readable.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?
    - The 5 behaviors I tested for were making status updates (updating a task from in progress to completed)for a task, the ability to add a task which should increase the total, task count, their chronological sorting order of tasks based on their time scheduled, scheduled recurring tasks, and conflict detection of tasks occuring at the same time. These tests are important because they serve as the main logic of my app since the app is all about managing tasks.


**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?
    - My Confidence Level: 4/5 stars
    - The tests cover the most important features, but not everything was tested, and there may be other edge cases that may not have been tested. For example, I would test for other edge cases like displaying lists when there are no stored owners, no pets, or no tasks. I would test time conflicts for when a task is scheduled at the same time as other tasks for the same pet, and other tasks for different pets. I would also test recurring tasks across all pets, and adding the same test twice.
---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
    - I am very satisfied with how the project turned out. I think it is a useful app to help people manage their pets and the tasks that they have for each pet. AI was very useful as a coding assistant while creating this project.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
    - I would mainly work on adding functionality to handle edge cases. While the core functionality works, according to the project directions, there are a few cases that I did not fully implement yet. I would also make the schedule and list of tasks more clear and separate, or combine them since they are qutie similar and show a lot of the same information.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
    - One important thing I learned about designing systems is that there are a lot of things to think about. From planning the design down to the core classes, to creating the backend, to the frontend, to testing the functionality, there are many parts to work on and design.
