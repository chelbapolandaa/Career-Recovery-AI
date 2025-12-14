"""
Module B: Rejection Pattern Analyzer API
Dengan Groq AI Integration - FIXED ABSOLUTE IMPORT
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import logging
import sys
import os

# ==================== FIX IMPORT PATH ====================
# Tambahkan project root ke Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.abspath(os.path.join(current_dir, '..', '..'))
sys.path.insert(0, backend_dir)

# Sekarang import dengan absolute path
try:
    from app.services.analyzer import RejectionAnalyzer
    from app.services.groq_service import get_groq_coach
    IMPORT_SUCCESS = True
except ImportError as e:
    IMPORT_SUCCESS = False
    print(f"⚠️ Import warning: {e}")
    print("⚠️ Some features may be disabled")

from ..database import get_db
from ..models.applications import JobApplication

# Setup logging
logger = logging.getLogger(__name__)

# Router TANPA prefix di sini
router = APIRouter()

# ==================== ENDPOINTS ====================

@router.get("/analysis/test")
def test_endpoint():
    """Test endpoint untuk cek API bekerja"""
    return {
        "status": "success",
        "message": "✅ Module B Analysis API is working!",
        "timestamp": datetime.now().isoformat(),
        "endpoints": [
            "/api/analysis/test",
            "/api/analysis/quick-insights", 
            "/api/analysis/role-performance",
            "/api/analysis/rejection-patterns",
            "/api/analysis/ai-test"
        ]
    }

@router.get("/analysis/quick-insights")
def get_quick_insights(
    days: int = Query(30, ge=1, le=365),
    db: Session = Depends(get_db)
):
    """Quick insights untuk dashboard"""
    try:
        from_date = datetime.now().date() - timedelta(days=days)
        applications = db.query(JobApplication).filter(
            JobApplication.date_applied >= from_date
        ).all()
        
        total = len(applications)
        
        if total == 0:
            return {
                "status": "no_data",
                "message": f"No applications in last {days} days",
                "recommendation": "Start adding applications"
            }
        
        # Hitung statistik
        counts = {"ghosted": 0, "rejected": 0, "interview": 0, "offer": 0}
        for app in applications:
            if app.status in counts:
                counts[app.status] += 1
        
        # Calculate rates
        response_rate = ((total - counts["ghosted"]) / total * 100) if total > 0 else 0
        interview_rate = (counts["interview"] / total * 100) if total > 0 else 0
        
        # Determine status
        if interview_rate > 15:
            status = "excellent"
        elif interview_rate > 5:
            status = "good"
        else:
            status = "needs_improvement"
        
        return {
            "status": "success",
            "period_days": days,
            "summary": {
                "total_applications": total,
                "response_rate": round(response_rate, 1),
                "interview_rate": round(interview_rate, 1),
                "ghosted": counts["ghosted"],
                "interviews": counts["interview"]
            },
            "performance_status": status,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Quick insights error: {e}")
        return {
            "status": "error",
            "message": str(e)
        }

@router.get("/analysis/role-performance")
def analyze_role_performance(
    days: int = Query(90, ge=1, le=365),
    db: Session = Depends(get_db)
):
    """Analisis performance berdasarkan role"""
    try:
        from_date = datetime.now().date() - timedelta(days=days)
        applications = db.query(JobApplication).filter(
            JobApplication.date_applied >= from_date
        ).all()
        
        if not applications:
            return {
                "status": "no_data",
                "message": "No applications to analyze"
            }
        
        # Group by role
        role_data = {}
        for app in applications:
            role = app.role_category or "Uncategorized"
            if role not in role_data:
                role_data[role] = {"total": 0, "interview": 0, "rejected": 0, "ghosted": 0}
            
            role_data[role]["total"] += 1
            if app.status in role_data[role]:
                role_data[role][app.status] += 1
        
        # Convert to list dengan calculations
        performance = []
        for role, stats in role_data.items():
            if stats["total"] > 0:
                interview_rate = (stats["interview"] / stats["total"] * 100) if stats["total"] > 0 else 0
                rejection_rate = (stats["rejected"] / stats["total"] * 100) if stats["total"] > 0 else 0
                
                performance.append({
                    "role": role,
                    "total_applications": stats["total"],
                    "interviews": stats["interview"],
                    "rejected": stats["rejected"],
                    "ghosted": stats["ghosted"],
                    "interview_rate": round(interview_rate, 1),
                    "rejection_rate": round(rejection_rate, 1),
                    "success_score": round(interview_rate - rejection_rate, 1)
                })
        
        # Sort by success score
        performance.sort(key=lambda x: x["success_score"], reverse=True)
        
        # Generate insight
        insight = ""
        if len(performance) > 0:
            best = performance[0]
            if best["interview_rate"] > 0:
                insight = f"Best role: {best['role']} ({best['interview_rate']}% interview rate)"
            else:
                insight = "No interviews yet. Keep applying!"
        
        return {
            "status": "success",
            "period_days": days,
            "total_applications": len(applications),
            "unique_roles": len(performance),
            "role_performance": performance,
            "best_role": performance[0] if performance else None,
            "worst_role": performance[-1] if len(performance) > 1 else None,
            "insight": insight,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Role analysis error: {e}")
        return {"status": "error", "message": str(e)}

@router.get("/analysis/rejection-patterns")
def analyze_rejection_patterns(
    days: int = Query(90, ge=1, le=365),
    use_ai: bool = Query(True, description="Enable AI insights"),
    db: Session = Depends(get_db)
):
    """
    MAIN ANALYSIS ENDPOINT dengan Groq AI integration
    
    Parameters:
    - days: Analysis period (default: 90)
    - use_ai: Enable/disable AI insights (default: true)
    """
    try:
        # Get applications dari database
        from_date = datetime.now().date() - timedelta(days=days)
        applications = db.query(JobApplication).filter(
            JobApplication.date_applied >= from_date
        ).all()
        
        if not applications:
            return {
                "status": "no_data",
                "message": f"No applications found in last {days} days",
                "recommendation": "Add applications via POST /api/applications",
                "ai_enabled": False
            }
        
        # Convert to format yang diharapkan analyzer
        # Convert to format yang diharapkan analyzer - FIXED VERSION
        apps_data = []
        for app in applications:
            # Build dictionary dengan safe attribute access
            app_dict = {
                "id": app.id,
                "role_category": app.role_category,
                "status": app.status,
                "date_applied": app.date_applied,
                "company": app.company,
                "job_title": app.job_title,
            }
            
            # HANYA tambahkan 'source' jika field tersebut ada di model
            if hasattr(app, 'source'):
                app_dict["source"] = app.source
            else:
                app_dict["source"] = "Unknown"  # Default value
            
            apps_data.append(app_dict)
        
        # Import analyzer - FIXED ABSOLUTE IMPORT
        if not IMPORT_SUCCESS:
            return {
                "status": "error",
                "message": "Analyzer module not found",
                "solution": "Check if app/services/analyzer.py exists",
                "ai_enabled": False
            }
        
        analyzer = RejectionAnalyzer(apps_data)
        
        # Run analysis
        analysis_result = analyzer.analyze_patterns(include_ai=use_ai)
        
        # Add metadata
        result = {
            "status": "success",
            "metadata": {
                "period_days": days,
                "applications_analyzed": len(applications),
                "analysis_date": datetime.now().isoformat(),
                "ai_requested": use_ai,
                "ai_used": analysis_result.get("metadata", {}).get("ai_used", False)
            },
            "summary": analysis_result.get("summary", {}),
            "role_analysis": analysis_result.get("role_analysis", []),
            "problem_patterns": analysis_result.get("problem_patterns", []),
            "recommendations": analysis_result.get("recommendations", [])
        }
        
        # Add AI insights jika ada
        if "ai_insights" in analysis_result:
            result["ai_insights"] = analysis_result["ai_insights"]
            result["metadata"]["ai_model"] = analysis_result["ai_insights"].get("model", "unknown")
            result["metadata"]["ai_cached"] = analysis_result["ai_insights"].get("cached", False)
        
        # Add basic insights jika tidak ada AI
        elif "text_insights" in analysis_result:
            result["text_insights"] = analysis_result["text_insights"]
        
        return result
        
    except Exception as e:
        logger.error(f"Rejection patterns analysis error: {e}")
        return {
            "status": "error",
            "message": f"Analysis failed: {str(e)}",
            "ai_enabled": False
        }

@router.get("/analysis/ai-test")
def test_ai_integration(
    db: Session = Depends(get_db)
):
    """Test endpoint untuk Groq AI integration"""
    if not IMPORT_SUCCESS:
        return {
            "status": "import_error",
            "message": "Required modules not found",
            "solution": "Check if groq_service.py exists in app/services/",
            "timestamp": datetime.now().isoformat()
        }
    
    try:
        coach = get_groq_coach()
        
        # Cek jika Groq available
        if not coach.client:
            return {
                "status": "ai_disabled",
                "message": "Groq AI is not configured",
                "solution": "1. Add GROQ_API_KEY to .env 2. Run 'pip install groq'",
                "timestamp": datetime.now().isoformat()
            }
        
        # Test dengan data sample
        test_data = {
            "summary": {
                "total_applications": 24,
                "response_rate": 45.0,
                "interview_rate": 12.0,
                "rejection_rate": 65.0,
                "ghost_rate": 55.0
            },
            "role_analysis": [
                {
                    "role": "Frontend Developer",
                    "applications": 12,
                    "interview_rate": 20.0,
                    "rejection_rate": 60.0
                },
                {
                    "role": "Full Stack Developer", 
                    "applications": 8,
                    "interview_rate": 5.0,
                    "rejection_rate": 85.0
                }
            ],
            "patterns": [
                {
                    "type": "high_ghost_rate",
                    "description": "55% of applications get no response"
                }
            ],
            "time_period_days": 30
        }
        
        # Test AI call
        logger.info("Testing Groq AI connection...")
        ai_result = coach.enhance_analysis(test_data)
        
        return {
            "status": "success",
            "ai_service": "Groq",
            "model": coach.model,
            "test_result": "AI connection successful",
            "sample_response": {
                "executive_summary": ai_result.get("executive_summary", "")[:100] + "...",
                "has_recommendations": "actionable_recommendations" in ai_result
            },
            "cache_info": {
                "cached": ai_result.get("cached", False),
                "model": ai_result.get("model", "unknown")
            },
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"AI test error: {e}")
        return {
            "status": "error",
            "message": str(e),
            "timestamp": datetime.now().isoformat()
        }

# ==================== HELPER FUNCTIONS ====================

def get_applications_by_period(db: Session, days: int):
    """Helper: Get applications within period"""
    from_date = datetime.now().date() - timedelta(days=days)
    return db.query(JobApplication).filter(
        JobApplication.date_applied >= from_date
    ).all()