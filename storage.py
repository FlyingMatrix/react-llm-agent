import json

class Storage:
    def __init__(self, file_path="tasks.json"):
        self.file_path = file_path
        self.tasks = self._load_tasks()

    def _load_tasks(self):
        try:
            with open(self.file_path, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_tasks(self):
        with open(self.file_path, "w") as f:
            json.dump(self.tasks, f, indent=2)