import re
from typing import List
from ..services.task_service import TaskService


class ConsoleInterface:
    """
    Handles user input/output:
    - Command parsing
    - User prompts
    - Display formatting
    - Error messages
    - Help system
    """

    def __init__(self, task_service: TaskService):
        """Initialize the console interface with a task service."""
        self.task_service = task_service
        self.running = True

    def display_help(self):
        """Display available commands and their usage."""
        help_text = """
Available Commands:
  add "task title" "optional description"    - Add a new task
  list                                      - Display all tasks
  update <id> "new title" "new description" - Update a task
  delete <id>                               - Delete a task
  complete <id>                             - Mark task as complete
  incomplete <id>                           - Mark task as incomplete
  help                                      - Show this help message
  quit/exit                                 - Exit the application

Examples:
  add "Buy groceries" "Milk, eggs, bread"
  list
  update 1 "Buy groceries and fruits" "Milk, eggs, bread, apples"
  delete 1
  complete 1
        """
        print(help_text)

    def display_tasks(self):
        """Display all tasks in a formatted way."""
        tasks = self.task_service.get_all_tasks()

        if not tasks:
            print("No tasks found.")
            return

        print("\nYour Tasks:")
        print("-" * 80)
        for task in tasks:
            status = "✓" if task.completed else "○"
            description = task.description if task.description else ""
            print(f"{status} [{task.id}] {task.title}")
            if description:
                print(f"      Description: {description}")
            print(f"      Created: {task.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
            if task.updated_at != task.created_at:
                print(f"      Updated: {task.updated_at.strftime('%Y-%m-%d %H:%M:%S')}")
            print()
        print("-" * 80)

    def parse_command(self, user_input: str) -> tuple:
        """Parse user input into command and arguments."""
        # Remove extra whitespace and split into parts
        parts = user_input.strip().split()
        if not parts:
            return "", []

        command = parts[0].lower()
        args = parts[1:] if len(parts) > 1 else []

        # Special handling for commands with quoted strings
        if command in ["add", "update"]:
            # Use regex to extract quoted strings
            pattern = r'"([^"]*)"|\'([^\']*)\'|(\S+)'
            matches = re.findall(pattern, user_input)
            # Each match is a tuple of (double_quoted, single_quoted, unquoted), get the non-empty one
            all_parts = [next(filter(None, match)) for match in matches]
            command = all_parts[0].lower()
            args = all_parts[1:] if len(all_parts) > 1 else []

        return command, args

    def execute_command(self, command: str, args: List[str]) -> bool:
        """Execute a command with given arguments."""
        try:
            if command == "add":
                return self.handle_add(args)
            elif command == "list":
                self.handle_list()
                return True
            elif command == "update":
                return self.handle_update(args)
            elif command == "delete":
                return self.handle_delete(args)
            elif command == "complete":
                return self.handle_complete(args)
            elif command == "incomplete":
                return self.handle_incomplete(args)
            elif command == "help":
                self.display_help()
                return True
            elif command in ["quit", "exit"]:
                return self.handle_exit()
            else:
                print(f"Unknown command: {command}. Type 'help' for available commands.")
                return True
        except Exception as e:
            print(f"Error executing command: {str(e)}")
            return True  # Continue running even if there's an error

    def handle_add(self, args: List[str]) -> bool:
        """Handle the add command."""
        if len(args) < 1:
            print("Usage: add \"task title\" \"optional description\"")
            return True

        title = args[0]
        description = args[1] if len(args) > 1 else None

        try:
            task = self.task_service.add_task(title, description)
            print(f"Task added successfully! ID: {task.id}, Title: {task.title}")
        except ValueError as e:
            print(f"Error adding task: {str(e)}")

        return True

    def handle_list(self):
        """Handle the list command."""
        self.display_tasks()

    def handle_update(self, args: List[str]) -> bool:
        """Handle the update command."""
        if len(args) < 2:
            print("Usage: update <id> \"new title\" \"optional new description\"")
            return True

        try:
            task_id = int(args[0])
        except ValueError:
            print("Task ID must be a number")
            return True

        new_title = args[1]
        new_description = args[2] if len(args) > 2 else None

        task = self.task_service.update_task(task_id, new_title, new_description)
        if task:
            print(f"Task {task_id} updated successfully!")
        else:
            print(f"Task with ID {task_id} not found")

        return True

    def handle_delete(self, args: List[str]) -> bool:
        """Handle the delete command."""
        if len(args) < 1:
            print("Usage: delete <id>")
            return True

        try:
            task_id = int(args[0])
        except ValueError:
            print("Task ID must be a number")
            return True

        success = self.task_service.delete_task(task_id)
        if success:
            print(f"Task {task_id} deleted successfully!")
        else:
            print(f"Task with ID {task_id} not found")

        return True

    def handle_complete(self, args: List[str]) -> bool:
        """Handle the complete command."""
        if len(args) < 1:
            print("Usage: complete <id>")
            return True

        try:
            task_id = int(args[0])
        except ValueError:
            print("Task ID must be a number")
            return True

        task = self.task_service.mark_task_complete(task_id)
        if task:
            print(f"Task {task_id} marked as complete!")
        else:
            print(f"Task with ID {task_id} not found")

        return True

    def handle_incomplete(self, args: List[str]) -> bool:
        """Handle the incomplete command."""
        if len(args) < 1:
            print("Usage: incomplete <id>")
            return True

        try:
            task_id = int(args[0])
        except ValueError:
            print("Task ID must be a number")
            return True

        task = self.task_service.mark_task_incomplete(task_id)
        if task:
            print(f"Task {task_id} marked as incomplete!")
        else:
            print(f"Task with ID {task_id} not found")

        return True

    def handle_exit(self) -> bool:
        """Handle the exit command."""
        print("Goodbye!")
        self.running = False
        return False

    def run(self):
        """Start the command loop."""
        print("Welcome to the Todo Console App!")
        print("Type 'help' for available commands or 'quit' to exit.")

        while self.running:
            try:
                user_input = input("\n> ").strip()
                if not user_input:
                    continue

                command, args = self.parse_command(user_input)
                should_continue = self.execute_command(command, args)

                if not should_continue:
                    break
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except EOFError:
                print("\nGoodbye!")
                break