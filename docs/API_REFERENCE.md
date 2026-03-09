# API Reference for PromptLab

This document provides details about the API endpoints available in the PromptLab application.

---

## Authentication

**Note**: Currently, there is no authentication required for any of the API endpoints. All endpoints are publicly accessible.

---

## Health Check

### `GET /health`

Check the health status of the API.

#### Response
- **200 OK**
  - Content-Type: `application/json`
  - Body:
    ```json
    {
      "status": "healthy",
      "version": "<version_number>"
    }
    ```

---

## Prompts Endpoints

### `GET /prompts`

List all prompts with optional filtering by collection and searching by title.

#### Optional Query Parameters
- `collection_id`: Filter prompts by a specific collection.
- `search`: Search prompts by title.

#### Response
- **200 OK**
  - Content-Type: `application/json`
  - Body:
    ```json
    {
      "prompts": [
        // List of prompt objects
      ],
      "total": <total_count>
    }
    ```

### `GET /prompts/{prompt_id}`

Retrieve a single prompt by its unique identifier.

#### Response
- **200 OK**
  - Content-Type: `application/json`
  - Body:
    ```json
    {
      "id": "<prompt_id>",
      "title": "<title>",
      "content": "<content>",
      ...
    }
    ```
- **404 Not Found**
  ```json
  {
    "detail": "Prompt not found"
  }
  ```

### `POST /prompts`

Create a new prompt with the provided data.

#### Request
- Content-Type: `application/json`
- Body:
  ```json
  {
    "title": "<title>",
    "content": "<content>",
    "collection_id": "<collection_id>", // Optional
    ...
  }
  ```

#### Responses
- **201 Created**
  ```json
  {
    "id": "<new_prompt_id>",
    ... // Other prompt details
  }
  ```
- **400 Bad Request** (if collection does not exist)
  ```json
  {
    "detail": "Collection not found"
  }
  ```

### `PUT /prompts/{prompt_id}`

Update an entire prompt (all fields required).

#### Request
- Content-Type: `application/json`
- Body:
  ```json
  {
    "title": "<new_title>",
    "content": "<new_content>",
    ...
  }
  ```

#### Responses
- **200 OK**
  ```json
  {
    "id": "<prompt_id>",
    ... // Updated prompt details
  }
  ```
- **404 Not Found**
  ```json
  {
    "detail": "Prompt not found"
  }
  ```

### `PATCH /prompts/{prompt_id}`

Partially update a prompt - only provided fields are changed.

#### Request
- Content-Type: `application/json`
- Body:
  ```json
  {
    "title": "<new_title>"
    // Other fields as needed
  }
  ```

#### Responses
- **200 OK**
  ```json
  {
    "id": "<prompt_id>",
    ... // Updated prompt details
  }
  ```
- **404 Not Found**
  ```json
  {
    "detail": "Prompt not found"
  }
  ```

### `DELETE /prompts/{prompt_id}`

Delete a prompt by its unique identifier.

#### Responses
- **204 No Content**
- **404 Not Found**
  ```json
  {
    "detail": "Prompt not found"
  }
  ```

---

## Collections Endpoints

### `GET /collections`

List all collections.

#### Response
- **200 OK**
  - Content-Type: `application/json`
  - Body:
    ```json
    {
      "collections": [
        // List of collection objects
      ],
      "total": <total_count>
    }
    ```

### `GET /collections/{collection_id}`

Retrieve a single collection by its unique identifier.

#### Response
- **200 OK**
  - Content-Type: `application/json`
  - Body:
    ```json
    {
      "id": "<collection_id>",
      "name": "<name>",
      ...
    }
    ```
- **404 Not Found**
  ```json
  {
    "detail": "Collection not found"
  }
  ```

### `POST /collections`

Create a new collection.

#### Request
- Content-Type: `application/json`
- Body:
  ```json
  {
    "name": "<name>",
    "description": "<description>", // Optional
    ...
  }
  ```

#### Responses
- **201 Created**
  ```json
  {
    "id": "<new_collection_id>",
    ... // Other collection details
  }
  ```

### `DELETE /collections/{collection_id}`

Delete a collection and orphan all associated prompts.

#### Responses
- **204 No Content**
- **404 Not Found**
  ```json
  {
    "detail": "Collection not found"
  }
  ```

---