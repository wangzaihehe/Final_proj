#!/usr/bin/env python3
"""
Audio quality test script to diagnose speech recognition issues
"""

import os
import tempfile
import subprocess
import shutil
from pathlib import Path

def test_ffmpeg_installation():
    """Test FFmpeg installation"""
    print("🔧 Testing FFmpeg installation...")
    
    ffmpeg_path = shutil.which('ffmpeg') or '/opt/homebrew/bin/ffmpeg'
    print(f"FFmpeg path: {ffmpeg_path}")
    
    if not os.path.exists(ffmpeg_path):
        print("❌ FFmpeg not found!")
        return False
    
    # Test FFmpeg version
    try:
        result = subprocess.run([ffmpeg_path, "-version"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            version_line = result.stdout.split('\n')[0]
            print(f"✅ FFmpeg version: {version_line}")
            return True
        else:
            print("❌ FFmpeg test failed")
            return False
    except Exception as e:
        print(f"❌ FFmpeg test error: {e}")
        return False

def test_audio_filters():
    """Test audio filter configuration"""
    print("\n🎵 Testing audio filters...")
    
    ffmpeg_path = shutil.which('ffmpeg') or '/opt/homebrew/bin/ffmpeg'
    
    # Create a test audio file (1 second of silence)
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as test_file:
        test_input = test_file.name
    
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as test_file:
        test_output = test_file.name
    
    # Generate test audio using FFmpeg
    generate_cmd = [
        ffmpeg_path, "-y",
        "-f", "lavfi",
        "-i", "anullsrc=channel_layout=mono:sample_rate=16000",
        "-t", "1",
        test_input
    ]
    
    print(f"Generating test audio: {' '.join(generate_cmd)}")
    
    try:
        result = subprocess.run(generate_cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"❌ Audio generation failed: {result.stderr}")
            return False
        
        # Apply audio filters
        filter_cmd = [
            ffmpeg_path, "-y",
            "-i", test_input,
            "-acodec", "pcm_s16le",
            "-ar", "16000",
            "-ac", "1",
            "-af", "highpass=f=200,lowpass=f=3000,volume=1.5",
            test_output
        ]
        
        print(f"Applying audio filters: {' '.join(filter_cmd)}")
        
        result = subprocess.run(filter_cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Audio filters applied successfully")
            
            # Check file sizes
            input_size = os.path.getsize(test_input)
            output_size = os.path.getsize(test_output)
            print(f"Input size: {input_size} bytes")
            print(f"Output size: {output_size} bytes")
            
            return True
        else:
            print(f"❌ Audio filtering failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Audio test error: {e}")
        return False
    finally:
        # Clean up
        for file_path in [test_input, test_output]:
            if os.path.exists(file_path):
                os.unlink(file_path)

def test_whisper_configuration():
    """Test Whisper API configuration"""
    print("\n🎤 Testing Whisper configuration...")
    
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        print("❌ OPENAI_API_KEY not set")
        return False
    
    print("✅ OpenAI API key found")
    
    # Test with a simple audio file
    try:
        import openai
        
        client = openai.OpenAI(api_key=openai_api_key)
        
        # Create a simple test audio (1 second of silence)
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as test_file:
            test_audio_path = test_file.name
        
        # Generate test audio
        ffmpeg_path = shutil.which('ffmpeg') or '/opt/homebrew/bin/ffmpeg'
        generate_cmd = [
            ffmpeg_path, "-y",
            "-f", "lavfi",
            "-i", "anullsrc=channel_layout=mono:sample_rate=16000",
            "-t", "1",
            test_audio_path
        ]
        
        subprocess.run(generate_cmd, capture_output=True)
        
        # Test Whisper API
        with open(test_audio_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                language="zh",
                response_format="text",
                temperature=0.0
            )
        
        print(f"✅ Whisper test successful: '{transcript}'")
        return True
        
    except Exception as e:
        print(f"❌ Whisper test failed: {e}")
        return False
    finally:
        if 'test_audio_path' in locals() and os.path.exists(test_audio_path):
            os.unlink(test_audio_path)

def check_audio_sources():
    """Check potential audio sources"""
    print("\n🔍 Checking audio sources...")
    
    # Check if there are any audio processes
    try:
        result = subprocess.run(["ps", "aux"], capture_output=True, text=True)
        if result.returncode == 0:
            lines = result.stdout.split('\n')
            audio_processes = [line for line in lines if any(keyword in line.lower() 
                           for keyword in ['audio', 'speech', 'whisper', 'ffmpeg'])]
            
            if audio_processes:
                print("⚠️  Found audio-related processes:")
                for process in audio_processes[:5]:  # Show first 5
                    print(f"   {process}")
            else:
                print("✅ No conflicting audio processes found")
    except Exception as e:
        print(f"⚠️  Could not check processes: {e}")

def main():
    """Main test function"""
    print("🎯 Audio Quality Diagnostic Test")
    print("=" * 50)
    
    tests = [
        ("FFmpeg Installation", test_ffmpeg_installation),
        ("Audio Filters", test_audio_filters),
        ("Whisper Configuration", test_whisper_configuration),
        ("Audio Sources", check_audio_sources)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    print("\n📊 Test Results:")
    print("=" * 50)
    
    all_passed = True
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if not result:
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 All tests passed! Audio system should work correctly.")
    else:
        print("⚠️  Some tests failed. Check the issues above.")
        print("\n💡 Recommendations:")
        print("1. Ensure FFmpeg is properly installed")
        print("2. Check OpenAI API key configuration")
        print("3. Verify audio input source (microphone)")
        print("4. Test in a quiet environment")
        print("5. Speak clearly and at normal volume")

if __name__ == "__main__":
    main() 