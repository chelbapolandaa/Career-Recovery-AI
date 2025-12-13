from pydantic import BaseModel, Field
from datetime import date
from typing import Optional
from enum import Enum

class RoleCategory(str, Enum):
    DEV = "dev"
    VA = "va"
    OPS = "ops"
    AI = "ai"
    IT = "it"
    OTHER = "other"

class ApplicationStatus(str, Enum):
    GHOSTED = "ghosted"
    REJECTED = "rejected"
    INTERVIEW = "interview"
    OFFER = "offer"

class ApplicationBase(BaseModel):
    job_title: str = Field(..., min_length=1, max_length=200)
    company: str = Field(..., min_length=1, max_length=200)
    role_category: RoleCategory
    date_applied: date
    status: ApplicationStatus = ApplicationStatus.GHOSTED
    notes: Optional[str] = None

class ApplicationCreate(ApplicationBase):
    pass

class ApplicationUpdate(BaseModel):
    status: Optional[ApplicationStatus] = None
    notes: Optional[str] = None

class ApplicationResponse(ApplicationBase):
    id: int
    
    class Config:
        from_attributes = True