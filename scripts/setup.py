#!/usr/bin/env python3
"""
🍮 PomPom-A2A Setup Script

This script helps you set up the PomPom-A2A development environment.
"""

import subprocess
import sys
import os
import platform
from pathlib import Path


def run_command(command, description, check=True):
    """Run a command and handle errors."""
    print(f"\n🔄 {description}...")
    try:
        if isinstance(command, str):
            result = subprocess.run(command, shell=True, check=check, capture_output=True, text=True)
        else:
            result = subprocess.run(command, check=check, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ {description} completed successfully")
            if result.stdout.strip():
                print(f"   Output: {result.stdout.strip()}")
        else:
            print(f"❌ {description} failed")
            if result.stderr.strip():
                print(f"   Error: {result.stderr.strip()}")
        
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed with error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error during {description}: {e}")
        return False


def check_python_version():
    """Check if Python version is compatible."""
    version = sys.version_info
    if version < (3, 8):
        print(f"❌ Python 3.8+ is required. You have Python {version.major}.{version.minor}")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")
    return True


def check_git():
    """Check if git is available."""
    return run_command(["git", "--version"], "Checking Git installation", check=False)


def setup_development_environment():
    """Set up the complete development environment."""
    print("🍮 PomPom-A2A Development Setup")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Check if we're in the right directory
    if not Path("pyproject.toml").exists():
        print("❌ Please run this script from the project root directory")
        sys.exit(1)
    
    # Install package in development mode
    if not run_command([sys.executable, "-m", "pip", "install", "-e", ".[dev]"], 
                      "Installing PomPom-A2A in development mode"):
        print("💡 Try upgrading pip: python -m pip install --upgrade pip")
        sys.exit(1)
    
    # Run tests to verify installation
    if not run_command([sys.executable, "-m", "pytest", "tests/", "-v"], 
                      "Running tests to verify installation"):
        print("⚠️  Some tests failed, but installation may still be working")
    
    # Check code quality tools
    print("\n🔧 Checking development tools...")
    
    tools_status = {
        "black": run_command([sys.executable, "-m", "black", "--version"], "Checking Black", check=False),
        "isort": run_command([sys.executable, "-m", "isort", "--version"], "Checking isort", check=False),
        "ruff": run_command([sys.executable, "-m", "ruff", "--version"], "Checking Ruff", check=False),
        "mypy": run_command([sys.executable, "-m", "mypy", "--version"], "Checking MyPy", check=False),
        "pytest": run_command([sys.executable, "-m", "pytest", "--version"], "Checking pytest", check=False),
    }
    
    print("\n📊 Development Tools Status:")
    for tool, status in tools_status.items():
        status_icon = "✅" if status else "❌"
        print(f"   {status_icon} {tool}")
    
    # Setup git hooks (if git is available)
    if check_git():
        setup_git_hooks()
    
    print("\n" + "=" * 50)
    print("🎉 Setup completed!")
    print("\n📋 Next steps:")
    print("1. Start the echo agent:     python samples/echo_agent/main.py")
    print("2. Test the client:         python samples/client_examples/basic_client.py")
    print("3. Run tests:               pytest")
    print("4. Format code:             black src/ tests/")
    print("5. Check types:             mypy src/")
    print("\n🔧 Development commands:")
    print("- make help                 # Show all available commands")
    print("- make test                 # Run tests")
    print("- make format               # Format code")
    print("- make check                # Run all checks")
    print("\n📚 Documentation:")
    print("- README.md                 # Main documentation")
    print("- CONTRIBUTING.md           # Contribution guidelines")
    print("- DEVELOPMENT.md            # Development guide")


def setup_git_hooks():
    """Set up git hooks for code quality."""
    hooks_dir = Path(".git/hooks")
    if not hooks_dir.exists():
        return
    
    pre_commit_hook = hooks_dir / "pre-commit"
    
    hook_content = """#!/bin/sh
# PomPom-A2A pre-commit hook

echo "🍮 Running PomPom-A2A pre-commit checks..."

# Format code
python -m black src/ tests/ samples/
python -m isort src/ tests/ samples/

# Lint code
python -m ruff check src/ tests/

# Type check
python -m mypy src/

# Run tests
python -m pytest

if [ $? -ne 0 ]; then
    echo "❌ Pre-commit checks failed. Please fix the issues before committing."
    exit 1
fi

echo "✅ Pre-commit checks passed!"
"""
    
    try:
        with open(pre_commit_hook, "w") as f:
            f.write(hook_content)
        
        # Make executable on Unix systems
        if platform.system() != "Windows":
            os.chmod(pre_commit_hook, 0o755)
        
        print("✅ Git pre-commit hook installed")
    except Exception as e:
        print(f"⚠️  Could not install git hook: {e}")


def quick_test():
    """Run a quick test to verify everything works."""
    print("\n🧪 Running quick verification test...")
    
    test_code = '''
import asyncio
from pompompurin_a2a import Message, MessageRole, TextPart, TaskManager

async def test():
    # Test basic functionality
    message = Message(
        role=MessageRole.USER,
        parts=[TextPart(text="Hello PomPom!")]
    )
    
    task_manager = TaskManager()
    print(f"✅ Created message: {message.parts[0].text}")
    print(f"✅ Created task manager: {type(task_manager).__name__}")
    print("🍮 PomPom-A2A is working correctly!")

asyncio.run(test())
'''
    
    try:
        exec(test_code)
        return True
    except Exception as e:
        print(f"❌ Quick test failed: {e}")
        return False


def main():
    """Main setup function."""
    if len(sys.argv) > 1 and sys.argv[1] == "--quick-test":
        quick_test()
        return
    
    setup_development_environment()
    
    # Run quick test
    if quick_test():
        print("\n🎊 All systems go! PomPom-A2A is ready for development!")
    else:
        print("\n⚠️  Setup completed but quick test failed. Please check the installation.")


if __name__ == "__main__":
    main()