class Logic:
    def __init__(self, storage):
        self.storage = storage
        self.tasks = storage.tasks

    def add_task(self, description):
        self.tasks.append({"description": description, "completed": False})
        self.storage.save_tasks()

    def mark_task_as_completed(self, task_id):
        if 0 <= task_id < len(self.tasks):
            self.tasks[task_id]["completed"] = True
            self.storage.save_tasks()
        else:
            raise IndexError("Invalid task ID")

    def list_tasks(self):
        for i, task in enumerate(self.tasks):
            status = "✓" if task["completed"] else ""
            print(f"{i}: {status} {task["description"]}")