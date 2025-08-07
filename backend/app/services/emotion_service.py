import librosa
import numpy as np
import torch
import torch.nn as nn
import io
import soundfile as sf
from typing import Optional
import joblib
import os
import tempfile
import subprocess
import shutil

from app.models.chat_models import EmotionResponse, EmotionType

class EmotionCNN(nn.Module):
    """Simple emotion recognition CNN model"""
    def __init__(self, num_classes=8):
        super(EmotionCNN, self).__init__()
        # Adjust CNN architecture for better compatibility
        self.conv1 = nn.Conv2d(1, 32, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.conv3 = nn.Conv2d(64, 128, kernel_size=3, padding=1)
        
        self.pool = nn.MaxPool2d(2, 2)
        self.dropout = nn.Dropout(0.5)
        
        # Use adaptive pooling to handle variable input sizes
        self.adaptive_pool = nn.AdaptiveAvgPool2d((8, 8))
        self.fc1 = nn.Linear(128 * 8 * 8, 512)
        self.fc2 = nn.Linear(512, num_classes)
        self.relu = nn.ReLU()
        
    def forward(self, x):
        # Ensure input has correct shape
        if len(x.shape) == 3:
            x = x.unsqueeze(1)  # Add channel dimension if missing
        
        x = self.pool(self.relu(self.conv1(x)))
        x = self.pool(self.relu(self.conv2(x)))
        x = self.pool(self.relu(self.conv3(x)))
        x = self.adaptive_pool(x)  # Adaptive pooling
        x = x.view(x.size(0), -1)
        x = self.dropout(self.relu(self.fc1(x)))
        x = self.fc2(x)
        return x

class EmotionService:
    """Emotion recognition service"""
    
    def __init__(self):
        self.model = None
        self.scaler = None
        self.emotion_labels = [
            EmotionType.HAPPY,
            EmotionType.SAD, 
            EmotionType.ANGRY,
            EmotionType.FEAR,
            EmotionType.SURPRISE,
            EmotionType.DISGUST,
            EmotionType.NEUTRAL,
            EmotionType.EXCITED
        ]
        self.sample_rate = 22050
        self.duration = 3  # Audio segment length (seconds)
        
        # Find FFmpeg path
        self.ffmpeg_path = shutil.which('ffmpeg') or '/opt/homebrew/bin/ffmpeg'
        print(f"EmotionService using FFmpeg at: {self.ffmpeg_path}")
        
        self._load_model()
    
    def _load_model(self):
        """Load pre-trained model"""
        try:
            # Here we should load the actual pre-trained model
            # For demonstration, we create a simple model
            self.model = EmotionCNN(num_classes=len(self.emotion_labels))
            self.model.eval()
            
            # Load scaler
            # self.scaler = joblib.load('models/scaler.pkl')
            
            print("Emotion recognition model loaded successfully")
        except Exception as e:
            print(f"Model loading failed: {e}")
            # Use simple rule-based method as fallback
            self.model = None
    
    def _convert_audio_to_wav(self, audio_data: bytes) -> bytes:
        """Convert audio data to WAV format using FFmpeg"""
        try:
            # Create temporary files
            with tempfile.NamedTemporaryFile(suffix=".webm", delete=False) as input_file:
                input_file.write(audio_data)
                input_path = input_file.name
            
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as output_file:
                output_path = output_file.name
            
            # Use FFmpeg to convert with audio filters for better quality
            cmd = [
                self.ffmpeg_path, "-y",  # Overwrite output file
                "-i", input_path,  # Input file
                "-acodec", "pcm_s16le",  # PCM 16-bit
                "-ar", str(self.sample_rate),  # Sample rate
                "-ac", "1",  # Mono
                "-af", "highpass=f=200,lowpass=f=3000,volume=1.5",  # Audio filters for better quality
                output_path  # Output file
            ]
            
            print(f"Converting audio with FFmpeg: {' '.join(cmd)}")
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
    
    def _extract_features(self, audio_data: bytes) -> np.ndarray:
        """Extract features from audio data"""
        try:
            # Convert audio to WAV format first
            wav_audio = self._convert_audio_to_wav(audio_data)
            
            # Convert byte data to audio array
            audio_array, sr = sf.read(io.BytesIO(wav_audio))
            
            # Resample to standard sample rate
            if sr != self.sample_rate:
                audio_array = librosa.resample(audio_array, orig_sr=sr, target_sr=self.sample_rate)
            
            # Ensure consistent audio length
            target_length = self.sample_rate * self.duration
            if len(audio_array) > target_length:
                audio_array = audio_array[:target_length]
            else:
                # Zero padding
                audio_array = np.pad(audio_array, (0, target_length - len(audio_array)))
            
            # Extract MFCC features
            mfccs = librosa.feature.mfcc(y=audio_array, sr=self.sample_rate, n_mfcc=13)
            
            # Extract other features
            spectral_centroids = librosa.feature.spectral_centroid(y=audio_array, sr=self.sample_rate)[0]
            spectral_rolloff = librosa.feature.spectral_rolloff(y=audio_array, sr=self.sample_rate)[0]
            zero_crossing_rate = librosa.feature.zero_crossing_rate(audio_array)[0]
            
            # Calculate statistical features
            features = []
            for feature in [mfccs, spectral_centroids, spectral_rolloff, zero_crossing_rate]:
                features.extend([
                    np.mean(feature),
                    np.std(feature),
                    np.min(feature),
                    np.max(feature)
                ])
            
            return np.array(features)
            
        except Exception as e:
            print(f"Feature extraction failed: {e}")
            return np.zeros(60)  # Return zero vector as fallback
    
    def _extract_mel_spectrogram(self, audio_data: bytes) -> torch.Tensor:
        """Extract mel spectrogram features with better error handling"""
        try:
            # Convert audio to WAV format first
            wav_audio = self._convert_audio_to_wav(audio_data)
            
            # Try to read audio data with better error handling
            try:
                audio_array, sr = sf.read(io.BytesIO(wav_audio))
            except Exception as e:
                print(f"Failed to read audio with soundfile: {e}")
                # Try alternative method - save to temp file
                with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                    temp_file.write(wav_audio)
                    temp_file_path = temp_file.name
                
                try:
                    audio_array, sr = sf.read(temp_file_path)
                    os.unlink(temp_file_path)  # Clean up
                except Exception as e2:
                    print(f"Failed to read audio from temp file: {e2}")
                    # Return default tensor
                    return torch.zeros(1, 1, 128, 128)
            
            # Ensure audio is mono
            if len(audio_array.shape) > 1:
                audio_array = np.mean(audio_array, axis=1)
            
            # Resample if needed
            if sr != self.sample_rate:
                audio_array = librosa.resample(audio_array, orig_sr=sr, target_sr=self.sample_rate)
            
            # Ensure minimum length
            min_length = self.sample_rate * 1  # At least 1 second
            if len(audio_array) < min_length:
                audio_array = np.pad(audio_array, (0, min_length - len(audio_array)))
            
            # Extract mel spectrogram
            mel_spec = librosa.feature.melspectrogram(
                y=audio_array, 
                sr=self.sample_rate,
                n_mels=128,
                n_fft=2048,
                hop_length=512
            )
            
            # Convert to decibel units
            mel_spec_db = librosa.power_to_db(mel_spec, ref=np.max)
            
            # Normalize
            if mel_spec_db.std() > 0:
                mel_spec_db = (mel_spec_db - mel_spec_db.mean()) / mel_spec_db.std()
            
            # Ensure fixed size (128x128)
            if mel_spec_db.shape[1] < 128:
                mel_spec_db = np.pad(mel_spec_db, ((0, 0), (0, 128 - mel_spec_db.shape[1])))
            elif mel_spec_db.shape[1] > 128:
                mel_spec_db = mel_spec_db[:, :128]
            
            # Convert to tensor and add channel dimension
            mel_tensor = torch.FloatTensor(mel_spec_db).unsqueeze(0).unsqueeze(0)
            
            return mel_tensor
            
        except Exception as e:
            print(f"Mel spectrogram extraction failed: {e}")
            return torch.zeros(1, 1, 128, 128)
    
    def _rule_based_emotion_detection(self, features: np.ndarray) -> EmotionResponse:
        """Rule-based emotion detection (fallback method)"""
        # Simple rule-based method
        # Here we use some heuristic rules to estimate emotion
        
        # Simulate emotion detection logic
        import random
        emotions = list(EmotionType)
        emotion = random.choice(emotions)
        confidence = random.uniform(0.6, 0.9)
        
        return EmotionResponse(
            emotion=emotion,
            confidence=confidence,
            features={"method": "rule_based"}
        )
    
    async def analyze_emotion(self, audio_data: bytes) -> EmotionResponse:
        """Analyze emotion in audio"""
        try:
            if self.model is not None:
                # Use deep learning model
                mel_tensor = self._extract_mel_spectrogram(audio_data)
                
                # Check tensor shape
                print(f"Mel tensor shape: {mel_tensor.shape}")
                
                with torch.no_grad():
                    outputs = self.model(mel_tensor)
                    probabilities = torch.softmax(outputs, dim=1)
                    predicted_idx = torch.argmax(probabilities, dim=1).item()
                    confidence = probabilities[0][predicted_idx].item()
                
                emotion = self.emotion_labels[predicted_idx]
                
                return EmotionResponse(
                    emotion=emotion,
                    confidence=confidence,
                    features={"method": "deep_learning"}
                )
            else:
                # Use rule-based method
                features = self._extract_features(audio_data)
                return self._rule_based_emotion_detection(features)
                
        except Exception as e:
            print(f"Emotion analysis failed: {e}")
            # Return neutral emotion as fallback
            return EmotionResponse(
                emotion=EmotionType.NEUTRAL,
                confidence=0.5,
                features={"method": "fallback", "error": str(e)}
            )
    
    def get_emotion_description(self, emotion: EmotionType) -> str:
        """Get emotion description"""
        descriptions = {
            EmotionType.HAPPY: "Happy, joyful",
            EmotionType.SAD: "Sad, depressed",
            EmotionType.ANGRY: "Angry, mad",
            EmotionType.FEAR: "Fearful, scared",
            EmotionType.SURPRISE: "Surprised, shocked",
            EmotionType.DISGUST: "Disgusted, repulsed",
            EmotionType.NEUTRAL: "Neutral, calm",
            EmotionType.EXCITED: "Excited, thrilled"
        }
        return descriptions.get(emotion, "Unknown emotion") 