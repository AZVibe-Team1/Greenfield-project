#!/usr/bin/env python3
"""Test script to diagnose server startup issues"""
import sys
import os
from pathlib import Path

# Get project root directory (parent of scripts directory)
project_root = Path(__file__).parent.parent

print("="*60)
print("TESTING SERVER STARTUP")
print("="*60)

# Test 1: Python environment
print("\n[1] Python Environment:")
print(f"   Python: {sys.version}")
print(f"   Executable: {sys.executable}")

# Test 2: Import FastAPI
print("\n[2] Testing FastAPI import...")
try:
    import fastapi
    print(f"   ✓ FastAPI version: {fastapi.__version__}")
except Exception as e:
    print(f"   ✗ Failed: {e}")
    sys.exit(1)

# Test 3: Import uvicorn
print("\n[3] Testing uvicorn import...")
try:
    import uvicorn
    print(f"   ✓ Uvicorn imported successfully")
except Exception as e:
    print(f"   ✗ Failed: {e}")
    sys.exit(1)

# Test 4: Environment variables
print("\n[4] Checking environment variables...")
from dotenv import load_dotenv
# Load .env from project root
load_dotenv(dotenv_path=project_root / ".env")

required_vars = ["MONGO_DB_USER", "MONGO_DB_PASSWORD", "MONGO_DB_URL"]
for var in required_vars:
    value = os.getenv(var)
    if value:
        if "PASSWORD" in var or "SECRET" in var:
            print(f"   ✓ {var}: ***hidden***")
        else:
            print(f"   ✓ {var}: {value[:50]}...")
    else:
        print(f"   ✗ {var}: NOT SET")

# Test 5: Try importing main app
print("\n[5] Testing main app import...")
try:
    # Add project root to path for imports
    sys.path.insert(0, str(project_root))
    from backend.main import app
    print(f"   ✓ App imported successfully")
    print(f"   App title: {app.title}")
except Exception as e:
    print(f"   ✗ Failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "="*60)
print("ALL TESTS PASSED! Server should be able to start.")
print("="*60)

