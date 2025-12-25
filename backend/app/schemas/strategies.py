from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

class StrategyBase(BaseModel):
    application_id: int
    strategy_type: str
    category: str
    title: str
    description: str
    action_items: List[str]
    priority: int
    confidence_score: int
    estimated_completion_hours: int

class StrategyCreate(StrategyBase):
    status: str = "pending"

class StrategyUpdate(BaseModel):
    status: Optional[str] = None
    priority: Optional[int] = None

class StrategyResponse(StrategyBase):
    id: int
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class PivotSuggestionResponse(BaseModel):
    id: int
    current_role: str
    suggested_roles: List[Dict[str, Any]]
    transferable_skills: List[str]
    skill_gaps: List[str]
    market_demand_score: int
    salary_impact: str
    created_at: datetime
    
    class Config:
        from_attributes = True