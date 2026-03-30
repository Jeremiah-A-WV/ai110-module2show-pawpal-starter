# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
![alt text](image.png)
Owner holds the user's basic information and a list of their pets.

Pet represents individual animals and owns a specific list of care tasks.

Task is the data structure for the actual chores, storing constraints like duration, priority, and frequency.

Scheduler aggregates all tasks from all pets and contains algorithms to sort them, detect overlaps, and generate the final daily plan.

- What classes did you include, and what responsibilities did you assign to each?
Task: Tracks properties like description, duration_mins, frequency, and is_completed.

Pet: Holds the pet's profile and a list of their specific tasks.

Scheduler: Acts as the brain storing multiple pets and defining placeholders for important logic like check_conflicts, get_upcoming_tasks, and generate_recurring_tasks.

- Core actions:
Add and edit profiles: A user needs to be able to enter basic information 
about themselves and their pet, such as the pet's name, species, and age.

Add and edit tasks: A user must be able to input specific care activities 
(e.g., walking, feeding, grooming) and define their constraints, primarily the 
task's duration in minutes and its priority level.

Generate schedule: A user should be able to click a button to generate a daily 
plan. The system will then automatically choose and order the tasks based on the 
provided constraints and priorities, and display the resulting schedule clearly.

**b. Design changes**

- Did your design change during implementation?

Yes, the design changed during implementation.

- If yes, describe at least one change and why you made it.

Initially, the skeleton had basic classes with empty methods and no explicit relationships between tasks and scheduled times. During implementation, I added a `pet_id` back-reference in `Task` and a `start_time` field to enable proper scheduling and querying. I also introduced a new `Calendar` class to centralize time management and conflict detection, as the original `Scheduler` lacked efficient data structures for handling overlaps. These changes were necessary to fix missing relationships (e.g., tasks not linked to pets beyond lists) and prevent logic bottlenecks (e.g., O(n) conflict checks becoming inefficient with many tasks), ensuring the system could scale and handle recurring tasks without manual workarounds.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?

The scheduler considers:
- **Time (due_time)**: Tasks are assigned to slots respecting their due times and duration.
- **Priority (High/Medium/Low)**: Higher-priority tasks are scheduled before lower-priority ones.
- **Duration (duration_mins)**: Tasks must fit within available time without exceeding the day.
- **Frequency (Once/Daily/Weekly)**: Recurring tasks are expanded and re-added automatically.
- **Completion status**: Completed tasks are excluded from scheduling.

- How did you decide which constraints mattered most?

I prioritized constraints based on user needs: **Time and Priority** are most critical because pet care requires consistency (e.g., morning walks must happen on schedule) and effort management (high-priority tasks like medications can't be deferred). **Duration** is next because it prevents overbooking. **Frequency** and **Completion status** follow naturally to support recurring care routines. I deprioritized optional constraints like owner availability windows or pet energy levels to keep the system simple for the initial build.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.

The scheduler uses a simple greedy algorithm that assigns tasks sequentially based on priority and due time, without backtracking to find optimal schedules. This may lead to suboptimal arrangements if higher-priority tasks could be swapped for better fits.

- Why is that tradeoff reasonable for this scenario?

This tradeoff is reasonable for pet care scheduling because simplicity and speed are prioritized over perfection. Pet owners typically have small numbers of tasks, so the greedy approach is fast and easy to understand, avoiding complex optimizations that could confuse users or slow down the app.

---

## 3. AI Collaboration

**a. How you used Claude (AI Agent)**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?

Claude was used extensively throughout the project for:
- **Design review and gap analysis**: Reviewing the initial skeleton to identify missing relationships and bottlenecks (e.g., lack of task-to-pet back-references, inefficient conflict detection).
- **Implementation guidance**: Generating class stubs, implementing scheduling algorithms, and adding helper methods for sorting/filtering.
- **Refactoring and optimization**: Suggesting improvements like using lambda functions for sorting, adding comparison operators to Task, and simplifying complex code.
- **Testing strategy**: Helping design a comprehensive test suite covering sorting, recurrence, and conflict detection.
- **UI integration**: Updating Streamlit components to display sorted/filtered data and show conflict warnings professionally.
- **Documentation**: Adding docstrings and creating a professional README with features list.

- What kinds of prompts or questions were most helpful?

Most helpful prompts were:
- Specific, scoped requests: "Add 1-line docstrings to all methods" was clearer than "improve documentation."
- Problem-statement prompts: "What are the most important edge cases to test?" led to focused test design.
- Codebase-aware queries: Using #codebase context to ask for updates based on actual implementation rather than hypotheticals.
- Iterative refinement: Asking for improvements to specific methods (e.g., "How could this algorithm be simplified?") yielded actionable suggestions.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.

When Claude suggested converting all sorting logic to nested list comprehensions for "Pythonic" style (`[...for pet in self.owner.pets for task in pet.tasks...]`), I kept the original explicit loops. The comprehension was more concise but harder for beginners to read. Since this is an educational project where clarity matters, I chose readability over brevity, balancing Pythonic ideals with maintainability.

- How did you evaluate or verify what the AI suggested?

Verification involved:
- **Testing**: Running `main.py` and `pytest` to confirm suggested code produced correct outputs.
- **Readability review**: Assessing if I could explain the logic to someone unfamiliar with the codebase.
- **Performance consideration**: Checking if suggestions addressed actual bottlenecks (e.g., heap-based sorting vs. simple list sorting for small datasets).
- **Design coherence**: Ensuring suggestions didn't break existing patterns or add unnecessary complexity.

**Key Learning on "Lead Architect" Role with AI:**

Using Claude as a collaborator taught me that AI is most effective as a **structured thinking partner**, not a code generator. The best workflow involved:
1. **Define clear problems first**: Vague requests led to generic solutions; specific requirements led to targeted help.
2. **Verify, don't assume**: Every AI suggestion improved when tested and reviewed, catching edge cases I missed.
3. **Stay in control**: Accepting all suggestions would have created a system optimized for AI readability, not user/developer needs. Strategic rejection of suggestions kept the design clean.
4. **Leverage multiple perspectives**: Asking Claude for alternative approaches revealed tradeoffs I hadn't considered, making better design decisions.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?

I tested core behaviors including task completion (marking tasks done), task addition to pets, sorting tasks by due time, automatic creation of next recurring task instances upon completion, and conflict detection for overlapping scheduled tasks.

- Why were these tests important?

These tests were important to verify that the fundamental scheduling logic works correctly, ensuring users can rely on the app for accurate pet care planning. They catch bugs early, prevent regressions during updates, and validate edge cases like sorting with missing times or handling recurring tasks, which are critical for a reliable pet scheduling system.

**b. Confidence**

- How confident are you that your scheduler works correctly?

I am highly confident (4/5) that the scheduler works correctly for typical use cases, as the tests cover key paths and edge cases, and manual runs in main.py confirm expected outputs.

- What edge cases would you test next if you had more time?

If I had more time, I would test edge cases like handling a large number of tasks (e.g., 50+ per pet) for performance, complex recurring patterns (e.g., bi-weekly or custom frequencies), time zone differences, tasks spanning midnight, and integration with the Streamlit UI for real-time updates.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

I'm most satisfied with the **scheduling algorithm and conflict detection logic**. The greedy scheduler is simple yet effective, and the conflict detection system catches overlaps without crashing, providing helpful warnings. The separation of concerns (Scheduler, Calendar, Task) also kept the codebase clean and testable. Additionally, the Streamlit UI integration successfully brings all the backend logic to the surface, making the advanced features accessible to users through an intuitive interface.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

If I had another iteration, I would:
1. **Implement interval trees or sorted lists** for O(log n) conflict detection instead of O(n) linear searches, improving performance for owners with many tasks.
2. **Add recurring task patterns**: Support bi-weekly, monthly, or custom frequencies instead of just Daily/Weekly.
3. **Include pet availability windows**: Allow owners to specify when pets are available (e.g., "no walks after 8 PM"), making schedules more realistic.
4. **Optimize recurring task expansion**: Cache pre-computed recurring instances instead of recalculating daily.
5. **Enhance the UI**: Add a visual calendar view, drag-and-drop task reordering, and time-zone support for remote owners.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

The key takeaway is that **good system design requires clear separation of concerns and intentional tradeoff decisions**. Rather than trying to handle every edge case or optimize prematurely, defining what matters most (simplicity, speed, reliability) up front made better design choices. Additionally, working with AI taught me that the tool is only as good as the questions asked—vague requests get generic solutions, but well-scoped problems with clear context produce powerful, tailored results. Finally, I learned that staying in the "lead architect" role means being willing to reject or modify AI suggestions when they don't align with project goals, even if they're technically "better." The best system is one the team understands and can maintain.
