#!/usr/bin/env python3
"""
Test script to check the setup of the Emotion-Aware Voice Chat Assistant project
"""

import os
import sys
import subprocess
import importlib.util
from pathlib import Path

def check_python_version():
    """Check Python version"""
    print("🐍 Checking Python version...")
    version = sys.version_info
    print(f"   Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("   ❌ Python 3.8+ is required")
        return False
    else:
        print("   ✅ Python version is compatible")
        return True

def check_dependencies():
    """Check required dependencies"""
    print("\n📦 Checking dependencies...")
    
    required_packages = [
        'fastapi',
        'uvicorn',
        'websockets',
        'openai',
        'requests',
        'python-dotenv',
        'pydantic',
        'librosa',
        'torch',
        'numpy',
        'soundfile',
        'joblib'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            importlib.import_module(package.replace('-', '_'))
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ❌ {package} - Not installed")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n   📋 Missing packages: {', '.join(missing_packages)}")
        print("   💡 Run: pip install -r requirements.txt")
        return False
    else:
        print("   ✅ All dependencies are installed")
        return True

def check_environment_variables():
    """Check environment variables"""
    print("\n🔧 Checking environment variables...")
    
    env_file = Path('.env')
    if env_file.exists():
        print("   ✅ .env file found")
        
        # Load and check key variables
        from dotenv import load_dotenv
        load_dotenv()
        
        openai_key = os.getenv('OPENAI_API_KEY')
        elevenlabs_key = os.getenv('ELEVENLABS_API_KEY')
        
        if openai_key and openai_key != 'your_openai_api_key_here':
            print("   ✅ OPENAI_API_KEY is configured")
        else:
            print("   ⚠️  OPENAI_API_KEY is not configured or using default value")
        
        if elevenlabs_key and elevenlabs_key != 'your_elevenlabs_api_key_here':
            print("   ✅ ELEVENLABS_API_KEY is configured")
        else:
            print("   ⚠️  ELEVENLABS_API_KEY is not configured or using default value")
    else:
        print("   ❌ .env file not found")
        print("   💡 Copy env.example to .env and configure your API keys")
        return False
    
    return True

def check_project_structure():
    """Check project structure"""
    print("\n📁 Checking project structure...")
    
    required_files = [
        'backend/main.py',
        'backend/requirements.txt',
        'backend/app/models/chat_models.py',
        'backend/app/services/emotion_service.py',
        'backend/app/services/chat_service.py',
        'backend/app/services/voice_service.py',
        'frontend/package.json',
        'frontend/src/app/page.tsx',
        'frontend/src/components/VoiceChat.tsx',
        'frontend/src/components/EmotionDisplay.tsx',
        'frontend/src/components/ChatHistory.tsx'
    ]
    
    missing_files = []
    
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"   ✅ {file_path}")
        else:
            print(f"   ❌ {file_path} - Not found")
            missing_files.append(file_path)
    
    if missing_files:
        print(f"\n   📋 Missing files: {len(missing_files)}")
        return False
    else:
        print("   ✅ All required files are present")
        return True

def test_backend_startup():
    """Test if backend can start"""
    print("\n🚀 Testing backend startup...")
    
    try:
        # Try to import main modules
        sys.path.append('backend')
        
        from main import app
        print("   ✅ FastAPI app can be imported")
        
        # Check if services can be initialized
        try:
            from app.services.emotion_service import EmotionService
            from app.services.chat_service import ChatService
            from app.services.voice_service import VoiceService
            print("   ✅ Service modules can be imported")
        except ImportError as e:
            print(f"   ⚠️  Some service modules cannot be imported: {e}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Backend startup test failed: {e}")
        return False

def main():
    """Main test function"""
    print("🔍 Checking Emotion-Aware Voice Chat Assistant project setup...")
    
    tests = [
        check_python_version,
        check_dependencies,
        check_environment_variables,
        check_project_structure,
        test_backend_startup
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"   ❌ Test failed with error: {e}")
            results.append(False)
    
    print("\n" + "="*50)
    print("📊 Test Results Summary:")
    
    passed = sum(results)
    total = len(results)
    
    print(f"   ✅ Passed: {passed}/{total}")
    print(f"   ❌ Failed: {total - passed}/{total}")
    
    if passed == total:
        print("\n🎉 All tests passed! The project is ready to run.")
        print("💡 Next steps:")
        print("   1. Start backend: cd backend && python main.py")
        print("   2. Start frontend: cd frontend && npm run dev")
    else:
        print("\n⚠️  Some tests failed. Please fix the issues above before running the project.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 