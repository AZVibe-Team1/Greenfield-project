#!/usr/bin/env python3
"""
Quick verification script to test that AI-powered matching is working.
Run this to verify the fixes are in place and working correctly.

Usage:
    uv run python scripts/verify_matching_works.py
"""
import asyncio
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.db.settings import connect_to_mongodb, close_mongodb_connection
from backend.db.employer_db_ops import EmployerCRUD
from backend.ai.chains.candidate_matching_service import CandidateMatchingService


async def main():
    """Quick verification test."""
    print("=" * 60)
    print("AI-Powered Matching Verification")
    print("=" * 60)
    
    await connect_to_mongodb()
    
    try:
        # 1. Find employer
        print("\n1. Looking up test employer...")
        employer = await EmployerCRUD.get_employer_by_email("alice.johnson@testtech.com")
        
        if not employer:
            print("   ❌ Test employer not found!")
            print("   Please create employer account first.")
            return
        
        print(f"   ✅ Found: {employer.company_information.company_name}")
        
        # 2. Check for jobs
        if not employer.open_jobs:
            print("\n   ⚠️  No open jobs found for this employer")
            return
        
        print(f"   ✅ Found {len(employer.open_jobs)} open job(s)")
        
        # 3. Test matching
        job = employer.open_jobs[0]
        print(f"\n2. Testing matching for job: {job.job_title}")
        
        service = CandidateMatchingService()
        recommendations = await service.match_job_to_candidates(
            job_id=str(job.job_id),
            employer_id=str(employer.id),
            n_results=10,
            min_score=0.0
        )
        
        # 4. Display results
        if not recommendations:
            print("\n   ❌ FAILED: No recommendations returned")
            print("   The matching is still not working correctly.")
            return
        
        print(f"\n   ✅ SUCCESS: Got {len(recommendations)} candidate recommendations!")
        print("\n" + "=" * 60)
        print("Top 3 Candidates:")
        print("=" * 60)
        
        for i, rec in enumerate(recommendations[:3], 1):
            print(f"\n{i}. {rec['first_name']} {rec['last_name']}")
            print(f"   Match Score: {rec['match_score']:.1f}/100")
            print(f"   Key Skills: {', '.join(rec['key_skills'][:4])}")
            print(f"   Education: {rec['education_level']} in {rec['edu_focus']}")
        
        print("\n" + "=" * 60)
        print("✅ AI-Powered Matching is WORKING CORRECTLY!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error during verification: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await close_mongodb_connection()


if __name__ == "__main__":
    asyncio.run(main())

