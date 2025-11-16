#!/usr/bin/env python3
"""
Sync ChromaDB seekers to MongoDB

This script ensures that all seekers in ChromaDB also exist in MongoDB
with matching UUIDs. It creates missing seekers with reasonable defaults.
"""
import asyncio
import sys
from pathlib import Path
from uuid import UUID

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from backend.db.settings import (
    connect_to_mongodb,
    close_mongodb_connection,
    Seeker_Resume_collection,
    get_mongodb_client,
)
from backend.db.seeker_db_ops import SeekerCRUD
from backend.schemas.seeker import Seeker, Information, Address
from bson.binary import Binary, UuidRepresentation


async def create_seeker_with_uuid(seeker_uuid: str, first_name: str, last_name: str, 
                                   email: str, skills: list[str], education: str = "BS", 
                                   edu_focus: str = "Computer Science", 
                                   resume: str = "") -> Seeker | None:
    """Create a seeker in MongoDB with a specific UUID."""
    try:
        # Check if seeker already exists
        existing = await SeekerCRUD.get_seeker_by_uuid(seeker_uuid)
        if existing:
            print(f"  ✅ Seeker already exists in MongoDB: {first_name} {last_name}")
            return existing
        
        # Create seeker data
        seeker_data = {
            "information": {
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "phone": "+14155550100",
                "address": {
                    "street": "123 Test St",
                    "city": "San Francisco",
                    "state": "CA",
                    "zip_code": "94102"
                }
            },
            "password_hash": "test_password_hash_for_chroma_sync",
            "education_level": education,
            "edu_focus": edu_focus,
            "pay_range": [80000, 150000],
            "pay_unit": "Yearly",
            "key_skills": skills,
            "resume": resume if resume else f"Resume for {first_name} {last_name}",
            "seeker_identification": UUID(seeker_uuid)  # Set the specific UUID
        }
        
        # Create the seeker
        seeker = Seeker(**seeker_data)
        
        # Insert directly to MongoDB to preserve the UUID
        client = get_mongodb_client()
        if not client:
            print("  ❌ MongoDB client not available")
            return None
        
        db = client['job-portal']
        collection = db['seekers']
        
        # Convert the seeker to dict for insertion
        seeker_dict = seeker.model_dump(by_alias=True, exclude={'id'})
        
        # Convert UUID to BSON Binary
        uuid_obj = UUID(seeker_uuid)
        uuid_binary = Binary.from_uuid(uuid_obj, uuid_representation=UuidRepresentation.STANDARD)
        seeker_dict["seeker_identification"] = uuid_binary
        
        # Remove _id if it's None
        if "_id" in seeker_dict and seeker_dict["_id"] is None:
            del seeker_dict["_id"]
        
        # Insert
        result = await collection.insert_one(seeker_dict)
        print(f"  ✅ Created seeker in MongoDB: {first_name} {last_name} (UUID: {seeker_uuid})")
        
        # Retrieve and return
        return await SeekerCRUD.get_seeker_by_uuid(seeker_uuid)
        
    except Exception as e:
        print(f"  ❌ Error creating seeker: {e}")
        import traceback
        traceback.print_exc()
        return None


async def main():
    """Sync ChromaDB seekers to MongoDB."""
    print("=== Syncing ChromaDB Seekers to MongoDB ===\n")
    
    await connect_to_mongodb()
    
    try:
        # Get all seekers from ChromaDB
        print("1. Getting all seekers from ChromaDB...")
        all_seekers = Seeker_Resume_collection.get(include=["metadatas"])
        seeker_count = len(all_seekers["ids"])
        print(f"   Found {seeker_count} seekers in ChromaDB\n")
        
        # Check each seeker
        created_count = 0
        existing_count = 0
        
        for i, seeker_uuid in enumerate(all_seekers["ids"], 1):
            print(f"2. Checking seeker {i}/{seeker_count}: {seeker_uuid}")
            
            # Check if exists in MongoDB
            existing = await SeekerCRUD.get_seeker_by_uuid(seeker_uuid)
            
            if existing:
                print(f"  ✅ Already in MongoDB: {existing.information.first_name} {existing.information.last_name}")
                existing_count += 1
            else:
                print(f"  ⚠️  Not found in MongoDB, creating...")
                
                # Create with default data (in a real scenario, you'd pull this from ChromaDB metadata or other sources)
                metadata = all_seekers["metadatas"][i-1] if all_seekers.get("metadatas") else {}
                
                # Generate reasonable defaults
                first_name = f"TestSeeker{i}"
                last_name = "User"
                email = f"testseeker{i}.{seeker_uuid[:8]}@example.com"
                skills = ["Python", "JavaScript", "SQL"]
                education = "BS"
                edu_focus = "Computer Science"
                resume = f"Test seeker profile {i} for matching tests."
                
                result = await create_seeker_with_uuid(
                    seeker_uuid=seeker_uuid,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    skills=skills,
                    education=education,
                    edu_focus=edu_focus,
                    resume=resume
                )
                
                if result:
                    created_count += 1
            
            print()
        
        # Summary
        print("=" * 50)
        print(f"✅ Sync Complete!")
        print(f"   Total in ChromaDB: {seeker_count}")
        print(f"   Already in MongoDB: {existing_count}")
        print(f"   Newly created: {created_count}")
        print("=" * 50)
        
    except Exception as e:
        print(f"\n❌ Error during sync: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await close_mongodb_connection()


if __name__ == "__main__":
    asyncio.run(main())

