import requests
import json
from datetime import date

BASE_URL = "http://localhost:8000/api"

def test_api():
    print("🧪 Testing Career Recovery AI API...")
    
    # 1. Test root endpoint
    print("\n1. Testing root endpoint...")
    response = requests.get("http://localhost:8000/")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
    
    # 2. Create application
    print("\n2. Creating test application...")
    new_app = {
        "job_title": "Frontend Developer",
        "company": "Tech Corp",
        "role_category": "dev",
        "date_applied": str(date.today()),
        "status": "rejected",
        "notes": "Technical test was difficult"
    }
    
    response = requests.post(
        f"{BASE_URL}/applications",
        json=new_app
    )
    
    if response.status_code == 200:
        app_data = response.json()
        app_id = app_data["id"]
        print(f"   ✅ Created application ID: {app_id}")
        print(f"   Data: {json.dumps(app_data, indent=2)}")
    else:
        print(f"   ❌ Failed: {response.status_code}")
        print(f"   Error: {response.text}")
        return
    
    # 3. Get all applications
    print("\n3. Getting all applications...")
    response = requests.get(f"{BASE_URL}/applications")
    if response.status_code == 200:
        apps = response.json()
        print(f"   ✅ Found {len(apps)} applications")
    
    # 4. Get stats
    print("\n4. Getting statistics...")
    response = requests.get(f"{BASE_URL}/applications/stats/summary?days=30")
    if response.status_code == 200:
        stats = response.json()
        print(f"   ✅ Stats retrieved")
        print(f"   Total applications: {stats['total_applications']}")
        print(f"   Response rate: {stats['response_rate']}%")
    
    # 5. Update application
    print("\n5. Updating application...")
    update_data = {
        "status": "interview",
        "notes": "Got interview scheduled!"
    }
    
    response = requests.put(
        f"{BASE_URL}/applications/{app_id}",
        json=update_data
    )
    
    if response.status_code == 200:
        print(f"   ✅ Updated application {app_id}")
    
    print("\n" + "="*50)
    print("🎉 API TEST COMPLETE!")
    print("="*50)
    print("\nNext steps:")
    print("1. Open http://localhost:8000/docs for Swagger UI")
    print("2. Test endpoints manually")
    print("3. Build frontend interface")

if __name__ == "__main__":
    test_api()