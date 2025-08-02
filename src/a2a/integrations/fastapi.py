"""FastAPI integration for A2A protocol."""

import json
from typing import Dict, Any
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import StreamingResponse
from ..server.task_manager import TaskManager
from ..models.message import Message
from ..models.task import TaskSendParams, TaskQueryParams
from ..exceptions import (
    TaskNotFoundException, TaskNotCancelableException,
    InvalidRequestException, InternalErrorException,
    A2AException
)


def add_a2a_routes(app: FastAPI, task_manager: TaskManager, prefix: str = ""):
    """
    Add A2A protocol routes to a FastAPI application.
    
    Args:
        app: FastAPI application instance
        task_manager: TaskManager instance to handle requests
        prefix: URL prefix for the agent (e.g., "/echo")
    """
    
    def handle_a2a_exception(e: Exception) -> HTTPException:
        """Convert A2A exceptions to HTTP exceptions."""
        if isinstance(e, TaskNotFoundException):
            return HTTPException(status_code=404, detail=str(e))
        elif isinstance(e, TaskNotCancelableException):
            return HTTPException(status_code=400, detail=str(e))
        elif isinstance(e, InvalidRequestException):
            return HTTPException(status_code=400, detail=str(e))
        elif isinstance(e, InternalErrorException):
            return HTTPException(status_code=500, detail=str(e))
        elif isinstance(e, A2AException):
            return HTTPException(status_code=500, detail=str(e))
        else:
            return HTTPException(status_code=500, detail="Internal server error")

    @app.get(f"{prefix}/card")
    async def get_agent_card(request: Request):
        """Get agent card information."""
        try:
            # Construct the agent URL from the request
            agent_url = f"{request.url.scheme}://{request.url.netloc}{prefix}"
            card = await task_manager.get_agent_card(agent_url)
            return card.model_dump()
        except Exception as e:
            raise handle_a2a_exception(e)

    @app.post(f"{prefix}/message/send")
    async def send_message(message: Message):
        """Send a message and get immediate response."""
        try:
            response = await task_manager.process_message(message)
            return response.model_dump()
        except Exception as e:
            raise handle_a2a_exception(e)

    @app.post(f"{prefix}/message/sendSubscribe")
    async def send_message_stream(message: Message):
        """Send a message and stream the response."""
        async def event_stream():
            try:
                response = await task_manager.process_message(message)
                # For simple message processing, just return the response
                yield f"data: {response.model_dump_json()}\n\n"
            except Exception as e:
                error_data = {
                    "error": str(e),
                    "type": "error"
                }
                yield f"data: {json.dumps(error_data)}\n\n"
        
        return StreamingResponse(
            event_stream(), 
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
            }
        )

    @app.post(f"{prefix}/tasks")
    async def create_task(params: TaskSendParams):
        """Create a new task."""
        try:
            task = await task_manager.create_task(params)
            return task.model_dump()
        except Exception as e:
            raise handle_a2a_exception(e)

    @app.get(f"{prefix}/tasks/{{task_id}}")
    async def get_task(
        task_id: str, 
        historyLength: int = None,
        metadata: str = None
    ):
        """Get a task by ID."""
        try:
            # Parse metadata if provided
            parsed_metadata = None
            if metadata:
                try:
                    parsed_metadata = json.loads(metadata)
                except json.JSONDecodeError:
                    raise InvalidRequestException("Invalid metadata JSON")
            
            params = TaskQueryParams(
                id=task_id,
                history_length=historyLength,
                metadata=parsed_metadata
            )
            task = await task_manager.get_task(params)
            return task.model_dump()
        except Exception as e:
            raise handle_a2a_exception(e)

    @app.post(f"{prefix}/tasks/{{task_id}}/send")
    async def send_task_message(
        task_id: str,
        params: TaskSendParams,
        historyLength: int = None,
        metadata: str = None
    ):
        """Send a message to an existing task."""
        try:
            task = await task_manager.send_task_message(task_id, params)
            
            # Apply history length limit if specified
            if historyLength is not None and task.history:
                task.history = task.history[-historyLength:]
            
            return task.model_dump()
        except Exception as e:
            raise handle_a2a_exception(e)

    @app.post(f"{prefix}/tasks/{{task_id}}/sendSubscribe")
    async def send_task_message_stream(
        task_id: str,
        params: TaskSendParams,
        historyLength: int = None,
        metadata: str = None
    ):
        """Send a message to a task and stream the response."""
        async def event_stream():
            try:
                async for event in task_manager.send_task_message_stream(task_id, params):
                    yield f"data: {json.dumps(event['data'])}\n\n"
            except Exception as e:
                error_data = {
                    "error": str(e),
                    "type": "error"
                }
                yield f"data: {json.dumps(error_data)}\n\n"
        
        return StreamingResponse(
            event_stream(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
            }
        )

    @app.post(f"{prefix}/tasks/{{task_id}}/cancel")
    async def cancel_task(task_id: str):
        """Cancel a task."""
        try:
            task = await task_manager.cancel_task(task_id)
            return task.model_dump()
        except Exception as e:
            raise handle_a2a_exception(e)

    @app.post(f"{prefix}/tasks/{{task_id}}/resubscribe")
    async def resubscribe_task(task_id: str):
        """Resubscribe to task updates."""
        async def event_stream():
            try:
                async for event in task_manager.resubscribe_task(task_id):
                    yield f"data: {json.dumps(event['data'])}\n\n"
            except Exception as e:
                error_data = {
                    "error": str(e),
                    "type": "error"
                }
                yield f"data: {json.dumps(error_data)}\n\n"
        
        return StreamingResponse(
            event_stream(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
            }
        )

    # Optional: Add push notification endpoints (placeholder for future implementation)
    @app.get(f"{prefix}/tasks/{{task_id}}/pushNotification")
    async def get_push_notification_config(task_id: str):
        """Get push notification configuration for a task."""
        raise HTTPException(status_code=501, detail="Push notifications not implemented")

    @app.put(f"{prefix}/tasks/{{task_id}}/pushNotification")
    async def set_push_notification_config(task_id: str, config: Dict[str, Any]):
        """Set push notification configuration for a task."""
        raise HTTPException(status_code=501, detail="Push notifications not implemented")

    @app.delete(f"{prefix}/tasks/{{task_id}}/pushNotification")
    async def delete_push_notification_config(task_id: str):
        """Delete push notification configuration for a task."""
        raise HTTPException(status_code=501, detail="Push notifications not implemented")