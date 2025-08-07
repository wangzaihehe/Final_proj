import openai
import requests
import os
import io
import base64
import tempfile
import soundfile as sf
import numpy as np
from typing import Optional
import json
import subprocess
import shutil

class VoiceService:
    """Voice service, integrating Whisper and ElevenLabs"""
    
    def __init__(self):
        self.openai_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.elevenlabs_api_key = os.getenv("ELEVENLABS_API_KEY")
        self.elevenlabs_base_url = "https://api.elevenlabs.io/v1"
        
        # Find FFmpeg path
        self.ffmpeg_path = shutil.which('ffmpeg') or '/opt/homebrew/bin/ffmpeg'
        print(f"Using FFmpeg at: {self.ffmpeg_path}")
        
        # ElevenLabs voice configuration
        self.voice_settings = {
            "stability": 0.5,
            "similarity_boost": 0.75,
            "style": 0.0,
            "use_speaker_boost": True
        }
        
        # Default voice ID (English female voice)
        self.default_voice_id = "21m00Tcm4TlvDq8ikWAM"  # Rachel voice
        
        # Emotion-based voice settings
        self.emotion_voice_settings = {
            "happy": {"stability": 0.6, "similarity_boost": 0.8, "style": 0.3},
            "sad": {"stability": 0.7, "similarity_boost": 0.6, "style": -0.2},
            "angry": {"stability": 0.4, "similarity_boost": 0.9, "style": 0.5},
            "fear": {"stability": 0.8, "similarity_boost": 0.5, "style": -0.3},
            "surprise": {"stability": 0.5, "similarity_boost": 0.8, "style": 0.4},
            "disgust": {"stability": 0.6, "similarity_boost": 0.7, "style": -0.1},
            "neutral": {"stability": 0.5, "similarity_boost": 0.75, "style": 0.0},
            "excited": {"stability": 0.4, "similarity_boost": 0.8, "style": 0.4}
        }
    
    def _convert_audio_format(self, audio_data: bytes, target_format: str = "wav") -> bytes:
        """Convert audio data to target format using FFmpeg"""
        try:
            # Create temporary files
            with tempfile.NamedTemporaryFile(suffix=".webm", delete=False) as input_file:
                input_file.write(audio_data)
                input_path = input_file.name
            
            with tempfile.NamedTemporaryFile(suffix=f".{target_format}", delete=False) as output_file:
                output_path = output_file.name
            
            # Use FFmpeg to convert with audio filters for better quality
            cmd = [
                self.ffmpeg_path, "-y",  # Overwrite output file
                "-i", input_path,  # Input file
                "-acodec", "pcm_s16le",  # PCM 16-bit
                "-ar", "16000",  # Sample rate 16kHz
                "-ac", "1",  # Mono
                "-af", "highpass=f=200,lowpass=f=3000,volume=1.5",  # Audio filters for better quality
                output_path  # Output file
            ]
            
            print(f"Running FFmpeg command: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                # Read converted audio
                with open(output_path, "rb") as f:
                    converted_audio = f.read()
                
                print(f"Audio conversion successful: {len(converted_audio)} bytes")
                
                # Clean up temporary files
                os.unlink(input_path)
                os.unlink(output_path)
                
                return converted_audio
            else:
                print(f"FFmpeg conversion failed: {result.stderr}")
                # Clean up and return original
                os.unlink(input_path)
                os.unlink(output_path)
                return audio_data
                
        except Exception as e:
            print(f"Audio conversion failed: {e}")
            return audio_data
    
    async def speech_to_text(self, audio_data: bytes) -> str:
        """Use Whisper to convert speech to text"""
        try:
            # Convert audio to WAV format for better compatibility
            wav_audio = self._convert_audio_format(audio_data, "wav")
            
            # Create temporary file
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                temp_file.write(wav_audio)
                temp_file_path = temp_file.name
            
            print(f"Created temporary WAV file: {temp_file_path} ({len(wav_audio)} bytes)")
            
            # Use OpenAI Whisper API with optimized settings
            with open(temp_file_path, "rb") as audio_file:
                transcript = self.openai_client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    language="zh",  # Use Chinese for better accuracy
                    response_format="text",
                    temperature=0.0,  # Lower temperature for more consistent results
                    prompt="This is a conversation in Chinese and English."  # Help with context
                )
            
            # Clean up temporary file
            os.unlink(temp_file_path)
            
            result = transcript.strip()
            print(f"Speech to text result: '{result}'")
            return result
            
        except Exception as e:
            print(f"Speech to text failed: {e}")
            return "Sorry, I didn't catch that. Could you please repeat?"
    
    async def text_to_speech(self, text: str, emotion: Optional[str] = None) -> bytes:
        """Use ElevenLabs to convert text to speech"""
        try:
            if not self.elevenlabs_api_key:
                print("ElevenLabs API key not configured, using fallback TTS")
                return self._fallback_tts(text)
            
            # Adjust voice settings based on emotion
            voice_settings = self.voice_settings.copy()
            if emotion and emotion in self.emotion_voice_settings:
                voice_settings.update(self.emotion_voice_settings[emotion])
            
            # Call ElevenLabs API
            url = f"{self.elevenlabs_base_url}/text-to-speech/{self.default_voice_id}"
            
            headers = {
                "Accept": "audio/mpeg",
                "Content-Type": "application/json",
                "xi-api-key": self.elevenlabs_api_key
            }
            
            data = {
                "text": text,
                "model_id": "eleven_multilingual_v2",
                "voice_settings": voice_settings
            }
            
            response = requests.post(url, json=data, headers=headers)
            
            if response.status_code == 200:
                return response.content
            else:
                print(f"ElevenLabs API error: {response.status_code}")
                return self._fallback_tts(text)
                
        except Exception as e:
            print(f"Text to speech failed: {e}")
            return self._fallback_tts(text)
    
    def _fallback_tts(self, text: str) -> bytes:
        """Fallback TTS method (using system TTS or return empty audio)"""
        try:
            # Here we can implement a simple fallback TTS
            # For demonstration, we return simple audio data
            # In actual applications, you can use pyttsx3 or other local TTS libraries
            
            # Create simple audio data (silence)
            sample_rate = 22050
            duration = 1.0  # 1 second
            samples = int(sample_rate * duration)
            
            # Generate simple sine wave
            frequency = 440  # A4 note
            t = np.linspace(0, duration, samples, False)
            audio_data = np.sin(2 * np.pi * frequency * t) * 0.1
            
            # Convert to WAV format
            with io.BytesIO() as audio_buffer:
                sf.write(audio_buffer, audio_data, sample_rate, format='WAV')
                return audio_buffer.getvalue()
                
        except Exception as e:
            print(f"Fallback TTS failed: {e}")
            # Return empty bytes
            return b""
    
    def get_available_voices(self) -> list:
        """Get available voice list"""
        try:
            if not self.elevenlabs_api_key:
                return []
            
            url = f"{self.elevenlabs_base_url}/voices"
            headers = {"xi-api-key": self.elevenlabs_api_key}
            
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                voices = response.json().get("voices", [])
                return [
                    {
                        "id": voice["voice_id"],
                        "name": voice["name"],
                        "language": voice.get("labels", {}).get("language", "unknown")
                    }
                    for voice in voices
                ]
            else:
                return []
                
        except Exception as e:
            print(f"Failed to get voice list: {e}")
            return []
    
    def set_voice(self, voice_id: str):
        """Set voice ID"""
        self.default_voice_id = voice_id
    
    def set_voice_settings(self, settings: dict):
        """Set voice parameters"""
        self.voice_settings.update(settings)
    
    def get_audio_duration(self, audio_data: bytes) -> float:
        """Get audio duration"""
        try:
            with io.BytesIO(audio_data) as audio_buffer:
                audio_array, sample_rate = sf.read(audio_buffer)
                return len(audio_array) / sample_rate
        except Exception as e:
            print(f"Failed to get audio duration: {e}")
            return 0.0
    
    def convert_audio_format(self, audio_data: bytes, target_format: str = "wav") -> bytes:
        """Convert audio format"""
        try:
            with io.BytesIO(audio_data) as input_buffer:
                audio_array, sample_rate = sf.read(input_buffer)
                
                with io.BytesIO() as output_buffer:
                    sf.write(output_buffer, audio_array, sample_rate, format=target_format.upper())
                    return output_buffer.getvalue()
                    
        except Exception as e:
            print(f"Audio format conversion failed: {e}")
            return audio_data
    
    def normalize_audio(self, audio_data: bytes) -> bytes:
        """Audio normalization"""
        try:
            with io.BytesIO(audio_data) as audio_buffer:
                audio_array, sample_rate = sf.read(audio_buffer)
                
                # Normalize volume
                if len(audio_array) > 0:
                    max_val = np.max(np.abs(audio_array))
                    if max_val > 0:
                        audio_array = audio_array / max_val * 0.8
                
                with io.BytesIO() as output_buffer:
                    sf.write(output_buffer, audio_array, sample_rate)
                    return output_buffer.getvalue()
                    
        except Exception as e:
            print(f"Audio normalization failed: {e}")
            return audio_data 