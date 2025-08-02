"""Task manager for handling A2A protocol operations."""

import uuid
from datetime import datetime, timezone
from typing import Callable, Optional, AsyncGenerator, Dict, Any
from ..models.message import Message
from ..models.agent_card import AgentCard
from ..models.task import (
    Task, TaskStatus, TaskState, TaskSendParams, TaskQueryParams,
    TaskStatusUpdateEvent, TaskArtifactUpdateEvent
)
from ..exceptions import (
    TaskNotFoundException, TaskNotCancelableException,
    InternalErrorException
)
from .task_store import TaskStore, InMemoryTaskStore


class TaskManager:
    """Manages A2A protocol tasks and message handling."""

    def __init__(self, task_store: Optional[TaskStore] = None):
        self.task_store = task_store or InMemoryTaskStore()
        
        # Event handlers - to be set by the agent implementation
        self.on_message_received: Optional[Callable[[Message], Message]] = None
        self.on_agent_card_query: Optional[Callable[[str], AgentCard]] = None
        self.on_task_created: Optional[Callable[[Task], None]] = None
        self.on_task_updated: Optional[Callable[[Task], None]] = None
        self.on_task_canceled: Optional[Callable[[Task], None]] = None

    async def process_message(self, message: Message) -> Message:
        """Process a direct message (stateless communication)."""
        if not self.on_message_received:
            raise InternalErrorException("No message handler registered")
        
        try:
            return await self.on_message_received(message)
        except Exception as e:
            raise InternalErrorException(f"Error processing message: {str(e)}")

    async def get_agent_card(self, agent_url: str) -> AgentCard:
        """Get agent card information."""
        if not self.on_agent_card_query:
            raise InternalErrorException("No agent card handler registered")
        
        try:
            return await self.on_agent_card_query(agent_url)
        except Exception as e:
            raise InternalErrorException(f"Error getting agent card: {str(e)}")

    async def create_task(self, params: TaskSendParams) -> Task:
        """Create a new task."""
        task_id = str(uuid.uuid4())
        
        # Create initial task
        task = Task(
            id=task_id,
            session_id=params.session_id,
            status=TaskStatus(
                state=TaskState.SUBMITTED,
                timestamp=datetime.utcnow()
            ),
            history=[params.message],
            metadata={}
        )
        
        # Store the task
        await self.task_store.create_task(task)
        
        # Notify handler
        if self.on_task_created:
            await self.on_task_created(task)
        
        # Process the initial message
        try:
            # Update task state to working
            task.status = TaskStatus(
                state=TaskState.WORKING,
                timestamp=datetime.utcnow()
            )
            await self.task_store.update_task(task)
            
            # Process the message
            if self.on_message_received:
                response = await self.on_message_received(params.message)
                
                # Add response to history
                task.history.append(response)
                
                # Update task state to completed
                task.status = TaskStatus(
                    state=TaskState.COMPLETED,
                    message=response,
                    timestamp=datetime.utcnow()
                )
                await self.task_store.update_task(task)
                
                if self.on_task_updated:
                    await self.on_task_updated(task)
            
        except Exception as e:
            # Update task state to failed
            task.status = TaskStatus(
                state=TaskState.FAILED,
                timestamp=datetime.utcnow()
            )
            await self.task_store.update_task(task)
            raise InternalErrorException(f"Error processing task: {str(e)}")
        
        return task

    async def get_task(self, params: TaskQueryParams) -> Task:
        """Get a task by ID."""
        task = await self.task_store.get_task(params.id)
        
        # Apply history length limit if specified
        if params.history_length is not None and task.history:
            task.history = task.history[-params.history_length:]
        
        return task

    async def send_task_message(self, task_id: str, params: TaskSendParams) -> Task:
        """Send a message to an existing task."""
        task = await self.task_store.get_task(task_id)
        
        # Add message to history
        if not task.history:
            task.history = []
        task.history.append(params.message)
        
        # Update task state to working
        task.status = TaskStatus(
            state=TaskState.WORKING,
            timestamp=datetime.utcnow()
        )
        await self.task_store.update_task(task)
        
        try:
            # Process the message
            if self.on_message_received:
                response = await self.on_message_received(params.message)
                
                # Add response to history
                task.history.append(response)
                
                # Update task state to completed
                task.status = TaskStatus(
                    state=TaskState.COMPLETED,
                    message=response,
                    timestamp=datetime.utcnow()
                )
                await self.task_store.update_task(task)
                
                if self.on_task_updated:
                    await self.on_task_updated(task)
            
        except Exception as e:
            # Update task state to failed
            task.status = TaskStatus(
                state=TaskState.FAILED,
                timestamp=datetime.utcnow()
            )
            await self.task_store.update_task(task)
            raise InternalErrorException(f"Error processing task message: {str(e)}")
        
        return task

    async def send_task_message_stream(
        self, 
        task_id: str, 
        params: TaskSendParams
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """Send a message to a task and stream the response."""
        task = await self.task_store.get_task(task_id)
        
        # Add message to history
        if not task.history:
            task.history = []
        task.history.append(params.message)
        
        # Update task state to working
        task.status = TaskStatus(
            state=TaskState.WORKING,
            timestamp=datetime.utcnow()
        )
        await self.task_store.update_task(task)
        
        # Yield status update
        yield {
            "type": "status_update",
            "data": TaskStatusUpdateEvent(
                id=task_id,
                status=task.status
            ).model_dump()
        }
        
        try:
            # Process the message
            if self.on_message_received:
                response = await self.on_message_received(params.message)
                
                # Add response to history
                task.history.append(response)
                
                # Update task state to completed
                task.status = TaskStatus(
                    state=TaskState.COMPLETED,
                    message=response,
                    timestamp=datetime.utcnow()
                )
                await self.task_store.update_task(task)
                
                # Yield final status update
                yield {
                    "type": "status_update",
                    "data": TaskStatusUpdateEvent(
                        id=task_id,
                        status=task.status,
                        final=True
                    ).model_dump()
                }
                
                if self.on_task_updated:
                    await self.on_task_updated(task)
            
        except Exception as e:
            # Update task state to failed
            task.status = TaskStatus(
                state=TaskState.FAILED,
                timestamp=datetime.utcnow()
            )
            await self.task_store.update_task(task)
            
            # Yield error status
            yield {
                "type": "status_update",
                "data": TaskStatusUpdateEvent(
                    id=task_id,
                    status=task.status,
                    final=True
                ).model_dump()
            }
            
            raise InternalErrorException(f"Error processing task message: {str(e)}")

    async def cancel_task(self, task_id: str) -> Task:
        """Cancel a task."""
        task = await self.task_store.get_task(task_id)
        
        # Check if task can be canceled
        if task.status.state in [TaskState.COMPLETED, TaskState.FAILED, TaskState.CANCELED]:
            raise TaskNotCancelableException(task_id)
        
        # Update task state to canceled
        task.status = TaskStatus(
            state=TaskState.CANCELED,
            timestamp=datetime.utcnow()
        )
        await self.task_store.update_task(task)
        
        if self.on_task_canceled:
            await self.on_task_canceled(task)
        
        return task

    async def resubscribe_task(self, task_id: str) -> AsyncGenerator[Dict[str, Any], None]:
        """Resubscribe to task updates."""
        task = await self.task_store.get_task(task_id)
        
        # Yield current status
        yield {
            "type": "status_update",
            "data": TaskStatusUpdateEvent(
                id=task_id,
                status=task.status,
                final=task.status.state in [TaskState.COMPLETED, TaskState.FAILED, TaskState.CANCELED]
            ).model_dump()
        }