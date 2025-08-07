import openai
import os
from typing import List, Optional
import json
from datetime import datetime

from app.models.chat_models import ChatResponse, EmotionType, ChatMessage

class ChatService:
    """Chat service, integrating OpenAI API"""
    
    def __init__(self):
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.conversation_history: List[ChatMessage] = []
        self.max_history = 10  # Maximum history count
        
        # Emotion-adaptive prompt templates
        self.emotion_prompts = {
            EmotionType.HAPPY: "The user is in a good mood now. Please respond with a positive and cheerful tone, and you can share some interesting thoughts or suggestions.",
            EmotionType.SAD: "The user is feeling down now. Please respond with a warm and comforting tone, providing emotional support and encouragement.",
            EmotionType.ANGRY: "The user is emotionally agitated now. Please respond with a calm and understanding tone, helping the user to calm down.",
            EmotionType.FEAR: "The user is feeling scared or anxious now. Please respond with a safe and reassuring tone, providing a sense of security.",
            EmotionType.SURPRISE: "The user is feeling surprised now. Please respond with an equally surprised but positive tone, sharing this excitement.",
            EmotionType.DISGUST: "The user is feeling disgusted now. Please respond with an understanding and sympathetic tone, avoiding aggravating negative emotions.",
            EmotionType.NEUTRAL: "The user is emotionally calm now. Please respond with a natural and friendly tone, maintaining the flow of conversation.",
            EmotionType.EXCITED: "The user is very excited now. Please respond with an equally excited and enthusiastic tone, sharing this positive emotion."
        }
    
    def _get_emotion_context(self, emotion: EmotionType, confidence: float) -> str:
        """Generate context prompt based on emotion"""
        base_prompt = self.emotion_prompts.get(emotion, "")
        confidence_level = "very" if confidence > 0.8 else "quite" if confidence > 0.6 else "slightly"
        
        return f"Detected that the user is {confidence_level} {self._get_emotion_description(emotion)}. {base_prompt}"
    
    def _get_emotion_description(self, emotion: EmotionType) -> str:
        """Get English description of emotion"""
        descriptions = {
            EmotionType.HAPPY: "happy",
            EmotionType.SAD: "sad",
            EmotionType.ANGRY: "angry",
            EmotionType.FEAR: "fearful",
            EmotionType.SURPRISE: "surprised",
            EmotionType.DISGUST: "disgusted",
            EmotionType.NEUTRAL: "calm",
            EmotionType.EXCITED: "excited"
        }
        return descriptions.get(emotion, "calm")
    
    def _build_system_prompt(self, emotion: EmotionType, confidence: float) -> str:
        """Build system prompt"""
        emotion_context = self._get_emotion_context(emotion, confidence)
        
        return f"""You are an emotionally intelligent AI assistant, specifically designed to provide emotional support and meaningful conversations.

{emotion_context}

Please follow these principles:
1. Adjust your response style and tone based on the user's emotional state
2. Provide sincere and empathetic responses
3. Avoid overly formal or mechanical language
4. Offer emotional support and encouragement when appropriate
5. Maintain naturalness and coherence in conversation
6. Respond in English, unless the user uses another language

Remember: Your goal is to be an understanding and supportive friend, not just an information provider."""
    
    def _build_conversation_context(self) -> str:
        """Build conversation history context"""
        if not self.conversation_history:
            return ""
        
        context = "Recent conversation history:\n"
        for i, msg in enumerate(self.conversation_history[-5:], 1):  # Only take the last 5
            context += f"{i}. User: {msg.text}\n"
            if msg.emotion:
                context += f"   Emotion: {self._get_emotion_description(msg.emotion)} (confidence: {msg.confidence:.2f})\n"
        
        return context
    
    def _add_to_history(self, text: str, emotion: Optional[EmotionType] = None, confidence: Optional[float] = None):
        """Add message to history"""
        message = ChatMessage(
            text=text,
            emotion=emotion,
            confidence=confidence,
            timestamp=datetime.now().isoformat()
        )
        
        self.conversation_history.append(message)
        
        # Keep history within limits
        if len(self.conversation_history) > self.max_history:
            self.conversation_history = self.conversation_history[-self.max_history:]
    
    async def generate_response(self, user_text: str, emotion: EmotionType, confidence: float) -> ChatResponse:
        """Generate chat response"""
        try:
            # Add user message to history
            self._add_to_history(user_text, emotion, confidence)
            
            # Build complete prompt
            system_prompt = self._build_system_prompt(emotion, confidence)
            conversation_context = self._build_conversation_context()
            
            full_prompt = f"{system_prompt}\n\n{conversation_context}\n\nUser: {user_text}\n\nAssistant:"
            
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"{conversation_context}\n\nUser: {user_text}"}
                ],
                max_tokens=200,
                temperature=0.7,
                presence_penalty=0.1,
                frequency_penalty=0.1
            )
            
            assistant_message = response.choices[0].message.content.strip()
            
            # Add assistant response to history
            self._add_to_history(assistant_message)
            
            return ChatResponse(
                message=assistant_message,
                emotion_adapted=True,
                suggested_emotion=emotion,
                confidence=confidence
            )
            
        except Exception as e:
            print(f"Failed to generate response: {e}")
            # Return fallback response
            fallback_response = self._generate_fallback_response(user_text, emotion)
            return ChatResponse(
                message=fallback_response,
                emotion_adapted=False,
                confidence=0.5
            )
    
    def _generate_fallback_response(self, user_text: str, emotion: EmotionType) -> str:
        """Generate fallback response"""
        fallback_responses = {
            EmotionType.HAPPY: [
                "It sounds like you're in a good mood! Is there anything happy you'd like to share?",
                "I'm glad to see you so happy! Keep up this good mood!",
                "Your good mood is contagious! What interesting things are happening?"
            ],
            EmotionType.SAD: [
                "I sense you might be feeling a bit down. Would you like to talk? I'm here to listen.",
                "Everyone has low moments, and that's completely normal. Would you like to share with me?",
                "I understand how you're feeling right now. If you need anything, I'm always here to support you."
            ],
            EmotionType.ANGRY: [
                "I sense you're a bit angry. Take a deep breath and tell me slowly, okay?",
                "Anger is a normal emotion, but we can work together to calm down.",
                "I understand your feelings. Let's find a solution together."
            ],
            EmotionType.FEAR: [
                "I sense you're a bit scared. It's okay, I'm here with you.",
                "Fear is a natural response. Would you like to tell me what happened?",
                "I'll always be here to support you. You're not alone."
            ],
            EmotionType.SURPRISE: [
                "Wow! That sounds really surprising! Can you tell me what happened?",
                "That's really unexpected! Your reaction is adorable.",
                "I didn't expect something like this to happen!"
            ],
            EmotionType.DISGUST: [
                "I understand your feelings. Some things are indeed uncomfortable.",
                "Your reaction is normal. When we encounter things we don't like, this is how we feel.",
                "I understand your thoughts. Everyone has their own preferences."
            ],
            EmotionType.NEUTRAL: [
                "I'm here to listen. What would you like to talk about?",
                "Okay, I understand. Is there anything else you'd like to say?",
                "Hmm, I understand what you mean."
            ],
            EmotionType.EXCITED: [
                "Wow! You seem really excited! What good things happened?",
                "Your excitement is contagious! Can you share with me?",
                "That's amazing! Your enthusiasm makes me happy too!"
            ]
        }
        
        import random
        responses = fallback_responses.get(emotion, ["I understand your feelings."])
        return random.choice(responses)
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history.clear()
    
    def get_conversation_summary(self) -> dict:
        """Get conversation summary"""
        if not self.conversation_history:
            return {"message": "No conversation history"}
        
        emotions = [msg.emotion for msg in self.conversation_history if msg.emotion]
        avg_confidence = sum(msg.confidence or 0 for msg in self.conversation_history) / len(self.conversation_history)
        
        return {
            "total_messages": len(self.conversation_history),
            "dominant_emotion": max(set(emotions), key=emotions.count) if emotions else None,
            "average_confidence": avg_confidence,
            "last_message_time": self.conversation_history[-1].timestamp if self.conversation_history else None
        } 