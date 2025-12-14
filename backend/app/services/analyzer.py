import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import json
import logging
import os

logger = logging.getLogger(__name__)

class RejectionAnalyzer:
    def __init__(self, applications_data: List[Dict]):
        """
        Initialize analyzer dengan data applications
        
        Args:
            applications_data: List of application dictionaries dari database
        """
        self.data = pd.DataFrame(applications_data)
        logger.info(f"📊 Analyzer initialized with {len(self.data)} applications")
        
        # Check AI availability
        self.ai_enabled = os.getenv("AI_ENABLED", "false").lower() == "true"
        if self.ai_enabled:
            try:
                from .groq_service import get_groq_coach
                self.groq_coach = get_groq_coach()
                logger.info("🤖 AI integration: ENABLED")
            except ImportError:
                self.ai_enabled = False
                logger.warning("🤖 AI integration: DISABLED (groq_service not found)")
        else:
            self.ai_enabled = False
            logger.info("🤖 AI integration: DISABLED (AI_ENABLED=false)")
    
    def analyze_patterns(self, include_ai: bool = True) -> Dict[str, Any]:
        """
        Analisis utama: Identifikasi pola rejection dengan optional AI
        
        Args:
            include_ai: Boolean, apakah include AI insights
            
        Returns:
            Dictionary lengkap dengan analysis
        """
        if self.data.empty:
            return {"error": "No data to analyze", "ai_enabled": False}
        
        # Basic analysis
        summary = self._get_summary_stats()
        role_analysis = self._analyze_by_role()
        patterns = self._identify_problem_patterns(summary, role_analysis)
        recommendations = self._generate_recommendations(role_analysis, summary)
        
        # Build base result
        results = {
            "summary": summary,
            "role_analysis": role_analysis,
            "problem_patterns": patterns,
            "recommendations": recommendations,
            "metadata": {
                "total_applications": len(self.data),
                "analysis_date": datetime.now().isoformat(),
                "ai_enabled": self.ai_enabled and include_ai
            }
        }
        
        # Add AI insights jika diminta dan available
        if include_ai and self.ai_enabled and self.groq_coach:
            try:
                # Prepare data for AI
                ai_data = {
                    "summary": summary,
                    "role_analysis": role_analysis,
                    "patterns": patterns,
                    "time_period_days": 30  # Default, bisa diadjust
                }
                
                # Get AI insights
                ai_insights = self.groq_coach.enhance_analysis(ai_data)
                
                results["ai_insights"] = ai_insights
                results["metadata"]["ai_used"] = True
                results["metadata"]["ai_model"] = ai_insights.get("model", "unknown")
                results["metadata"]["ai_cached"] = ai_insights.get("cached", False)
                
            except Exception as e:
                logger.error(f"AI analysis failed: {e}")
                results["ai_insights"] = {"error": str(e), "fallback": True}
                results["metadata"]["ai_used"] = False
        else:
            # Add basic text insights jika AI tidak digunakan
            results["text_insights"] = self._generate_text_insights(summary, patterns, recommendations)
            results["metadata"]["ai_used"] = False
        
        return results
    
    def _get_summary_stats(self) -> Dict:
        """Statistik summary lengkap"""
        if self.data.empty:
            return {
                "total_applications": 0,
                "rejected_count": 0,
                "ghosted_count": 0,
                "interview_count": 0,
                "rejection_rate": 0,
                "response_rate": 0,
                "interview_rate": 0,
                "ghost_rate": 0
            }
        
        total = len(self.data)
        
        # Pastikan kolom 'status' ada
        if 'status' not in self.data.columns:
            return {
                "total_applications": total,
                "rejected_count": 0,
                "ghosted_count": 0,
                "interview_count": 0,
                "rejection_rate": 0,
                "response_rate": 0,
                "interview_rate": 0,
                "ghost_rate": 0
            }
        
        # Count berdasarkan status
        status_counts = self.data['status'].value_counts()
        
        rejected = status_counts.get('rejected', 0)
        ghosted = status_counts.get('ghosted', 0)
        interview = status_counts.get('interview', 0)
        offered = status_counts.get('offer', 0)
        
        # Calculate rates
        rejection_rate = round((rejected / total * 100), 1) if total > 0 else 0
        response_rate = round(((total - ghosted) / total * 100), 1) if total > 0 else 0
        interview_rate = round((interview / total * 100), 1) if total > 0 else 0
        ghost_rate = round((ghosted / total * 100), 1) if total > 0 else 0
        
        return {
            "total_applications": total,
            "rejected_count": int(rejected),
            "ghosted_count": int(ghosted),
            "interview_count": int(interview),
            "offer_count": int(offered),
            "rejection_rate": rejection_rate,
            "response_rate": response_rate,
            "interview_rate": interview_rate,
            "ghost_rate": ghost_rate
        }
    
    def _analyze_by_role(self) -> List[Dict]:
        """Analisis berdasarkan role category"""
        if self.data.empty or 'role_category' not in self.data.columns:
            return []
        
        role_analysis = []
        
        # Group by role
        for role in self.data['role_category'].unique():
            if pd.isna(role):
                continue
                
            role_data = self.data[self.data['role_category'] == role]
            total = len(role_data)
            
            # Count statuses untuk role ini
            status_counts = role_data['status'].value_counts()
            
            rejected = status_counts.get('rejected', 0)
            interview = status_counts.get('interview', 0)
            ghosted = status_counts.get('ghosted', 0)
            
            # Calculate rates
            rejection_rate = round((rejected / total * 100), 1) if total > 0 else 0
            interview_rate = round((interview / total * 100), 1) if total > 0 else 0
            ghost_rate = round((ghosted / total * 100), 1) if total > 0 else 0
            
            # Calculate success score (interview - rejection dengan weighting)
            success_score = (interview_rate * 2) - rejection_rate - ghost_rate
            
            role_analysis.append({
                "role": str(role),
                "total_applications": total,
                "rejected": int(rejected),
                "interview": int(interview),
                "ghosted": int(ghosted),
                "rejection_rate": rejection_rate,
                "interview_rate": interview_rate,
                "ghost_rate": ghost_rate,
                "success_score": round(success_score, 1)
            })
        
        # Sort by success score (highest first)
        role_analysis.sort(key=lambda x: x['success_score'], reverse=True)
        
        return role_analysis
    
    def _identify_problem_patterns(self, summary: Dict, roles: List[Dict]) -> List[Dict]:
        """Identifikasi pola masalah berdasarkan data"""
        patterns = []
        total = summary.get('total_applications', 0)
        
        if total == 0:
            return patterns
        
        # Pattern 1: High ghost rate
        ghost_rate = summary.get('ghost_rate', 0)
        if ghost_rate > 70:
            patterns.append({
                "type": "high_ghost_rate",
                "severity": "high",
                "description": f"High ghost rate: {ghost_rate}% of applications get no response",
                "suggestion": "Improve resume targeting or add follow-up strategy"
            })
        
        # Pattern 2: No interviews
        interview_count = summary.get('interview_count', 0)
        if interview_count == 0 and total >= 5:
            patterns.append({
                "type": "no_interviews",
                "severity": "critical",
                "description": "No interviews despite multiple applications",
                "suggestion": "Revise resume, portfolio, or application strategy"
            })
        
        # Pattern 3: Over-specialization
        if roles:
            top_role = roles[0]
            if top_role['total_applications'] > total * 0.6:  # >60% ke satu role
                patterns.append({
                    "type": "over_specialization",
                    "severity": "medium",
                    "description": f"Over-specialization: {top_role['total_applications']}/{total} apps to {top_role['role']}",
                    "suggestion": "Consider diversifying to related roles"
                })
        
        # Pattern 4: Low response rate
        response_rate = summary.get('response_rate', 0)
        if response_rate < 20 and total > 10:
            patterns.append({
                "type": "low_response_rate",
                "severity": "medium",
                "description": f"Low response rate: Only {response_rate}% of applications get responses",
                "suggestion": "Improve resume or target more relevant positions"
            })
        
        return patterns
    
    def _generate_recommendations(self, roles: List[Dict], summary: Dict) -> List[Dict]:
        """Generate rekomendasi berdasarkan analisis"""
        recommendations = []
        total = summary.get('total_applications', 0)
        
        if total == 0:
            return [{
                "type": "get_started",
                "priority": "high",
                "action": "Start adding job applications",
                "reason": "No data to analyze yet",
                "timeline": "Immediate"
            }]
        
        # Recommendation berdasarkan role performance
        if len(roles) >= 2:
            best_role = roles[0]
            worst_role = roles[-1]
            
            # Focus on best performing role
            if best_role['interview_rate'] > 0:
                recommendations.append({
                    "type": "focus_role",
                    "priority": "high",
                    "action": f"Focus on {best_role['role']} roles",
                    "reason": f"{best_role['role']} has {best_role['interview_rate']}% interview rate",
                    "timeline": "Next 2 weeks"
                })
            
            # Pause worst role jika sangat buruk
            if worst_role['rejection_rate'] > 80 and worst_role['interview_rate'] == 0:
                recommendations.append({
                    "type": "pause_role",
                    "priority": "medium",
                    "action": f"Pause applying to {worst_role['role']} roles",
                    "reason": f"{worst_role['rejection_rate']}% rejection rate with 0 interviews",
                    "timeline": "30 days"
                })
        
        # Volume recommendation
        if total > 20:
            apps_per_week = total / 4  # Assuming 4 weeks
            if apps_per_week > 10:
                recommendations.append({
                    "type": "reduce_volume",
                    "priority": "medium",
                    "action": "Reduce application volume",
                    "reason": f"Currently {round(apps_per_week)} apps/week. Focus on quality.",
                    "timeline": "Immediate"
                })
        
        # Response rate recommendation
        response_rate = summary.get('response_rate', 0)
        if response_rate < 30:
            recommendations.append({
                "type": "improve_response",
                "priority": "high",
                "action": "Improve resume and cover letters",
                "reason": f"Only {response_rate}% response rate",
                "timeline": "1 week"
            })
        
        # Default recommendation jika tidak ada
        if not recommendations:
            recommendations.append({
                "type": "continue",
                "priority": "low",
                "action": "Continue current strategy",
                "reason": "Data looks reasonable",
                "timeline": "Monitor weekly"
            })
        
        return recommendations
    
    def _generate_text_insights(self, summary: Dict, patterns: List, recs: List) -> str:
        """Generate basic text insights untuk non-AI mode"""
        insights = [
            f"📊 Summary: {summary['total_applications']} applications\n",
            f"📈 Response Rate: {summary['response_rate']}%\n",
            f"🎯 Interview Rate: {summary['interview_rate']}%\n",
            f"📉 Rejection Rate: {summary['rejection_rate']}%\n"
        ]
        
        if patterns:
            insights.append("\n⚠️ Issues Detected:\n")
            for pattern in patterns[:3]:
                insights.append(f"• {pattern['description']}\n")
        
        if recs:
            insights.append("\n🎯 Recommendations:\n")
            for rec in recs[:3]:
                insights.append(f"• {rec['action']} - {rec['reason']}\n")
        
        return "".join(insights)
    
    def quick_analysis(self) -> Dict:
        """Quick analysis tanpa detail lengkap"""
        summary = self._get_summary_stats()
        
        return {
            "total_applications": summary["total_applications"],
            "response_rate": summary["response_rate"],
            "interview_rate": summary["interview_rate"],
            "status": "good" if summary["interview_rate"] > 10 else "needs_improvement",
            "timestamp": datetime.now().isoformat()
        }


# Simple analyzer untuk backward compatibility
class SimpleAnalyzer(RejectionAnalyzer):
    """Simplified analyzer (compatible dengan kode lama)"""
    
    def analyze(self) -> Dict:
        """Simple analysis untuk MVP"""
        return self.analyze_patterns(include_ai=False)