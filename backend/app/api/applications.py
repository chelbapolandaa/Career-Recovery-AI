from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date, timedelta
import logging

from ..database import get_db
from ..models.applications import JobApplication
from ..schemas.applications import (
    ApplicationCreate, 
    ApplicationUpdate, 
    ApplicationResponse,
    RoleCategory,
    ApplicationStatus
)

router = APIRouter(tags=["applications"])
logger = logging.getLogger(__name__)

# CREATE - Tambah aplikasi baru
@router.post("/applications", response_model=ApplicationResponse)
def create_application(
    application: ApplicationCreate,
    db: Session = Depends(get_db)
):
    logger.info(f"Creating application: {application.job_title} at {application.company}")
    
    db_application = JobApplication(
        job_title=application.job_title,
        company=application.company,
        role_category=application.role_category.value,
        date_applied=application.date_applied,
        status=application.status.value,
        notes=application.notes
    )
    
    db.add(db_application)
    db.commit()
    db.refresh(db_application)
    
    return db_application

# READ - Get semua aplikasi
@router.get("/applications", response_model=List[ApplicationResponse])
def get_applications(
    skip: int = 0,
    limit: int = 100,
    role_category: Optional[RoleCategory] = None,
    status: Optional[ApplicationStatus] = None,
    db: Session = Depends(get_db)
):
    query = db.query(JobApplication)
    
    if role_category:
        query = query.filter(JobApplication.role_category == role_category.value)
    
    if status:
        query = query.filter(JobApplication.status == status.value)
    
    applications = query.order_by(JobApplication.date_applied.desc())\
                       .offset(skip).limit(limit).all()
    
    logger.info(f"Retrieved {len(applications)} applications")
    return applications

# READ - Get satu aplikasi
@router.get("/applications/{application_id}", response_model=ApplicationResponse)
def get_application(application_id: int, db: Session = Depends(get_db)):
    application = db.query(JobApplication).filter(JobApplication.id == application_id).first()
    
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    
    return application

# UPDATE - Update aplikasi
@router.put("/applications/{application_id}", response_model=ApplicationResponse)
def update_application(
    application_id: int,
    application_update: ApplicationUpdate,
    db: Session = Depends(get_db)
):
    db_application = db.query(JobApplication).filter(JobApplication.id == application_id).first()
    
    if not db_application:
        raise HTTPException(status_code=404, detail="Application not found")
    
    # Update fields jika diberikan
    if application_update.status:
        db_application.status = application_update.status.value
    
    if application_update.notes is not None:
        db_application.notes = application_update.notes
    
    db.commit()
    db.refresh(db_application)
    
    logger.info(f"Updated application {application_id}")
    return db_application

# DELETE - Hapus aplikasi
@router.delete("/applications/{application_id}")
def delete_application(application_id: int, db: Session = Depends(get_db)):
    application = db.query(JobApplication).filter(JobApplication.id == application_id).first()
    
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    
    db.delete(application)
    db.commit()
    
    logger.info(f"Deleted application {application_id}")
    return {"message": "Application deleted successfully"}

# STATS - Get statistik
@router.get("/applications/stats/summary")
def get_application_stats(
    days: int = Query(30, ge=1, le=365, description="Period in days"),
    db: Session = Depends(get_db)
):
    from_date = date.today() - timedelta(days=days)
    
    # Query data
    query = db.query(JobApplication).filter(JobApplication.date_applied >= from_date)
    total = query.count()
    
    # Count by status
    status_counts = {}
    for status in ApplicationStatus:
        count = query.filter(JobApplication.status == status.value).count()
        status_counts[status.value] = count
    
    # Response rate
    ghosted = status_counts.get("ghosted", 0)
    responded = total - ghosted
    response_rate = (responded / total * 100) if total > 0 else 0
    
    # Count by role
    role_counts = {}
    for role in RoleCategory:
        count = query.filter(JobApplication.role_category == role.value).count()
        role_counts[role.value] = count
    
    return {
        "period": {
            "days": days,
            "from": from_date.isoformat(),
            "to": date.today().isoformat()
        },
        "total_applications": total,
        "status_breakdown": status_counts,
        "role_breakdown": role_counts,
        "response_rate": round(response_rate, 2),
        "metrics": {
            "applications_per_day": round(total / days, 2) if days > 0 else 0,
            "ghost_rate": round((ghosted / total * 100), 2) if total > 0 else 0,
            "interview_rate": round((status_counts.get("interview", 0) / total * 100), 2) if total > 0 else 0
        }
    }