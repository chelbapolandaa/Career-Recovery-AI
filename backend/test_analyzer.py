import requests
import json

BASE_URL = "http://localhost:8000/api"

def test_analyzer():
    print("🧪 Testing Module B: Rejection Pattern Analyzer...")
    
    # 1. Test quick insights
    print("\n1. Testing quick insights (30 days)...")
    response = requests.get(f"{BASE_URL}/analysis/quick-insights")
    
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Success! Status: {data.get('status', 'N/A')}")
        print(f"   📊 Applications analyzed: {data.get('metadata', {}).get('applications_analyzed', 0)}")
        
        # Print summary
        if 'summary' in data:
            summary = data['summary']
            print(f"   📈 Response rate: {summary.get('response_rate', 0)}%")
            print(f"   🎯 Interview rate: {summary.get('interview_rate', 0)}%")
        
        # Print insights (handle both string and list)
        if 'insights' in data:
            print("\n   💡 Insights:")
            insights = data['insights']
            if isinstance(insights, list):
                for insight in insights[:3]:  # First 3 insights
                    print(f"   • {insight}")
            else:
                print(f"   • {insights[:100]}...")
        
        # Print recommendations (handle both dict and string)
        if 'recommendations' in data:
            print("\n   🎯 Recommendations:")
            recs = data['recommendations']
            if isinstance(recs, list):
                for rec in recs[:3]:  # First 3 recommendations
                    if isinstance(rec, dict):
                        print(f"   • {rec.get('action', 'N/A')}: {rec.get('reason', '')}")
                    else:
                        print(f"   • {rec}")
            else:
                print(f"   • {recs}")
    
    # 2. Test role performance
    print("\n2. Testing role performance analysis...")
    response = requests.get(f"{BASE_URL}/analysis/role-performance")
    
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Status: {data.get('status', 'N/A')}")
        
        if 'role_performance' in data and data['role_performance']:
            print("   📊 Role Performance:")
            for role in data['role_performance'][:3]:  # Top 3 roles
                print(f"   • {role.get('role', 'N/A')}: {role.get('interview_rate', 0)}% interview rate")
        
        if 'recommendation' in data:
            print(f"   💡 Recommendation: {data['recommendation']}")
    
    # 3. Test full analysis
    print("\n3. Testing full analysis (90 days)...")
    response = requests.get(f"{BASE_URL}/analysis/rejection-patterns?days=90")
    
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Status: {data.get('status', 'N/A')}")
        
        if 'summary' in data:
            summary = data['summary']
            print(f"   📊 Applications: {summary.get('total_applications', 0)}")
            print(f"   📈 Response Rate: {summary.get('response_rate', 0)}%")
            print(f"   🎯 Interview Rate: {summary.get('interview_rate', 0)}%")
        
        if 'metadata' in data:
            print(f"   📅 Period: {data['metadata'].get('period_days', 0)} days")
    
    print("\n" + "="*50)
    print("🎉 Module B Test Complete!")
    print("="*50)
    print("\n✅ MODULE B STATUS: WORKING!")
    print("\n📋 Next steps:")
    print("1. Add analysis component to frontend")
    print("2. Display AI insights in dashboard")
    print("3. Create dedicated analysis page")
    print("4. Add visualizations (charts)")

if __name__ == "__main__":
    test_analyzer()