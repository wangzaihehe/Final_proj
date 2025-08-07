export enum EmotionType {
  HAPPY = "happy",
  SAD = "sad",
  ANGRY = "angry",
  FEAR = "fear",
  SURPRISE = "surprise",
  DISGUST = "disgust",
  NEUTRAL = "neutral",
  EXCITED = "excited"
}

export interface Message {
  id: string
  text: string
  sender: 'user' | 'assistant'
  emotion?: EmotionType
  confidence?: number
  timestamp: string
  audioUrl?: string
}

export interface EmotionData {
  emotion: EmotionType
  confidence: number
  features?: Record<string, any>
}

export interface ChatResponse {
  type: 'chat_response'
  user_text: string
  assistant_text: string
  emotion: EmotionType
  emotion_confidence: number
  audio_data: string // base64 encoded audio
}

export interface VoiceChatState {
  isConnected: boolean
  isRecording: boolean
  isProcessing: boolean
  currentEmotion: EmotionType | null
  error: string | null
} 