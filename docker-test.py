#!/usr/bin/env python3
"""
Simple test script to validate the application can start correctly
Run this before building the Docker image
"""

import os
import sys
import subprocess
import importlib.util

def check_dependencies():
    """Check if all required dependencies are available"""
    required_packages = [
        'fastapi',
        'uvicorn',
        'google.generativeai',
        'dotenv',
        'aiohttp',
        'requests'
    ]
    
    missing = []
    for package in required_packages:
        # Handle packages with different import names
        import_name = package
        if package == 'google.generativeai':
            import_name = 'google.generativeai'
        elif package == 'dotenv':
            import_name = 'dotenv'
            
        try:
            __import__(import_name)
            print(f"✅ {package} - OK")
        except ImportError:
            missing.append(package)
            print(f"❌ {package} - Missing")
    
    return missing

def test_app_import():
    """Test if the main app can be imported"""
    try:
        from main import app
        print("✅ FastAPI app import - OK")
        return True
    except Exception as e:
        print(f"❌ FastAPI app import - Failed: {e}")
        return False

def test_health_endpoint():
    """Test if the health endpoint exists"""
    try:
        from main import app
        from fastapi.testclient import TestClient
        
        client = TestClient(app)
        response = client.get("/health")
        if response.status_code == 200:
            print("✅ Health endpoint - OK")
            return True
        else:
            print(f"❌ Health endpoint - Failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health endpoint test - Failed: {e}")
        return False

def main():
    print("🚀 Testing Viraa Care Application for Docker Deployment")
    print("=" * 60)
    
    # Check Python version
    python_version = sys.version_info
    print(f"🐍 Python version: {python_version.major}.{python_version.minor}.{python_version.micro}")
    if python_version < (3, 8):
        print("❌ Python 3.8+ required")
        return False
    else:
        print("✅ Python version - OK")
    
    print("\n📦 Checking Dependencies:")
    missing_deps = check_dependencies()
    
    if missing_deps:
        print(f"\n❌ Missing dependencies: {', '.join(missing_deps)}")
        print("Install them with: pip install -r requirements.txt")
        return False
    
    print("\n🔧 Testing Application:")
    app_ok = test_app_import()
    
    print("\n🏥 Testing Health Endpoint:")
    health_ok = test_health_endpoint()
    
    print("\n" + "=" * 60)
    if app_ok and health_ok and not missing_deps:
        print("🎉 All tests passed! Ready for Docker deployment.")
        print("\nNext steps:")
        print("1. Start Docker Desktop")
        print("2. Run: docker build -t viraa-care .")
        print("3. Run: docker run -p 8080:8080 -e GOOGLE_API_KEY='your-key' viraa-care")
        return True
    else:
        print("❌ Some tests failed. Please fix the issues before Docker deployment.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 