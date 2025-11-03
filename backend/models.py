"""
Data models for CE Email Summarizer API
"""
from typing import List, Literal
from pydantic import BaseModel, Field


class Message(BaseModel):
    """Individual email message in a thread"""
    id: str
    sender: Literal["customer", "company"]
    timestamp: str
    body: str


class Thread(BaseModel):
    """Email thread with all messages"""
    thread_id: str
    topic: str
    subject: str
    initiated_by: Literal["customer", "company"]
    order_id: str
    product: str
    messages: List[Message]


class ThreadSummary(BaseModel):
    """AI-generated summary of an email thread"""
    thread_id: str
    order_id: str
    product: str
    issue_category: str
    summary: str
    sentiment: Literal["positive", "neutral", "negative", "frustrated"]
    status: Literal["pending", "in_progress", "resolved", "unresolved"]
    action_items: List[str]
    priority: Literal["low", "medium", "high"]


class SummarizeRequest(BaseModel):
    """Request to summarize a thread"""
    thread: Thread


class SummarizeResponse(BaseModel):
    """Response with generated summary"""
    success: bool
    summary: ThreadSummary
    message: str = "Summary generated successfully"


class ErrorResponse(BaseModel):
    """Error response"""
    success: bool = False
    error: str
    detail: str = ""
