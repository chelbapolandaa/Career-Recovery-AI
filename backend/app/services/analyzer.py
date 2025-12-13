"""
Module B: Rejection Pattern Analyzer
AI system untuk menganalisis pola penolakan job applications
"""
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import json
import logging

logger = logging.getLogger(__name__)

class RejectionAnalyzer:
    def __init__(self, applications_data: List[Dict]):
        """
        Initialize analyzer dengan data applications
        
        Args:
            applications_data: List of application dictionaries dari database
        """
        self.data = pd.DataFrame(applications_data)
        logger.info(f"Analyzer initialized with {len(self.data)} applications")
    
    def analyze_patterns(self) -> Dict[str, Any]:
        """
        Analisis utama: Identifikasi pola rejection
        """
        if self.data.empty:
            return {"error": "No data to analyze"}
        
        results = {
            "summary": self._get_summary_stats(),
            "role_analysis": self._analyze_by_role(),
            "time_analysis": self._analyze_time_patterns(),
            "problem_patterns": self._identify_problem_patterns(),
            "recommendations": self._generate_recommendations(),
            "ai_insights": self._generate_ai_insights()
        }
        
        return results
    
    def _get_summary_stats(self) -> Dict:
        """Statistik summary"""
        total = len(self.data)
        rejected = len(self.data[self.data['status'] == 'rejected'])
        ghosted = len(self.data[self.data['status'] == 'ghosted'])
        interview = len(self.data[self.data['status'] == 'interview'])
        
        return {
            "total_applications": total,
            "rejected_count": rejected,
            "ghosted_count": ghosted,
            "interview_count": interview,
            "rejection_rate": round((rejected / total * 100), 1) if total > 0 else 0,
            "response_rate": round(((total - ghosted) / total * 100), 1) if total > 0 else 0,
            "interview_rate": round((interview / total * 100), 1) if total > 0 else 0
        }
    
    def _analyze_by_role(self) -> List[Dict]:
        """Analisis berdasarkan role category"""
        if 'role_category' not in self.data.columns:
            return []
        
        role_analysis = []
        for role in self.data['role_category'].unique():
            role_data = self.data[self.data['role_category'] == role]
            total = len(role_data)
            rejected = len(role_data[role_data['status'] == 'rejected'])
            interview = len(role_data[role_data['status'] == 'interview'])
            
            role_analysis.append({
                "role": role,
                "total_applications": total,
                "rejected": rejected,
                "interview": interview,
                "rejection_rate": round((rejected / total * 100), 1) if total > 0 else 0,
                "interview_rate": round((interview / total * 100), 1) if total > 0 else 0,
                "success_score": round((interview / total * 100) if total > 0 else 0, 1)
            })
        
        # Sort by success score (highest first)
        role_analysis.sort(key=lambda x: x['success_score'], reverse=True)
        return role_analysis
    
    def _analyze_time_patterns(self) -> Dict:
        """Analisis pola waktu"""
        if 'date_applied' not in self.data.columns:
            return {}
        
        # Convert to datetime
        self.data['date_applied'] = pd.to_datetime(self.data['date_applied'])
        
        # Weekly patterns
        self.data['week'] = self.data['date_applied'].dt.isocalendar().week
        weekly_data = self.data.groupby('week').agg({
            'status': 'count',
            'id': lambda x: (x == 'interview').sum() if 'interview' in self.data['status'].values else 0
        }).rename(columns={'status': 'total', 'id': 'interviews'})
        
        return {
            "applications_per_week": weekly_data.to_dict('index'),
            "best_week": int(weekly_data['interviews'].idxmax()) if not weekly_data.empty else None,
            "worst_week": int(weekly_data['interviews'].idxmin()) if not weekly_data.empty else None,
        }
    
    def _identify_problem_patterns(self) -> List[Dict]:
        """Identifikasi pola masalah"""
        patterns = []
        
        # Pattern 1: Too many applications to one role type
        if 'role_category' in self.data.columns:
            role_counts = self.data['role_category'].value_counts()
            most_applied_role = role_counts.index[0] if not role_counts.empty else None
            most_applied_count = role_counts.iloc[0] if not role_counts.empty else 0
            
            if most_applied_count > len(self.data) * 0.6:  # >60% ke satu role
                patterns.append({
                    "type": "over_specialization",
                    "severity": "high",
                    "message": f"Over-specialization: {most_applied_count}/{len(self.data)} applications ({round(most_applied_count/len(self.data)*100)}%) are to {most_applied_role} roles",
                    "recommendation": "Consider diversifying to related roles"
                })
        
        # Pattern 2: High ghost rate
        ghost_rate = len(self.data[self.data['status'] == 'ghosted']) / len(self.data) if len(self.data) > 0 else 0
        if ghost_rate > 0.7:  # >70% ghosted
            patterns.append({
                "type": "high_ghost_rate",
                "severity": "high",
                "message": f"High ghost rate: {round(ghost_rate*100)}% of applications get no response",
                "recommendation": "Improve resume targeting or follow-up strategy"
            })
        
        # Pattern 3: No interviews
        interview_count = len(self.data[self.data['status'] == 'interview'])
        if interview_count == 0 and len(self.data) > 10:
            patterns.append({
                "type": "no_interviews",
                "severity": "critical",
                "message": "No interviews despite multiple applications",
                "recommendation": "Revise resume and application strategy immediately"
            })
        
        return patterns
    
    def _generate_recommendations(self) -> List[Dict]:
        """Generate rekomendasi berdasarkan analisis"""
        recommendations = []
        
        # Get role analysis
        role_analysis = self._analyze_by_role()
        
        if len(role_analysis) >= 2:
            # Recommend focusing on best performing role
            best_role = role_analysis[0]
            worst_role = role_analysis[-1]
            
            if best_role['success_score'] > worst_role['success_score'] * 2:  # 2x better
                recommendations.append({
                    "type": "focus_role",
                    "priority": "high",
                    "action": f"Focus on {best_role['role']} roles",
                    "reason": f"{best_role['role']} has {best_role['interview_rate']}% interview rate vs {worst_role['interview_rate']}% for {worst_role['role']}",
                    "timeline": "Next 2 weeks"
                })
            
            # Recommend pausing worst role
            if worst_role['rejection_rate'] > 80:
                recommendations.append({
                    "type": "pause_role",
                    "priority": "medium",
                    "action": f"Pause applying to {worst_role['role']} roles",
                    "reason": f"{worst_role['rejection_rate']}% rejection rate with 0 interviews",
                    "timeline": "30 days"
                })
        
        # Volume recommendation
        total_apps = len(self.data)
        if total_apps > 20:
            apps_per_week = total_apps / 4  # Assuming 4 weeks
            if apps_per_week > 10:
                recommendations.append({
                    "type": "reduce_volume",
                    "priority": "medium",
                    "action": "Reduce application volume",
                    "reason": f"Currently applying to {round(apps_per_week)} jobs/week. Focus on quality over quantity.",
                    "timeline": "Immediate"
                })
        
        return recommendations
    
    def _generate_ai_insights(self) -> str:
        """Generate AI insights summary (simple version)"""
        summary = self._get_summary_stats()
        patterns = self._identify_problem_patterns()
        recs = self._generate_recommendations()
        
        insights = [
            f"📊 Summary: {summary['total_applications']} applications, ",
            f"{summary['response_rate']}% response rate, ",
            f"{summary['interview_rate']}% interview rate.\n\n"
        ]
        
        if patterns:
            insights.append("⚠️ Issues detected:\n")
            for pattern in patterns[:3]:  # Top 3 issues
                insights.append(f"• {pattern['message']}\n")
        
        if recs:
            insights.append("\n🎯 Recommendations:\n")
            for rec in recs[:3]:  # Top 3 recommendations
                insights.append(f"• {rec['action']} - {rec['reason']}\n")
        
        return "".join(insights)


# Simple analyzer tanpa AI eksternal dulu
class SimpleAnalyzer(RejectionAnalyzer):
    """Simplified analyzer tanpa dependency eksternal"""
    
    def analyze(self) -> Dict:
        """Simple analysis untuk MVP"""
        return self.analyze_patterns()