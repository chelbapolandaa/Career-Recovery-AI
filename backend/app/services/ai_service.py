import openai
import json
import asyncio
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from functools import lru_cache
from app.config import settings

class OpenAIAnalyzer:
    def __init__(self):
        if not settings.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY not configured")
        
        self.client = openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.OPENAI_MODEL
        self.cache = {}
        self.cache_ttl = timedelta(seconds=settings.CACHE_TTL)
        
    def _generate_cache_key(self, data: Dict, analysis_type: str) -> str:
        """Generate unique cache key from data"""
        import hashlib
        data_str = json.dumps(data, sort_keys=True) + analysis_type
        return hashlib.md5(data_str.encode()).hexdigest()
    
    def _check_cache(self, cache_key: str) -> Optional[Dict]:
        """Check if valid cached result exists"""
        if cache_key in self.cache:
            cached_item = self.cache[cache_key]
            if datetime.now() - cached_item['timestamp'] < self.cache_ttl:
                return cached_item['data']
        return None
    
    def _set_cache(self, cache_key: str, data: Dict):
        """Cache the result with timestamp"""
        self.cache[cache_key] = {
            'data': data,
            'timestamp': datetime.now()
        }
    
    async def generate_insights(
        self, 
        analysis_data: Dict, 
        user_context: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Generate AI-powered insights for job application analysis
        """
        cache_key = self._generate_cache_key(analysis_data, "insights")
        cached = self._check_cache(cache_key)
        if cached:
            return {**cached, 'cached': True}
        
        try:
            prompt = self._build_insights_prompt(analysis_data, user_context)
            
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": """You are an expert career coach and data analyst specializing in job search strategies. 
                        Your task is to analyze job application data and provide actionable insights, recommendations, 
                        and encouragement. Be specific, data-driven, and empathetic."""
                    },
                    {"role": "user", "content": prompt}
                ],
                temperature=settings.OPENAI_TEMPERATURE,
                max_tokens=settings.OPENAI_MAX_TOKENS,
                response_format={"type": "json_object"}
            )
            
            content = response.choices[0].message.content
            insights_data = json.loads(content)
            
            # Add metadata
            result = {
                **insights_data,
                'cached': False,
                'generated_at': datetime.now().isoformat(),
                'model': self.model
            }
            
            self._set_cache(cache_key, result)
            return result
            
        except openai.APIError as e:
            # Fallback to rule-based insights if API fails
            return self._generate_fallback_insights(analysis_data)
        except json.JSONDecodeError:
            return self._generate_fallback_insights(analysis_data)
    
    def _build_insights_prompt(self, data: Dict, user_context: Optional[Dict]) -> str:
        """Build detailed prompt for analysis"""
        
        prompt_template = """
        ANALYZE this job search data and provide JSON output with this exact structure:
        {
            "key_insights": ["insight1", "insight2", "insight3"],
            "actionable_recommendations": ["rec1", "rec2", "rec3"],
            "encouragement_message": "string",
            "risk_factors": ["risk1", "risk2"],
            "opportunities": ["opp1", "opp2"],
            "priority_action": "string"
        }

        DATA TO ANALYZE:
        Overall Statistics:
        - Total Applications: {total_applications}
        - Response Rate: {response_rate}%
        - Interview Rate: {interview_rate}%
        - Rejection Rate: {rejection_rate}%
        - Ghost Rate (No Response): {ghost_rate}%
        - Average Days to Response: {avg_days_to_response}
        
        Role Performance Breakdown:
        {role_performance}
        
        Patterns Detected:
        {patterns}
        
        Time Period: Last {days} days
        
        ADDITIONAL CONTEXT:
        {user_context}
        
        INSTRUCTIONS:
        1. Focus on patterns that indicate what's working vs not working
        2. Suggest specific, actionable changes to strategy
        3. Consider industry norms (tech: 10-20% response rate is normal)
        4. Identify if the volume, targeting, or materials need adjustment
        5. Provide encouragement based on the data
        
        Be specific. Instead of "improve resume", say "Add 3 quantifiable achievements to your {weak_role} applications".
        """
        
        # Format role performance
        role_perf_text = "\n".join([
            f"- {rp['role']}: {rp['applications']} apps, {rp['response_rate']}% response, {rp['interview_rate']}% interview"
            for rp in data.get('role_performance', [])
        ])
        
        # Format patterns
        patterns_text = "\n".join([
            f"- {p['type']}: {p['description']}"
            for p in data.get('patterns', [])
        ])
        
        # Format user context
        user_ctx_text = ""
        if user_context:
            user_ctx_text = f"User Experience Level: {user_context.get('experience_level', 'Not specified')}\n"
            user_ctx_text += f"Target Industry: {user_context.get('target_industry', 'Not specified')}"
        
        return prompt_template.format(
            total_applications=data.get('total_applications', 0),
            response_rate=data.get('response_rate', 0),
            interview_rate=data.get('interview_rate', 0),
            rejection_rate=data.get('rejection_rate', 0),
            ghost_rate=data.get('ghost_rate', 0),
            avg_days_to_response=data.get('avg_days_to_response', 'N/A'),
            role_performance=role_perf_text,
            patterns=patterns_text,
            days=data.get('analysis_period_days', 30),
            user_context=user_ctx_text
        )
    
    def _generate_fallback_insights(self, data: Dict) -> Dict:
        """Fallback insights when OpenAI API fails"""
        return {
            "key_insights": [
                "Basic analysis: Focus on roles with highest response rates",
                "Consider adjusting application volume or targeting",
                "Review application materials for improvement opportunities"
            ],
            "actionable_recommendations": [
                "A/B test different resume versions for low-response roles",
                "Increase networking efforts for target companies",
                "Request feedback from rejections when possible"
            ],
            "encouragement_message": "Job search is a marathon, not a sprint. Every application is data for improvement.",
            "risk_factors": ["High ghost rate may indicate targeting issue"],
            "opportunities": ["Strong performance in specific roles"],
            "priority_action": "Focus on roles with >20% response rate",
            "fallback": True,
            "generated_at": datetime.now().isoformat()
        }