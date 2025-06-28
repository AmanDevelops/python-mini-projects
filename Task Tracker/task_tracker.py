import time
import json

class TaskTracker:
    """
    Handles Tasks
    """

    def __init__(self, user: str) -> None:
        self.user = user
        self.tasks = []
        self.fileName = f"{user}_{int(time.time())}.json"
    
    def write_file(taskFunc) -> None:
        def wrapper(self,  *args, **kwargs):
            result = taskFunc(self,   *args, **kwargs)
            with open(self.fileName, 'w') as f:
                json.dump(self.tasks,f, default=str, indent=4)
            return result
        return wrapper

    @write_file
    def add_task(self, task: str) -> int:
        task = {
            "id": len(self.tasks) + 1,
            "description": task,
            "status": "todo",
            "createdAt": int(time.time()),
            "updatedAt": int(time.time())

        }

        self.tasks.append(task)

    @write_file
    def update_task(self, id: int, task: str) -> None:
        self.tasks[id - 1]["description"] = task
        self.tasks[id - 1]["updatedAt"] = int(time.time())
    
    @write_file
    def delete_task(self, id: int) -> None:
        self.tasks.pop(id - 1)

    @write_file
    def mark_progress(self, id: int, newStatus: str) -> None:
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
