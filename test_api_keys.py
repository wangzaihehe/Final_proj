#!/usr/bin/env python3
"""
Test script to check API key configuration
"""

import os
from dotenv import load_dotenv

def test_api_keys():
    """Test if API keys are properly configured"""
    print("🔑 Testing API Key Configuration")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv()
    
    # Check OpenAI API key
    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key and openai_key != "your_openai_api_key_here":
        print("✅ OpenAI API key found")
        print(f"   Key: {openai_key[:10]}...{openai_key[-4:]}")
    else:
        print("❌ OpenAI API key not configured")
        print("   Please set OPENAI_API_KEY in .env file")
    
    # Check ElevenLabs API key
    elevenlabs_key = os.getenv("ELEVENLABS_API_KEY")
    if elevenlabs_key and elevenlabs_key != "your_elevenlabs_api_key_here":
        print("✅ ElevenLabs API key found")
        print(f"   Key: {elevenlabs_key[:10]}...{elevenlabs_key[-4:]}")
    else:
        print("❌ ElevenLabs API key not configured")
        print("   Please set ELEVENLABS_API_KEY in .env file")
    
    # Check other environment variables
    host = os.getenv("HOST", "0.0.0.0")
    port = os.getenv("PORT", "8000")
    debug = os.getenv("DEBUG", "True")
    
    print(f"✅ Server config: {host}:{port} (debug={debug})")
    
    # Summary
    print("\n📊 Configuration Summary:")
    print("=" * 50)
    
    if (openai_key and openai_key != "your_openai_api_key_here" and 
        elevenlabs_key and elevenlabs_key != "your_elevenlabs_api_key_here"):
        print("🎉 All API keys are configured!")
        print("✅ Speech recognition should work properly")
        print("✅ Text-to-speech should work properly")
        return True
    else:
        print("⚠️  Some API keys are missing")
        print("❌ Speech recognition may not work properly")
        print("❌ Text-to-speech may not work properly")
        print("\n💡 To fix this:")
        print("1. Edit the .env file in the backend directory")
        print("2. Replace 'your_openai_api_key_here' with your actual OpenAI API key")
        print("3. Replace 'your_elevenlabs_api_key_here' with your actual ElevenLabs API key")
        print("4. Restart the backend server")
        return False

if __name__ == "__main__":
    test_api_keys() 