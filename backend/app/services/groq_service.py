"""
Groq AI Service untuk Career Recovery AI
Simplified version untuk integrasi mudah
"""
import os
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, Optional

# Coba import Groq, tapi jangan error jika belum diinstall
try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False
    print("⚠️ Groq package not installed. Run: pip install groq")

logger = logging.getLogger(__name__)

class GroqCareerCoach:
    def __init__(self):
        """Initialize Groq client dengan API key dari .env"""
        import os
        print(f"🔍 GroqCareerCoach init - Checking .env...")
        print(f"🔍 Current directory: {os.getcwd()}")
        print(f"🔍 .env exists: {os.path.exists('.env')}")
        
        # Cek semua env variables
        env_vars = {k: v for k, v in os.environ.items() if 'GROQ' in k or 'AI' in k}
        print(f"🔍 Environment vars: {env_vars}")
        
        api_key = os.getenv("GROQ_API_KEY")
        print(f"🔍 GROQ_API_KEY from os.getenv: {'SET' if api_key else 'NOT SET'}")
        if api_key:
            print(f"🔍 Key length: {len(api_key)}")
            print(f"🔍 Key starts with: {api_key[:10]}...")
        api_key = os.getenv("GROQ_API_KEY")
        
        if not api_key or api_key == "your-groq-key-here":
            logger.warning("⚠️ GROQ_API_KEY not configured. AI features will use fallback.")
            self.client = None
            self.model = "fallback"
            return
        
        if not GROQ_AVAILABLE:
            logger.warning("⚠️ Groq package not installed. Run: pip install groq")
            self.client = None
            self.model = "fallback"
            return
        
        try:
            self.client = Groq(api_key=api_key)
            self.model = os.getenv("GROQ_MODEL", "llama3-70b-8192")
            self.cache = {}
            self.cache_ttl = timedelta(seconds=int(os.getenv("CACHE_TTL", "3600")))
            logger.info(f"✅ Groq AI initialized with model: {self.model}")
        except Exception as e:
            logger.error(f"❌ Failed to initialize Groq: {e}")
            self.client = None
            self.model = "fallback"
    
    def enhance_analysis(self, analysis_data: Dict) -> Dict[str, Any]:
        """
        Tambahkan AI insights ke analisis data aplikasi
        
        Args:
            analysis_data: Dictionary dengan keys: summary, role_analysis, patterns
        
        Returns:
            Enhanced insights dengan AI analysis
        """
        # Jika client tidak ada, return fallback
        if not self.client:
            return self._get_fallback_insights(analysis_data)
        
        # Generate cache key
        cache_key = self._generate_cache_key(analysis_data)
        
        # Check cache dulu
        cached = self._check_cache(cache_key)
        if cached:
            logger.info("📦 Using cached AI response")
            return {**cached, "cached": True}
        
        try:
            # Build prompt
            prompt = self._build_career_prompt(analysis_data)
            
            logger.info(f"🤖 Calling Groq API: {self.model}")
            
            # API call ke Groq
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": """Anda adalah career coach khusus industri teknologi. 
                        Analisis data aplikasi kerja dan berikan insight spesifik, actionable, dan encouraging.
                        Gunakan data yang diberikan, jangan membuat asumsi."""
                    },
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ],
                temperature=float(os.getenv("AI_TEMPERATURE", "0.7")),
                max_tokens=int(os.getenv("AI_MAX_TOKENS", "600")),
                stream=False
            )
            
            # Parse response
            ai_text = response.choices[0].message.content
            insights = self._parse_ai_response(ai_text)
            
            # Add metadata
            insights["generated_at"] = datetime.now().isoformat()
            insights["model"] = self.model
            insights["cached"] = False
            
            # Save to cache
            self._save_to_cache(cache_key, insights)
            
            logger.info("✅ AI analysis completed")
            return insights
            
        except Exception as e:
            logger.error(f"❌ Groq API error: {e}")
            return self._get_fallback_insights(analysis_data)
    
    def _build_career_prompt(self, data: Dict) -> str:
        """Build prompt untuk job application analysis"""
        summary = data.get("summary", {})
        roles = data.get("role_analysis", [])
        patterns = data.get("patterns", [])
        days = data.get("time_period_days", 30)
        
        # Format role data
        role_text = ""
        if roles:
            for role in roles[:3]:  # Top 3 roles
                role_text += f"- {role.get('role', 'Unknown')}: {role.get('applications', 0)} apps, {role.get('interview_rate', 0)}% interview\n"
        else:
            role_text = "No role data\n"
        
        # Format patterns
        pattern_text = ""
        if patterns:
            for pattern in patterns[:3]:
                pattern_text += f"- {pattern.get('description', '')}\n"
        else:
            pattern_text = "No patterns detected\n"
        
        prompt = f"""ANALYZE this job search data and provide JSON response with these exact keys:

1. "executive_summary": "2-sentence summary in Indonesian/English"
2. "key_strengths": ["strength1", "strength2"] 
3. "critical_issues": ["issue1", "issue2"]
4. "actionable_recommendations": [
    {{"title": "Rec1", "action": "specific step", "priority": "high/medium/low"}},
    {{"title": "Rec2", "action": "specific step", "priority": "high/medium/low"}},
    {{"title": "Rec3", "action": "specific step", "priority": "high/medium/low"}}
]
5. "encouragement": "motivational message"
6. "next_week_focus": "specific task for next 7 days"

DATA:
- Period: Last {days} days
- Total Applications: {summary.get('total_applications', 0)}
- Response Rate: {summary.get('response_rate', 0)}%
- Interview Rate: {summary.get('interview_rate', 0)}%
- Rejection Rate: {summary.get('rejection_rate', 0)}%
- Ghost Rate: {summary.get('ghost_rate', 0)}%

ROLE PERFORMANCE:
{role_text}

DETECTED PATTERNS:
{pattern_text}

Be SPECIFIC. Example: Instead of "improve resume", say "Add 3 quantifiable achievements to your resume for {roles[0].get('role', 'target')} roles".
"""
        return prompt
    
    def _parse_ai_response(self, text: str) -> Dict:
        """Parse AI response, cari JSON di dalamnya"""
        try:
            # Cari JSON dalam response
            import re
            json_match = re.search(r'\{.*\}', text, re.DOTALL)
            
            if json_match:
                json_str = json_match.group()
                parsed = json.loads(json_str)
                
                # Validasi struktur minimum
                if "executive_summary" in parsed:
                    return parsed
        except Exception:
            logger.warning("Could not parse JSON from AI response")
        
        # Fallback jika parsing gagal
        return {
            "executive_summary": text[:200] + "..." if len(text) > 200 else text,
            "key_strengths": ["Analysis completed"],
            "critical_issues": ["Response format issue"],
            "actionable_recommendations": [
                {"title": "Check Response", "action": "Review AI output manually", "priority": "medium"}
            ],
            "encouragement": "Keep tracking your applications!",
            "next_week_focus": "Continue with your current strategy"
        }
    
    def _get_fallback_insights(self, analysis_data: Dict) -> Dict:
        """Fallback insights jika AI tidak tersedia"""
        summary = analysis_data.get("summary", {})
        
        return {
            "executive_summary": f"Based on {summary.get('total_applications', 0)} applications. AI service not configured.",
            "key_strengths": ["You are systematically tracking applications"],
            "critical_issues": ["Set GROQ_API_KEY in .env file for AI insights"],
            "actionable_recommendations": [
                {"title": "Configure AI", "action": "Add your Groq API key to .env", "priority": "high"}
            ],
            "encouragement": "Data tracking is the first step to improvement!",
            "next_week_focus": "Apply to 5 targeted positions",
            "fallback": True,
            "generated_at": datetime.now().isoformat()
        }
    
    def _generate_cache_key(self, data: Dict) -> str:
        """Generate cache key sederhana"""
        import hashlib
        data_str = f"{data.get('summary', {}).get('total_applications', 0)}-{data.get('summary', {}).get('response_rate', 0)}"
        return hashlib.md5(data_str.encode()).hexdigest()[:8]
    
    def _check_cache(self, key: str) -> Optional[Dict]:
        """Check cache"""
        if key in self.cache:
            cached = self.cache[key]
            if datetime.now() - cached["time"] < self.cache_ttl:
                return cached["data"]
        return None
    
    def _save_to_cache(self, key: str, data: Dict):
        """Save to cache"""
        self.cache[key] = {
            "data": data,
            "time": datetime.now()
        }


# Singleton instance untuk digunakan di seluruh app
groq_coach = None

def get_groq_coach() -> GroqCareerCoach:
    """Get or create GroqCareerCoach instance (singleton)"""
    global groq_coach
    if groq_coach is None:
        groq_coach = GroqCareerCoach()
    return groq_coach