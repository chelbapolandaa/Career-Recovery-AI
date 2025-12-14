"""
Career Recovery AI - Main FastAPI Application
UPDATED VERSION dengan .env loading
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from dotenv import load_dotenv  # <-- TAMBAHKAN INI
import os  # <-- TAMBAHKAN INI

print("🚀 Starting Career Recovery AI API...")

# ==================== LOAD .ENV FILE ====================
# Load environment variables dari .env file
print("📁 Loading environment variables...")
load_dotenv()  # Ini akan load .env dari current directory

# Cek jika GROQ_API_KEY sudah di-load
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if GROQ_API_KEY:
    print(f"✅ GROQ_API_KEY loaded: {GROQ_API_KEY[:10]}...{GROQ_API_KEY[-10:] if len(GROQ_API_KEY) > 20 else ''}")
else:
    print("❌ GROQ_API_KEY not found in .env")
    print("💡 Make sure .env file exists in backend/ folder")
    print("💡 Check if GROQ_API_KEY is set in .env")

# Cek AI_ENABLED
AI_ENABLED = os.getenv("AI_ENABLED", "false").lower() == "true"
print(f"🤖 AI Enabled: {AI_ENABLED}")

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Career Recovery AI API",
    description="AI system untuk analisis job rejection dan recovery strategy",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import routers manually (avoid __init__.py issues)
print("📦 Importing routers...")

# Module A: Applications
from .api.applications import router as applications_router
app.include_router(applications_router, prefix="/api")
print("✅ Module A: Application Tracker loaded")

# Module B: Analysis (try to load)
try:
    from .api.analysis import router as analysis_router
    app.include_router(analysis_router, prefix="/api")
    print("✅ Module B: Rejection Analyzer loaded")
except ImportError as e:
    print(f"⚠️ Module B: Failed to load - {e}")
    # Create dummy router for analysis
    from fastapi import APIRouter
    analysis_router = APIRouter()
    
    @analysis_router.get("/analysis/test")
    def analysis_test():
        return {"message": "Analysis module loading, check server logs"}
    
    app.include_router(analysis_router, prefix="/api")

@app.get("/")
async def root():
    return {
        "message": "Career Recovery AI API",
        "status": "running",
        "docs": "/docs",
        "ai_enabled": AI_ENABLED,
        "modules": {
            "A": "Application Tracker - ✅ READY",
            "B": "Rejection Analyzer - ✅ LOADED",
            "C": "Strategy Engine - TODO",
            "D": "Burnout Monitor - TODO",
            "E": "Weekly Report - TODO"
        },
        "endpoints": {
            "applications": "/api/applications",
            "analysis": "/api/analysis/*",
            "swagger": "/docs"
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/env-check")
async def env_check():
    """Endpoint untuk cek environment variables"""
    return {
        "groq_api_key_loaded": bool(os.getenv("GROQ_API_KEY")),
        "ai_enabled": os.getenv("AI_ENABLED", "false"),
        "groq_model": os.getenv("GROQ_MODEL", "not set"),
        "env_vars": {k: "***" if "KEY" in k else v for k, v in os.environ.items() if "GROQ" in k or "AI" in k}
    }

print("🎯 API ready! Available endpoints:")
print("  • http://localhost:8000/")
print("  • http://localhost:8000/docs")
print("  • http://localhost:8000/api/applications")
print("  • http://localhost:8000/api/analysis/*")
print("  • http://localhost:8000/env-check (check .env loading)")