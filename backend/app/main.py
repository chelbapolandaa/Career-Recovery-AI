"""
Career Recovery AI - Main FastAPI Application
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

print("🚀 Starting Career Recovery AI API...")

# ==================== LOAD .ENV FILE ====================
print("📁 Loading environment variables...")
load_dotenv()

# Import database
try:
    from .database import engine, Base
    print("✅ Database module loaded")
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created/verified")
    
except ImportError as e:
    print(f"❌ Database import error: {e}")
    raise

# Cek jika GROQ_API_KEY sudah di-load
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if GROQ_API_KEY:
    print(f"✅ GROQ_API_KEY loaded: {GROQ_API_KEY[:10]}...")
else:
    print("⚠️ GROQ_API_KEY not found in .env")

# Cek AI_ENABLED
AI_ENABLED = os.getenv("AI_ENABLED", "false").lower() == "true"
print(f"🤖 AI Enabled: {AI_ENABLED}")

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

# Import routers
print("📦 Importing routers...")

# Module A: Applications
try:
    from .api.applications import router as applications_router
    app.include_router(applications_router, prefix="/api")
    print("✅ Module A: Application Tracker loaded")
except ImportError as e:
    print(f"⚠️ Module A: Failed to load - {e}")

# Module B: Analysis
try:
    from .api.analysis import router as analysis_router
    app.include_router(analysis_router, prefix="/api")
    print("✅ Module B: Rejection Analyzer loaded")
except ImportError as e:
    print(f"⚠️ Module B: Failed to load - {e}")

# Module C: Strategy Engine
try:
    from .api.strategies import router as strategies_router
    app.include_router(strategies_router, prefix="/api")
    print("✅ Module C: Strategy Engine loaded")
except ImportError as e:
    print(f"⚠️ Module C: Failed to load - {e}")

@app.get("/")
async def root():
    return {
        "message": "Career Recovery AI API",
        "status": "running",
        "docs": "/docs",
        "modules": {
            "A": "Application Tracker",
            "B": "Rejection Analyzer", 
            "C": "Strategy Engine"
        }
    }

print("🎯 API ready! Visit http://localhost:8000/docs")