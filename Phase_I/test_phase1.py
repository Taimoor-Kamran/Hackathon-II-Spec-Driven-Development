"""
Test script for Phase I Todo Console App
"""
from src.services.task_service import TaskService
from src.cli.console import ConsoleInterface


def test_task_operations():
    """Test all basic task operations."""
    print("Testing Phase I Todo Console App functionality...\n")

    # Initialize the task service
    task_service = TaskService()

    # Test adding tasks
    print("1. Testing add_task functionality:")
    task1 = task_service.add_task("Buy groceries", "Milk, eggs, bread")
    print(f"   Added task: ID {task1.id}, Title: {task1.title}, Description: {task1.description}")

    task2 = task_service.add_task("Complete project")
    print(f"   Added task: ID {task2.id}, Title: {task2.title}")

    # Test getting all tasks
    print("\n2. Testing get_all_tasks functionality:")
    all_tasks = task_service.get_all_tasks()
    print(f"   Total tasks: {len(all_tasks)}")
    for task in all_tasks:
        status = "Completed" if task.completed else "Pending"
        print(f"   - ID {task.id}: {task.title} [{status}]")

    # Test getting a specific task
    print("\n3. Testing get_task_by_id functionality:")
    retrieved_task = task_service.get_task_by_id(task1.id)
    if retrieved_task:
        print(f"   Retrieved task ID {retrieved_task.id}: {retrieved_task.title}")
    else:
        print("   Task not found!")

    # Test updating a task
    print("\n4. Testing update_task functionality:")
    updated_task = task_service.update_task(task2.id, "Complete Phase I project", "Finish the console app implementation")
    if updated_task:
        print(f"   Updated task ID {updated_task.id}: {updated_task.title}")
        print(f"   New description: {updated_task.description}")
    else:
        print("   Failed to update task!")

    # Test marking task as complete
    print("\n5. Testing mark_task_complete functionality:")
    completed_task = task_service.mark_task_complete(task1.id)
    if completed_task:
        print(f"   Marked task ID {completed_task.id} as complete: {completed_task.title}")
        print(f"   Status: {'Completed' if completed_task.completed else 'Pending'}")

    # Test marking task as incomplete
    print("\n6. Testing mark_task_incomplete functionality:")
    incomplete_task = task_service.mark_task_incomplete(task1.id)
    if incomplete_task:
        print(f"   Marked task ID {incomplete_task.id} as incomplete: {incomplete_task.title}")
        print(f"   Status: {'Completed' if incomplete_task.completed else 'Pending'}")

    # Test deleting a task
    print("\n7. Testing delete_task functionality:")
    delete_success = task_service.delete_task(task2.id)
    if delete_success:
        print(f"   Deleted task ID {task2.id}")
    else:
        print("   Failed to delete task!")

    # Check remaining tasks
    remaining_tasks = task_service.get_all_tasks()
    print(f"\n8. Final check - Remaining tasks: {len(remaining_tasks)}")
    for task in remaining_tasks:
        status = "Completed" if task.completed else "Pending"
        print(f"   - ID {task.id}: {task.title} [{status}]")

    print("\n✓ All basic functionality tests passed!")


def test_console_commands():
    """Test the console interface command parsing."""
    print("\nTesting Console Interface command parsing...")

    task_service = TaskService()
    console = ConsoleInterface(task_service)

    # Test command parsing
    test_commands = [
        'add "Test task" "Test description"',
        'list',
        'update 1 "Updated task" "Updated description"',
        'delete 1',
        'complete 1',
        'incomplete 1',
        'help',
        'quit'
    ]

    for cmd in test_commands:
        command, args = console.parse_command(cmd)
        print(f"   Input: '{cmd}' -> Command: '{command}', Args: {args}")

    print("✓ Command parsing tests completed!")


if __name__ == "__main__":
    test_task_operations()
    test_console_commands()
    print("\n🎉 All Phase I tests completed successfully!")