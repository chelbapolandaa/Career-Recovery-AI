from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from app.database import get_db  # PERBAIKAN: dari app.database, bukan app.db.database
from app.models.applications import JobApplication
from app.services.strategy_engine import StrategyEngine
from app.schemas.strategies import StrategyCreate, StrategyUpdate, StrategyResponse, PivotSuggestionResponse

# Import models strategies yang baru
from app.models.strategies import Strategy, CareerPivotSuggestion

router = APIRouter(prefix="/strategies", tags=["strategies"])

# Helper function untuk menghitung market score
def _calculate_market_score(pivot_data: Dict) -> int:
    """Calculate market demand score for pivot suggestions"""
    demand_map = {"high": 90, "medium": 65, "low": 40}
    return demand_map.get(pivot_data.get("market_demand", "medium"), 65)

@router.post("/generate/{application_id}", response_model=Dict[str, Any])
def generate_strategies(application_id: int, db: Session = Depends(get_db)):
    """Generate AI-powered recovery strategies"""
    
    # Get application
    application = db.query(JobApplication).filter(JobApplication.id == application_id).first()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    
    # Get all user applications untuk konteks
    all_applications = db.query(JobApplication).all()
    
    # Create AI-powered strategy engine
    engine = StrategyEngine()
    
    # Generate strategies DENGAN AI ANALYSIS
    strategies_data = engine.generate_strategies_based_on_analysis(
        application=application,
        all_applications=all_applications
    )
    
    # Save to database
    for strategy_data in strategies_data["strategies"]:
        strategy = Strategy(
            application_id=application_id,
            **strategy_data
        )
        db.add(strategy)
    
    # Save pivot suggestions
    if strategies_data["pivot_suggestions"]:
        pivot = CareerPivotSuggestion(
            user_id=1,  # Default user
            current_role=application.role_category or "Not specified",
            suggested_roles=strategies_data["pivot_suggestions"].get("suggested_roles", []),
            transferable_skills=strategies_data["pivot_suggestions"].get("transferable_skills", []),
            skill_gaps=strategies_data["pivot_suggestions"].get("skill_gaps", []),
            market_demand_score=_calculate_market_score(strategies_data["pivot_suggestions"]),
            salary_impact="increase"
        )
        db.add(pivot)
    
    db.commit()
    
    return {
        "message": "AI-powered strategies generated successfully",
        "strategies_count": len(strategies_data["strategies"]),
        "has_pivot_suggestions": bool(strategies_data["pivot_suggestions"]),
        "ai_analysis": True  # Flag bahwa ini hasil AI
    }

@router.get("/application/{application_id}", response_model=List[StrategyResponse])
def get_application_strategies(application_id: int, db: Session = Depends(get_db)):
    """Get all strategies for an application"""
    strategies = db.query(Strategy).filter(Strategy.application_id == application_id).all()
    return strategies

@router.get("/user/{user_id}/pivot-suggestions", response_model=List[PivotSuggestionResponse])
def get_pivot_suggestions(user_id: int, db: Session = Depends(get_db)):
    """Get career pivot suggestions for user"""
    suggestions = db.query(CareerPivotSuggestion).filter(CareerPivotSuggestion.user_id == user_id).all()
    return suggestions

@router.put("/strategy/{strategy_id}", response_model=StrategyResponse)
def update_strategy_status(strategy_id: int, update_data: StrategyUpdate, db: Session = Depends(get_db)):
    """Update strategy status (e.g., mark as completed)"""
    strategy = db.query(Strategy).filter(Strategy.id == strategy_id).first()
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    
    for key, value in update_data.dict(exclude_unset=True).items():
        setattr(strategy, key, value)
    
    db.commit()
    db.refresh(strategy)
    return strategy

@router.get("/dashboard/{user_id}", response_model=Dict[str, Any])
def get_strategy_dashboard(user_id: int, db: Session = Depends(get_db)):
    """Get strategy dashboard overview"""
    
    # Get all applications
    applications = db.query(JobApplication).all()
    
    # Collect strategies
    all_strategies = []
    for app in applications:
        strategies = db.query(Strategy).filter(Strategy.application_id == app.id).all()
        for strategy in strategies:
            strategy_dict = {
                "id": strategy.id,
                "title": strategy.title,
                "category": strategy.category,
                "priority": strategy.priority,
                "status": strategy.status,
                "confidence_score": strategy.confidence_score,
                "app_title": app.job_title
            }
            all_strategies.append(strategy_dict)
    
    # Categorize strategies
    by_category = {}
    by_priority = {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0}
    by_status = {"pending": 0, "in_progress": 0, "completed": 0}
    
    for strategy in all_strategies:
        # By category
        category = strategy["category"]
        by_category[category] = by_category.get(category, 0) + 1
        
        # By priority
        by_priority[str(strategy["priority"])] = by_priority.get(str(strategy["priority"]), 0) + 1
        
        # By status
        by_status[strategy["status"]] = by_status.get(strategy["status"], 0) + 1
    
    # Calculate completion rate
    total = len(all_strategies)
    completed = by_status.get("completed", 0)
    completion_rate = (completed / total * 100) if total > 0 else 0
    
    return {
        "total_strategies": total,
        "completion_rate": round(completion_rate, 1),
        "by_category": by_category,
        "by_priority": by_priority,
        "by_status": by_status,
        "top_priority_strategies": [s for s in all_strategies if s["priority"] == 1][:5]
    }