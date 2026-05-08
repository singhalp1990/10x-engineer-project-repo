"""API tests for PromptLab

These tests verify the API endpoints work correctly.
Students should expand these tests significantly in Week 3.
"""

import pytest
from fastapi.testclient import TestClient
import time


class TestHealth:
    """Tests for health endpoint."""
    
    def test_health_check(self, client: TestClient):
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data


class TestPrompts:
    """Tests for prompt endpoints."""
    
    def test_create_prompt(self, client: TestClient, sample_prompt_data):
        response = client.post("/prompts", json=sample_prompt_data)
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == sample_prompt_data["title"]
        assert data["content"] == sample_prompt_data["content"]
        assert "id" in data
        assert "created_at" in data
    
    def test_create_prompt_with_collection(self, client: TestClient, sample_collection_data, sample_prompt_data):
        """Test creating a prompt with a collection_id."""
        col_response = client.post("/collections", json=sample_collection_data)
        collection_id = col_response.json()["id"]
        
        prompt_data = {**sample_prompt_data, "collection_id": collection_id}
        response = client.post("/prompts", json=prompt_data)
        assert response.status_code == 201
        data = response.json()
        assert data["collection_id"] == collection_id
    
    def test_create_prompt_invalid_collection(self, client: TestClient, sample_prompt_data):
        """Test that creating a prompt with invalid collection_id fails."""
        prompt_data = {**sample_prompt_data, "collection_id": "invalid-id"}
        response = client.post("/prompts", json=prompt_data)
        assert response.status_code == 400
    
    def test_list_prompts_empty(self, client: TestClient):
        response = client.get("/prompts")
        assert response.status_code == 200
        data = response.json()
        assert data["prompts"] == []
        assert data["total"] == 0
    
    def test_list_prompts_with_data(self, client: TestClient, sample_prompt_data):
        client.post("/prompts", json=sample_prompt_data)
        
        response = client.get("/prompts")
        assert response.status_code == 200
        data = response.json()
        assert len(data["prompts"]) == 1
        assert data["total"] == 1
    
    def test_list_prompts_sorted_newest_first(self, client: TestClient):
        """Test that prompts are returned sorted newest first."""
        prompt1 = {"title": "First Prompt", "content": "First prompt content"}
        prompt2 = {"title": "Second Prompt", "content": "Second prompt content"}
        
        client.post("/prompts", json=prompt1)
        time.sleep(0.05)
        client.post("/prompts", json=prompt2)
        
        response = client.get("/prompts")
        prompts = response.json()["prompts"]
        
        assert prompts[0]["title"] == "Second Prompt"
        assert prompts[1]["title"] == "First Prompt"
    
    def test_list_prompts_filter_by_collection(self, client: TestClient, sample_collection_data, sample_prompt_data):
        """Test filtering prompts by collection_id."""
        col_response = client.post("/collections", json=sample_collection_data)
        collection_id = col_response.json()["id"]
        
        prompt_data = {**sample_prompt_data, "collection_id": collection_id}
        client.post("/prompts", json=prompt_data)
        client.post("/prompts", json=sample_prompt_data)  # No collection
        
        response = client.get(f"/prompts?collection_id={collection_id}")
        assert response.status_code == 200
        prompts = response.json()["prompts"]
        assert len(prompts) == 1
        assert prompts[0]["collection_id"] == collection_id
    
    def test_list_prompts_search_by_title(self, client: TestClient):
        """Test searching prompts by title."""
        client.post("/prompts", json={"title": "Python Guide", "content": "Learn Python"})
        client.post("/prompts", json={"title": "JavaScript Basics", "content": "Learn JS"})
        
        response = client.get("/prompts?search=python")
        prompts = response.json()["prompts"]
        assert len(prompts) == 1
        assert prompts[0]["title"] == "Python Guide"
    
    def test_list_prompts_search_by_content(self, client: TestClient):
        """Test searching prompts by content."""
        client.post("/prompts", json={"title": "Guide", "content": "Learn Python programming"})
        client.post("/prompts", json={"title": "Basics", "content": "Learn JavaScript"})
        
        response = client.get("/prompts?search=python")
        prompts = response.json()["prompts"]
        assert len(prompts) == 1
        assert "Python" in prompts[0]["content"]
    
    def test_get_prompt_success(self, client: TestClient, sample_prompt_data):
        create_response = client.post("/prompts", json=sample_prompt_data)
        prompt_id = create_response.json()["id"]
        
        response = client.get(f"/prompts/{prompt_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == prompt_id
    
    def test_get_prompt_not_found(self, client: TestClient):
        """Test that getting a non-existent prompt returns 404."""
        response = client.get("/prompts/nonexistent-id")
        assert response.status_code == 404
    
    def test_update_prompt_full(self, client: TestClient, sample_prompt_data):
        """Test full update of a prompt with PUT."""
        create_response = client.post("/prompts", json=sample_prompt_data)
        prompt_id = create_response.json()["id"]
        
        updated_data = {
            "title": "Updated Title",
            "content": "Updated content",
            "description": "Updated description"
        }
        
        response = client.put(f"/prompts/{prompt_id}", json=updated_data)
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Title"
        assert data["content"] == "Updated content"
        assert data["description"] == "Updated description"
    
    def test_update_prompt_partial(self, client: TestClient, sample_prompt_data):
        """Test partial update of a prompt with PATCH."""
        create_response = client.post("/prompts", json=sample_prompt_data)
        prompt_id = create_response.json()["id"]
        original_content = create_response.json()["content"]
        
        patch_data = {"title": "Only Title Updated"}
        
        response = client.patch(f"/prompts/{prompt_id}", json=patch_data)
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Only Title Updated"
        assert data["content"] == original_content
    
    def test_update_prompt_not_found(self, client: TestClient):
        """Test updating a non-existent prompt returns 404."""
        update_data = {"title": "New Title"}
        response = client.put("/prompts/nonexistent-id", json=update_data)
        assert response.status_code == 404
    
    def test_delete_prompt(self, client: TestClient, sample_prompt_data):
        create_response = client.post("/prompts", json=sample_prompt_data)
        prompt_id = create_response.json()["id"]
        
        response = client.delete(f"/prompts/{prompt_id}")
        assert response.status_code == 204
        
        get_response = client.get(f"/prompts/{prompt_id}")
        assert get_response.status_code == 404
    
    def test_delete_prompt_not_found(self, client: TestClient):
        """Test deleting a non-existent prompt returns 404."""
        response = client.delete("/prompts/nonexistent-id")
        assert response.status_code == 404


class TestCollections:
    """Tests for collection endpoints."""
    
    def test_create_collection(self, client: TestClient, sample_collection_data):
        response = client.post("/collections", json=sample_collection_data)
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == sample_collection_data["name"]
        assert "id" in data
        assert "created_at" in data
    
    def test_list_collections_empty(self, client: TestClient):
        response = client.get("/collections")
        assert response.status_code == 200
        data = response.json()
        assert data["collections"] == []
        assert data["total"] == 0
    
    def test_list_collections(self, client: TestClient, sample_collection_data):
        client.post("/collections", json=sample_collection_data)
        
        response = client.get("/collections")
        assert response.status_code == 200
        data = response.json()
        assert len(data["collections"]) == 1
        assert data["total"] == 1
    
    def test_list_collections_multiple(self, client: TestClient):
        """Test listing multiple collections."""
        col1 = {"name": "Collection 1", "description": "First collection"}
        col2 = {"name": "Collection 2", "description": "Second collection"}
        
        client.post("/collections", json=col1)
        client.post("/collections", json=col2)
        
        response = client.get("/collections")
        collections = response.json()["collections"]
        assert len(collections) == 2
        assert collections[0]["total"] == 2
    
    def test_get_collection_success(self, client: TestClient, sample_collection_data):
        """Test retrieving a specific collection."""
        create_response = client.post("/collections", json=sample_collection_data)
        collection_id = create_response.json()["id"]
        
        response = client.get(f"/collections/{collection_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == collection_id
        assert data["name"] == sample_collection_data["name"]
    
    def test_get_collection_not_found(self, client: TestClient):
        response = client.get("/collections/nonexistent-id")
        assert response.status_code == 404
    
    def test_delete_collection(self, client: TestClient, sample_collection_data):
        """Test deleting a collection."""
        create_response = client.post("/collections", json=sample_collection_data)
        collection_id = create_response.json()["id"]
        
        response = client.delete(f"/collections/{collection_id}")
        assert response.status_code == 204
        
        get_response = client.get(f"/collections/{collection_id}")
        assert get_response.status_code == 404
    
    def test_delete_collection_not_found(self, client: TestClient):
        """Test deleting a non-existent collection returns 404."""
        response = client.delete("/collections/nonexistent-id")
        assert response.status_code == 404
    
    def test_delete_collection_orphans_prompts(self, client: TestClient, sample_collection_data, sample_prompt_data):
        """Test that deleting a collection orphans its prompts (sets collection_id to None)."""
        col_response = client.post("/collections", json=sample_collection_data)
        collection_id = col_response.json()["id"]
        
        prompt_data = {**sample_prompt_data, "collection_id": collection_id}
        prompt_response = client.post("/prompts", json=prompt_data)
        prompt_id = prompt_response.json()["id"]
        
        # Delete collection
        response = client.delete(f"/collections/{collection_id}")
        assert response.status_code == 204
        
        # Verify prompt still exists but is orphaned
        prompt_response = client.get(f"/prompts/{prompt_id}")
        assert prompt_response.status_code == 200
        prompt = prompt_response.json()
        assert prompt["id"] == prompt_id
        assert prompt["collection_id"] is None
        assert prompt["title"] == sample_prompt_data["title"]


class TestErrorHandling:
    """Tests for error handling and edge cases."""
    
    def test_create_prompt_missing_required_field(self, client: TestClient):
        """Test that creating a prompt without required fields fails."""
        invalid_data = {"title": "No content field"}  # Missing 'content'
        response = client.post("/prompts", json=invalid_data)
        assert response.status_code == 422  # Validation error
    
    def test_create_collection_missing_name(self, client: TestClient):
        """Test that creating a collection without name fails."""
        invalid_data = {"description": "No name provided"}
        response = client.post("/collections", json=invalid_data)
        assert response.status_code == 422
    
    def test_create_prompt_empty_title(self, client: TestClient):
        """Test that empty title is rejected."""
        invalid_data = {"title": "", "content": "Some content"}
        response = client.post("/prompts", json=invalid_data)
        assert response.status_code == 422
    
    def test_create_prompt_title_too_long(self, client: TestClient):
        """Test that very long title is rejected."""
        invalid_data = {"title": "x" * 201, "content": "Content"}  # Max 200
        response = client.post("/prompts", json=invalid_data)
        assert response.status_code == 422
