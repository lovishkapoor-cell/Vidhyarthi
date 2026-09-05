from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import csv
import io
from datetime import datetime
from typing import List
import os

from . import models, schemas
from .database import engine, get_db
from .ai_agent import agent

# Create all tables in the SQLite database
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Vidhyarthi - B.Tech Student Hub")

# --- Users CRUD ---

@app.post("/api/users", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = models.User(**user.model_dump())
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email already registered")

@app.get("/api/users", response_model=List[schemas.UserResponse])
def get_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()

# --- Events CRUD & CSV Parsing ---

@app.post("/api/events", response_model=schemas.EventResponse)
def create_event(event: schemas.EventCreate, db: Session = Depends(get_db)):
    db_event = models.Event(**event.model_dump())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

@app.get("/api/events", response_model=List[schemas.EventResponse])
def get_events(db: Session = Depends(get_db)):
    return db.query(models.Event).all()

@app.post("/api/events/upload")
async def upload_events_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Parses a CSV file of upcoming events, sanitizes dates, handles missing values,
    and loads them into the database.
    Expected columns: title, type, date, tech_stack_tags, college_name, location, organizing_club
    """
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a CSV.")
    
    content = await file.read()
    decoded_content = content.decode('utf-8')
    csv_reader = csv.DictReader(io.StringIO(decoded_content))
    
    events_added = 0
    for row in csv_reader:
        # Sanitize and format date
        raw_date = row.get('date', '').strip()
        parsed_date = None
        
        # Try a few common formats, default to today if totally broken (or skip)
        try:
            if raw_date:
                # Attempt to parse DD/MM/YYYY or YYYY-MM-DD
                for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y"):
                    try:
                        parsed_date = datetime.strptime(raw_date, fmt).date()
                        break
                    except ValueError:
                        pass
        except Exception:
            pass

        if not parsed_date:
            parsed_date = datetime.utcnow().date() # Fallback

        # Fill missing values with 'TBD'
        event_data = {
            "title": row.get('title') or "TBD",
            "type": row.get('type') or "TBD",
            "date": parsed_date,
            "tech_stack_tags": row.get('tech_stack_tags') or "",
            "college_name": row.get('college_name') or "TBD",
            "location": row.get('location') or "TBD",
            "organizing_club": row.get('organizing_club') or "TBD"
        }
        
        db_event = models.Event(**event_data)
        db.add(db_event)
        events_added += 1

    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error during CSV upload: {str(e)}")

    return {"message": f"Successfully uploaded and processed {events_added} events."}

# --- Registration Endpoint ---

@app.post("/api/register", response_model=schemas.RegistrationResponse)
def register_for_event(req: schemas.RegistrationRequest, db: Session = Depends(get_db)):
    """
    Robust POST endpoint where a student registers for an event.
    Validates input payload (email format handled by Pydantic schema).
    Ensures user and event exist.
    Returns clean JSON response.
    """
    # 1. Verify User exists
    user = db.query(models.User).filter(models.User.email == req.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User with this email not found.")

    # 2. Verify Event exists
    event = db.query(models.Event).filter(models.Event.id == req.event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found.")

    # 3. Check for existing registration
    existing_reg = db.query(models.Registration).filter(
        models.Registration.user_id == user.id,
        models.Registration.event_id == event.id
    ).first()
    
    if existing_reg:
        raise HTTPException(status_code=400, detail="User is already registered for this event.")

    # 4. Create Registration
    new_reg = models.Registration(user_id=user.id, event_id=event.id)
    try:
        db.add(new_reg)
        db.commit()
        db.refresh(new_reg)
        return new_reg
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="An internal error occurred during registration.")

# --- Zen Metrics CRUD ---
@app.post("/api/zen_metrics", response_model=schemas.ZenMetricResponse)
def create_zen_metric(metric: schemas.ZenMetricCreate, db: Session = Depends(get_db)):
    db_metric = models.ZenMetric(**metric.model_dump())
    db.add(db_metric)
    db.commit()
    db.refresh(db_metric)
    return db_metric

# --- AI Chatbot Endpoint ---
class ChatMessage(schemas.BaseModel):
    message: str

@app.post("/api/chat")
def chat_with_bot(chat: ChatMessage):
    """
    Endpoint for the floating chat widget to communicate with HubBot.
    """
    response = agent.process_message(chat.message)
    return response

# --- Serve Static Frontend ---
# Make sure this is at the bottom so it doesn't override API routes
frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")
