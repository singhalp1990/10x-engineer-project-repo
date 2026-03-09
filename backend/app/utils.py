"""Utility functions for PromptLab.

This module provides helper functions for prompt manipulation, filtering,
searching, and validation. These utilities are used throughout the PromptLab
application to process and organize prompt data.
"""

from typing import List
import re
from app.models import Prompt


def sort_prompts_by_date(prompts: List[Prompt], descending: bool = True) -> List[Prompt]:
    """Sort prompts by their updated_at timestamp.
    
    Sorts a list of prompts in chronological order based on when they were
    last updated. By default, sorts in descending order (newest first).
    
    Args:
        prompts: List of Prompt objects to sort.
        descending: If True, sorts newest first (descending). If False,
                   sorts oldest first (ascending). Default is True.
    
    Returns:
        List[Prompt]: A new sorted list of prompts. The original list is
                     not modified.
    
    Raises:
        No exceptions raised. Returns empty list if input is empty.
    
    Example:
        >>> prompt1 = Prompt(id="1", title="Old", created_at=datetime(2026, 1, 1))
        >>> prompt2 = Prompt(id="2", title="New", created_at=datetime(2026, 3, 8))
        >>> sorted_desc = sort_prompts_by_date([prompt2, prompt1], descending=True)
        >>> sorted_desc[0].id
        "2"
    """
    return sorted(prompts, key=lambda p: p.updated_at, reverse=descending)


def filter_prompts_by_collection(prompts: List[Prompt], collection_id: str) -> List[Prompt]:
    """Filter prompts by their collection_id.
    
    Returns only the prompts that belong to the specified collection.
    If a collection_id is None, those prompts are excluded (not in any collection).
    
    Args:
        prompts: List of Prompt objects to filter.
        collection_id: The collection ID to filter by. Only prompts with
                      this collection_id will be returned.
    
    Returns:
        List[Prompt]: A new list containing only prompts that match the
                     specified collection_id. Returns empty list if no
                     prompts match.
    
    Raises:
        No exceptions raised. Returns empty list if no matches found.
    
   Example:
        >>> prompt1 = Prompt(id="1", collection_id="col_1")
        >>> prompt2 = Prompt(id="2", collection_id="col_2")
        >>> prompt3 = Prompt(id="3", collection_id="col_1")
        >>> filtered = filter_prompts_by_collection([prompt1, prompt2, prompt3], "col_1")
        >>> len(filtered)
        2
    """
    return [p for p in prompts if p.collection_id == collection_id]


def search_prompts(prompts: List[Prompt], query: str) -> List[Prompt]:
    """Search prompts by title and description.
    
    Searches for prompts matching the query string in the prompt title
    or description (if present). Search is case-insensitive.
    
    Args:
        prompts: List of Prompt objects to search.
        query: The search query string. Will match partial strings.
    
    Returns:
        List[Prompt]: A new list containing only prompts where the query
                     matches the title or description (case-insensitive).
                     Returns empty list if no prompts match.
    
    Raises:
        No exceptions raised. Returns empty list if no matches found.
    
   Example:
        >>> prompt1 = Prompt(id="1", title="Email Summarizer")
        >>> prompt2 = Prompt(id="2", title="Code Reviewer")
        >>> prompt3 = Prompt(id="3", title="Email Generator", description="")
        >>> results = search_prompts([prompt1, prompt2, prompt3], "email")
        >>> len(results)
        2
        
        >>> results = search_prompts([prompt1, prompt2, prompt3], "xyz")
        >>> len(results)
        0
    """
    query_lower = query.lower()
    return [
        p for p in prompts 
        if query_lower in p.title.lower() or 
           (p.description and query_lower in p.description.lower())
    ]


def validate_prompt_content(content: str) -> bool:
    """Validate if prompt content meets quality requirements.
    
    Checks that prompt content meets the following criteria:
    - Is not empty or None
    - Is not just whitespace
    - Contains at least 10 characters (after stripping whitespace)
    
    Args:
        content: The prompt content string to validate.
    
    Returns:
        bool: True if the content is valid, False otherwise.
    
    Raises:
        No exceptions raised.
    
    Example:
        >>> validate_prompt_content("Valid prompt content here")
        True
        
        >>> validate_prompt_content("short")
        False
        
        >>> validate_prompt_content("   ")
        False
        
        >>> validate_prompt_content("")
        False
        
        >>> validate_prompt_content(None)
        False
    """
    if not content or not content.strip():
        return False
    return len(content.strip()) >= 10


def extract_variables(content: str) -> List[str]:
    """Extract template variables from prompt content.
    
    Identifies all variables in the prompt content that are enclosed in
    double curly braces (e.g., {{variable_name}}). Returns a list of unique
    variable names found. Variables are identified using regex pattern matching.
    
    Args:
        content: The prompt template content string to parse.
    
    Returns:
        List[str]: A list of variable names found in the content (without
                  the curly braces). Returns empty list if no variables found.
                  Each variable appears only once even if used multiple times.
    
    Raises:
        No exceptions raised.
    
    Example:
        >>> extract_variables("Hello {{name}}, you are {{age}} years old")
        ["name", "age"]
        
        >>> extract_variables("Summarize: {{email}}")
        ["email"]
        
        >>> extract_variables("No variables here")
        []
        
        >>> extract_variables("Duplicate {{var}} and {{var}} again")
        ["var"]
    """
    pattern = r'\{\{(\w+)\}\}'
    matches = re.findall(pattern, content)
    # Return unique variables preserving order
    return list(dict.fromkeys(matches))
