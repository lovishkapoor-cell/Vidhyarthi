# Vidhyarthi - B.Tech Student Hub

A minimal, highly functional dashboard for engineering students to track upcoming exams, register for college events/hackathons, and maintain their mental well-being.

## Architecture

This prototype utilizes a decoupled monolithic structure for easy local deployment while maintaining clean architectural boundaries.

- **Backend:** FastAPI (Python), serving static frontend files.
- **Database:** SQLite (managed via SQLAlchemy ORM).
- **Frontend:** Vanilla HTML/CSS/JS (no framework, to keep the footprint lightweight).
- **Theme:** Cool & Minimal (Inter & JetBrains Mono, #F8FAFC & #0EA5E9).

## Project Structure

```
my_prototype_project/
├── backend/
│   ├── main.py              # FastAPI app and API routes
│   ├── database.py          # SQLite engine setup
│   ├── models.py            # SQLAlchemy schema
│   ├── schemas.py           # Pydantic validation & JSON schemas for AI
│   ├── ai_agent.py          # Mocked LLM tool-calling logic
│   ├── requirements.txt     # Python dependencies
│   └── prompts/
│       └── system_role.md   # HubBot System Prompt
├── frontend/
│   ├── index.html           # Structural HTML
│   ├── style.css            # Minimalist styling
│   └── app.js               # Vanilla JS logic (API calls, UI states)
├── docs/
│   └── debugging_template.md # Ready-to-use prompt for bug fixing
└── README.md
```

## Running the Project

1. Navigate to the project directory:
   ```bash
   cd my_prototype_project/backend
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the FastAPI server:
   ```bash
   uvicorn backend.main:app --reload
   ```
   *(Ensure you run this from the `my_prototype_project` root directory if your path setup requires it, e.g., `uvicorn backend.main:app --reload`)*

4. Open your browser and navigate to `http://localhost:8000`.
