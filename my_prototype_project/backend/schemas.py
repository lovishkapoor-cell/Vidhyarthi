from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import date, datetime

# User Schemas
class UserBase(BaseModel):
    name: str
    email: EmailStr
    semester: int
    branch: str

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    id: str

    class Config:
        from_attributes = True

# Event Schemas
class EventBase(BaseModel):
    title: str
    type: str
    date: date
    tech_stack_tags: Optional[str] = None
    college_name: Optional[str] = "TBD"
    location: Optional[str] = "TBD"
    organizing_club: Optional[str] = "TBD"

class EventCreate(EventBase):
    pass

class EventResponse(EventBase):
    id: str

    class Config:
        from_attributes = True

# Registration Schema
class RegistrationRequest(BaseModel):
    email: EmailStr
    event_id: str

class RegistrationResponse(BaseModel):
    user_id: str
    event_id: str
    registered_at: datetime

    class Config:
        from_attributes = True

# Zen Metric Schemas
class ZenMetricCreate(BaseModel):
    user_id: str
    session_length_minutes: int
    stress_level: int = Field(..., ge=1, le=10)

class ZenMetricResponse(BaseModel):
    id: str
    user_id: str
    session_length_minutes: int
    stress_level: int
    created_at: datetime

    class Config:
        from_attributes = True

# AI Agent Function Schemas
class NavigateToPage(BaseModel):
    """To redirect the user's screen to the Dashboard, Zen Zone, or Registration portal."""
    page_name: str = Field(..., description="The name of the page to navigate to (Dashboard, Zen Zone, Registration)")

class FetchUpcomingDeadlines(BaseModel):
    """To retrieve calendar data."""
    student_id: str = Field(..., description="The ID of the student to fetch deadlines for")

class RegisterForEventTool(BaseModel):
    """To trigger a backend registration via chat."""
    event_id: str = Field(..., description="The ID of the event to register for")
