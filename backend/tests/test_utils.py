"""Test suite for utility functions in app/utils.py"""

import pytest
from datetime import datetime, timedelta
from app.models import Prompt, get_current_time
from app.utils import (
    sort_prompts_by_date,
    filter_prompts_by_collection,
    search_prompts,
    validate_prompt_content,
    extract_variables
)


# ============== Fixtures ==============

@pytest.fixture
def sample_prompts():
    """Create sample prompts for testing."""
    base_time = datetime(2026, 1, 1)
    return [
        Prompt(
            id="1",
            title="Email Summarizer",
            content="Summarize the following email in 3 bullet points: {{email}}",
            description="Extracts key points from emails",
            collection_id="col_1",
            created_at=base_time
        ),
        Prompt(
            id="2",
            title="Code Reviewer",
            content="Review this code and suggest improvements: {{code}}",
            description="Provides code review feedback",
            collection_id="col_2",
            created_at=base_time + timedelta(days=1)
        ),
        Prompt(
            id="3",
            title="Email Generator",
            content="Write a professional email to {{recipient}} about {{topic}}",
            description=None,
            collection_id="col_1",
            created_at=base_time + timedelta(days=2)
        ),
        Prompt(
            id="4",
            title="Data Analyzer",
            content="Analyze the dataset and identify trends",
            description="",
            collection_id=None,
            created_at=base_time - timedelta(days=1)
        ),
    ]


# ============== Tests for sort_prompts_by_date ==============

class TestSortPromptsByDate:
    """Tests for sort_prompts_by_date function."""
    
    def test_sort_descending_default(self, sample_prompts):
        """Test sorting prompts in descending order (newest first)."""
        sorted_prompts = sort_prompts_by_date(sample_prompts)
        # Should be sorted newest first
        assert sorted_prompts[0].id == "3"
        assert sorted_prompts[-1].id == "4"
    
    def test_sort_ascending(self, sample_prompts):
        """Test sorting prompts in ascending order (oldest first)."""
        sorted_prompts = sort_prompts_by_date(sample_prompts, descending=False)
        # Should be sorted oldest first
        assert sorted_prompts[0].id == "4"
        assert sorted_prompts[-1].id == "3"
    
    def test_sort_empty_list(self):
        """Test sorting an empty list."""
        result = sort_prompts_by_date([])
        assert result == []
    
    def test_sort_single_prompt(self, sample_prompts):
        """Test sorting a list with a single prompt."""
        result = sort_prompts_by_date([sample_prompts[0]])
        assert len(result) == 1
        assert result[0].id == "1"
    
    def test_sort_preserves_prompt_data(self, sample_prompts):
        """Test that sorting doesn't modify prompt data."""
        original_title = sample_prompts[0].title
        sorted_prompts = sort_prompts_by_date(sample_prompts)
        assert sorted_prompts[0].title == original_title
    
    def test_sort_does_not_modify_original(self, sample_prompts):
        """Test that sorting doesn't modify the original list."""
        original_order = [p.id for p in sample_prompts]
        sort_prompts_by_date(sample_prompts)
        assert [p.id for p in sample_prompts] == original_order


# ============== Tests for filter_prompts_by_collection ==============

class TestFilterPromptsByCollection:
    """Tests for filter_prompts_by_collection function."""
    
    def test_filter_by_collection_col_1(self, sample_prompts):
        """Test filtering prompts by collection_id col_1."""
        filtered = filter_prompts_by_collection(sample_prompts, "col_1")
        assert len(filtered) == 2
        assert all(p.collection_id == "col_1" for p in filtered)
        assert filtered[0].id == "1"
        assert filtered[1].id == "3"
    
    def test_filter_by_collection_col_2(self, sample_prompts):
        """Test filtering prompts by collection_id col_2."""
        filtered = filter_prompts_by_collection(sample_prompts, "col_2")
        assert len(filtered) == 1
        assert filtered[0].id == "2"
    
    def test_filter_by_nonexistent_collection(self, sample_prompts):
        """Test filtering by a collection_id that doesn't exist."""
        filtered = filter_prompts_by_collection(sample_prompts, "col_99")
        assert len(filtered) == 0
    
    def test_filter_empty_list(self):
        """Test filtering an empty list."""
        result = filter_prompts_by_collection([], "col_1")
        assert result == []
    
    def test_filter_none_collection(self, sample_prompts):
        """Test that prompts with None collection_id are not included."""
        filtered = filter_prompts_by_collection(sample_prompts, None)
        assert len(filtered) == 1
        assert filtered[0].id == "4"


# ============== Tests for search_prompts ==============

class TestSearchPrompts:
    """Tests for search_prompts function."""
    
    def test_search_by_title_case_insensitive(self, sample_prompts):
        """Test searching by title (case-insensitive)."""
        results = search_prompts(sample_prompts, "email")
        assert len(results) == 2
        assert any(p.id == "1" for p in results)
        assert any(p.id == "3" for p in results)
    
    def test_search_by_title_exact_match(self, sample_prompts):
        """Test searching by exact title match."""
        results = search_prompts(sample_prompts, "Code Reviewer")
        assert len(results) == 1
        assert results[0].id == "2"
    
    def test_search_by_description(self, sample_prompts):
        """Test searching by description."""
        results = search_prompts(sample_prompts, "code")
        assert len(results) == 1
        assert results[0].id == "2"
    
    def test_search_no_matches(self, sample_prompts):
        """Test search with no matching results."""
        results = search_prompts(sample_prompts, "xyz")
        assert len(results) == 0
    
    def test_search_empty_list(self):
        """Test searching an empty list."""
        result = search_prompts([], "query")
        assert result == []
    
    def test_search_case_insensitive(self, sample_prompts):
        """Test that search is case-insensitive."""
        results1 = search_prompts(sample_prompts, "EMAIL")
        results2 = search_prompts(sample_prompts, "email")
        assert len(results1) == len(results2)
    
    def test_search_partial_match(self, sample_prompts):
        """Test that search matches partial strings."""
        results = search_prompts(sample_prompts, "review")
        assert len(results) == 1
        assert results[0].id == "2"


# ============== Tests for validate_prompt_content ==============

class TestValidatePromptContent:
    """Tests for validate_prompt_content function."""
    
    def test_valid_content(self):
        """Test with valid prompt content."""
        assert validate_prompt_content("This is a valid prompt content") is True
    
    def test_minimum_length_valid(self):
        """Test with exactly 10 characters (minimum valid)."""
        assert validate_prompt_content("1234567890") is True
    
    def test_below_minimum_length(self):
        """Test with content below 10 characters."""
        assert validate_prompt_content("short") is False
    
    def test_empty_string(self):
        """Test with empty string."""
        assert validate_prompt_content("") is False
    
    def test_whitespace_only(self):
        """Test with whitespace only."""
        assert validate_prompt_content("   ") is False
        assert validate_prompt_content("\t\n") is False
    
    def test_none_value(self):
        """Test with None value."""
        assert validate_prompt_content(None) is False
    
    def test_whitespace_padding(self):
        """Test that whitespace is stripped before length check."""
        # 10 chars + surrounding whitespace
        assert validate_prompt_content("   1234567890   ") is True
        # Less than 10 chars + surrounding whitespace
        assert validate_prompt_content("   short   ") is False
    
    def test_long_content(self):
        """Test with very long content."""
        long_content = "a" * 10000
        assert validate_prompt_content(long_content) is True


# ============== Tests for extract_variables ==============

class TestExtractVariables:
    """Tests for extract_variables function."""
    
    def test_extract_single_variable(self):
        """Test extracting a single variable."""
        result = extract_variables("Hello {{name}}")
        assert result == ["name"]
    
    def test_extract_multiple_variables(self):
        """Test extracting multiple variables."""
        result = extract_variables("Hello {{name}}, you are {{age}} years old")
        assert len(result) == 2
        assert "name" in result
        assert "age" in result
    
    def test_extract_no_variables(self):
        """Test content with no variables."""
        result = extract_variables("No variables here")
        assert result == []
    
    def test_extract_duplicate_variables(self):
        """Test that duplicate variables appear only once."""
        result = extract_variables("Say {{word}} and {{word}} again")
        assert result == ["word"]
    
    def test_extract_empty_string(self):
        """Test with empty string."""
        result = extract_variables("")
        assert result == []
    
    def test_extract_underscore_variables(self):
        """Test extracting variables with underscores."""
        result = extract_variables("Process {{user_email}} and {{user_id}}")
        assert len(result) == 2
        assert "user_email" in result
        assert "user_id" in result
    
    def test_extract_numeric_variables(self):
        """Test extracting variables with numbers."""
        result = extract_variables("Process {{var1}} and {{var2}}")
        assert len(result) == 2
        assert "var1" in result
        assert "var2" in result
    
    def test_extract_preserves_order(self):
        """Test that extraction preserves variable order."""
        result = extract_variables("{{first}} {{second}} {{third}} {{first}}")
        assert result == ["first", "second", "third"]
    
    def test_extract_ignores_malformed_braces(self):
        """Test that malformed braces are ignored."""
        result = extract_variables("Single { brace } and {{valid}}")
        assert result == ["valid"]
    
    def test_extract_special_cases(self):
        """Test with nested or unusual brace patterns."""
        result = extract_variables("{{var}} and {not_var} and {{another}}")
        assert len(result) == 2
        assert "var" in result
        assert "another" in result