# ReAct-LLM-Agent

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

### 🔍 What is a ReAct Agent?

A **ReAct agent** (short for **Reason + Act**) is an agent design pattern where a language model **interleaves reasoning steps with actions** taken in an environment (such as calling tools, executing code, querying APIs, or reading files). Instead of reasoning everything upfront or acting blindly, the agent repeatedly **thinks about the current state**, **decides what action to take**, **observes the result**, and then reasons again. This loop allows the agent to handle complex, multi-step tasks, recover from errors, and adapt its behavior based on intermediate feedback. ReAct is especially effective for tasks that require planning, tool use, and stateful interaction—like coding, debugging, data analysis, or navigating external systems.

### 🔄 ReAct Agent Pipeline

```
Task Goal
    ↓
Reasoning / Planning
    ↓
Action / Tool Execution
    ↓
Observation / Result
    ↓
Update Plan
    ↓
(loop back to Reasoning until the task goal is achieved)
```

### ✅ Validation

- **Task II**:
  
  > Find the population of the capital city of the country that hosted the 2016 Summer Olympics. Then determine whether that population is larger or smaller than the population of New York City.

- **Responses** from `ReAct-LLM-Agent`:
  
  ```
  TBD
  ```

- **Task II**:
  
  > Please input your task: Implement a Python command-line to-do application with separated modules for logic, storage, and CLI, The system should allow users to add tasks, list tasks, and mark tasks as completed.

- **Responses** from `ReAct-LLM-Agent`:
  
  ```
    >>> Calling Ollama model, please wait...
  
    💭 Thought: I need to create a Python to-do application with separated modules. First, I'll outline the structure and then implement each component step by step.
  
    🔧 Action: write_to_file(storage.py, import json
  
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
                json.dump(self.tasks, f, indent=2))
  
    🔍 Observation：Write successfully
  
    >>> Calling Ollama model, please wait...
  
    💭 Thought: Next, I'll implement the logic module to handle task operations. This will include adding, marking as completed, and listing tasks. I'll create a logic.py file with these functionalities.
  
    🔧 Action: write_to_file(logic.py, class Logic:
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
                  print(f"{i}: {status} {task["description"]}"))
  
    🔍 Observation：Write successfully
  
    >>> Calling Ollama model, please wait...
  
    💭 Thought: Now, I'll implement the CLI module to handle user interactions. This will include a main loop for adding, listing, and marking tasks as completed. I'll create a cli.py file with these functionalities.
  
    🔧 Action: write_to_file(cli.py, import click
    from logic import Logic
    from storage import Storage
  
    @click.command()
    @click.option("--task-file", default="tasks.json", help="Path to task storage file")
    def main(task_file):
        storage = Storage(task_file)
        logic = Logic(storage)
  
        while True:
            print("\
    To-Do List Application")
            print("1. Add Task")
            print("2. List Tasks")
            print("3. Mark Task as Completed")
            print("4. Exit")
            choice = input("Select an option: ")
  
            try:
                if choice == "1":
                    description = input("Enter task description: ")
                    logic.add_task(description)
                elif choice == "2":
                    logic.list_tasks()
                elif choice == "3":
                    task_id = int(input("Enter task ID to mark as completed: "))
                    logic.mark_task_as_completed(task_id)
                elif choice == "4":
                    break
                else:
                    print("Invalid choice. Please try again.")
            except Exception as e:
                print(f"Error: {str(e)}")
  
    if __name__ == "__main__":
        main())
  
    🔍 Observation：Write successfully
  
    >>> Calling Ollama model, please wait...
  
    💭 Thought: All modules are implemented. To complete the task, I'll provide the code structure and instructions to run the application.
  
    ✅ Final Answer：
    Here's the implementation for the to-do application with separated modules:
  
    1. **storage.py** (Handles data persistence):
  
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
  
    2. **logic.py** (Handles business logic):
  
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
                  print(f"{i}: {status} {task['description']}")
  
    3. **cli.py** (Command-line interface):
  
       import click
       from logic import Logic
       from storage import Storage
  
       @click.command()
       @click.option("--task-file", default="tasks.json", help="Path to task storage file")
       def main(task_file):
          storage = Storage(task_file)
          logic = Logic(storage)
  
          while True:
              print("\nTo-Do List Application")
              print("1. Add Task")
              print("2. List Tasks")
              print("3. Mark Task as Completed")
              print("4. Exit")
              choice = input("Select an option: ")
  
              try:
                  if choice == "1":
                      description = input("Enter task description: ")
                      logic.add_task(description)
                  elif choice == "2":
                      logic.list_tasks()
                  elif choice:  # Handle option 3 and 4
                      task_id = int(input("Enter task ID to mark as completed: "))
                      logic.mark_task_as_completed(task_id)
                  elif choice == "4":
                      break
                  else:
                      print("Invalid choice. Please try again.")
              except Exception as e:
                  print(f"Error: {str(e)}")
  
       if __name__ == "__main__":
            main()
  
    **Usage Instructions:**
  
    1. Ensure all files are in the same directory
  
    2. Run `python cli.py` to start the application
  
    3. Use the menu options to add, list, and mark tasks as completed
  
    4. Tasks will be saved in `tasks.json` automatically
  
    The application uses a JSON file for storage, with separate modules for logic, storage, and CLI interface as requested.
  ```
