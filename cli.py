import click
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
    main()