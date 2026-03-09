backend/app/storage.py
class Storage:
    """In-memory storage for prompts and collections.
    
    This class provides methods for creating, retrieving, updating,
    and deleting prompts and collections. It uses dictionaries to
    store prompts and collections by their unique identifiers.
    """
    
    def __init__(self):
        """Initializes Storage with empty prompts and collections."""
        self._prompts: Dict[str, Prompt] = {}
        self._collections: Dict[str, Collection] = {}
    
    def create_prompt(self, prompt: Prompt) -> Prompt:
        """Creates a new prompt.
        
        Args:
            prompt (Prompt): The prompt to be added to storage.
        
        Returns:
            Prompt: The added prompt.
        """
        self._prompts[prompt.id] = prompt
        return prompt
    
    def get_prompt(self, prompt_id: str) -> Optional[Prompt]:
        """Retrieves a prompt by ID.
        
        Args:
            prompt_id (str): The unique identifier of the prompt.
        
        Returns:
            Optional[Prompt]: The prompt if found, otherwise None.
        """
        return self._prompts.get(prompt_id)
    
    def get_all_prompts(self) -> List[Prompt]:
        """Retrieves all prompts.
        
        Returns:
            List[Prompt]: A list of all stored prompts.
        """
        return list(self._prompts.values())
    
    def update_prompt(self, prompt_id: str, prompt: Prompt) -> Optional[Prompt]:
        """Updates an existing prompt.
        
        Args:
            prompt_id (str): The unique identifier of the prompt to be updated.
            prompt (Prompt): The updated prompt data.
        
        Returns:
            Optional[Prompt]: The updated prompt, or None if not found.
        """
        if prompt_id not in self._prompts:
            return None
        self._prompts[prompt_id] = prompt
        return prompt
    
    def delete_prompt(self, prompt_id: str) -> bool:
        """Deletes a prompt by ID.
        
        Args:
            prompt_id (str): The unique identifier of the prompt to be deleted.
        
        Returns:
            bool: True if the prompt was deleted, False if not found.
        """
        if prompt_id in self._prompts:
            del self._prompts[prompt_id]
            return True
        return False
    
    def create_collection(self, collection: Collection) -> Collection:
        """Creates a new collection.
        
        Args:
            collection (Collection): The collection to be added to storage.
        
        Returns:
            Collection: The added collection.
        """
        self._collections[collection.id] = collection
        return collection
    
    def get_collection(self, collection_id: str) -> Optional[Collection]:
        """Retrieves a collection by ID.
        
        Args:
            collection_id (str): The unique identifier of the collection.
        
        Returns:
            Optional[Collection]: The collection if found, otherwise None.
        """
        return self._collections.get(collection_id)
    
    def get_all_collections(self) -> List[Collection]:
        """Retrieves all collections.
        
        Returns:
            List[Collection]: A list of all stored collections.
        """
        return list(self._collections.values())
    
    def delete_collection(self, collection_id: str) -> bool:
        """Deletes a collection by ID.
        
        Args:
            collection_id (str): The unique identifier of the collection to be deleted.
        
        Returns:
            bool: True if the collection was deleted, False if not found.
        """
        if collection_id in self._collections:
            del self._collections[collection_id]
            return True
        return False
    
    def get_prompts_by_collection(self, collection_id: str) -> List[Prompt]:
        """Retrieves all prompts for a specific collection.
        
        Args:
            collection_id (str): The unique identifier of the collection.
        
        Returns:
            List[Prompt]: A list of prompts associated with the specified collection.
        """
        return [p for p in self._prompts.values() if p.collection_id == collection_id]
    
    def clear(self):
        """Clears all stored prompts and collections."""
        self._prompts.clear()
        self._collections.clear()
