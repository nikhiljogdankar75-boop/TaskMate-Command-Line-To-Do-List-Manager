"""Simple To-Do List application (command line).

Features: add tasks, delete tasks, mark tasks done, filter the list,
clear completed tasks. Tasks are saved in tasks.json so they are
still there the next time you run the program.
"""

import json
import os

FILE_NAME = "tasks.json"


# ---------- Storage ----------
def load_tasks():
    """Read tasks from the JSON file (empty list if missing or broken)."""
    if not os.path.exists(FILE_NAME):
        return []
    try:
        with open(FILE_NAME, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return []


def save_tasks(tasks):
    """Write tasks to the JSON file."""
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2)


# ---------- Actions ----------
def show_tasks(tasks, mode="all"):
    shown = [
        (i, t) for i, t in enumerate(tasks, start=1)
        if mode == "all"
        or (mode == "active" and not t["done"])
        or (mode == "done" and t["done"])
    ]
    print()
    if not shown:
        print("  Nothing here.")
    for i, t in shown:
        mark = "[x]" if t["done"] else "[ ]"
        print(f"  {i}. {mark} {t['text']}")
    remaining = sum(1 for t in tasks if not t["done"])
    print(f"\n  {remaining} of {len(tasks)} tasks remaining")


def add_task(tasks):
    text = input("Enter task: ").strip()
    if not text:
        print("Please enter a task.")
        return
    tasks.append({"text": text, "done": False})
    save_tasks(tasks)
    print("Task added.")


def get_number(tasks, prompt):
    """Ask for a task number and return its index, or None if invalid."""
    value = input(prompt).strip()
    if not value.isdigit() or not (1 <= int(value) <= len(tasks)):
        print("Invalid task number.")
        return None
    return int(value) - 1


def delete_task(tasks):
    if not tasks:
        print("No tasks to delete.")
        return
    show_tasks(tasks)
    index = get_number(tasks, "Task number to delete: ")
    if index is not None:
        removed = tasks.pop(index)
        save_tasks(tasks)
        print(f"Deleted: {removed['text']}")


def toggle_task(tasks):
    if not tasks:
        print("No tasks yet.")
        return
    show_tasks(tasks)
    index = get_number(tasks, "Task number to mark done/undone: ")
    if index is not None:
        tasks[index]["done"] = not tasks[index]["done"]
        save_tasks(tasks)
        print("Task updated.")


def clear_completed(tasks):
    before = len(tasks)
    tasks[:] = [t for t in tasks if not t["done"]]
    save_tasks(tasks)
    print(f"Removed {before - len(tasks)} completed task(s).")


# ---------- Main menu ----------
MENU = """
===== TO-DO LIST =====
1. View all tasks
2. View active tasks
3. View completed tasks
4. Add task
5. Mark task done / undone
6. Delete task
7. Clear completed tasks
8. Exit
"""


def main():
    tasks = load_tasks()
    while True:
        print(MENU)
        choice = input("Choose an option (1-8): ").strip()

        if choice == "1":
            show_tasks(tasks, "all")
        elif choice == "2":
            show_tasks(tasks, "active")
        elif choice == "3":
            show_tasks(tasks, "done")
        elif choice == "4":
            add_task(tasks)
        elif choice == "5":
            toggle_task(tasks)
        elif choice == "6":
            delete_task(tasks)
        elif choice == "7":
            clear_completed(tasks)
        elif choice == "8":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Enter a number from 1 to 8.")


if __name__ == "__main__":
    main()
