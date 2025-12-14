"""
Script untuk generate data aplikasi dummy - COMPATIBLE VERSION
Hanya menggunakan field yang ada: id, job_title, company, role_category, date_applied, status, notes
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal, engine
from app.models.applications import JobApplication, Base
from datetime import datetime, timedelta
import random

def create_dummy_applications():
    """Generate dummy job applications dengan field yang tepat"""
    print("🧪 Generating dummy job applications...")
    
    # Buat tabel jika belum ada
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Hapus data dummy lama jika ada
        db.query(JobApplication).filter(
            JobApplication.company.ilike("%Dummy%") |
            JobApplication.company.ilike("%Test%")
        ).delete(synchronize_session=False)
        
        # Role categories dengan performance berbeda
        roles = [
            ("Frontend Developer", 0.25),    # 25% interview rate
            ("Backend Developer", 0.15),     # 15% interview rate  
            ("Full Stack Developer", 0.20),  # 20% interview rate
            ("DevOps Engineer", 0.30),       # 30% interview rate (best)
            ("Data Scientist", 0.10),        # 10% interview rate (worst)
            ("Product Manager", 0.18),
            ("UX Designer", 0.22),
            ("QA Engineer", 0.12),
            ("Mobile Developer", 0.16),
            ("Systems Analyst", 0.14)
        ]
        
        companies = [
            "Google", "Microsoft", "Amazon", "Meta", "Netflix",
            "Spotify", "Airbnb", "Uber", "Shopify", "Stripe",
            "TechCorp", "InnovateInc", "DigitalWorks", "ByteLabs"
        ]
        
        dummy_apps = []
        
        # Generate 30 applications dengan pola realistis
        for i in range(1, 31):
            # Pilih role
            role_name, role_interview_rate = random.choice(roles)
            
            # Tentukan status berdasarkan role performance
            rand = random.random()
            
            # Adjust probabilities berdasarkan role performance
            if rand < 0.40:  # 40% ghosted (base)
                # Role dengan interview rate tinggi punya ghost rate lebih rendah
                ghost_prob = 0.40 * (1 - role_interview_rate)
                status = "ghosted" if random.random() < ghost_prob else "rejected"
            elif rand < 0.75:  # 35% rejected (total 75%)
                status = "rejected"
            elif rand < 0.95:  # 20% interview (disesuaikan dengan role performance)
                # Role dengan interview rate tinggi lebih mungkin dapat interview
                interview_prob = 0.20 * (role_interview_rate / 0.20)  # Normalize
                status = "interview" if random.random() < interview_prob else "rejected"
            else:  # 5% offer
                status = "offer" if random.random() < 0.05 else "interview"
            
            # Random date dalam 90 hari terakhir
            days_ago = random.randint(1, 90)
            app_date = datetime.now() - timedelta(days=days_ago)
            
            # Buat application object
            app = JobApplication(
                job_title=f"{role_name} Position",
                company=f"{random.choice(companies)}",
                role_category=role_name,
                date_applied=app_date.date(),
                status=status
            )
            
            # Tambahkan notes untuk 30% aplikasi
            if random.random() < 0.3:
                note_templates = [
                    f"Applied through company website. Followed up after 1 week.",
                    f"Referred by former colleague. Technical interview scheduled.",
                    f"Customized resume for this role. Waiting for response.",
                    f"Networking event connection. Submitted portfolio.",
                    f"Second round interview completed. Awaiting final decision."
                ]
                app.notes = random.choice(note_templates)
            
            dummy_apps.append(app)
            
            # Print progress
            status_icon = {
                "ghosted": "👻",
                "rejected": "❌", 
                "interview": "🎯",
                "offer": "💰"
            }
            print(f"  {status_icon.get(status, '📝')} {role_name} at {app.company} - {status}")
        
        # Tambahkan ke database
        db.add_all(dummy_apps)
        db.commit()
        
        print(f"\n✅ Successfully added {len(dummy_apps)} dummy applications!")
        
        # Hitung statistics
        total = len(dummy_apps)
        status_counts = {"ghosted": 0, "rejected": 0, "interview": 0, "offer": 0}
        role_stats = {}
        
        for app in dummy_apps:
            status_counts[app.status] += 1
            
            if app.role_category not in role_stats:
                role_stats[app.role_category] = {"total": 0, "interview": 0}
            role_stats[app.role_category]["total"] += 1
            if app.status == "interview":
                role_stats[app.role_category]["interview"] += 1
        
        print(f"\n📊 Overall Statistics:")
        print(f"  Total applications: {total}")
        for status, count in status_counts.items():
            percentage = (count / total * 100) if total > 0 else 0
            print(f"  {status.capitalize()}: {count} ({percentage:.1f}%)")
        
        # Interview rate
        interview_rate = (status_counts["interview"] / total * 100) if total > 0 else 0
        print(f"  📈 Interview rate: {interview_rate:.1f}%")
        
        print(f"\n👔 Role Performance (Top 5):")
        # Hitung interview rate per role
        role_performance = []
        for role, stats in role_stats.items():
            if stats["total"] > 0:
                int_rate = (stats["interview"] / stats["total"] * 100)
                role_performance.append((role, int_rate, stats["total"]))
        
        # Sort by interview rate
        role_performance.sort(key=lambda x: x[1], reverse=True)
        
        for role, int_rate, count in role_performance[:5]:
            print(f"  {role}: {int_rate:.1f}% interview rate ({count} apps)")
        
        # Worst performing role
        if len(role_performance) > 1:
            worst_role, worst_rate, worst_count = role_performance[-1]
            print(f"  ⚠️  Need improvement: {worst_role} ({worst_rate:.1f}% interview rate)")
        
        print("\n🎯 Ready for AI analysis!")
        print("\n💡 Test commands:")
        print('   curl "http://localhost:8000/api/analysis/rejection-patterns?days=90&use_ai=true"')
        print('   curl "http://localhost:8000/api/analysis/role-performance?days=90"')
        
        return dummy_apps
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return []
    finally:
        db.close()

def test_ai_analysis():
    """Test AI analysis dengan data yang baru dibuat"""
    print("\n🤖 Testing AI analysis...")
    
    # Tunggu sebentar untuk memastikan data tersimpan
    import time
    time.sleep(2)
    
    # Test via curl atau langsung
    print("\n📡 Testing via API...")
    print("Run these commands in another terminal:")
    print('1. Full analysis with AI:')
    print('   curl "http://localhost:8000/api/analysis/rejection-patterns?days=90&use_ai=true"')
    print('\n2. Role performance only:')
    print('   curl "http://localhost:8000/api/analysis/role-performance?days=90"')
    print('\n3. Quick insights:')
    print('   curl "http://localhost:8000/api/analysis/quick-insights?days=90"')

def cleanup_dummy_data():
    """Hapus semua data dummy"""
    db = SessionLocal()
    try:
        # Hapus berdasarkan pola company name
        deleted = db.query(JobApplication).delete()
        db.commit()
        print(f"🧹 Cleaned up {deleted} applications (all data)")
    except Exception as e:
        db.rollback()
        print(f"❌ Cleanup error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    print("=" * 60)
    print("🧪 DUMMY DATA GENERATOR - CAREER RECOVERY AI")
    print("=" * 60)
    
    import argparse
    parser = argparse.ArgumentParser(description="Generate dummy job applications")
    parser.add_argument("--clean", action="store_true", help="Clean all data")
    parser.add_argument("--generate", action="store_true", help="Generate dummy data")
    parser.add_argument("--test", action="store_true", help="Generate and show test commands")
    
    args = parser.parse_args()
    
    if args.clean:
        cleanup_dummy_data()
    elif args.test:
        create_dummy_applications()
        test_ai_analysis()
    else:
        # Default: generate data
        create_dummy_applications()