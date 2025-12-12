# Phase I Testing Guide

## How to Test Phase I Todo Console App

### Prerequisites
- Python 3.8+ (Python 3.13+ recommended as per original specification)
- UV package manager (install with `pip install uv`)

### Step-by-Step Setup

1. **Navigate to Phase_I directory:**
   ```bash
   cd /home/taimoor/Hackathon_II/Phase_I
   ```

2. **Create a virtual environment:**
   ```bash
   uv venv
   # or if you don't have uv: python -m venv .venv
   ```

3. **Activate the virtual environment:**
   ```bash
   # On Linux/Mac:
   source .venv/bin/activate

   # On Windows:
   source .venv\Scripts\activate
   ```

4. **Install the package in development mode:**
   ```bash
   uv pip install -e .
   # or if using regular venv: pip install -e .
   ```

5. **Run the application:**
   ```bash
   python -m src.main
   ```

### Testing All Features Manually

Once the application is running, you can test all 5 Basic Level features:

1. **Add a task:**
   ```
   > add "Buy groceries" "Milk, eggs, bread"
   ```

2. **List all tasks:**
   ```
   > list
   ```

3. **Update a task:**
   ```
   > update 1 "Buy weekly groceries" "Milk, eggs, bread, fruits"
   ```

4. **Mark a task as complete:**
   ```
   > complete 1
   ```

5. **Mark a task as incomplete:**
   ```
   > incomplete 1
   ```

6. **Delete a task:**
   ```
   > delete 1
   ```

7. **Get help:**
   ```
   > help
   ```

8. **Exit the application:**
   ```
   > quit
   # or
   > exit
   ```

### Automated Testing

You can also run the automated tests I created:

1. **Run functionality tests:**
   ```bash
   python test_phase1.py
   ```

2. **Run the demo:**
   ```bash
   python demo_phase1.py
   ```

### Quick Run Script

I've also created a convenience script that handles setup and running:

```bash
python run_app.py
```

This script will:
- Check Python version
- Install UV if needed
- Create virtual environment
- Install dependencies
- Run the application

### Expected Output

When you run `python test_phase1.py`, you should see output similar to:
```
Testing Phase I Todo Console App functionality...

1. Testing add_task functionality:
   Added task: ID 1, Title: Buy groceries, Description: Milk, eggs, bread
   Added task: ID 2, Title: Complete project

2. Testing get_all_tasks functionality:
   Total tasks: 2
   - ID 1: Buy groceries [Pending]
   - ID 2: Complete project [Pending]
...
✓ All basic functionality tests passed!
```

### Troubleshooting

- If you get a "module not found" error, make sure you're running from the Phase_I directory
- If UV is not installed, install it with: `pip install uv`
- Make sure you activate the virtual environment before running the app
- If you're using Windows, the activation command is: `.venv\Scripts\activate`

### Files Included in Phase I
- `src/` - Main source code (models, services, CLI)
- `specs/` - Specification files
- `test_phase1.py` - Automated tests
- `demo_phase1.py` - Demo script
- `run_app.py` - Convenience runner script
- `CLAUDE.md` - Claude Code instructions
- `pyproject.toml` - Project configuration
- `README.md` - Documentation