"""A2A protocol exceptions."""

from typing import Optional, Any, Dict


class A2AException(Exception):
    """Base exception for A2A protocol errors."""
    
    def __init__(self, message: str, code: Optional[int] = None, data: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.code = code
        self.data = data


class A2AClientException(A2AException):
    """Exception for A2A client errors."""
    pass


class A2AServerException(A2AException):
    """Exception for A2A server errors."""
    pass


class TaskNotFoundException(A2AException):
    """Exception raised when a task is not found."""
    
    def __init__(self, task_id: str):
        super().__init__(f"Task not found: {task_id}", code=-32001)


class TaskNotCancelableException(A2AException):
    """Exception raised when a task cannot be canceled."""
    
    def __init__(self, task_id: str):
        super().__init__(f"Task cannot be canceled: {task_id}", code=-32002)


class PushNotificationNotSupportedException(A2AException):
    """Exception raised when push notifications are not supported."""
    
    def __init__(self):
        super().__init__("Push Notification is not supported", code=-32003)


class UnsupportedOperationException(A2AException):
    """Exception raised when an operation is not supported."""
    
    def __init__(self, operation: str):
        super().__init__(f"This operation is not supported: {operation}", code=-32004)


class InvalidRequestException(A2AException):
    """Exception raised for invalid requests."""
    
    def __init__(self, message: str = "Request payload validation error"):
        super().__init__(message, code=-32600)


class MethodNotFoundException(A2AException):
    """Exception raised when a method is not found."""
    
    def __init__(self, method: str):
        super().__init__(f"Method not found: {method}", code=-32601)


class InvalidParamsException(A2AException):
    """Exception raised for invalid parameters."""
    
    def __init__(self, message: str = "Invalid parameters"):
        super().__init__(message, code=-32602)


class InternalErrorException(A2AException):
    """Exception raised for internal errors."""
    
    def __init__(self, message: str = "Internal error"):
        super().__init__(message, code=-32603)