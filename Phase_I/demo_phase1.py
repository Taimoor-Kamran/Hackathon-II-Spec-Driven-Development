"""
Demo script showing Phase I Todo Console App in action
"""
from src.services.task_service import TaskService
from src.cli.console import ConsoleInterface


def demo():
    print("🚀 Phase I Todo Console App Demo")
    print("="*40)

    # Create a fresh task service for the demo
    task_service = TaskService()
    console = ConsoleInterface(task_service)

    # Simulate some user interactions
    print("\n📝 Adding some tasks...")
    task_service.add_task("Learn Python", "Complete Python tutorial")
    task_service.add_task("Build Todo App", "Implement Phase I requirements")
    print("   Added 2 tasks")

    print("\n📋 Listing all tasks...")
    console.display_tasks()

    print("\n✅ Marking first task as complete...")
    task_service.mark_task_complete(1)
    print("   Task 1 marked as complete")

    print("\n📋 Listing tasks again to see the change...")
    console.display_tasks()

    print("\n✏️  Updating second task...")
    task_service.update_task(2, "Build Spec-Driven Todo App", "Implement Phase I with Claude Code and Spec-Kit Plus")
    print("   Task 2 updated")

    print("\n📋 Final list of tasks...")
    console.display_tasks()

    print("\n🎉 Demo completed successfully!")
    print("The Phase I Todo Console App is working as expected!")


if __name__ == "__main__":
    demo()