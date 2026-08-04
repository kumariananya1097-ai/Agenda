import json
import datetime

tasks=[]
def add_task(text, priority, due_date=None, note=None):
    tasks.append({"task": text, "done": False, "priority": priority, "due_date": due_date, "note": note})
    print(f"Task added: {text} (Priority: {priority}) Due Date: {due_date}")

def view_tasks():
    if not tasks:
            print("No tasks available.")
            return
    for i, t in enumerate(tasks):
        status = "X" if t["done"] else " "
        print(f"{i+1}. [{status}]{t['task']} (Priority: {t['priority']})")
        if t["due_date"]:
            display_date = datetime.datetime.strptime(t["due_date"], "%Y-%m-%d").strftime("%d-%m-%Y")
            print(f"  Due Date: {display_date}")
        if t["note"]:
            print(f"  Note: {t['note']}")
        

def complete_task(index):
    if index < 1 or index > len(tasks):
        print("Invalid task number.")
        return
    tasks[index-1]["done"] = True
    print(f"Marked task {index} as done")

def delete_task(index):
    if index < 1 or index > len(tasks):
        print("Invalid task number.")
        return
    task = tasks.pop(index-1)
    print(f"Deleted task: {task['task']}")

def save_tasks():
    with open("tasks.json", "w") as f:
        json.dump(tasks, f, indent=4)
    print("Tasks saved to tasks.json")

def load_tasks():
    global tasks
    try:
        with open("tasks.json", "r") as f:
            tasks = json.load(f)
            print("Tasks loaded successfully!")
    except FileNotFoundError:
        tasks = []
        print("No existing tasks found. Starting with an empty task list.")

def edit_task(index, new_text, new_priority, due_date, new_note=None):
    if index < 1 or index > len(tasks):
        print("Invalid task number.")
        return
    old_text = tasks[index-1]["task"]
    old_priority = tasks[index-1]["priority"]
    old_due_date = tasks[index-1]["due_date"]
    tasks[index-1]["task"] = new_text
    tasks[index-1]["priority"] = new_priority
    tasks[index-1]["due_date"] = due_date
    if new_note is not None:
        tasks[index-1]["note"] = new_note
    print(f"Task {index} updated from '{old_text},{old_priority},{old_due_date}' to: {new_text} (Priority: {new_priority}) Due Date: {due_date}")

def search_tasks(keyword):
    found = False
    for i, t in enumerate(tasks):
        if keyword.lower() in t["task"].lower():
            status = "X" if t["done"] else " "
            print(f"{i+1}: [{status}]{t['task']} (Priority: {t['priority']})")
            if t.get("due_date"):
                try:
                    display_date = datetime.datetime.strptime(t["due_date"], "%Y-%m-%d").strftime("%d-%m-%Y")
                except Exception:
                    display_date = t["due_date"]
                print(f"  Due Date: {display_date}")
            found = True
    if not found:
        print("No tasks found containing the keyword.")

def sort_tasks():
    while True:
        print("Sort by:")
        print("1. Priority")
        print("2. Completion Status")
        print("3. Name")
        print("4. Default Sort")
        print("5. Back to main menu")
        sort_choice = input("Choose a sort option: ")
        if sort_choice == "1":
            sort_by_priority()
        elif sort_choice == "2":
            sort_by_completion()
        elif sort_choice == "3":
            sort_by_name()
        elif sort_choice == "4":
            default_sort()
        elif sort_choice == "5":
            print("Back to main menu.")
            return
        else:
            print("Invalid sort option.")
    

def sort_by_priority():
    priority_order = {"high": 1, "medium": 2, "low": 3}
    tasks.sort(key=lambda t: priority_order[t["priority"]])
    print("Tasks sorted by priority.")
    view_tasks()

def sort_by_completion():
    tasks.sort(key=lambda t: t["done"])
    print("Tasks sorted by completion status.")
    view_tasks()

def sort_by_name():
    tasks.sort(key=lambda t: t["task"].lower())
    print("Tasks sorted by name.")
    view_tasks()

def default_sort():
    priority_order = {"high": 1, "medium": 2, "low": 3}
    def due_date_key(t):
        return t["due_date"] or "9999-12-31"
    tasks.sort(key=lambda t: (t["done"],due_date_key(t), priority_order[t["priority"]], t["task"].lower()))
    print("Tasks sorted by completion status, due date, priority and name.")
    view_tasks()
def _main_loop():
    load_tasks()

    while True:
        print("\n=====To-Do List=====:")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Complete Task")
        print("4. Delete Task")
        print("5. Edit Task")
        print("6. Search Tasks")
        print("7. Sort Tasks")
        print("8. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            task_text = input("Enter the task: ")
            priority = input("Enter the priority (low, medium, high): ")
            while priority.lower() not in ["low", "medium", "high"]:
                print("Invalid priority. Please enter 'low', 'medium', or 'high'.")
                priority = input("Enter the priority (low, medium, high): ")
            while True:
                due_date_input = input("Enter the due date (DD-MM-YYYY) or press Enter to skip: ")
                if due_date_input:
                    try:
                        due_date = datetime.datetime.strptime(due_date_input, "%d-%m-%Y").strftime("%Y-%m-%d")
                        break
                    except ValueError:
                        print("Invalid date format. Please use DD-MM-YYYY.")
                        continue
                else:
                    due_date = None
                    break
            note = input("Enter a note (press Enter to skip): ")
            if note=="":
                note=None
            add_task(task_text, priority, due_date, note)
            save_tasks()
        elif choice == "2":
            view_tasks()
        elif choice == "3":
            index = int(input("Enter the task number to mark as done: "))
            complete_task(index)
            save_tasks()
        elif choice == "4":
            index = int(input("Enter the task number to delete: "))
            delete_task(index)
            save_tasks()
        elif choice == "5":
            index = int(input("Enter the task number to edit: "))
            new_text = input("Enter the new task text: ")
            new_priority = input("Enter the new priority (low, medium, high): ")
            while new_priority.lower() not in ["low", "medium", "high"]:
                print("Invalid priority. Please enter 'low', 'medium', or 'high'.")
                new_priority = input("Enter the new priority (low, medium, high): ")
            new_note = input("Enter a new note (press Enter to skip): ")
            if new_note == "":
                new_note = None
            while True:
                new_due_date = input("Enter the due date (DD-MM-YYYY) or press Enter to skip: ")
                if new_due_date:
                    try:
                        new_due_date = datetime.datetime.strptime(new_due_date, "%d-%m-%Y").strftime("%Y-%m-%d")
                        break
                    except ValueError:
                        print("Invalid date format. Please use DD-MM-YYYY.")
                        continue
                else:
                    new_due_date = None
                    break
            edit_task(index, new_text, new_priority, new_due_date, new_note)
            save_tasks()
        elif choice == "6":
            keyword = input("Enter the keyword to search for: ")
            search_tasks(keyword)
        elif choice == "7":
            sort_tasks()
            save_tasks()
        elif choice == "8":
            print("Exiting...")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    _main_loop()
            