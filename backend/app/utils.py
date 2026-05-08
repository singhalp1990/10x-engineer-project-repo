"""Utility functions for PromptLab.

This module provides helper functions for prompt manipulation, filtering,
searching, and validation.
"""

import re
from typing import List
from app.models import Prompt


# ============== Prompt Sorting ==============

def sort_prompts_by_date(prompts: List[Prompt], descending: bool = True) -> List[Prompt]:
    """Sort prompts by creation date.
    
    Args:
        prompts: List of prompts to sort.
        descending: If True, sort newest first; if False, oldest first.
    
    Returns:
        Sorted list of prompts.
    """
    return sorted(prompts, key=lambda p: p.created_at, reverse=descending)


# ============== Prompt Filtering ==============

def filter_prompts_by_collection(prompts: List[Prompt], collection_id: str) -> List[Prompt]:
    """Filter prompts by collection ID.
    
    Args:
        prompts: List of prompts to filter.
        collection_id: The collection ID to filter by.
    
    Returns:
        List of prompts matching the collection ID.
    """
    return [p for p in prompts if p.collection_id == collection_id]


# ============== Prompt Searching ==============

def search_prompts(prompts: List[Prompt], query: str) -> List[Prompt]:
    """Search prompts by title or description.
    
    Args:
        prompts: List of prompts to search.
        query: Search query string (case-insensitive).
    
    Returns:
        List of prompts matching the search query.
    """
    query_lower = query.lower()
    return [
        p for p in prompts
        if _matches_search_query(p, query_lower)
    ]


def _matches_search_query(prompt: Prompt, query_lower: str) -> bool:
    """Check if a prompt matches a search query.
    
    Args:
        prompt: The prompt to check.
        query_lower: The lowercase search query.
    
    Returns:
        True if the prompt matches the query.
    """
    title_match = query_lower in prompt.title.lower()
    desc_match = prompt.description and query_lower in prompt.description.lower()
    return title_match or desc_match


# ============== Prompt Validation ==============

MIN_CONTENT_LENGTH = 10


def validate_prompt_content(content: str) -> bool:
    """Validate prompt content.
    
    Args:
        content: The prompt content to validate.
    
    Returns:
        True if content is valid (at least 10 characters after stripping),
        False otherwise.
    """
    if content is None:
        return False
    
    stripped = content.strip()
    return len(stripped) >= MIN_CONTENT_LENGTH


# ============== Variable Extraction ==============

VARIABLE_PATTERN = r'\{\{(\w+)\}\}'


def extract_variables(content: str) -> List[str]:
    """Extract variables from prompt content.
    
    Variables are identified by {{variable_name}} pattern.
    
    Args:
        content: The prompt content to extract variables from.
    
    Returns:
        List of unique variable names in order of first appearance.
    """
    matches = re.findall(VARIABLE_PATTERN, content)
    return _deduplicate_preserving_order(matches)


def _deduplicate_preserving_order(items: List[str]) -> List[str]:
    """Remove duplicates from a list while preserving order.
    
    Args:
        items: The list to deduplicate.
    
    Returns:
        List with duplicates removed, maintaining original order.
    """
    seen: set = set()
    result: List[str] = []
    
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    
    return result

