"""In-memory storage for prompts and collections."""

from typing import Dict, List, Optional
from app.models import Prompt, Collection


class Storage:
    """In-memory storage for prompts and collections.
    
    This class provides methods for creating, retrieving, updating,
    and deleting prompts and collections. It uses dictionaries to
    store prompts and collections by their unique identifiers.
    """
    
    def __init__(self) -> None:
        """Initialize Storage with empty prompts and collections."""
        self._prompts: Dict[str, Prompt] = {}
        self._collections: Dict[str, Collection] = {}
    
    # ============== Prompt Operations ==============
    
    def create_prompt(self, prompt: Prompt) -> Prompt:
        """Create a new prompt.
        
        Args:
            prompt: The Prompt instance to create.
        
        Returns:
            The created Prompt instance.
        """
        self._prompts[prompt.id] = prompt
        return prompt
    
    def get_prompt(self, prompt_id: str) -> Optional[Prompt]:
        """Retrieve a prompt by ID.
        
        Args:
            prompt_id: The prompt ID to retrieve.
        
        Returns:
            The Prompt instance if found, None otherwise.
        """
        return self._prompts.get(prompt_id)
    
    def get_all_prompts(self) -> List[Prompt]:
        """Retrieve all prompts.
        
        Returns:
            A list of all Prompt instances.
        """
        return list(self._prompts.values())
    
    def update_prompt(self, prompt_id: str, prompt: Prompt) -> Optional[Prompt]:
        """Update an existing prompt.
        
        Args:
            prompt_id: The prompt ID to update.
            prompt: The updated Prompt instance.
        
        Returns:
            The updated Prompt instance if found, None otherwise.
        """
        if prompt_id not in self._prompts:
            return None
        self._prompts[prompt_id] = prompt
        return prompt
    
    def delete_prompt(self, prompt_id: str) -> bool:
        """Delete a prompt by ID.
        
        Args:
            prompt_id: The prompt ID to delete.
        
        Returns:
            True if deleted, False if not found.
        """
        if prompt_id in self._prompts:
            del self._prompts[prompt_id]
            return True
        return False
    
    def get_prompts_by_collection(self, collection_id: str) -> List[Prompt]:
        """Retrieve all prompts in a collection.
        
        Args:
            collection_id: The collection ID to filter by.
        
        Returns:
            A list of Prompt instances in the collection.
        """
        return [p for p in self._prompts.values() if p.collection_id == collection_id]
    
    # ============== Collection Operations ==============
    
    def create_collection(self, collection: Collection) -> Collection:
        """Create a new collection.
        
        Args:
            collection: The Collection instance to create.
        
        Returns:
            The created Collection instance.
        """
        self._collections[collection.id] = collection
        return collection
    
    def get_collection(self, collection_id: str) -> Optional[Collection]:
        """Retrieve a collection by ID.
        
        Args:
            collection_id: The collection ID to retrieve.
        
        Returns:
            The Collection instance if found, None otherwise.
        """
        return self._collections.get(collection_id)
    
    def get_all_collections(self) -> List[Collection]:
        """Retrieve all collections.
        
        Returns:
            A list of all Collection instances.
        """
        return list(self._collections.values())
    
    def delete_collection(self, collection_id: str) -> bool:
        """Delete a collection by ID.
        
        Args:
            collection_id: The collection ID to delete.
        
        Returns:
            True if deleted, False if not found.
        """
        if collection_id in self._collections:
            del self._collections[collection_id]
            return True
        return False
    
    def clear(self) -> None:
        """Clear all prompts and collections."""
        self._prompts.clear()
        self._collections.clear()


# Singleton instance
storage = Storage()
