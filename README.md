# README.md

iNITIAL README FILE
# 10x Engineer Project Repo

A sample service used during the **10x Engineer** training exercises.  
This repository contains the backend code for a simple RESTful API and any
supporting libraries/scripts. It is intended to demonstrate typical project
structure, build & run procedures, and how to document a service for other
developers.

---

## 📌 Project Overview

The service exposes a small set of HTTP endpoints for managing `widgets`
(you can substitute your own domain object).  It is written in Node.js with
Express (a Python variant is included for reference), and is packaged so that
it can be run locally or in a container.

Key features:

* CRUD operations on widgets
* JSON‑based request/response
* Lightweight, easy to extend

---

## 🛠️ Setup Instructions

1. **Clone the repository**

   ```bash
   git clone https://github.com/SarasAI-Institute/10x-engineer-project-repo.git
   cd 10x-engineer-project-repo
   git checkout week2            # or switch to the branch you need

2. Install dependencies
npm install          # installs packages listed in package.json
npm run lint         # run eslint if configured

3. Run the service
npm start            # starts the Node server on port 3000 by default
# or
python3 app.py       # starts the Python flask server

4. Configuration

Environment variables may be used to override defaults (PORT, DB_URI,
etc.). See config/default.json (or the code) for details.

API Endpoints
Method	Endpoint	Description	Request body
GET	/widgets	List all widgets	—
GET	/widgets/:id	Get a single widget by ID	—
POST	/widgets	Create a new widget	{ "name": "...", ... }
PUT	/widgets/:id	Update an existing widget	{ "name": "...", ... }
DELETE	/widgets/:id	Delete a widget	—
Replace widgets with your actual resource name if different.

Data Models
A simple JSON representation of a widget:


{
  "id": "string",
  "name": "string",
  "description": "string",
  "createdAt": "ISO‑8601 timestamp"
}

In a database schema (MongoDB/Mongoose or similar) the model might look like:
const WidgetSchema = new Schema({
  name: { type: String, required: true },
  description: String,
  createdAt: { type: Date, default: Date.now }
});

Usage Examples
Create a new widget:

curl -X POST http://localhost:3000/widgets \
  -H "Content-Type: application/json" \
  -d '{"name":"My Widget","description":"Test item"}'

Fetch all widgets:

curl http://localhost:3000/widgets

Update a widget:
curl -X PUT http://localhost:3000/widgets/123 \
  -H "Content-Type: application/json" \
  -d '{"name":"Updated name"}'

Delete a widget:
curl -X DELETE http://localhost:3000/widgets/123

References
Express documentation
Node.js
Flask documentation – if using the
Python variant
ESLint configuration for coding standards


API endpoint summary
Prompts
GET /prompts
List all prompts, newest first.
Query parameters:

search – substring filter on title.
sort – asc or desc (default desc).
collection_id – filter by collection.
curl 'http://localhost:8000/prompts?search=haiku&sort=asc'

POST /prompts
Create a prompt.
{
  "title": "My Prompt",
  "prompt": "Describe the lifecycle of a butterfly.",
  "description": "For a biology lesson.",
  "collection_id": "col-123"  // optional
}

GET /prompts/{id}
Retrieve a prompt.

PUT /prompts/{id}
Replace an existing prompt (all updatable fields).

DELETE /prompts/{id}
Remove a prompt (204 No Content or 404 Not Found).

PATCH /prompts/{id} – partial updates are planned for later
weeks.

Collections
GET /collections
List all collections.

POST /collections
Create a collection:
{ "name": "Short prompts" }

DELETE /collections/{id}
Remove a collection. Prompts that referenced it retain the
now‑invalid collection_id.

Error responses
{ "detail": "A descriptive error message" }


Development setup
Clone the repository and open in VS Code (preferably in the
dev container).
Create & activate a Python virtual environment.
Install dependencies with pip install -r requirements.txt.
Run the app with uvicorn app.main:app --reload.
Run tests from the project root with pytest (coverage with
--cov).
Lint/format using flake8/black (or npm run lint for JS).
The backend source lives under app/; routers, models and the storage
layer are easy to locate. Tests are in tests/. Refer to docs/ and
specs/ for documentation generated in week 2.

Contributing
Contributions are welcome! Follow these guidelines:

Fork the repository and branch from main.
Write focused commits with meaningful messages.
Add or update tests for any new functionality.
Run formatting and linting before committing.
Update documentation (README.md, docs/, specs/) as needed.
Ensure the dev container builds and the application starts.
Please see CONTRIBUTING.md for more details (create one if missing).

