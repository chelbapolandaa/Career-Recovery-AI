# Di file models/applications.py
from ..database import Base  # Import Base dari database.py
from sqlalchemy import Column, Integer, String, Date, Text
import enum

# Hapus line: Base = declarative_base()
# Gunakan Base dari database.py

class JobApplication(Base):
    __tablename__ = "job_applications"
    
    id = Column(Integer, primary_key=True, index=True)
    job_title = Column(String(200), nullable=False)
    company = Column(String(200), nullable=False)
    role_category = Column(String(50), nullable=False)
    date_applied = Column(Date, nullable=False)
    status = Column(String(50), nullable=False, default="ghosted")
    notes = Column(Text, nullable=True)