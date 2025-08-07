from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
from dotenv import load_dotenv
import json
import base64
from datetime import datetime
import random
import asyncio

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Emotion-Aware Voice Chat Assistant",
    description="AI-powered emotional intelligence voice chat application",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Try to import real services
try:
    from app.services.emotion_service import EmotionService
    from app.services.chat_service import ChatService
    from app.services.voice_service import VoiceService
    from app.models.chat_models import ChatMessage, EmotionResponse, EmotionType
    SERVICES_AVAILABLE = True
    print("Real service modules imported successfully")
except ImportError as e:
    print(f"Real service import failed: {e}")
    SERVICES_AVAILABLE = False

# Mock service classes (as fallback)
class MockEmotionService:
    async def analyze_emotion(self, audio_data: bytes):
        emotions = ["happy", "sad", "angry", "fear", "surprise", "disgust", "neutral", "excited"]
        emotion = random.choice(emotions)
        return type('EmotionResponse', (), {
            'emotion': emotion,
            'confidence': random.uniform(0.6, 0.9),
            'features': {"method": "mock"}
        })()

class MockChatService:
    async def generate_response(self, text: str, emotion, confidence):
        responses = {
            "happy": ["It sounds like you're in a good mood!", "I'm glad to see you so happy!", "Your good mood is contagious!"],
            "sad": ["I sense you might be feeling a bit down, would you like to talk?", "Everyone has low moments, and that's completely normal."],
            "angry": ["I sense you're a bit angry, take a deep breath okay?", "Anger is a normal emotion, we can work together to calm down."],
            "fear": ["I sense you're a bit scared, it's okay, I'm here with you.", "Fear is a natural response, would you like to tell me what happened?"],
            "surprise": ["Wow! That sounds really surprising!", "That's really unexpected! Your reaction is adorable."],
            "disgust": ["I understand your feelings, some things are indeed uncomfortable.", "Your reaction is normal, when we encounter things we don't like, this is how we feel."],
            "neutral": ["I'm here to listen, what would you like to talk about?", "Okay, I understand. Is there anything else you'd like to say?"],
            "excited": ["Wow! You seem really excited!", "Your excitement is contagious! Can you share with me?"]
        }
        
        response_list = responses.get(emotion, ["I understand your feelings."])
        return type('ChatResponse', (), {
            'message': random.choice(response_list),
            'emotion_adapted': True,
            'suggested_emotion': emotion,
            'confidence': confidence
        })()

class MockVoiceService:
    async def speech_to_text(self, audio_data: bytes):
        mock_texts = [
            "Hello, how's the weather today?",
            "I feel a bit tired",
            "I'm very happy today",
            "I want to chat with you",
            "Thank you for your help"
        ]
        return random.choice(mock_texts)
    
    async def text_to_speech(self, text: str):
        return b"mock_audio_data"

# Initialize services
if SERVICES_AVAILABLE:
    try:
        print("Forcing use of real API services")
        emotion_service = EmotionService()
        chat_service = ChatService()
        voice_service = VoiceService()
        print("✅ Real API services initialized successfully")
    except Exception as e:
        print(f"❌ Real service initialization failed: {e}")
        print("Using mock services as fallback")
        emotion_service = MockEmotionService()
        chat_service = MockChatService()
        voice_service = MockVoiceService()
else:
    print("❌ Service modules unavailable, using mock services")
    emotion_service = MockEmotionService()
    chat_service = MockChatService()
    voice_service = MockVoiceService()

# Active connections list
active_connections = []

@app.get("/")
async def root():
    return {"message": "Emotion-Aware Voice Chat Assistant API"}

@app.get("/health")
async def health_check():
    # Check current service types
    try:
        from app.services.emotion_service import EmotionService
        from app.services.chat_service import ChatService
        from app.services.voice_service import VoiceService
        
        emotion_type = "real" if isinstance(emotion_service, EmotionService) else "mock"
        chat_type = "real" if isinstance(chat_service, ChatService) else "mock"
        voice_type = "real" if isinstance(voice_service, VoiceService) else "mock"
    except ImportError:
        emotion_type = "mock"
        chat_type = "mock"
        voice_type = "mock"
    
    return {
        "status": "healthy",
        "services": {
            "emotion_recognition": emotion_type,
            "chat_service": chat_type, 
            "voice_service": voice_type
        },
        "active_connections": len(active_connections),
        "api_keys_configured": {
            "openai": bool(os.getenv("OPENAI_API_KEY") and os.getenv("OPENAI_API_KEY") != "your_openai_api_key_here"),
            "elevenlabs": bool(os.getenv("ELEVENLABS_API_KEY") and os.getenv("ELEVENLABS_API_KEY") != "your_elevenlabs_api_key_here")
        }
    }

@app.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    print(f"WebSocket connection established, current connections: {len(active_connections)}")
    
    try:
        while True:
            # Check connection status
            if websocket.client_state.value > 2:  # Connection closed
                print("Connection closed detected")
                break
                
            try:
                # Set receive timeout
                data = await asyncio.wait_for(websocket.receive(), timeout=30.0)
                
                # Process received data
                if data["type"] == "websocket.receive":
                    if "text" in data:
                        # Process text data
                        text_data = data["text"]
                        print(f"Received text data: {text_data[:100]}...")
                        
                        try:
                            json_data = json.loads(text_data)
                            if 'audio' in json_data:
                                audio_data = base64.b64decode(json_data['audio'])
                                print(f"Decoded audio data from JSON: {len(audio_data)} bytes")
                            else:
                                audio_data = b"mock_audio_data"
                                print("Using mock audio data")
                        except json.JSONDecodeError:
                            audio_data = b"mock_audio_data"
                            print("JSON parsing failed, using mock audio data")
                            
                    elif "bytes" in data:
                        # Process binary data
                        audio_data = data["bytes"]
                        print(f"Received binary data: {len(audio_data)} bytes")
                    else:
                        print("Unknown data type")
                        continue
                        
                    # Process audio data
                    await process_audio_data(websocket, audio_data)
                    
                elif data["type"] == "websocket.disconnect":
                    print("Received disconnect message")
                    break
                    
            except asyncio.TimeoutError:
                print("Data receive timeout, sending heartbeat")
                try:
                    await websocket.send_json({
                        "type": "heartbeat",
                        "timestamp": datetime.now().isoformat()
                    })
                except:
                    print("Failed to send heartbeat, connection may be broken")
                    break
                    
            except Exception as e:
                print(f"Error processing data: {e}")
                # Send error response
                try:
                    await websocket.send_json({
                        "type": "error",
                        "message": "Processing failed, please retry",
                        "timestamp": datetime.now().isoformat()
                    })
                except:
                    print("Failed to send error response")
                    break
                    
    except WebSocketDisconnect:
        print("WebSocket connection normally disconnected")
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        if websocket in active_connections:
            active_connections.remove(websocket)
        print(f"WebSocket connection cleaned up, current connections: {len(active_connections)}")

async def process_audio_data(websocket: WebSocket, audio_data: bytes):
    """Process audio data"""
    try:
        print(f"Starting to process audio data, length: {len(audio_data)} bytes")
        
        # Process audio and recognize emotion
        emotion_result = await emotion_service.analyze_emotion(audio_data)
        print(f"Recognized emotion: {emotion_result.emotion} (confidence: {emotion_result.confidence})")
        
        # Speech to text
        text = await voice_service.speech_to_text(audio_data)
        print(f"Speech to text: {text}")
        
        # Generate chat response
        chat_response = await chat_service.generate_response(
            text, 
            emotion_result.emotion,
            emotion_result.confidence
        )
        print(f"Generated response: {chat_response.message}")
        
        # Text to speech
        audio_response = await voice_service.text_to_speech(chat_response.message)
        print(f"Generated audio response, length: {len(audio_response) if isinstance(audio_response, bytes) else 0} bytes")
        
        # Send response
        response = {
            "type": "chat_response",
            "user_text": text,
            "assistant_text": chat_response.message,
            "emotion": emotion_result.emotion,
            "emotion_confidence": emotion_result.confidence,
            "audio_data": base64.b64encode(audio_response).decode() if isinstance(audio_response, bytes) else "",
            "timestamp": datetime.now().isoformat()
        }
        
        await websocket.send_json(response)
        print("Response sent")
        
    except Exception as e:
        print(f"Error processing audio data: {e}")
        import traceback
        traceback.print_exc()
        
        # Send error response
        try:
            await websocket.send_json({
                "type": "error",
                "message": "Audio processing failed, please retry",
                "timestamp": datetime.now().isoformat()
            })
        except:
            print("Failed to send error response")

@app.post("/api/emotion")
async def analyze_emotion_endpoint(audio_data: bytes):
    """Analyze emotion in audio"""
    try:
        result = await emotion_service.analyze_emotion(audio_data)
        return result
    except Exception as e:
        return {"error": str(e)}

@app.post("/api/chat")
async def chat_endpoint(message: dict):
    """Chat endpoint"""
    try:
        text = message.get("text", "")
        emotion = message.get("emotion", "neutral")
        confidence = message.get("confidence", 0.5)
        
        response = await chat_service.generate_response(text, emotion, confidence)
        return response
    except Exception as e:
        return {"error": str(e)}

@app.post("/api/tts")
async def text_to_speech_endpoint(text: str):
    """Text to speech endpoint"""
    try:
        audio_data = await voice_service.text_to_speech(text)
        return {"audio_data": base64.b64encode(audio_data).decode()}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 