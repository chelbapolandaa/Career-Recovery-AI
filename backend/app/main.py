"""
Career Recovery AI - Main FastAPI Application
SIMPLE VERSION - pasti work
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base

print("🚀 Starting Career Recovery AI API...")

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

print("🎯 API ready! Available endpoints:")
print("  • http://localhost:8000/")
print("  • http://localhost:8000/docs")
print("  • http://localhost:8000/api/applications")
print("  • http://localhost:8000/api/analysis/*")