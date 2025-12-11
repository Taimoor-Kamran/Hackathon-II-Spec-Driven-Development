#!/usr/bin/env python3
"""
Simple runner script for the Phase I Todo Console App
This script provides a single command way to run the application
"""

import sys
import subprocess
import os
from pathlib import Path


def check_python_version():
    """Check if Python 3.8+ is available (required for basic functionality)."""
    if sys.version_info < (3, 8):
        print(f"Python 3.8 or higher is required. You have {sys.version}.")
        return False
    return True


def check_uv_installed():
    """Check if UV is installed."""
    try:
        result = subprocess.run(['uv', '--version'], capture_output=True, text=True)
        return True
    except FileNotFoundError:
        return False


def install_uv():
    """Install UV package manager."""
    print("Installing UV package manager...")
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'uv'], check=True)
        print("UV installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("Failed to install UV. Please install it manually with: pip install uv")
        return False


def setup_and_run():
    """Setup virtual environment and run the application."""
    print("Setting up the Todo Console App...")

    # Check Python version
    if not check_python_version():
        return False

    # Check if UV is installed
    if not check_uv_installed():
        print("UV package manager not found.")
        if not install_uv():
            return False

    # Create virtual environment if it doesn't exist
    venv_path = Path('.venv')
    if not venv_path.exists():
        print("Creating virtual environment...")
        try:
            subprocess.run(['uv', 'venv'], check=True)
            print("Virtual environment created successfully!")
        except subprocess.CalledProcessError:
            print("Failed to create virtual environment.")
            return False

    # Install the package in development mode
    print("Installing the application...")
    try:
        subprocess.run(['uv', 'pip', 'install', '-e', '.'], check=True)
        print("Application installed successfully!")
    except subprocess.CalledProcessError:
        print("Failed to install the application.")
        return False

    # Determine the activation script path
    if os.name == 'nt':  # Windows
        activate_script = '.venv\\Scripts\\activate'
        python_cmd = '.venv\\Scripts\\python'
    else:  # Unix/Linux/Mac
        activate_script = '.venv/bin/activate'
        python_cmd = '.venv/bin/python'

    print(f"\nTo run the application manually, activate the virtual environment:")
    print(f"  source {activate_script}  # On Linux/Mac")
    print(f"  {activate_script}  # On Windows")
    print(f"And then run: python -m src.main")

    print(f"\nStarting the application now...")
    try:
        subprocess.run([python_cmd, '-m', 'src.main'])
        return True
    except subprocess.CalledProcessError:
        print("Failed to start the application.")
        return False


def main():
    """Main function to run the setup and application."""
    print("Todo Console App - Phase I Runner")
    print("=" * 40)

    success = setup_and_run()

    if not success:
        print("\nSetup failed. Please follow the manual installation steps in the README.")
        sys.exit(1)


if __name__ == "__main__":
    main()