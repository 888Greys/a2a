"""Task storage interfaces and implementations."""

from abc import ABC, abstractmethod
from typing import Dict, Optional, List
from ..models.task import Task
from ..exceptions import TaskNotFoundException


class TaskStore(ABC):
    """Abstract base class for task storage."""

    @abstractmethod
    async def create_task(self, task: Task) -> Task:
        """Create a new task."""
        pass

    @abstractmethod
    async def get_task(self, task_id: str) -> Task:
        """Get a task by ID."""
        pass

    @abstractmethod
    async def update_task(self, task: Task) -> Task:
        """Update an existing task."""
        pass

    @abstractmethod
    async def delete_task(self, task_id: str) -> bool:
        """Delete a task by ID."""
        pass

    @abstractmethod
    async def list_tasks(self, session_id: Optional[str] = None) -> List[Task]:
        """List tasks, optionally filtered by session ID."""
        pass

    @abstractmethod
    async def task_exists(self, task_id: str) -> bool:
        """Check if a task exists."""
        pass


class InMemoryTaskStore(TaskStore):
    """In-memory implementation of TaskStore for development and testing."""

    def __init__(self):
        self._tasks: Dict[str, Task] = {}

    async def create_task(self, task: Task) -> Task:
        """Create a new task."""
        if task.id in self._tasks:
            raise ValueError(f"Task with ID {task.id} already exists")
        
        self._tasks[task.id] = task
        return task

    async def get_task(self, task_id: str) -> Task:
        """Get a task by ID."""
        if task_id not in self._tasks:
            raise TaskNotFoundException(task_id)
        
        return self._tasks[task_id]

    async def update_task(self, task: Task) -> Task:
        """Update an existing task."""
        if task.id not in self._tasks:
            raise TaskNotFoundException(task.id)
        
        self._tasks[task.id] = task
        return task

    async def delete_task(self, task_id: str) -> bool:
        """Delete a task by ID."""
        if task_id not in self._tasks:
            return False
        
        del self._tasks[task_id]
        return True

    async def list_tasks(self, session_id: Optional[str] = None) -> List[Task]:
        """List tasks, optionally filtered by session ID."""
        tasks = list(self._tasks.values())
        
        if session_id is not None:
            tasks = [task for task in tasks if task.session_id == session_id]
        
        return tasks

    async def task_exists(self, task_id: str) -> bool:
        """Check if a task exists."""
        return task_id in self._tasks

    def clear(self) -> None:
        """Clear all tasks (useful for testing)."""
        self._tasks.clear()

    def size(self) -> int:
        """Get the number of stored tasks."""
        return len(self._tasks)