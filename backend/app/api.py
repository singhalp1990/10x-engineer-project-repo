"""FastAPI routes for PromptLab.

This module defines all API endpoints for the PromptLab application.
It includes endpoints for managing prompts and collections, with CORS
support and comprehensive error handling.
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import uuid

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


# ============== Helper Functions ==============

def _create_prompt_from_data(prompt_data: PromptCreate) -> Prompt:
    """Create a Prompt instance from PromptCreate data.
    
    Args:
        prompt_data: The prompt creation data.
    
    Returns:
        A new Prompt instance with generated ID and timestamp.
    """
    return Prompt(
        id=str(uuid.uuid4()),
        title=prompt_data.title,
        content=prompt_data.content,
        description=prompt_data.description,
        collection_id=prompt_data.collection_id,
        created_at=get_current_time()
    )


def _validate_collection_exists(collection_id: Optional[str]) -> None:
    """Validate that a collection exists.
    
    Args:
        collection_id: The collection ID to validate.
    
    Raises:
        HTTPException: If collection_id is provided but doesn't exist.
    """
    if collection_id and storage.get_collection(collection_id) is None:
        raise HTTPException(status_code=400, detail="Collection does not exist")


def _get_prompt_or_404(prompt_id: str) -> Prompt:
    """Retrieve a prompt or raise 404 error.
    
    Args:
        prompt_id: The prompt ID to retrieve.
    
    Returns:
        The Prompt instance.
    
    Raises:
        HTTPException: If prompt not found.
    """
    prompt = storage.get_prompt(prompt_id)
    if prompt is None:
        raise HTTPException(status_code=404, detail="Prompt not found")
    return prompt


def _get_collection_or_404(collection_id: str) -> Collection:
    """Retrieve a collection or raise 404 error.
    
    Args:
        collection_id: The collection ID to retrieve.
    
    Returns:
        The Collection instance.
    
    Raises:
        HTTPException: If collection not found.
    """
    collection = storage.get_collection(collection_id)
    if collection is None:
        raise HTTPException(status_code=404, detail="Collection not found")
    return collection


def _orphan_collection_prompts(collection_id: str) -> None:
    """Remove all prompts from a collection by setting collection_id to None.
    
    Args:
        collection_id: The collection ID to orphan prompts from.
    """
    prompts = storage.get_prompts_by_collection(collection_id)
    for prompt in prompts:
        updated_prompt = Prompt(
            id=prompt.id,
            title=prompt.title,
            content=prompt.content,
            description=prompt.description,
            collection_id=None,
            created_at=prompt.created_at
        )
        storage.update_prompt(prompt.id, updated_prompt)


# ============== Health Check ==============

@app.get("/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    """Check API health status."""
    return HealthResponse(status="healthy", version=__version__)


# ============== Prompt Endpoints ==============

@app.get("/prompts", response_model=PromptList)
def list_prompts(
    collection_id: Optional[str] = None,
    search: Optional[str] = None
) -> PromptList:
    """List all prompts with optional filtering and searching.
    
    Args:
        collection_id: Optional collection ID to filter by.
        search: Optional search query for title/description.
    
    Returns:
        List of prompts matching the criteria.
    """
    prompts = storage.get_all_prompts()
    
    if collection_id:
        prompts = filter_prompts_by_collection(prompts, collection_id)
    
    if search:
        prompts = search_prompts(prompts, search)
    
    prompts = sort_prompts_by_date(prompts)
    return PromptList(prompts=prompts, total=len(prompts))


@app.get("/prompts/{prompt_id}", response_model=Prompt)
def get_prompt(prompt_id: str) -> Prompt:
    """Retrieve a specific prompt by ID.
    
    Args:
        prompt_id: The prompt ID to retrieve.
    
    Returns:
        The requested Prompt instance.
    """
    return _get_prompt_or_404(prompt_id)


@app.post("/prompts", response_model=Prompt, status_code=201)
def create_prompt(prompt_data: PromptCreate) -> Prompt:
    """Create a new prompt.
    
    Args:
        prompt_data: The prompt creation data.
    
    Returns:
        The created Prompt instance.
    """
    _validate_collection_exists(prompt_data.collection_id)
    prompt = _create_prompt_from_data(prompt_data)
    return storage.create_prompt(prompt)


@app.put("/prompts/{prompt_id}", response_model=Prompt)
def update_prompt(prompt_id: str, prompt_data: PromptUpdate) -> Prompt:
    """Fully update an existing prompt.
    
    Args:
        prompt_id: The prompt ID to update.
        prompt_data: The updated prompt data.
    
    Returns:
        The updated Prompt instance.
    """
    existing = _get_prompt_or_404(prompt_id)
    updated_data = existing.dict()
    updated_data.update(prompt_data.dict(exclude_unset=True))
    updated_prompt = Prompt(**updated_data)
    return storage.update_prompt(prompt_id, updated_prompt)


@app.patch("/prompts/{prompt_id}", response_model=Prompt)
def partial_update_prompt(prompt_id: str, prompt_data: PromptUpdate) -> Prompt:
    """Partially update an existing prompt.
    
    Args:
        prompt_id: The prompt ID to update.
        prompt_data: The partial prompt data to update.
    
    Returns:
        The updated Prompt instance.
    """
    existing = _get_prompt_or_404(prompt_id)
    updated_data = existing.dict()
    updated_data.update(prompt_data.dict(exclude_unset=True))
    updated_prompt = Prompt(**updated_data)
    return storage.update_prompt(prompt_id, updated_prompt)


@app.delete("/prompts/{prompt_id}", status_code=204)
def delete_prompt(prompt_id: str) -> None:
    """Delete a prompt by ID.
    
    Args:
        prompt_id: The prompt ID to delete.
    """
    if not storage.delete_prompt(prompt_id):
        raise HTTPException(status_code=404, detail="Prompt not found")


# ============== Collection Endpoints ==============

@app.get("/collections", response_model=CollectionList)
def list_collections() -> CollectionList:
    """List all collections.
    
    Returns:
        List of all Collection instances.
    """
    collections = storage.get_all_collections()
    return CollectionList(collections=collections, total=len(collections))


@app.get("/collections/{collection_id}", response_model=Collection)
def get_collection(collection_id: str) -> Collection:
    """Retrieve a specific collection by ID.
    
    Args:
        collection_id: The collection ID to retrieve.
    
    Returns:
        The requested Collection instance.
    """
    return _get_collection_or_404(collection_id)


@app.post("/collections", response_model=Collection, status_code=201)
def create_collection(collection_data: CollectionCreate) -> Collection:
    """Create a new collection.
    
    Args:
        collection_data: The collection creation data.
    
    Returns:
        The created Collection instance.
    """
    collection = Collection(
        id=str(uuid.uuid4()),
        name=collection_data.name,
        description=collection_data.description,
        created_at=get_current_time()
    )
    return storage.create_collection(collection)


@app.delete("/collections/{collection_id}", status_code=204)
def delete_collection(collection_id: str) -> None:
    """Delete a collection and orphan its prompts.
    
    Args:
        collection_id: The collection ID to delete.
    """
    _get_collection_or_404(collection_id)
    _orphan_collection_prompts(collection_id)
    
    if not storage.delete_collection(collection_id):
        raise HTTPException(status_code=404, detail="Collection not found")
