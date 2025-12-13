#!/usr/bin/env python3
"""
Setup script untuk Career Recovery AI Project
Menghasilkan struktur folder lengkap untuk backend dan frontend
"""

import os
import sys
from pathlib import Path

# Struktur folder lengkap
PROJECT_STRUCTURE = {
    "backend": {
        "app": {
            "api": {
                "__init__.py": "",
                "applications.py": "# Module A: Application Tracker API endpoints",
                "analysis.py": "# Module B: Rejection Pattern Analyzer API",
                "strategy.py": "# Module C: Strategy Pivot Engine API",
                "wellbeing.py": "# Module D: Burnout & Survival Monitor API",
                "reports.py": "# Module E: Weekly Survival Report API",
            },
            "core": {
                "__init__.py": "",
                "config.py": "# Application configuration",
                "security.py": "# Authentication & security (jika perlu)",
                "dependencies.py": "# FastAPI dependencies",
            },
            "models": {
                "__init__.py": "# Database models (SQLAlchemy)",
                "applications.py": "# JobApplication model",
                "checkins.py": "# DailyCheckIn model",
                "recommendations.py": "# SkillRecommendation model",
                "reports.py": "# WeeklyReport model",
            },
            "schemas": {
                "__init__.py": "",
                "applications.py": "# Pydantic schemas untuk Application",
                "analysis.py": "# Schemas untuk analysis results",
                "recommendations.py": "# Schemas untuk AI recommendations",
            },
            "services": {
                "__init__.py": "",
                "analyzer.py": "# Module B: Rejection Pattern Analyzer logic",
                "strategizer.py": "# Module C: Strategy Pivot Engine logic",
                "wellbeing.py": "# Module D: Burnout Monitor logic",
                "reporter.py": "# Module E: Report Generator",
                "llm_service.py": "# LLM integration service",
            },
            "utils": {
                "__init__.py": "",
                "database.py": "# Database connection & session",
                "calculations.py": "# Utility calculations & metrics",
                "validators.py": "# Data validation helpers",
            },
            "__init__.py": "# Main application package",
            "main.py": "# FastAPI application entry point",
            "database.py": "# Database setup & models",
        },
        "tests": {
            "__init__.py": "",
            "test_applications.py": "# Tests untuk Module A",
            "test_analysis.py": "# Tests untuk Module B",
            "test_strategy.py": "# Tests untuk Module C",
            "conftest.py": "# Test configuration",
        },
        "alembic": {
            "versions": {},
            "env.py": "# Alembic environment",
            "script.py.mako": "# Alembic migration template",
        },
        "requirements.txt": "# Python dependencies",
        ".env.example": "# Environment variables template",
        "Dockerfile": "# Docker configuration",
        "docker-compose.yml": "# Docker compose setup",
    },
    "frontend": {
        "public": {
            "index.html": "# HTML template",
            "favicon.ico": "",
        },
        "src": {
            "components": {
                "dashboard": {
                    "__init__.py": "",
                    "Dashboard.jsx": "# Main dashboard component",
                    "StatsCards.jsx": "# Statistics cards",
                    "Charts.jsx": "# Data visualization charts",
                },
                "applications": {
                    "__init__.py": "",
                    "ApplicationList.jsx": "# Application tracker table",
                    "ApplicationForm.jsx": "# Add/edit application form",
                    "ApplicationStats.jsx": "# Application statistics",
                },
                "analysis": {
                    "__init__.py": "",
                    "RejectionAnalysis.jsx": "# Module B visualization",
                    "PatternInsights.jsx": "# AI insights display",
                },
                "strategy": {
                    "__init__.py": "",
                    "Recommendations.jsx": "# Module C recommendations",
                    "SkillSuggestions.jsx": "# Skill learning suggestions",
                },
                "wellbeing": {
                    "__init__.py": "",
                    "BurnoutMonitor.jsx": "# Module D check-in form",
                    "MoodTracker.jsx": "# Mood tracking visualization",
                },
                "reports": {
                    "__init__.py": "",
                    "WeeklyReport.jsx": "# Module E report viewer",
                    "ReportExport.jsx": "# PDF export functionality",
                },
                "ui": {
                    "__init__.py": "",
                    "Card.jsx": "# Reusable card component",
                    "Button.jsx": "# Button component",
                    "Table.jsx": "# Table component",
                    "Modal.jsx": "# Modal dialog",
                },
                "__init__.py": "",
                "Layout.jsx": "# Application layout",
                "Navbar.jsx": "# Navigation bar",
            },
            "hooks": {
                "__init__.py": "",
                "useApplications.js": "# Custom hook for applications data",
                "useAnalysis.js": "# Custom hook for analysis data",
                "useRecommendations.js": "# Custom hook for AI recommendations",
            },
            "services": {
                "__init__.py": "",
                "api.js": "# API service client",
                "applications.js": "# Applications API calls",
                "analysis.js": "# Analysis API calls",
                "reports.js": "# Reports API calls",
            },
            "utils": {
                "__init__.py": "",
                "formatters.js": "# Data formatting utilities",
                "charts.js": "# Chart data preparation",
                "download.js": "# File download utilities",
            },
            "styles": {
                "__init__.py": "",
                "globals.css": "# Global CSS styles",
                "tailwind.css": "# Tailwind imports",
            },
            "App.jsx": "# Main React application",
            "index.js": "# React entry point",
            "routes.js": "# Application routes",
        },
        "package.json": "# NPM dependencies",
        "tailwind.config.js": "# Tailwind CSS configuration",
        "postcss.config.js": "# PostCSS configuration",
        "vite.config.js": "# Vite configuration",
        ".gitignore": "# Git ignore file",
    },
    "docs": {
        "api": {
            "endpoints.md": "# API documentation",
            "models.md": "# Data models documentation",
        },
        "modules": {
            "module_a.md": "# Module A: Application Tracker spec",
            "module_b.md": "# Module B: Rejection Analyzer spec",
            "module_c.md": "# Module C: Strategy Engine spec",
            "module_d.md": "# Module D: Burnout Monitor spec",
            "module_e.md": "# Module E: Weekly Report spec",
        },
        "decisions": {
            "architecture.md": "# Architecture decisions",
            "tech_stack.md": "# Technology choices",
        },
    },
    "scripts": {
        "init_db.py": "# Initialize database script",
        "seed_data.py": "# Seed sample data",
        "generate_report.py": "# Manual report generation",
    },
    ".github": {
        "workflows": {
            "ci.yml": "# CI pipeline",
            "deploy.yml": "# Deployment pipeline",
        },
    },
    ".vscode": {
        "settings.json": "# VS Code settings",
        "extensions.json": "# Recommended extensions",
    },
    "docker-compose.yml": "# Main docker compose",
    ".env.example": "# Environment variables",
    ".gitignore": "# Git ignore",
    "README.md": "# Project documentation",
    "requirements.txt": "# Backend dependencies",
}

# File templates dengan minimal content
FILE_TEMPLATES = {
    # BACKEND
    "backend/app/main.py": '''"""
Career Recovery AI - Main FastAPI Application
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .api import applications, analysis, strategy, wellbeing, reports

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Career Recovery AI API",
    description="AI system untuk analisis job rejection dan recovery strategy",
    version="1.0.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(applications.router)
app.include_router(analysis.router)
app.include_router(strategy.router)
app.include_router(wellbeing.router)
app.include_router(reports.router)

@app.get("/")
async def root():
    return {"message": "Career Recovery AI API", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
''',

    "backend/app/database.py": '''"""
Database configuration
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# Use SQLite for development, PostgreSQL for production
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./career_ai.db")

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency untuk mendapatkan DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
''',

    "backend/app/models/applications.py": '''"""
Database models untuk Module A: Application Tracker
"""
from sqlalchemy import Column, Integer, String, Date, Enum, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
import enum

Base = declarative_base()

class ApplicationStatus(enum.Enum):
    GHOSTED = "ghosted"
    REJECTED = "rejected"
    INTERVIEW = "interview"
    OFFER = "offer"

class RoleCategory(enum.Enum):
    DEV = "dev"
    VA = "va"
    OPS = "ops"
    AI = "ai"
    IT = "it"
    OTHER = "other"

class JobApplication(Base):
    __tablename__ = "job_applications"
    
    id = Column(Integer, primary_key=True, index=True)
    job_title = Column(String(200), nullable=False)
    company = Column(String(200), nullable=False)
    role_category = Column(Enum(RoleCategory), nullable=False)
    date_applied = Column(Date, nullable=False)
    status = Column(Enum(ApplicationStatus), nullable=False, default=ApplicationStatus.GHOSTED)
    notes = Column(Text, nullable=True)
    
    # Untuk analisis lanjutan
    job_description = Column(Text, nullable=True)
    salary_expectation = Column(String(100), nullable=True)
    job_portal = Column(String(100), nullable=True)
    contact_person = Column(String(200), nullable=True)
    
    def __repr__(self):
        return f"<JobApplication {self.job_title} at {self.company}>"
''',

    "backend/app/schemas/applications.py": '''"""
Pydantic schemas untuk Module A: Application Tracker
"""
from pydantic import BaseModel, Field
from datetime import date
from typing import Optional
from enum import Enum

class RoleCategory(str, Enum):
    DEV = "dev"
    VA = "va"
    OPS = "ops"
    AI = "ai"
    IT = "it"
    OTHER = "other"

class ApplicationStatus(str, Enum):
    GHOSTED = "ghosted"
    REJECTED = "rejected"
    INTERVIEW = "interview"
    OFFER = "offer"

class ApplicationBase(BaseModel):
    job_title: str = Field(..., min_length=1, max_length=200)
    company: str = Field(..., min_length=1, max_length=200)
    role_category: RoleCategory
    date_applied: date
    status: ApplicationStatus = ApplicationStatus.GHOSTED
    notes: Optional[str] = None
    job_description: Optional[str] = None
    salary_expectation: Optional[str] = None

class ApplicationCreate(ApplicationBase):
    pass

class ApplicationUpdate(BaseModel):
    status: Optional[ApplicationStatus] = None
    notes: Optional[str] = None

class ApplicationResponse(ApplicationBase):
    id: int
    
    class Config:
        from_attributes = True  # Untuk kompatibilitas SQLAlchemy 2.0
''',

    "backend/app/api/applications.py": '''"""
Module A: Application Tracker API Endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date, timedelta

from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/api/applications", tags=["applications"])

@router.post("/", response_model=schemas.ApplicationResponse)
def create_application(
    application: schemas.ApplicationCreate,
    db: Session = Depends(get_db)
):
    """
    Tambah aplikasi pekerjaan baru
    """
    db_application = models.JobApplication(**application.dict())
    db.add(db_application)
    db.commit()
    db.refresh(db_application)
    return db_application

@router.get("/", response_model=List[schemas.ApplicationResponse])
def get_applications(
    skip: int = 0,
    limit: int = 100,
    role_category: Optional[schemas.RoleCategory] = None,
    status: Optional[schemas.ApplicationStatus] = None,
    db: Session = Depends(get_db)
):
    """
    Get semua aplikasi dengan filter opsional
    """
    query = db.query(models.JobApplication)
    
    if role_category:
        query = query.filter(models.JobApplication.role_category == role_category)
    
    if status:
        query = query.filter(models.JobApplication.status == status)
    
    return query.order_by(models.JobApplication.date_applied.desc())\
                .offset(skip).limit(limit).all()

@router.get("/{application_id}", response_model=schemas.ApplicationResponse)
def get_application(
    application_id: int,
    db: Session = Depends(get_db)
):
    """
    Get aplikasi spesifik berdasarkan ID
    """
    application = db.query(models.JobApplication)\
                    .filter(models.JobApplication.id == application_id)\
                    .first()
    
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    
    return application

@router.put("/{application_id}", response_model=schemas.ApplicationResponse)
def update_application(
    application_id: int,
    application_update: schemas.ApplicationUpdate,
    db: Session = Depends(get_db)
):
    """
    Update status atau notes aplikasi
    """
    db_application = db.query(models.JobApplication)\
                       .filter(models.JobApplication.id == application_id)\
                       .first()
    
    if not db_application:
        raise HTTPException(status_code=404, detail="Application not found")
    
    update_data = application_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_application, field, value)
    
    db.commit()
    db.refresh(db_application)
    return db_application

@router.delete("/{application_id}")
def delete_application(
    application_id: int,
    db: Session = Depends(get_db)
):
    """
    Hapus aplikasi (jika salah input)
    """
    application = db.query(models.JobApplication)\
                    .filter(models.JobApplication.id == application_id)\
                    .first()
    
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    
    db.delete(application)
    db.commit()
    
    return {"message": "Application deleted successfully"}

@router.get("/stats/summary")
def get_application_stats(
    days: int = Query(30, description="Jumlah hari terakhir untuk dianalisis"),
    db: Session = Depends(get_db)
):
    """
    Get statistik aplikasi
    """
    from_date = date.today() - timedelta(days=days)
    
    # Total applications
    total = db.query(models.JobApplication)\
              .filter(models.JobApplication.date_applied >= from_date)\
              .count()
    
    # Count by status
    status_counts = {}
    for status in schemas.ApplicationStatus:
        count = db.query(models.JobApplication)\
                  .filter(
                      models.JobApplication.date_applied >= from_date,
                      models.JobApplication.status == status
                  )\
                  .count()
        status_counts[status.value] = count
    
    # Response rate (non-ghosted)
    responded = total - status_counts.get("ghosted", 0)
    response_rate = (responded / total * 100) if total > 0 else 0
    
    # Count by role category
    role_counts = {}
    for role in schemas.RoleCategory:
        count = db.query(models.JobApplication)\
                  .filter(
                      models.JobApplication.date_applied >= from_date,
                      models.JobApplication.role_category == role
                  )\
                  .count()
        role_counts[role.value] = count
    
    return {
        "total_applications": total,
        "status_breakdown": status_counts,
        "response_rate": round(response_rate, 1),
        "role_breakdown": role_counts,
        "period_days": days,
        "period_from": from_date.isoformat()
    }
''',

    "backend/requirements.txt": '''# Career Recovery AI - Backend Dependencies
# Core
fastapi==0.104.1
uvicorn[standard]==0.24.0

# Database
sqlalchemy==2.0.23
alembic==1.12.1
psycopg2-binary==2.9.9  # untuk PostgreSQL
# python-dotenv==1.0.0

# AI & Data Analysis
openai==0.28.0
pandas==2.1.3
scikit-learn==1.3.2
numpy==1.24.3

# Utilities
python-multipart==0.0.6
pydantic[email]==2.5.0
pydantic-settings==2.1.0

# Development
pytest==7.4.3
httpx==0.25.1
black==23.11.0
flake8==6.1.0
''',

    "backend/.env.example": '''# Career Recovery AI - Environment Variables
# Database
DATABASE_URL=sqlite:///./career_ai.db
# DATABASE_URL=postgresql://user:password@localhost/careerai_db

# OpenAI (untuk Module B, C)
OPENAI_API_KEY=sk-your-openai-api-key-here
# Opsional: LLM lokal
# OLLAMA_BASE_URL=http://localhost:11434
# OLLAMA_MODEL=llama2

# Application
APP_ENV=development
SECRET_KEY=your-secret-key-here
DEBUG=True

# CORS
FRONTEND_URL=http://localhost:3000
''',

    # FRONTEND
    "frontend/package.json": '''{
  "name": "career-recovery-ai-frontend",
  "version": "1.0.0",
  "private": true,
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.20.0",
    "axios": "^1.6.2",
    "recharts": "^2.10.4",
    "date-fns": "^2.30.0",
    "clsx": "^2.0.0",
    "tailwind-merge": "^2.0.0",
    "react-hot-toast": "^2.4.1"
  },
  "devDependencies": {
    "@types/react": "^18.2.37",
    "@types/react-dom": "^18.2.15",
    "@vitejs/plugin-react": "^4.2.0",
    "autoprefixer": "^10.4.16",
    "postcss": "^8.4.31",
    "tailwindcss": "^3.3.5",
    "vite": "^5.0.0"
  },
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "lint": "eslint . --ext js,jsx --report-unused-disable-directives --max-warnings 0",
    "preview": "vite preview"
  }
}
''',

    "frontend/src/App.jsx": '''import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Layout from "./components/Layout";
import Dashboard from "./components/dashboard/Dashboard";
import ApplicationTracker from "./components/applications/ApplicationList";
import Analysis from "./components/analysis/RejectionAnalysis";
import Strategy from "./components/strategy/Recommendations";
import Wellbeing from "./components/wellbeing/BurnoutMonitor";
import Reports from "./components/reports/WeeklyReport";

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/applications" element={<ApplicationTracker />} />
          <Route path="/analysis" element={<Analysis />} />
          <Route path="/strategy" element={<Strategy />} />
          <Route path="/wellbeing" element={<Wellbeing />} />
          <Route path="/reports" element={<Reports />} />
        </Routes>
      </Layout>
    </Router>
  );
}

export default App;
''',

    "frontend/src/components/dashboard/Dashboard.jsx": '''import React, { useState, useEffect } from "react";
import StatsCards from "./StatsCards";
import Charts from "./Charts";
import { getApplicationsStats } from "../../services/api";

const Dashboard = () => {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      setLoading(true);
      const data = await getApplicationsStats();
      setStats(data);
    } catch (error) {
      console.error("Error fetching stats:", error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Career Recovery AI Dashboard</h1>
        <p className="text-gray-600 mt-2">
          AI-powered insights untuk job search strategy Anda
        </p>
      </div>

      {stats && <StatsCards stats={stats} />}
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Charts stats={stats} />
        
        <div className="bg-white rounded-xl shadow p-6">
          <h2 className="text-xl font-semibold text-gray-800 mb-4">
            🎯 Quick Actions
          </h2>
          <div className="space-y-3">
            <button className="w-full text-left p-3 bg-blue-50 hover:bg-blue-100 rounded-lg transition">
              📝 Add New Application
            </button>
            <button className="w-full text-left p-3 bg-green-50 hover:bg-green-100 rounded-lg transition">
              📊 Generate Weekly Report
            </button>
            <button className="w-full text-left p-3 bg-yellow-50 hover:bg-yellow-100 rounded-lg transition">
              🧠 Get AI Recommendations
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
''',

    "frontend/tailwind.config.js": '''/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#eff6ff',
          100: '#dbeafe',
          200: '#bfdbfe',
          300: '#93c5fd',
          400: '#60a5fa',
          500: '#3b82f6',
          600: '#2563eb',
          700: '#1d4ed8',
          800: '#1e40af',
          900: '#1e3a8a',
        }
      }
    },
  },
  plugins: [],
}
'''}

# ====== TAMBAHKAN DI BAWAH INI ======

def create_structure(base_path=".", structure=PROJECT_STRUCTURE, file_templates=FILE_TEMPLATES):
    """Membuat struktur folder dan file"""
    base_path = Path(base_path)
    
    def create_items(path, items):
        for name, content in items.items():
            item_path = path / name
            
            if isinstance(content, dict):
                # Ini adalah folder
                item_path.mkdir(parents=True, exist_ok=True)
                print(f"📁 Created folder: {item_path.relative_to(base_path)}")
                
                # Rekursif untuk sub-items
                create_items(item_path, content)
            else:
                # Ini adalah file
                if str(item_path.relative_to(base_path)) in file_templates:
                    # Gunakan template jika ada
                    content = file_templates[str(item_path.relative_to(base_path))]
                
                item_path.parent.mkdir(parents=True, exist_ok=True)
                item_path.write_text(content, encoding="utf-8")
                print(f"📄 Created file: {item_path.relative_to(base_path)}")
    
    print("🚀 Creating Career Recovery AI Project Structure...")
    print("=" * 60)
    
    try:
        create_items(base_path, structure)
        print("=" * 60)
        print("✅ Project structure created successfully!")
        print("\n📋 Next steps:")
        print("1. cd career-recovery-ai")
        print("2. Setup backend: cd backend && pip install -r requirements.txt")
        print("3. Setup frontend: cd frontend && npm install")
        print("4. Run backend: uvicorn app.main:app --reload")
        print("5. Run frontend: npm run dev")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Setup Career Recovery AI project structure")
    parser.add_argument(
        "--path",
        type=str,
        default=".",
        help="Base path untuk membuat project (default: current directory)"
    )
    
    args = parser.parse_args()
    
    # Confirm creation
    confirm = input(f"Create project structure in '{args.path}'? (y/n): ")
    if confirm.lower() != 'y':
        print("Operation cancelled.")
        return
    
    create_structure(args.path)

if __name__ == "__main__":
    main()