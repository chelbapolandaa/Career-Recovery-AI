from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Strategy(Base):
    __tablename__ = "strategies"
    __table_args__ = {'extend_existing': True}  # ← INI PENTING!
    
    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("job_applications.id", ondelete="CASCADE"))
    strategy_type = Column(String(50))
    category = Column(String(50))
    title = Column(String(200))
    description = Column(Text)
    action_items = Column(JSON)
    priority = Column(Integer)
    confidence_score = Column(Integer)
    status = Column(String(20), default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)
    estimated_completion_hours = Column(Integer)
    source = Column(String(50), default="ai_analysis")  # ← FIELD BARU
    
    application = relationship("JobApplication", back_populates="strategies")

class CareerPivotSuggestion(Base):
    __tablename__ = "career_pivot_suggestions"
    __table_args__ = {'extend_existing': True}  # ← INI JUGA!
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, default=1)
    current_role = Column(String(100))
    suggested_roles = Column(JSON)
    transferable_skills = Column(JSON)
    skill_gaps = Column(JSON)
    market_demand_score = Column(Integer)
    salary_impact = Column(String(20))
    created_at = Column(DateTime, default=datetime.utcnow)