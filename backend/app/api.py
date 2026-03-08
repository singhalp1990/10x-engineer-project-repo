"""FastAPI routes for PromptLab.

This module defines all API endpoints for the PromptLab application.
It includes endpoints for managing prompts and collections, with CORS
support and comprehensive error handling.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional

from app.models import (
    Prompt, PromptCreate, PromptUpdate,
    Collection, CollectionCreate,
    PromptList, CollectionList, HealthResponse,
    get_current_time
)
from app.storage import storage
from app.utils import sort_prompts_by_date, filter_prompts_by_collection, search_prompts
from app import __version__


app = FastAPI(
    title="PromptLab API",
    description="AI Prompt Engineering Platform",
    version=__version__
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============== Health Check ==============

@app.get("/health", response_model=HealthResponse)
def health_check():
    """Check the health status of the API.
    
    Returns a simple health status response to verify the API is running
    and operational. Useful for monitoring, load balancers, and health
    checks in containerized environments.
    
    Returns:
        HealthResponse: Object containing status and version information.
        
    Raises:
        No exceptions. Always returns a healthy status if endpoint is reached.
        
    Example:
        >>> response = client.get("/health")
        >>> response.status_code
        200
        >>> response.json()["status"]
        "healthy"
    """
    return HealthResponse(status="healthy", version=__version__)


# ============== Prompt Endpoints ==============

@app.get("/prompts", response_model=PromptList)
def list_prompts(
    collection_id: Optional[str] = None,
    search: Optional[str] = None
):
    """List all prompts with optional filtering and search.
    
    Retrieves all prompts from storage with support for filtering by
    collection and searching by title. Results are sorted by creation
    date with newest prompts first.
    
    Args:
        collection_id: Optional collection ID to filter prompts by a
                      specific collection.
        search: Optional search query string to find prompts by title.
        
    Returns:
        PromptList: Object containing list of prompts and total count.
        
    Raises:
        No exceptions. Returns empty list if no prompts match criteria.
        
    Example:
        >>> response = client.get("/prompts")
        >>> response.json()["total"]
        5
        
        >>> response = client.get("/prompts?collection_id=col_1")
        >>> len(response.json()["prompts"])
        2
        
        >>> response = client.get("/prompts?search=email")
        >>> response.json()["prompts"][0]["title"]
        "Email Summarizer"
    """
    prompts = storage.get_all_prompts()
    
    # Filter by collection if specified
    if collection_id:
        prompts = filter_prompts_by_collection(prompts, collection_id)
    
    # Search if query provided
    if search:
        prompts = search_prompts(prompts, search)
    
    # Sort by date (newest first)
    # Note: There might be an issue with the sorting...
    prompts = sort_prompts_by_date(prompts, descending=True)
    
    return PromptList(prompts=prompts, total=len(prompts))


@app.get("/prompts/{prompt_id}", response_model=Prompt)
def get_prompt(prompt_id: str):
    """Retrieve a single prompt by its unique identifier.
    
    Fetches a specific prompt from storage using the provided prompt ID.
    Returns the complete prompt object with all fields and timestamps.
    
    Args:
        prompt_id: The unique identifier of the prompt to retrieve.
        
    Returns:
        Prompt: The complete prompt object if found.
        
    Raises:
        HTTPException: 404 Not Found error if the prompt does not exist.
        
    Example:
        >>> response = client.get("/prompts/prompt_123")
        >>> response.status_code
        200
        >>> response.json()["title"]
        "Email Summarizer"
        
        >>> response = client.get("/prompts/nonexistent_id")
        >>> response.status_code
        404
        >>> response.json()["detail"]
        "Prompt not found"
    """
    prompt = storage.get_prompt(prompt_id)
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    return prompt


@app.post("/prompts", response_model=Prompt, status_code=201)
def create_prompt(prompt_data: PromptCreate):
    """Create a new prompt.
    
    Creates a new prompt with the provided data. If a collection_id is
    specified, validates that the collection exists. Automatically
    generates a unique ID and sets creation timestamp.
    
    Args:
        prompt_data: PromptCreate object containing title, content, and
                    optional description and collection_id.
        
    Returns:
        Prompt: The newly created prompt with auto-generated ID and
               timestamps.
        
    Raises:
        HTTPException: 400 Bad Request if the specified collection does
                      not exist.
        HTTPException: Validation error (422) if required fields are
                      missing or invalid.
        
    Example:
        >>> payload = {
        ...     "title": "Email Summarizer",
        ...     "content": "Summarize this email: {{email}}"
        ... }
        >>> response = client.post("/prompts", json=payload)
        >>> response.status_code
        201
        >>> response.json()["id"]
        "prompt_abc123..."
        
        >>> payload = {
        ...     "title": "Invalid",
        ...     "content": "Content",
        ...     "collection_id": "nonexistent"
        ... }
        >>> response = client.post("/prompts", json=payload)
        >>> response.status_code
        400
    """
    # Validate collection exists if provided
    if prompt_data.collection_id:
        collection = storage.get_collection(prompt_data.collection_id)
        if not collection:
            raise HTTPException(status_code=400, detail="Collection not found")
    
    prompt = Prompt(**prompt_data.model_dump())
    return storage.create_prompt(prompt)


@app.put("/prompts/{prompt_id}", response_model=Prompt)
def update_prompt(prompt_id: str, prompt_data: PromptUpdate):
    """Update an entire prompt (all fields required).
    
    Replaces all fields of an existing prompt with new values. Validates
    that the prompt exists and that any specified collection_id is valid.
    Automatically updates the updated_at timestamp to the current time.
    
    Args:
        prompt_id: The unique identifier of the prompt to update.
        prompt_data: PromptUpdate object containing new values for all
                    fields (title, content, description, collection_id).
        
    Returns:
        Prompt: The updated prompt object with new values and updated
               timestamp.
        
    Raises:
        HTTPException: 404 Not Found if the prompt does not exist.
        HTTPException: 400 Bad Request if the specified collection does
                      not exist.
        HTTPException: Validation error (422) if required fields are
                      missing or invalid.
        
    Example:
        >>> payload = {
        ...     "title": "Updated Title",
        ...     "content": "Updated content with {{new_var}}",
        ...     "description": "New description",
        ...     "collection_id": None
        ... }
        >>> response = client.put("/prompts/prompt_123", json=payload)
        >>> response.status_code
        200
        >>> response.json()["updated_at"]
        "2026-03-08T10:45:00Z"
    """
    existing = storage.get_prompt(prompt_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Prompt not found")
    
    # Validate collection if provided
    if prompt_data.collection_id:
        collection = storage.get_collection(prompt_data.collection_id)
        if not collection:
            raise HTTPException(status_code=400, detail="Collection not found")
    
    updated_prompt = Prompt(
        id=existing.id,
        title=prompt_data.title,
        content=prompt_data.content,
        description=prompt_data.description,
        collection_id=prompt_data.collection_id,
        created_at=existing.created_at,
        updated_at=get_current_time()
    )
    
    return storage.update_prompt(prompt_id, updated_prompt)


@app.patch("/prompts/{prompt_id}", response_model=Prompt)
def partial_update_prompt(prompt_id: str, prompt_data: PromptUpdate):
    """Partially update a prompt - only provided fields are changed.
    
    Updates only the fields that are provided in the request body, leaving
    all other fields unchanged. This is useful for updating a single field
    without having to send all fields like in PUT. Automatically updates
    the updated_at timestamp to the current time.
    
    Args:
        prompt_id: The unique identifier of the prompt to update.
        prompt_data: PromptUpdate object containing only the fields to
                    update. Unset fields will not be modified.
        
    Returns:
        Prompt: The updated prompt object with only the specified fields
               changed and updated timestamp.
        
    Raises:
        HTTPException: 404 Not Found if the prompt does not exist.
        HTTPException: 400 Bad Request if the specified collection does
                      not exist.
        
    Example:
        >>> payload = {"title": "New Title Only"}
        >>> response = client.patch("/prompts/prompt_123", json=payload)
        >>> response.status_code
        200
        >>> response.json()["title"]
        "New Title Only"
        
        >>> payload = {"collection_id": "col_456"}
        >>> response = client.patch("/prompts/prompt_123", json=payload)
        >>> response.status_code
        200
    """
    existing = storage.get_prompt(prompt_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Prompt not found")
    
    # Validate collection if provided
    if prompt_data.collection_id:
        collection = storage.get_collection(prompt_data.collection_id)
        if not collection:
            raise HTTPException(status_code=400, detail="Collection not found")
    
    # Only update fields that are provided (not None)
    update_data = prompt_data.model_dump(exclude_unset=True)
    
    updated_prompt = Prompt(
        id=existing.id,
        title=update_data.get("title", existing.title),
        content=update_data.get("content", existing.content),
        description=update_data.get("description", existing.description),
        collection_id=update_data.get("collection_id", existing.collection_id),
        created_at=existing.created_at,
        updated_at=get_current_time()
    )
    
    return storage.update_prompt(prompt_id, updated_prompt)


@app.delete("/prompts/{prompt_id}", status_code=204)
def delete_prompt(prompt_id: str):
    """Delete a prompt by its unique identifier.
    
    Permanently removes a prompt from storage. Returns 204 No Content
    on successful deletion. The operation cannot be undone.
    
    Args:
        prompt_id: The unique identifier of the prompt to delete.
        
    Returns:
        None: Returns empty response (204 No Content) on success.
        
    Raises:
        HTTPException: 404 Not Found if the prompt does not exist.
        
    Example:
        >>> response = client.delete("/prompts/prompt_123")
        >>> response.status_code
        204
        >>> response.content
        b''
        
        >>> response = client.delete("/prompts/nonexistent")
        >>> response.status_code
        404
    """
    if not storage.delete_prompt(prompt_id):
        raise HTTPException(status_code=404, detail="Prompt not found")
    return None


# ============== Collection Endpoints ==============

@app.get("/collections", response_model=CollectionList)
def list_collections():
    """List all collections.
    
    Retrieves all collections from storage. Each collection includes
    its metadata and associated prompts information.
    
    Returns:
        CollectionList: Object containing list of all collections and
                       total count.
        
    Raises:
        No exceptions. Returns empty list if no collections exist.
        
    Example:
        >>> response = client.get("/collections")
        >>> response.status_code
        200
        >>> response.json()["total"]
        3
        >>> len(response.json()["collections"])
        3
    """
    collections = storage.get_all_collections()
    return CollectionList(collections=collections, total=len(collections))


@app.get("/collections/{collection_id}", response_model=Collection)
def get_collection(collection_id: str):
    """Retrieve a single collection by its unique identifier.
    
    Fetches a specific collection from storage using the provided
    collection ID. Returns the complete collection object with all
    metadata.
    
    Args:
        collection_id: The unique identifier of the collection to retrieve.
        
    Returns:
        Collection: The complete collection object if found.
        
    Raises:
        HTTPException: 404 Not Found if the collection does not exist.
        
    Example:
        >>> response = client.get("/collections/col_123")
        >>> response.status_code
        200
        >>> response.json()["name"]
        "Customer Support"
        
        >>> response = client.get("/collections/nonexistent")
        >>> response.status_code
        404
    """
    collection = storage.get_collection(collection_id)
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    return collection


@app.post("/collections", response_model=Collection, status_code=201)
def create_collection(collection_data: CollectionCreate):
    """Create a new collection.
    
    Creates a new collection for organizing prompts. Automatically
    generates a unique ID and sets creation timestamp.
    
    Args:
        collection_data: CollectionCreate object containing name and
                        optional description.
        
    Returns:
        Collection: The newly created collection with auto-generated ID
                   and timestamps.
        
    Raises:
        HTTPException: Validation error (422) if required fields are
                      missing or invalid.
        
    Example:
        >>> payload = {
        ...     "name": "Customer Support",
        ...     "description": "Prompts for customer service automation"
        ... }
        >>> response = client.post("/collections", json=payload)
        >>> response.status_code
        201
        >>> response.json()["id"]
        "col_abc123..."
    """
    collection = Collection(**collection_data.model_dump())
    return storage.create_collection(collection)


@app.delete("/collections/{collection_id}", status_code=204)
def delete_collection(collection_id: str):
    """Delete a collection and set all associated prompts' collection_id to None.
    
    Permanently removes a collection from storage. All prompts that were
    assigned to this collection are orphaned by setting their
    collection_id to None. The prompts themselves are not deleted.
    Returns 204 No Content on success. The operation cannot be undone.
    
    Args:
        collection_id: The unique identifier of the collection to delete.
        
    Returns:
        None: Returns empty response (204 No Content) on success.
        
    Raises:
        HTTPException: 404 Not Found if the collection does not exist.
        
    Example:
        >>> response = client.delete("/collections/col_123")
        >>> response.status_code
        204
        >>> response.content
        b''
        
        >>> response = client.delete("/collections/nonexistent")
        >>> response.status_code
        404
    """
    if not storage.get_collection(collection_id):
        raise HTTPException(status_code=404, detail="Collection not found")
    
    # Get all prompts in this collection
    prompts = storage.get_all_prompts()
    for prompt in prompts:
        if prompt.collection_id == collection_id:
            # Remove collection reference and update timestamp
            orphaned_prompt = Prompt(
                id=prompt.id,
                title=prompt.title,
                content=prompt.content,
                description=prompt.description,
                collection_id=None,
                created_at=prompt.created_at,
                updated_at=get_current_time()
            )
            storage.update_prompt(prompt.id, orphaned_prompt)
    
    storage.delete_collection(collection_id)
    return None
