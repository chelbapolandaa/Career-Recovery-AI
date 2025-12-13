"""
Module B: Rejection Pattern Analyzer API
FIXED VERSION - dengan paths yang benar
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from ..database import get_db
from ..models.applications import JobApplication

# Router TANPA prefix di sini
router = APIRouter()

# ENDPOINT PATHS HARUS DIMULAI DENGAN "/analysis/"
@router.get("/analysis/quick-insights")
def get_quick_insights(db: Session = Depends(get_db)):
    """Quick insights endpoint - 30 days"""
    return analyze_data(db, days=30, endpoint="quick-insights")

@router.get("/analysis/role-performance")
def analyze_role_performance(db: Session = Depends(get_db)):
    """Simple role analysis"""
    return analyze_role_data(db)

@router.get("/analysis/rejection-patterns")
def analyze_rejection_patterns(
    days: int = Query(90, ge=1, le=365),
    db: Session = Depends(get_db)
):
    """Main analysis endpoint"""
    return analyze_data(db, days, endpoint="full-analysis")

@router.get("/analysis/test")
def test_endpoint():
    """Test endpoint"""
    return {
        "message": "✅ Module B Analysis API is working!",
        "endpoints": [
            "/api/analysis/test",
            "/api/analysis/quick-insights", 
            "/api/analysis/role-performance",
            "/api/analysis/rejection-patterns"
        ],
        "note": "Access via /api/analysis/[endpoint]"
    }

# Helper functions
def analyze_data(db: Session, days: int, endpoint: str):
    """Generic analysis function"""
    try:
        from_date = datetime.now().date() - timedelta(days=days)
        applications = db.query(JobApplication).filter(
            JobApplication.date_applied >= from_date
        ).all()
        
        total = len(applications)
        
        if total == 0:
            return {
                "status": "no_data",
                "message": f"No applications found in last {days} days",
                "recommendation": "Start adding job applications to get insights"
            }
        
        # Count statuses
        counts = {"ghosted": 0, "rejected": 0, "interview": 0, "offer": 0}
        for app in applications:
            if app.status in counts:
                counts[app.status] += 1
        
        # Calculate rates
        response_rate = ((total - counts["ghosted"]) / total * 100) if total > 0 else 0
        interview_rate = (counts["interview"] / total * 100) if total > 0 else 0
        
        # Generate insights
        insights = []
        insights.append(f"📊 Analyzed {total} applications from last {days} days")
        insights.append(f"📈 Response rate: {round(response_rate, 1)}% ({total - counts['ghosted']}/{total} got response)")
        insights.append(f"🎯 Interview rate: {round(interview_rate, 1)}% ({counts['interview']}/{total} interviews)")
        
        # Recommendations
        recommendations = []
        if counts["ghosted"] / total > 0.7:
            recommendations.append("🚨 High ghost rate (>70%). Improve targeting or follow-up strategy")
        
        if counts["interview"] == 0 and total > 5:
            recommendations.append("⚠️ No interviews yet. Consider revising resume/portfolio")
        
        if interview_rate > 20:
            recommendations.append("✅ Good interview rate! Keep up the good work")
        
        return {
            "status": "success",
            "metadata": {
                "endpoint": endpoint,
                "analysis_date": datetime.now().isoformat(),
                "period_days": days,
                "applications_analyzed": total
            },
            "summary": {
                "total_applications": total,
                **counts,
                "response_rate": round(response_rate, 1),
                "interview_rate": round(interview_rate, 1)
            },
            "insights": insights,
            "recommendations": recommendations if recommendations else ["Continue current strategy"],
            "raw_data_sample": [
                {
                    "id": app.id,
                    "job_title": app.job_title[:30] + "..." if len(app.job_title) > 30 else app.job_title,
                    "company": app.company,
                    "role": app.role_category,
                    "status": app.status,
                    "date": app.date_applied.isoformat() if app.date_applied else None
                }
                for app in applications[:3]  # First 3 apps as sample
            ]
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Analysis failed: {str(e)}",
            "tip": "Check if database has applications table"
        }

def analyze_role_data(db: Session):
    """Analyze performance by role"""
    try:
        applications = db.query(JobApplication).all()
        total = len(applications)
        
        if total == 0:
            return {
                "status": "no_data",
                "message": "No applications in database",
                "tip": "Add applications via /api/applications endpoint"
            }
        
        # Group by role
        role_data = {}
        for app in applications:
            role = app.role_category
            if role not in role_data:
                role_data[role] = {"total": 0, "interview": 0, "rejected": 0, "ghosted": 0}
            
            role_data[role]["total"] += 1
            if app.status in role_data[role]:
                role_data[role][app.status] += 1
        
        # Convert to list with calculations
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
                    "success_score": stats["interview"] * 10 - stats["rejected"]  # Simple scoring
                })
        
        # Sort by success score
        performance.sort(key=lambda x: x["success_score"], reverse=True)
        
        # Generate recommendations
        if len(performance) > 1:
            best = performance[0]
            worst = performance[-1]
            
            if best["interview_rate"] > 0:
                recommendation = f"Focus on {best['role']} roles ({best['interview_rate']}% interview rate)"
            else:
                recommendation = "Try different roles or improve applications"
        else:
            recommendation = "Apply to more roles for better analysis"
        
        return {
            "status": "success",
            "total_applications": total,
            "unique_roles": len(performance),
            "role_performance": performance,
            "best_role": performance[0] if performance else None,
            "worst_role": performance[-1] if len(performance) > 1 else None,
            "recommendation": recommendation,
            "insight": f"Applied to {len(performance)} different role categories"
        }
        
    except Exception as e:
        return {"status": "error", "message": str(e)}