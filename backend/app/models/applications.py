from sqlalchemy import Column, Integer, String, Date, Text
from sqlalchemy.orm import relationship
from app.database import Base  # PERBAIKAN: dari app.database

class JobApplication(Base):
    __tablename__ = "job_applications"
    
    id = Column(Integer, primary_key=True, index=True)
    job_title = Column(String(200), nullable=False)
    company = Column(String(200), nullable=False)
    role_category = Column(String(50), nullable=False)
    date_applied = Column(Date, nullable=False)
    status = Column(String(50), nullable=False, default="ghosted")
    notes = Column(Text, nullable=True)
    
    # Tambahkan relationship untuk strategies
    strategies = relationship("Strategy", back_populates="application", cascade="all, delete-orphan")