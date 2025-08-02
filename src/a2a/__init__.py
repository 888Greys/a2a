"""
🍮 PomPom-A2A: A delightfully simple Python SDK for the Agent2Agent (A2A) protocol

PomPom-A2A makes building AI agents as easy as enjoying a pudding! This Python SDK 
provides a complete, production-ready implementation of the Agent2Agent (A2A) Protocol,
enabling seamless communication between AI agents and applications.

Example:
    >>> from pompompurin_a2a import TaskManager, Message, MessageRole, TextPart
    >>> 
    >>> # Create a simple agent
    >>> task_manager = TaskManager()
    >>> 
    >>> async def my_agent(message: Message) -> Message:
    ...     return Message(
    ...         role=MessageRole.AGENT,
    ...         parts=[TextPart(text=f"🍮 PomPom says: {message.parts[0].text}")]
    ...     )
    >>> 
    >>> task_manager.on_message_received = my_agent
"""

__version__ = "0.1.0"
__author__ = "PomPom-A2A Team"
__email__ = "team@pompom-a2a.dev"
__license__ = "Apache-2.0"
__description__ = "🍮 PomPom-A2A: A delightfully simple Python SDK for the Agent2Agent (A2A) protocol"

# Core models
from .models.message import Message, MessageRole, TextPart, FilePart, DataPart, FileContent
from .models.agent_card import (
    AgentCard, 
    AgentCapabilities, 
    AgentSkill, 
    AgentProvider,
    AgentAuthentication
)
from .models.task import (
    Task, 
    TaskStatus, 
    TaskState, 
    TaskSendParams,
    TaskQueryParams,
    TaskStatusUpdateEvent,
    TaskArtifactUpdateEvent,
    Artifact
)

# Client components
from .client.a2a_client import A2AClient
from .client.card_resolver import A2ACardResolver

# Server components
from .server.task_manager import TaskManager
from .server.task_store import TaskStore, InMemoryTaskStore

# Exceptions
from .exceptions import (
    A2AException,
    A2AClientException,
    A2AServerException,
    TaskNotFoundException,
    TaskNotCancelableException,
    PushNotificationNotSupportedException,
    UnsupportedOperationException,
    InvalidRequestException,
    MethodNotFoundException,
    InvalidParamsException,
    InternalErrorException
)

# Main exports
__all__ = [
    # Core models
    "Message",
    "MessageRole", 
    "TextPart",
    "FilePart",
    "DataPart",
    "FileContent",
    "AgentCard",
    "AgentCapabilities",
    "AgentSkill",
    "AgentProvider", 
    "AgentAuthentication",
    "Task",
    "TaskStatus",
    "TaskState",
    "TaskSendParams",
    "TaskQueryParams",
    "TaskStatusUpdateEvent",
    "TaskArtifactUpdateEvent",
    "Artifact",
    
    # Client components
    "A2AClient",
    "A2ACardResolver",
    
    # Server components
    "TaskManager",
    "TaskStore",
    "InMemoryTaskStore",
    
    # Exceptions
    "A2AException",
    "A2AClientException", 
    "A2AServerException",
    "TaskNotFoundException",
    "TaskNotCancelableException",
    "PushNotificationNotSupportedException",
    "UnsupportedOperationException",
    "InvalidRequestException",
    "MethodNotFoundException",
    "InvalidParamsException",
    "InternalErrorException",
]

# Package metadata
__package_name__ = "pompompurin-a2a"
__repository__ = "https://github.com/yourusername/pompompurin-a2a"
__documentation__ = "https://github.com/yourusername/pompompurin-a2a#readme"
__homepage__ = "https://github.com/yourusername/pompompurin-a2a"