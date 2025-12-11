from .services.task_service import TaskService
from .cli.console import ConsoleInterface


def main():
    """Application entry point."""
    # Initialize the task service
    task_service = TaskService()

    # Initialize the console interface
    console = ConsoleInterface(task_service)

    # Start the application
    console.run()


if __name__ == "__main__":
    main()