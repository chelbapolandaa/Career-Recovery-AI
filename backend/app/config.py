import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Database
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./career_ai.db")
    
    # OpenAI
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
    OPENAI_MAX_TOKENS = int(os.getenv("OPENAI_MAX_TOKENS", 500))
    OPENAI_TEMPERATURE = float(os.getenv("OPENAI_TEMPERATURE", 0.7))
    
    # Caching & Rate Limiting
    CACHE_TTL = int(os.getenv("CACHE_TTL", 3600))  # 1 hour
    RATE_LIMIT_PER_DAY = int(os.getenv("RATE_LIMIT_PER_DAY", 50))
    
    # Analysis
    ANALYSIS_DAYS_DEFAULT = int(os.getenv("ANALYSIS_DAYS_DEFAULT", 30))

settings = Settings()