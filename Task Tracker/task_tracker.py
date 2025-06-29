import argparse
import pickle
import time


class TaskTracker:
    """
    Handles Tasks
    """

    fileName = "Tasks.db"

    def write_file(taskFunc) -> None:
        def wrapper(self, *args, **kwargs):
            result = taskFunc(self, *args, *kwargs)
            try:
                with open(TaskTracker.fileName, "wb") as file:
                    pickle.dump(self, file)
            except:
                raise IOError("Could not write data to file")
            return result

        return wrapper

    def __init__(self) -> None:
        self.tasks = []

    @write_file
    def add_task(self, task: str) -> int:
        if task == "":
            raise ValueError("Please provide an input")
        currentTime = int(time.time())
        task = {
            "id": len(self.tasks) + 1,
            "description": task,
            "status": "todo",
            "createdAt": currentTime,
            "updatedAt": currentTime,
        }
        self.tasks.append(task)

    @write_file
    def update_task(self, id: int, task: str) -> None:
        if id > len(self.tasks):
            raise IndexError(f"Task with ID {id} does not exist")
        if task == "":
            raise ValueError("Please provide an input")
        self.tasks[id - 1]["description"] = task
        self.tasks[id - 1]["updatedAt"] = int(time.time())

    @write_file
    def delete_task(self, id: int) -> None:
        if id > len(self.tasks):
            raise IndexError(f"Task with ID {id} does not exist")
        self.tasks.pop(id - 1)

    @write_file
    def update_status(self, id: int, newStatus: str) -> None:
        if id > len(self.tasks):
            raise IndexError("Task Does Not Exists")
        if newStatus not in ("todo", "in-progress", "done"):
            raise TypeError("Invalid Operation")
        self.tasks[id - 1]["status"] = newStatus
        self.tasks[id - 1]["updatedAt"] = int(time.time())

    def list_tasks(self, filter: str = None) -> list:
        if filter is None:
            return self.tasks
        filtered_list = []
        for task in self.tasks:
            if task["status"] == filter:
                filtered_list.append(task)

        return filtered_list


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simple Tasks CLI")

    sub_parser = parser.add_subparsers(dest="command")

    add_parser = sub_parser.add_parser("add", help="add tasks to the to do list")
    add_parser.add_argument("task", type=str, help="To-Do Task")

    update_parser = sub_parser.add_parser("update", help="update existing task")
    update_parser.add_argument("number", type=int, help="index to to-do")
    update_parser.add_argument("content", type=str, help="updated content")

    delete_parser = sub_parser.add_parser("delete", help="delete existing task")
    delete_parser.add_argument("number", type=int, help="index to delete")

    mark_pending_parser = sub_parser.add_parser(
        "mark-in-progress", help="mark-in-progress existing task"
    )
    mark_pending_parser.add_argument(
        "number", type=int, help="index to mark-in-progress"
    )

    mark_done_parser = sub_parser.add_parser(
        "mark-done", help="mark-done existing task"
    )
    mark_done_parser.add_argument("number", type=int, help="index to mark-done")

    list_parser = sub_parser.add_parser("list", help="list all the tasks")
    list_parser.add_argument(
        "filter",
        type=str,
        nargs="?",
        help="filter tasks by status (todo, in-progress, done)",
    )

    args = parser.parse_args()

    try:
        with open(TaskTracker.fileName, "rb") as file:
            tracker = pickle.load(file)
    except:
        tracker = TaskTracker()

    try:
        if args.command == "add":
            tracker.add_task(args.task)
            print(f"Task added successfully (ID: {len(tracker.tasks)})")
        elif args.command == "update":
            tracker.update_task(args.number, args.content)
            print(f"Task {args.number} updated successfully")

        elif args.command == "delete":
            tracker.delete_task(args.number)
            print(f"Task {args.number} deleted successfully")

        elif args.command == "mark-in-progress":
            tracker.update_status(args.number, "in-progress")
            print(f"Task {args.number} marked as in-progress")

        elif args.command == "mark-done":
            tracker.update_status(args.number, "done")
            print(f"Task {args.number} marked as done")

        elif args.command == "list":
            tasks = tracker.list_tasks(args.filter)
            if not tasks:
                print(
                    f"No tasks found{' with status: ' + args.filter if args.filter else ''}"
                )
            else:
                print(f"Tasks{' with status: ' + args.filter if args.filter else ''}:")
                for task in tasks:
                    print(f"[{task['id']}] {task['description']} - {task['status']}")

    except Exception as e:
        print(f"[Error] {e}")
