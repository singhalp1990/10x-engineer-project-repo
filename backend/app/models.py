"""Pydantic models for PromptLab.

This module defines all data models used for request validation,
response serialization, and database representation in the PromptLab
application. Models are organized into logical groups: Prompts,
Collections, and API Responses.
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from uuid import uuid4


def generate_id() -> str:
    """Generate a unique identifier using UUID4.
    
    Creates a new UUID4 string that can be used as a unique identifier
    for prompts, collections, and other entities.
    
    Returns:
        A string representation of a UUID4 identifier.
        
    Example:
        >>> id_value = generate_id()
        >>> len(id_value)
        36
        >>> isinstance(id_value, str)
        True
    """
    return str(uuid4())


def get_current_time() -> datetime:
    """Get the current UTC time.
    
    Returns the current date and time in UTC timezone, used for
    setting created_at and updated_at timestamps on all entities.
    
    Returns:
        A datetime object representing the current UTC time.
        
    Example:
        >>> time = get_current_time()
        >>> isinstance(time, datetime)
        True
    """
    return datetime.utcnow()


# ============== Prompt Models ==============

class PromptBase(BaseModel):
    """Base model for prompt data validation.
    
    Defines common fields and validation rules shared between
    prompt creation and update operations.
    
    Attributes:
        title: The title of the prompt (1-200 characters).
        content: The prompt template content (minimum 1 character).
        description: Optional detailed description of the prompt.
        collection_id: Optional ID linking prompt to a collection.
        
    Example:
        >>> prompt = PromptBase(
        ...     title="Python Tips",
        ...     content="Write a Python function that...",
        ...     description="Basic Python prompt",
        ...     collection_id=None
        ... )
        >>> prompt.title
        'Python Tips'
    """
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1)
    description: Optional[str] = Field(None, max_length=500)
    collection_id: Optional[str] = None


class PromptCreate(PromptBase):
    """Request model for creating a new prompt.
    
    Inherits all validation rules from PromptBase. Used to validate
    incoming POST requests for prompt creation.
    
    This model ensures that required fields are provided and optional
    fields meet their constraints before database insertion.
    
    Example:
        >>> prompt_data = PromptCreate(
        ...     title="New Prompt",
        ...     content="Prompt content here"
        ... )
        >>> isinstance(prompt_data, PromptBase)
        True
    """
    pass


class PromptUpdate(PromptBase):
    """Request model for updating an existing prompt.
    
    Inherits all validation rules from PromptBase. Used to validate
    incoming PUT requests for prompt updates.
    
    Note: This model requires all fields from PromptBase. For partial
    updates, only provided fields should be applied to existing records.
    
    Example:
        >>> update_data = PromptUpdate(
        ...     title="Updated Title",
        ...     content="Updated content"
        ... )
        >>> update_data.title
        'Updated Title'
    """
    pass


class Prompt(PromptBase):
    """Complete prompt model with timestamps and identifier.
    
    Represents a fully populated prompt record as stored in or returned
    from the database. Includes auto-generated ID and timestamps.
    
    Attributes:
        id: Unique identifier auto-generated using UUID4.
        created_at: Timestamp when the prompt was first created (UTC).
        updated_at: Timestamp when the prompt was last modified (UTC).
        title: The title of the prompt (1-200 characters).
        content: The prompt template content (minimum 1 character).
        description: Optional detailed description of the prompt.
        collection_id: Optional ID linking prompt to a collection.
        
    Example:
        >>> prompt = Prompt(
        ...     title="Example",
        ...     content="Content here"
        ... )
        >>> len(prompt.id) > 0
        True
        >>> isinstance(prompt.created_at, datetime)
        True
    """
    id: str = Field(default_factory=generate_id)
    created_at: datetime = Field(default_factory=get_current_time)
    updated_at: datetime = Field(default_factory=get_current_time)

    class Config:
        """Pydantic configuration for the Prompt model.
        
        Enables compatibility with SQLAlchemy ORM models through
        the from_attributes setting.
        """
        from_attributes = True


class CollectionBase(BaseModel):
    """Base model for collection data validation.
    
    Defines common fields and validation rules shared between
    collection creation and update operations.
    
    Attributes:
        name: The name of the collection (1-100 characters).
        description: Optional detailed description of the collection (max 500 characters).
        
    Example:
        >>> collection = CollectionBase(
        ...     name="My Prompts",
        ...     description="Collection of my favorite prompts"
        ... )
        >>> collection.name
        'My Prompts'
    """
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)


class CollectionCreate(CollectionBase):
    """Request model for creating a new collection.
    
    Inherits all validation rules from CollectionBase. Used to validate
    incoming POST requests for collection creation.
    
    This model ensures that required fields are provided and optional
    fields meet their constraints before database insertion.
    
    Example:
        >>> collection_data = CollectionCreate(
        ...     name="Programming Tips"
        ... )
        >>> collection_data.name
        'Programming Tips'
    """
    pass


class Collection(CollectionBase):
    """Complete collection model with timestamp and identifier.
    
    Represents a fully populated collection record as stored in or
    returned from the database. Includes auto-generated ID and timestamp.
    
    Attributes:
        id: Unique identifier auto-generated using UUID4.
        created_at: Timestamp when the collection was first created (UTC).
        name: The name of the collection (1-100 characters).
        description: Optional detailed description of the collection (max 500 characters).
        
    Example:
        >>> collection = Collection(
        ...     name="Example Collection"
        ... )
        >>> len(collection.id) > 0
        True
        >>> isinstance(collection.created_at, datetime)
        True
    """
    id: str = Field(default_factory=generate_id)
    created_at: datetime = Field(default_factory=get_current_time)

    class Config:
        """Pydantic configuration for the Collection model.
        
        Enables compatibility with SQLAlchemy ORM models through
        the from_attributes setting.
        """
        from_attributes = True


class PromptList(BaseModel):
    """Response model for listing prompts with pagination.
    
    Used when returning multiple prompts from the API with total count
    information for pagination support.
    
    Attributes:
        prompts: List of Prompt objects returned from the query.
        total: Total number of prompts available (for pagination).
        
    Example:
        >>> prompt_list = PromptList(
        ...     prompts=[Prompt(title="Example", content="Content")],
        ...     total=1
        ... )
        >>> len(prompt_list.prompts)
        1
        >>> prompt_list.total
        1
    """
    prompts: List[Prompt]
    total: int


class CollectionList(BaseModel):
    """Response model for listing collections with pagination.
    
    Used when returning multiple collections from the API with total
    count information for pagination support.
    
    Attributes:
        collections: List of Collection objects returned from the query.
        total: Total number of collections available (for pagination).
        
    Example:
        >>> collection_list = CollectionList(
        ...     collections=[Collection(name="Test")],
        ...     total=1
        ... )
        >>> len(collection_list.collections)
        1
        >>> collection_list.total
        1
    """
    collections: List[Collection]
    total: int


class HealthResponse(BaseModel):
    """Response model for health check endpoint.
    
    Used to indicate the API is running and healthy. Returned by
    the /health endpoint.
    
    Attributes:
        status: String indicator of API health (e.g., "healthy", "ok").
        version: Version string of the running application (e.g., "1.0.0").
        
    Example:
        >>> health = HealthResponse(
        ...     status="healthy",
        ...     version="1.0.0"
        ... )
        >>> health.status
        'healthy'
        >>> health.version
        '1.0.0'
    """
    status: str
    version: str