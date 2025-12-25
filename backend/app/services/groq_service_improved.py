"""
Groq AI Service untuk Career Recovery AI - IMPROVED VERSION
Dengan pattern-specific analysis dan differentiated recommendations
"""
import os
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
import re

# Coba import Groq
try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False

logger = logging.getLogger(__name__)

class GroqCareerCoach:
    def __init__(self):
        """Initialize Groq client dengan enhanced configuration"""
        self.api_key = os.getenv("GROQ_API_KEY")
        self.model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
        self.client = None
        self.cache = {}
        self.cache_ttl = timedelta(seconds=int(os.getenv("CACHE_TTL", "1800")))  # 30 minutes
        
        if not self.api_key or self.api_key == "your-groq-key-here":
            logger.warning("GROQ_API_KEY not configured. Using fallback mode.")
            return
        
        if not GROQ_AVAILABLE:
            logger.warning("Groq package not installed. Using fallback mode.")
            return
        
        try:
            self.client = Groq(api_key=self.api_key)
            logger.info(f"✅ Groq AI initialized with model: {self.model}")
        except Exception as e:
            logger.error(f"Failed to initialize Groq: {e}")
    
    def analyze_career_patterns(self, analysis_data: Dict) -> Dict[str, Any]:
        """
        Enhanced career pattern analysis dengan differentiated recommendations
        
        Args:
            analysis_data: Dictionary dengan:
                - summary: application statistics
                - role_analysis: performance by role
                - patterns: detected patterns
                - current_application: details of current app
                - timing_analysis: application timing patterns
                - company_analysis: company targeting patterns
        
        Returns:
            Enhanced insights dengan pattern-specific recommendations
        """
        # Jika client tidak ada, return enhanced fallback
        if not self.client:
            return self._get_enhanced_fallback(analysis_data)
        
        # Generate cache key berdasarkan analysis data
        cache_key = self._generate_enhanced_cache_key(analysis_data)
        
        # Check cache
        cached = self._check_cache(cache_key)
        if cached:
            logger.info("Using cached AI response")
            return {**cached, "cached": True}
        
        try:
            # Build enhanced prompt
            prompt = self._build_enhanced_prompt(analysis_data)
            
            logger.info(f"Calling Groq API for pattern analysis: {self.model}")
            
            # API call dengan enhanced parameters
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": self._get_system_prompt(analysis_data)
                    },
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ],
                temperature=float(os.getenv("AI_TEMPERATURE", "0.8")),  # Higher temp for creativity
                max_tokens=int(os.getenv("AI_MAX_TOKENS", "1200")),  # More tokens for detailed analysis
                top_p=0.9,
                frequency_penalty=0.1,  # Reduce repetition
                stream=False
            )
            
            # Parse enhanced response
            ai_text = response.choices[0].message.content
            insights = self._parse_enhanced_response(ai_text, analysis_data)
            
            # Add metadata and enhance with pattern detection
            insights.update({
                "generated_at": datetime.now().isoformat(),
                "model": self.model,
                "cached": False,
                "pattern_based": True
            })
            
            # Save to cache
            self._save_to_cache(cache_key, insights)
            
            logger.info("Enhanced AI analysis completed")
            return insights
            
        except Exception as e:
            logger.error(f"Groq API error: {e}")
            return self._get_enhanced_fallback(analysis_data)
    
    def _get_system_prompt(self, analysis_data: Dict) -> str:
        """Get system prompt berdasarkan pattern yang terdeteksi"""
        
        patterns = analysis_data.get("patterns", [])
        current_app = analysis_data.get("current_application", {})
        status = current_app.get("status", "")
        
        base_prompt = """Anda adalah career coach AI khusus untuk software engineers dan tech professionals di Indonesia.
        Analisis data aplikasi kerja dan berikan:
        1. Insight yang SPECIFIC dan ACTIONABLE
        2. Rekomendasi yang DIFFERENTIATED berdasarkan pola unik
        3. Contoh KONKRET dan TERUKUR
        4. Bahasa Indonesia yang natural dengan istilah tech yang tepat
        
        Fokus pada SOLUSI NYATA, bukan saran generik."""
        
        # Add pattern-specific guidance
        if any("low_response" in str(p.get("type", "")) for p in patterns):
            base_prompt += "\n\nPERHATIAN: User memiliki response rate rendah. Fokus pada resume optimization dan application strategy."
        
        if any("high_ghosting" in str(p.get("type", "")) for p in patterns):
            base_prompt += "\n\nPERHATIAN: User sering di-ghost. Fokus pada follow-up strategy dan networking."
        
        if status == "rejected":
            base_prompt += f"\n\nAplikasi saat ini: DITOLAK sebagai {current_app.get('job_title', '')}. Analisis spesifik kenapa ditolak dan recovery strategy."
        elif status == "ghosted":
            base_prompt += "\n\nAplikasi saat ini: DI-GHOST. Fokus pada improvement application quality dan follow-up."
        
        return base_prompt
    
    def _build_enhanced_prompt(self, data: Dict) -> str:
        """Build enhanced prompt untuk differentiated analysis"""
        
        summary = data.get("summary", {})
        roles = data.get("role_analysis", [])
        patterns = data.get("patterns", [])
        current_app = data.get("current_application", {})
        timing = data.get("timing_analysis", {})
        companies = data.get("company_analysis", {}).get("top_companies", [])
        
        # Format role analysis dengan detail
        role_text = ""
        if roles:
            for role in roles[:5]:  # Top 5 roles
                role_text += (
                    f"- {role.get('role', 'Unknown')}: "
                    f"{role.get('applications', 0)} aplikasi, "
                    f"{role.get('rejection_rate', 0)}% ditolak, "
                    f"{role.get('interview_rate', 0)}% interview, "
                    f"Performance: {role.get('performance', 'unknown')}\n"
                )
        
        # Format patterns dengan severity
        pattern_text = ""
        if patterns:
            for pattern in patterns[:5]:
                pattern_text += (
                    f"- {pattern.get('type', 'unknown').upper()}: "
                    f"{pattern.get('description', '')} "
                    f"[Severity: {pattern.get('severity', 'medium')}]\n"
                )
        
        # Format timing analysis
        timing_text = ""
        if timing:
            timing_text = (
                f"Frekuensi aplikasi: {timing.get('applications_per_week', 0)}/minggu "
                f"({timing.get('application_frequency', 'low')})\n"
            )
        
        # Format company analysis
        company_text = ""
        if companies:
            company_text = "Perusahaan yang paling sering di-apply:\n"
            for company in companies[:3]:
                company_text += (
                    f"- {company.get('company', '')}: {company.get('applications', 0)}x apply, "
                    f"{company.get('response_rate', 0)}% response rate\n"
                )
        
        prompt = f"""ANALYZE this specific career situation and provide DIFFERENTIATED recommendations:

CURRENT APPLICATION:
- Posisi: {current_app.get('job_title', 'N/A')}
- Perusahaan: {current_app.get('company', 'N/A')}
- Status: {current_app.get('status', 'N/A')}
- Kategori: {current_app.get('role_category', 'N/A')}
- Catatan: {current_app.get('notes', 'Tidak ada catatan')}

CAREER STATISTICS:
- Total Aplikasi: {summary.get('total_applications', 0)}
- Response Rate: {summary.get('response_rate', 0)}% (target: >30%)
- Interview Rate: {summary.get('interview_rate', 0)}% (target: >20%)
- Rejection Rate: {summary.get('rejection_rate', 0)}% (target: <50%)
- Ghost Rate: {summary.get('ghost_rate', 0)}% (target: <40%)

{timing_text}
{company_text}

ROLE PERFORMANCE:
{role_text if role_text else "Tidak ada data role"}

DETECTED PATTERNS:
{pattern_text if pattern_text else "Tidak ada pattern yang terdeteksi"}

Berdasarkan data di atas, berikan JSON response dengan struktur TEPAT:

{{
  "executive_summary": "ringkasan 2 kalimat dalam Bahasa Indonesia",
  "pattern_diagnosis": "diagnosis spesifik pola karir user",
  "key_strengths": ["strength1", "strength2", "strength3"],
  "critical_issues": ["issue1_spesifik", "issue2_spesifik"],
  "immediate_actions": [
    {{
      "title": "judul aksi spesifik",
      "description": "deskripsi detail dengan contoh konkret",
      "action_items": ["item1_spesifik", "item2_spesifik", "item3_spesifik"],
      "priority": "high/medium/low",
      "estimated_hours": angka,
      "expected_impact": "impact yang diharapkan"
    }}
  ],
  "medium_term_strategies": [
    {{
      "title": "strategi 3-6 bulan",
      "focus_area": "area fokus",
      "key_activities": ["aktivitas1", "aktivitas2"],
      "success_metrics": ["metric1", "metric2"]
    }}
  ],
  "career_pivot_considerations": {{
    "needed": true/false,
    "reason": "alasan jika needed=true",
    "suggested_directions": ["direction1", "direction2"]
  }},
  "motivational_note": "catatan motivasi personal"
}}

CONTOH BAIK (untuk low response rate):
- "immediate_actions": [{{
  "title": "Resume ATS Optimization untuk Backend Roles",
  "description": "Resume Anda tidak lolos screening ATS. Optimasi dengan:",
  "action_items": [
    "Analisis 5 job description Backend Developer, ekstrak 15 keywords utama",
    "Tambahkan section 'Technical Skills' dengan keywords: Python, FastAPI, PostgreSQL, Docker, AWS",
    "Ubah 'developed features' menjadi 'Increased API response time by 40% using async Python'",
    "Gunakan template ATS-friendly dari resume.io"
  ],
  "priority": "high",
  "estimated_hours": 4,
  "expected_impact": "Meningkatkan response rate dari {summary.get('response_rate', 0)}% menjadi >30% dalam 30 hari"
}}]

JANGAN berikan saran generik seperti "perbaiki resume" atau "perbanyak networking".
"""
        return prompt
    
    def _parse_enhanced_response(self, text: str, analysis_data: Dict) -> Dict:
        """Parse enhanced AI response dengan better error handling"""
        
        # Clean text - hapus markdown, extra spaces
        cleaned_text = self._clean_ai_response(text)
        
        # Coba parse sebagai JSON
        try:
            parsed = json.loads(cleaned_text)
            if self._validate_ai_response(parsed):
                parsed["analysis_context"] = {
                    "total_applications": analysis_data.get("summary", {}).get("total_applications", 0),
                    "response_rate": analysis_data.get("summary", {}).get("response_rate", 0),
                    "primary_pattern": self._extract_primary_pattern(analysis_data.get("patterns", []))
                }
                return parsed
        except json.JSONDecodeError as e:
            logger.warning(f"JSON decode error: {e}")
            # Coba extract JSON dari text
            extracted = self._extract_json_from_text(cleaned_text)
            if extracted and self._validate_ai_response(extracted):
                return extracted
        
        # Jika semua gagal, gunakan pattern-based fallback
        logger.warning("Using pattern-based fallback due to JSON parsing issues")
        return self._generate_pattern_based_fallback(analysis_data)

    def _clean_ai_response(self, text: str) -> str:
        """Clean AI response untuk parsing yang lebih baik"""
        # Hapus markdown code blocks
        text = re.sub(r'```json\s*', '', text)
        text = re.sub(r'```\s*', '', text)
        
        # Hapur whitespace berlebihan
        text = re.sub(r'\n\s*\n', '\n', text)
        
        # Fix common JSON issues
        text = re.sub(r',\s*}', '}', text)  # Trailing commas
        text = re.sub(r',\s*]', ']', text)  # Trailing commas in arrays
        
        return text.strip()

    def _extract_json_from_text(self, text: str) -> Optional[Dict]:
        """Extract JSON dari text yang mungkin mengandung markdown"""
        try:
            # Cari object JSON
            pattern = r'\{[\s\S]*\}'
            matches = re.findall(pattern, text)
            
            for match in matches:
                try:
                    # Coba parse
                    parsed = json.loads(match)
                    if self._validate_ai_response(parsed):
                        return parsed
                except:
                    continue
            
            # Coba find array jika object tidak ditemukan
            pattern = r'\[[\s\S]*\]'
            matches = re.findall(pattern, text)
            
            for match in matches:
                try:
                    parsed = json.loads(match)
                    if isinstance(parsed, list) and len(parsed) > 0:
                        # Convert array ke expected format
                        return {
                            "executive_summary": f"Parsed {len(parsed)} recommendations",
                            "immediate_actions": parsed[:3] if isinstance(parsed[0], dict) else []
                        }
                except:
                    continue
                    
        except Exception as e:
            logger.warning(f"Failed to extract JSON: {e}")
        
        return None

    def _validate_ai_response(self, data: Dict) -> bool:
        """Validate minimal AI response structure"""
        required_keys = ["executive_summary", "immediate_actions"]
        return all(key in data for key in required_keys)
    
    def _extract_primary_pattern(self, patterns: List[Dict]) -> str:
        """Extract primary pattern untuk contextual recommendations"""
        if not patterns:
            return "no_pattern"
        
        # Prioritize by severity
        severity_order = {"high": 3, "medium": 2, "low": 1}
        
        sorted_patterns = sorted(
            patterns,
            key=lambda x: severity_order.get(x.get("severity", "low"), 1),
            reverse=True
        )
        
        primary = sorted_patterns[0].get("type", "unknown")
        
        # Map to actionable pattern types
        pattern_map = {
            "low_response": "resume_ats_issue",
            "high_ghosting": "application_quality_issue",
            "interview_failure": "interview_skills_gap",
            "role_specific_issue": "role_targeting_mismatch"
        }
        
        return pattern_map.get(primary, "general_improvement")
    
    def _generate_pattern_based_fallback(self, analysis_data: Dict) -> Dict:
        """Generate pattern-specific fallback recommendations"""
        
        patterns = analysis_data.get("patterns", [])
        summary = analysis_data.get("summary", {})
        current_app = analysis_data.get("current_application", {})
        
        # Determine primary issue
        primary_pattern = self._extract_primary_pattern(patterns)
        
        # Pattern-specific recommendations
        recommendations_map = {
            "resume_ats_issue": {
                "executive_summary": f"Response rate rendah ({summary.get('response_rate', 0)}%) menunjukkan resume tidak optimal untuk ATS",
                "immediate_actions": [{
                    "title": "ATS Resume Optimization Sprint",
                    "description": "Resume tidak lolos screening automated systems",
                    "action_items": [
                        "Download 3 job descriptions untuk role target",
                        "Extract 20 keywords utama",
                        "Rewrite 3 bullet points dengan metrics (e.g., 'Improved X by Y%')",
                        "Test resume di free ATS checker"
                    ],
                    "priority": "high",
                    "estimated_hours": 6,
                    "expected_impact": "+25% response rate dalam 2 minggu"
                }]
            },
            "application_quality_issue": {
                "executive_summary": f"Ghost rate tinggi ({summary.get('ghost_rate', 0)}%) - aplikasi tidak menarik perhatian recruiter",
                "immediate_actions": [{
                    "title": "Application Quality Improvement",
                    "description": "Tingkatkan kualitas aplikasi dengan personalisasi",
                    "action_items": [
                        "Research 1 company deeply sebelum apply",
                        "Customize cover letter dengan 3 poin spesifik",
                        "Follow up setelah 7 hari dengan value-add question",
                        "Apply hanya ke role yang 80% match dengan skills"
                    ],
                    "priority": "high",
                    "estimated_hours": 3,
                    "expected_impact": "Reduce ghost rate by 30%"
                }]
            },
            "interview_skills_gap": {
                "executive_summary": "Interview conversion rate rendah - perlu improvement interview skills",
                "immediate_actions": [{
                    "title": "Structured Interview Preparation",
                    "description": "Sistematic interview practice untuk technical dan behavioral",
                    "action_items": [
                        "Practice 5 technical questions daily (LeetCode Easy/Medium)",
                        "Prepare 8 STAR stories untuk common behavioral questions",
                        "Record 3 mock interviews dengan peers",
                        "Create interview cheat sheet dengan company research"
                    ],
                    "priority": "high",
                    "estimated_hours": 10,
                    "expected_impact": "+40% interview success rate"
                }]
            },
            "general_improvement": {
                "executive_summary": f"Karir tracking aktif dengan {summary.get('total_applications', 0)} aplikasi. Perlahan tapi pasti!",
                "immediate_actions": [{
                    "title": "Focused Skill Development",
                    "description": "Build in-demand skills berdasarkan market trends",
                    "action_items": [
                        "Identifikasi 2 skills paling dicari di job descriptions target",
                        "Selesaikan 1 online course/certification",
                        "Build 1 portfolio project menggunakan skills tersebut",
                        "Update resume dan LinkedIn dengan skill baru"
                    ],
                    "priority": "medium",
                    "estimated_hours": 15,
                    "expected_impact": "Increase job match score by 30%"
                }]
            }
        }
        
        # Get recommendations based on pattern
        recommendations = recommendations_map.get(
            primary_pattern, 
            recommendations_map["general_improvement"]
        )
        
        return {
            **recommendations,
            "key_strengths": ["Consistent application tracking", "Awareness of improvement areas"],
            "critical_issues": ["Using fallback analysis - AI service issue"],
            "career_pivot_considerations": {
                "needed": summary.get("rejection_rate", 0) > 70,
                "reason": "High rejection rate suggests possible role/skill mismatch" if summary.get("rejection_rate", 0) > 70 else "Current direction seems appropriate",
                "suggested_directions": ["Related tech roles", "Adjacent industries"]
            },
            "motivational_note": "Setiap aplikasi adalah learning opportunity. Data tracking Anda sudah lebih baik dari 90% job seekers!",
            "fallback_mode": True,
            "pattern_detected": primary_pattern
        }
    
    def _get_enhanced_fallback(self, analysis_data: Dict) -> Dict:
        """Enhanced fallback dengan lebih banyak insight"""
        return self._generate_pattern_based_fallback(analysis_data)
    
    def _generate_enhanced_cache_key(self, data: Dict) -> str:
        """Generate lebih specific cache key"""
        import hashlib
        
        # Include more data points for better cache differentiation
        key_data = {
            "total_apps": data.get("summary", {}).get("total_applications", 0),
            "response_rate": data.get("summary", {}).get("response_rate", 0),
            "status": data.get("current_application", {}).get("status", ""),
            "role": data.get("current_application", {}).get("role_category", ""),
            "patterns": str([p.get("type", "") for p in data.get("patterns", [])[:3]])
        }
        
        key_str = json.dumps(key_data, sort_keys=True)
        return hashlib.md5(key_str.encode()).hexdigest()[:12]
    
    def _check_cache(self, key: str) -> Optional[Dict]:
        """Check cache with TTL"""
        if key in self.cache:
            cached = self.cache[key]
            if datetime.now() - cached["time"] < self.cache_ttl:
                return cached["data"]
        return None
    
    def _save_to_cache(self, key: str, data: Dict):
        """Save to cache with timestamp"""
        self.cache[key] = {
            "data": data,
            "time": datetime.now()
        }


# Singleton instance
groq_coach_enhanced = None

def get_enhanced_groq_coach() -> GroqCareerCoach:
    """Get or create enhanced GroqCareerCoach instance"""
    global groq_coach_enhanced
    if groq_coach_enhanced is None:
        groq_coach_enhanced = GroqCareerCoach()
    return groq_coach_enhanced