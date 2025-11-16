"""
Live Performance Test for AI Candidate Matching

Tests the actual API endpoint with timing
"""

import time
import requests
import json

# Configuration
BACKEND_URL = "http://localhost:8000"
API_BASE = f"{BACKEND_URL}/api/v1"

def get_auth_token():
    """Get auth token for test employer account."""
    login_url = f"{API_BASE}/auth/login"
    
    # Using the test employer account
    credentials = {
        "email": "alice.johnson@testtech.com",
        "password": "TestPass123!",
        "role": "employer"
    }
    
    print("🔐 Logging in as test employer...")
    response = requests.post(login_url, json=credentials)
    
    if response.status_code == 200:
        data = response.json()
        token = data.get("access_token")
        print(f"✅ Login successful")
        return token
    else:
        print(f"❌ Login failed: {response.status_code}")
        print(f"   Response: {response.text}")
        return None

def get_employer_jobs(token):
    """Get employer's job listings."""
    headers = {"Authorization": f"Bearer {token}"}
    jobs_url = f"{API_BASE}/employers/jobs"
    
    print("\n📋 Fetching job listings...")
    response = requests.get(jobs_url, headers=headers)
    
    if response.status_code == 200:
        jobs = response.json()
        print(f"✅ Found {len(jobs)} jobs")
        return jobs
    else:
        print(f"❌ Failed to fetch jobs: {response.status_code}")
        return []

def test_candidate_matching(token, job_id, job_title):
    """Test AI candidate matching performance."""
    headers = {"Authorization": f"Bearer {token}"}
    candidates_url = f"{API_BASE}/employers/jobs/{job_id}/candidates"
    
    # Parameters: 15 candidates, min_score 0
    params = {
        "n_results": 15,
        "min_score": 0.0
    }
    
    print(f"\n{'='*70}")
    print(f"Testing AI Matching for: {job_title}")
    print(f"Job ID: {job_id}")
    print('='*70)
    
    # Test 1: First Load (no cache)
    print("\n⏱️  TEST 1: First Load (No Cache)")
    print("   Starting request...")
    
    start_time = time.time()
    response = requests.get(candidates_url, headers=headers, params=params, timeout=90)
    first_load_time = time.time() - start_time
    
    if response.status_code == 200:
        candidates = response.json()
        print(f"   ✅ Success!")
        print(f"   Time: {first_load_time:.2f} seconds")
        print(f"   Candidates: {len(candidates)}")
        
        if first_load_time < 15:
            print(f"   Result: ✅ EXCELLENT (< 15s target)")
        elif first_load_time < 30:
            print(f"   Result: ⚠️  ACCEPTABLE (< 30s)")
        else:
            print(f"   Result: ❌ TOO SLOW (> 30s)")
        
        # Show top 3 candidates
        if candidates:
            print(f"\n   📊 Top 3 Candidates:")
            for i, candidate in enumerate(candidates[:3], 1):
                name = f"{candidate.get('first_name', 'N/A')} {candidate.get('last_name', 'N/A')}"
                score = candidate.get('match_score', 0)
                print(f"      {i}. {name} - {score:.1f}%")
    else:
        print(f"   ❌ Failed: {response.status_code}")
        print(f"   Error: {response.text}")
        candidates = []
        first_load_time = 0
    
    # Test 2: Cached Load (should be instant)
    print(f"\n⏱️  TEST 2: Cached Load (Same Job)")
    print("   Starting request...")
    
    start_time = time.time()
    response = requests.get(candidates_url, headers=headers, params=params, timeout=90)
    cached_load_time = time.time() - start_time
    
    if response.status_code == 200:
        candidates_cached = response.json()
        print(f"   ✅ Success!")
        print(f"   Time: {cached_load_time:.2f} seconds")
        print(f"   Candidates: {len(candidates_cached)}")
        
        if cached_load_time < 2:
            print(f"   Result: ✅ EXCELLENT (< 2s - cached)")
        elif cached_load_time < 5:
            print(f"   Result: ⚠️  GOOD (< 5s)")
        else:
            print(f"   Result: ❌ NOT CACHED (> 5s)")
    else:
        print(f"   ❌ Failed: {response.status_code}")
        cached_load_time = 0
        candidates_cached = []
    
    # Performance Summary
    print(f"\n{'─'*70}")
    print("PERFORMANCE SUMMARY")
    print('─'*70)
    
    if first_load_time > 0 and cached_load_time > 0:
        speedup = first_load_time / cached_load_time if cached_load_time > 0 else 0
        improvement = ((first_load_time - cached_load_time) / first_load_time * 100) if first_load_time > 0 else 0
        
        print(f"First Load:      {first_load_time:.2f}s")
        print(f"Cached Load:     {cached_load_time:.2f}s")
        print(f"Speedup:         {speedup:.1f}x faster")
        print(f"Cache Benefit:   {improvement:.1f}% time saved")
        
        # Compare to old system (estimated)
        estimated_old = len(candidates) * 3  # 3s per candidate sequential
        print(f"\n📊 Comparison to OLD system:")
        print(f"   Old (50 candidates sequential): ~150s")
        print(f"   Old (15 candidates sequential): ~{estimated_old}s")
        print(f"   New (15 candidates parallel):   {first_load_time:.2f}s")
        if estimated_old > 0:
            old_speedup = estimated_old / first_load_time if first_load_time > 0 else 0
            print(f"   Overall Speedup: {old_speedup:.1f}x faster")
    
    return first_load_time, cached_load_time, len(candidates)

def main():
    print("="*70)
    print("AI CANDIDATE MATCHING - LIVE PERFORMANCE TEST")
    print("="*70)
    print("\nThis test connects to the running backend and measures real performance.")
    print("Make sure both backend (port 8000) and MongoDB are running.")
    
    # Get auth token
    token = get_auth_token()
    if not token:
        print("\n❌ Cannot proceed without authentication")
        return
    
    # Get jobs
    jobs = get_employer_jobs(token)
    if not jobs:
        print("\n⚠️  No jobs found. Create some jobs first or check test account.")
        return
    
    # Test with first available job
    job = jobs[0]
    job_id = job.get("job_id")
    job_title = job.get("job_title", "Unknown Job")
    
    first_time, cached_time, num_candidates = test_candidate_matching(token, job_id, job_title)
    
    # Final Summary
    print(f"\n\n{'='*70}")
    print("FINAL RESULTS")
    print('='*70)
    
    tests_passed = 0
    tests_total = 3
    
    if first_time > 0 and first_time < 15:
        print("✅ Test 1: First load < 15s")
        tests_passed += 1
    else:
        print(f"❌ Test 1: First load >= 15s ({first_time:.2f}s)")
    
    if cached_time > 0 and cached_time < 2:
        print("✅ Test 2: Cached load < 2s")
        tests_passed += 1
    else:
        print(f"❌ Test 2: Cached load >= 2s ({cached_time:.2f}s)")
    
    if num_candidates > 0:
        print(f"✅ Test 3: Found {num_candidates} candidates")
        tests_passed += 1
    else:
        print("❌ Test 3: No candidates found")
    
    print(f"\n{'='*70}")
    print(f"SCORE: {tests_passed}/{tests_total} tests passed")
    print('='*70)
    
    if tests_passed == tests_total:
        print("🎉 ALL TESTS PASSED! Optimization successful!")
    elif tests_passed >= 2:
        print("⚠️  Most tests passed. Minor issues to review.")
    else:
        print("❌ Multiple tests failed. Review implementation.")
    
    print("\n✅ Live performance test complete!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user.")
    except Exception as e:
        print(f"\n\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()

