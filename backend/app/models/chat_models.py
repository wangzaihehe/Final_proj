from pydantic import BaseModel
from typing import Optional, List
from enum import Enum

class EmotionType(str, Enum):
    """Emotion type enumeration"""
    HAPPY = "happy"
    SAD = "sad"
    ANGRY = "angry"
    FEAR = "fear"
    SURPRISE = "surprise"
    DISGUST = "disgust"
    NEUTRAL = "neutral"
    EXCITED = "excited"

class ChatMessage(BaseModel):
    """Chat message model"""
    text: str
    emotion: Optional[EmotionType] = None
    confidence: Optional[float] = None
    timestamp: Optional[str] = None

class EmotionResponse(BaseModel):
    """Emotion recognition response model"""
    emotion: EmotionType
    confidence: float
    features: Optional[dict] = None

class ChatResponse(BaseModel):
    """Chat response model"""
    message: str
    emotion_adapted: bool
    suggested_emotion: Optional[EmotionType] = None
    confidence: float

class VoiceResponse(BaseModel):
    """Voice response model"""
    audio_data: bytes
    text: str
    duration: Optional[float] = None

class ConversationSession(BaseModel):
    """Conversation session model"""
    session_id: str
    messages: List[ChatMessage] = []
    current_emotion: Optional[EmotionType] = None
    emotion_history: List[EmotionResponse] = []
    created_at: str
    updated_at: str

class SystemStatus(BaseModel):
    """System status model"""
    emotion_service: bool
    chat_service: bool
    voice_service: bool
    model_loaded: bool
    memory_usage: Optional[float] = None 