#!/usr/bin/env python3
"""
Test script to verify CNN model fixes
"""

import asyncio
import sys
import os
import numpy as np

# Add backend to path
sys.path.append('backend')

async def test_cnn_model():
    """Test the CNN model with mock audio data"""
    try:
        # Import after adding to path
        sys.path.insert(0, 'backend')
        from app.services.emotion_service import EmotionService
        
        print("🧪 Testing CNN model fixes...")
        
        # Initialize emotion service
        emotion_service = EmotionService()
        
        # Create mock audio data (1 second of sine wave)
        sample_rate = 22050
        duration = 1.0
        samples = int(sample_rate * duration)
        
        # Generate different frequency sine waves for different emotions
        test_cases = [
            ("happy", 440),    # A4 - bright sound
            ("sad", 220),      # A3 - lower sound
            ("angry", 880),    # A5 - higher sound
            ("neutral", 330),  # E4 - middle sound
        ]
        
        for emotion_name, frequency in test_cases:
            print(f"\n--- Testing {emotion_name} emotion ---")
            
            # Generate audio data
            t = np.linspace(0, duration, samples, False)
            audio_data = np.sin(2 * np.pi * frequency * t) * 0.3
            
            # Convert to WAV format
            import soundfile as sf
            import io
            
            with io.BytesIO() as audio_buffer:
                sf.write(audio_buffer, audio_data, sample_rate, format='WAV')
                audio_bytes = audio_buffer.getvalue()
            
            # Test emotion analysis
            try:
                result = await emotion_service.analyze_emotion(audio_bytes)
                print(f"✅ {emotion_name}: {result.emotion} (confidence: {result.confidence:.2f})")
                print(f"   Method: {result.features.get('method', 'unknown')}")
            except Exception as e:
                print(f"❌ {emotion_name} failed: {e}")
        
        print("\n🎉 CNN model test completed!")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
    except Exception as e:
        print(f"❌ Test failed: {e}")

async def test_audio_processing():
    """Test audio processing pipeline"""
    try:
        from app.services.voice_service import VoiceService
        
        print("\n🎵 Testing audio processing pipeline...")
        
        # Initialize voice service
        voice_service = VoiceService()
        
        # Create mock audio data
        sample_rate = 22050
        duration = 2.0
        samples = int(sample_rate * duration)
        
        t = np.linspace(0, duration, samples, False)
        audio_data = np.sin(2 * np.pi * 440 * t) * 0.3
        
        # Convert to WAV format
        import soundfile as sf
        import io
        
        with io.BytesIO() as audio_buffer:
            sf.write(audio_buffer, audio_data, sample_rate, format='WAV')
            audio_bytes = audio_buffer.getvalue()
        
        # Test speech to text
        try:
            text = await voice_service.speech_to_text(audio_bytes)
            print(f"✅ Speech to text: {text}")
        except Exception as e:
            print(f"❌ Speech to text failed: {e}")
        
        # Test text to speech
        try:
            audio_response = await voice_service.text_to_speech("Hello, this is a test.")
            print(f"✅ Text to speech: {len(audio_response)} bytes")
        except Exception as e:
            print(f"❌ Text to speech failed: {e}")
        
        print("\n🎉 Audio processing test completed!")
        
    except Exception as e:
        print(f"❌ Audio processing test failed: {e}")

async def main():
    """Main test function"""
    print("🔍 Testing CNN model and audio processing fixes...")
    
    # Test CNN model
    await test_cnn_model()
    
    # Test audio processing
    await test_audio_processing()
    
    print("\n✅ All tests completed!")

if __name__ == "__main__":
    asyncio.run(main()) 