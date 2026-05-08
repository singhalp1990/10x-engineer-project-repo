"""Data models for PromptLab using Pydantic."""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


def get_current_time() -> datetime:
    """Get current UTC time.

    Returns:
        Current datetime in UTC.
    """
    return datetime.utcnow()


# ============== Base Models ==============

class PromptBase(BaseModel):
    """Base model for prompt data."""
    
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1, max_length=10000)
    description: Optional[str] = Field(None, max_length=500)
    collection_id: Optional[str] = None


class CollectionBase(BaseModel):
    """Base model for collection data."""
    
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=500)


# ============== Request Models ==============

class PromptCreate(PromptBase):
    """Model for creating a new prompt."""
    pass


class PromptUpdate(BaseModel):
    """Model for updating an existing prompt."""
    
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    content: Optional[str] = Field(None, min_length=1, max_length=10000)
    description: Optional[str] = Field(None, max_length=500)
    collection_id: Optional[str] = None


class CollectionCreate(CollectionBase):
    """Model for creating a new collection."""
    pass


# ============== Response Models ==============

class Prompt(PromptBase):
    """Prompt model with metadata."""
    
    id: str
    created_at: datetime

    class Config:
        from_attributes = True


class Collection(CollectionBase):
    """Collection model with metadata."""
    
    id: str
    created_at: datetime

    class Config:
        from_attributes = True


class PromptList(BaseModel):
    """Response model for listing prompts."""
    
    prompts: List[Prompt]
    total: int


class CollectionList(BaseModel):
    """Response model for listing collections."""
    
    collections: List[Collection]
    total: int


class HealthResponse(BaseModel):
    """Response model for health check."""
    
    status: str
    version: str
