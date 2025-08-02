#!/usr/bin/env python3
"""Setup script for A2A Python SDK development."""

import subprocess
import sys
import os


def run_command(command, description):
    """Run a command and handle errors."""
    print(f"\n{description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✓ {description} completed successfully")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {description} failed")
        print(f"Error: {e.stderr}")
        return False


def main():
    """Main setup function."""
    print("A2A Python SDK Development Setup")
    print("=" * 40)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("Error: Python 3.8 or higher is required")
        sys.exit(1)
    
    print(f"✓ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    
    # Install dependencies
    if not run_command("pip install -r requirements.txt", "Installing dependencies"):
        print("Failed to install dependencies. Please install manually:")
        print("pip install -r requirements.txt")
        sys.exit(1)
    
    # Install package in development mode
    if not run_command("pip install -e .", "Installing package in development mode"):
        print("Failed to install package in development mode")
        sys.exit(1)
    
    # Run tests
    if not run_command("python -m pytest tests/ -v", "Running tests"):
        print("Some tests failed. Please check the output above.")
    
    print("\n" + "=" * 40)
    print("Setup completed!")
    print("\nNext steps:")
    print("1. Start the echo agent: python samples/echo_agent/main.py")
    print("2. In another terminal, run the client: python samples/client_examples/basic_client.py")
    print("3. Visit http://localhost:8000/echo/card to see the agent card")
    print("\nFor development:")
    print("- Run tests: pytest")
    print("- Format code: black src/ tests/")
    print("- Type check: mypy src/")


if __name__ == "__main__":
    main()