"""A2A protocol client implementation."""

import json
from typing import Optional, AsyncGenerator, Dict, Any
import httpx
from ..models.message import Message
from ..models.agent_card import AgentCard
from ..models.task import Task, TaskSendParams, TaskQueryParams
from ..exceptions import (
    A2AClientException, TaskNotFoundException, 
    InvalidRequestException, InternalErrorException
)


class A2AClient:
    """Client for communicating with A2A protocol agents."""

    def __init__(
        self, 
        base_url: str, 
        timeout: float = 30.0,
        headers: Optional[Dict[str, str]] = None
    ):
        """
        Initialize A2A client.
        
        Args:
            base_url: Base URL of the A2A agent
            timeout: Request timeout in seconds
            headers: Additional headers to include in requests
        """
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.headers = headers or {}
        self.client = httpx.AsyncClient(
            timeout=timeout,
            headers=self.headers
        )

    async def __aenter__(self):
        """Async context manager entry."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()

    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()

    async def get_agent_card(self) -> AgentCard:
        """
        Get agent capabilities and metadata.
        
        Returns:
            AgentCard: Agent capabilities and metadata
            
        Raises:
            A2AClientException: If the request fails
        """
        try:
            response = await self.client.get(f"{self.base_url}/card")
            response.raise_for_status()
            return AgentCard(**response.json())
        except httpx.HTTPStatusError as e:
            raise A2AClientException(f"Failed to get agent card: {e.response.status_code}")
        except httpx.RequestError as e:
            raise A2AClientException(f"Request failed: {str(e)}")
        except Exception as e:
            raise A2AClientException(f"Unexpected error: {str(e)}")

    async def send_message(self, message: Message) -> Message:
        """
        Send a message and get immediate response (stateless communication).
        
        Args:
            message: Message to send
            
        Returns:
            Message: Response message
            
        Raises:
            A2AClientException: If the request fails
        """
        try:
            response = await self.client.post(
                f"{self.base_url}/message/send",
                json=message.model_dump(),
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            return Message(**response.json())
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 400:
                raise InvalidRequestException("Invalid message format")
            elif e.response.status_code == 500:
                raise InternalErrorException("Server error")
            else:
                raise A2AClientException(f"HTTP error: {e.response.status_code}")
        except httpx.RequestError as e:
            raise A2AClientException(f"Request failed: {str(e)}")
        except Exception as e:
            raise A2AClientException(f"Unexpected error: {str(e)}")

    async def send_message_stream(self, message: Message) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Send a message and stream the response.
        
        Args:
            message: Message to send
            
        Yields:
            Dict[str, Any]: Streaming response events
            
        Raises:
            A2AClientException: If the request fails
        """
        try:
            async with self.client.stream(
                "POST",
                f"{self.base_url}/message/sendSubscribe",
                json=message.model_dump(),
                headers={
                    "Content-Type": "application/json",
                    "Accept": "text/event-stream"
                }
            ) as response:
                response.raise_for_status()
                
                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        try:
                            data = json.loads(line[6:])
                            yield data
                        except json.JSONDecodeError:
                            # Skip invalid JSON lines
                            continue
                    elif line.strip() == "":
                        # Empty line, continue
                        continue
                        
        except httpx.HTTPStatusError as e:
            raise A2AClientException(f"HTTP error: {e.response.status_code}")
        except httpx.RequestError as e:
            raise A2AClientException(f"Request failed: {str(e)}")
        except Exception as e:
            raise A2AClientException(f"Unexpected error: {str(e)}")

    async def create_task(self, params: TaskSendParams) -> Task:
        """
        Create a new task.
        
        Args:
            params: Task creation parameters
            
        Returns:
            Task: Created task
            
        Raises:
            A2AClientException: If the request fails
        """
        try:
            response = await self.client.post(
                f"{self.base_url}/tasks",
                json=params.model_dump(),
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            return Task(**response.json())
        except httpx.HTTPStatusError as e:
            raise A2AClientException(f"HTTP error: {e.response.status_code}")
        except httpx.RequestError as e:
            raise A2AClientException(f"Request failed: {str(e)}")
        except Exception as e:
            raise A2AClientException(f"Unexpected error: {str(e)}")

    async def get_task(self, task_id: str, history_length: Optional[int] = None) -> Task:
        """
        Get a task by ID.
        
        Args:
            task_id: Task identifier
            history_length: Maximum number of history items to return
            
        Returns:
            Task: Task information
            
        Raises:
            TaskNotFoundException: If the task is not found
            A2AClientException: If the request fails
        """
        try:
            params = {}
            if history_length is not None:
                params["historyLength"] = history_length
                
            response = await self.client.get(
                f"{self.base_url}/tasks/{task_id}",
                params=params
            )
            
            if response.status_code == 404:
                raise TaskNotFoundException(task_id)
                
            response.raise_for_status()
            return Task(**response.json())
        except TaskNotFoundException:
            raise
        except httpx.HTTPStatusError as e:
            raise A2AClientException(f"HTTP error: {e.response.status_code}")
        except httpx.RequestError as e:
            raise A2AClientException(f"Request failed: {str(e)}")
        except Exception as e:
            raise A2AClientException(f"Unexpected error: {str(e)}")

    async def send_task_message(
        self, 
        task_id: str, 
        params: TaskSendParams,
        history_length: Optional[int] = None
    ) -> Task:
        """
        Send a message to an existing task.
        
        Args:
            task_id: Task identifier
            params: Message parameters
            history_length: Maximum number of history items to return
            
        Returns:
            Task: Updated task
            
        Raises:
            TaskNotFoundException: If the task is not found
            A2AClientException: If the request fails
        """
        try:
            query_params = {}
            if history_length is not None:
                query_params["historyLength"] = history_length
                
            response = await self.client.post(
                f"{self.base_url}/tasks/{task_id}/send",
                json=params.model_dump(),
                params=query_params,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 404:
                raise TaskNotFoundException(task_id)
                
            response.raise_for_status()
            return Task(**response.json())
        except TaskNotFoundException:
            raise
        except httpx.HTTPStatusError as e:
            raise A2AClientException(f"HTTP error: {e.response.status_code}")
        except httpx.RequestError as e:
            raise A2AClientException(f"Request failed: {str(e)}")
        except Exception as e:
            raise A2AClientException(f"Unexpected error: {str(e)}")

    async def send_task_message_stream(
        self, 
        task_id: str, 
        params: TaskSendParams,
        history_length: Optional[int] = None
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Send a message to a task and stream the response.
        
        Args:
            task_id: Task identifier
            params: Message parameters
            history_length: Maximum number of history items to return
            
        Yields:
            Dict[str, Any]: Streaming response events
            
        Raises:
            TaskNotFoundException: If the task is not found
            A2AClientException: If the request fails
        """
        try:
            query_params = {}
            if history_length is not None:
                query_params["historyLength"] = history_length
                
            async with self.client.stream(
                "POST",
                f"{self.base_url}/tasks/{task_id}/sendSubscribe",
                json=params.model_dump(),
                params=query_params,
                headers={
                    "Content-Type": "application/json",
                    "Accept": "text/event-stream"
                }
            ) as response:
                if response.status_code == 404:
                    raise TaskNotFoundException(task_id)
                    
                response.raise_for_status()
                
                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        try:
                            data = json.loads(line[6:])
                            yield data
                        except json.JSONDecodeError:
                            continue
                            
        except TaskNotFoundException:
            raise
        except httpx.HTTPStatusError as e:
            raise A2AClientException(f"HTTP error: {e.response.status_code}")
        except httpx.RequestError as e:
            raise A2AClientException(f"Request failed: {str(e)}")
        except Exception as e:
            raise A2AClientException(f"Unexpected error: {str(e)}")

    async def cancel_task(self, task_id: str) -> Task:
        """
        Cancel a task.
        
        Args:
            task_id: Task identifier
            
        Returns:
            Task: Canceled task
            
        Raises:
            TaskNotFoundException: If the task is not found
            A2AClientException: If the request fails
        """
        try:
            response = await self.client.post(f"{self.base_url}/tasks/{task_id}/cancel")
            
            if response.status_code == 404:
                raise TaskNotFoundException(task_id)
                
            response.raise_for_status()
            return Task(**response.json())
        except TaskNotFoundException:
            raise
        except httpx.HTTPStatusError as e:
            raise A2AClientException(f"HTTP error: {e.response.status_code}")
        except httpx.RequestError as e:
            raise A2AClientException(f"Request failed: {str(e)}")
        except Exception as e:
            raise A2AClientException(f"Unexpected error: {str(e)}")

    async def resubscribe_task(self, task_id: str) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Resubscribe to task updates.
        
        Args:
            task_id: Task identifier
            
        Yields:
            Dict[str, Any]: Task update events
            
        Raises:
            TaskNotFoundException: If the task is not found
            A2AClientException: If the request fails
        """
        try:
            async with self.client.stream(
                "POST",
                f"{self.base_url}/tasks/{task_id}/resubscribe",
                headers={"Accept": "text/event-stream"}
            ) as response:
                if response.status_code == 404:
                    raise TaskNotFoundException(task_id)
                    
                response.raise_for_status()
                
                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        try:
                            data = json.loads(line[6:])
                            yield data
                        except json.JSONDecodeError:
                            continue
                            
        except TaskNotFoundException:
            raise
        except httpx.HTTPStatusError as e:
            raise A2AClientException(f"HTTP error: {e.response.status_code}")
        except httpx.RequestError as e:
            raise A2AClientException(f"Request failed: {str(e)}")
        except Exception as e:
            raise A2AClientException(f"Unexpected error: {str(e)}")