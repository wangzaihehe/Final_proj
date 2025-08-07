'use client'

import { EmotionType } from '@/types/chat'
import { Heart, Frown, Angry, AlertTriangle, Meh, Smile, Zap } from 'lucide-react'

interface EmotionDisplayProps {
  emotion: EmotionType | null
  isRecording: boolean
  isConnected: boolean
}

const emotionConfig = {
  [EmotionType.HAPPY]: {
    icon: Smile,
    color: 'text-yellow-500',
    bgColor: 'bg-yellow-100',
    borderColor: 'border-yellow-300',
    label: 'Happy',
    description: 'You look very happy!'
  },
  [EmotionType.SAD]: {
    icon: Frown,
    color: 'text-blue-500',
    bgColor: 'bg-blue-100',
    borderColor: 'border-blue-300',
    label: 'Sad',
    description: 'I sense you might be feeling down...'
  },
  [EmotionType.ANGRY]: {
    icon: Angry,
    color: 'text-red-500',
    bgColor: 'bg-red-100',
    borderColor: 'border-red-300',
    label: 'Angry',
    description: 'You seem a bit angry...'
  },
  [EmotionType.FEAR]: {
    icon: AlertTriangle,
    color: 'text-purple-500',
    bgColor: 'bg-purple-100',
    borderColor: 'border-purple-300',
    label: 'Fearful',
    description: 'You look a bit scared...'
  },
  [EmotionType.SURPRISE]: {
    icon: AlertTriangle,
    color: 'text-orange-500',
    bgColor: 'bg-orange-100',
    borderColor: 'border-orange-300',
    label: 'Surprised',
    description: 'You seem very surprised!'
  },
  [EmotionType.DISGUST]: {
    icon: Meh,
    color: 'text-green-500',
    bgColor: 'bg-green-100',
    borderColor: 'border-green-300',
    label: 'Disgusted',
    description: 'You look a bit disgusted...'
  },
  [EmotionType.NEUTRAL]: {
    icon: Heart,
    color: 'text-gray-500',
    bgColor: 'bg-gray-100',
    borderColor: 'border-gray-300',
    label: 'Calm',
    description: 'You look very calm'
  },
  [EmotionType.EXCITED]: {
    icon: Zap,
    color: 'text-pink-500',
    bgColor: 'bg-pink-100',
    borderColor: 'border-pink-300',
    label: 'Excited',
    description: 'You look very excited!'
  }
}

export default function EmotionDisplay({ emotion, isRecording, isConnected }: EmotionDisplayProps) {
  const config = emotion ? emotionConfig[emotion] : null
  const IconComponent = config?.icon || Heart

  return (
    <div className="bg-white rounded-2xl shadow-lg p-6 card-hover">
      <div className="text-center mb-6">
        <h2 className="text-2xl font-bold text-gray-800 mb-2">Emotion Recognition</h2>
        <p className="text-gray-600">Real-time analysis of your voice emotions</p>
      </div>
      
      <div className="flex flex-col items-center space-y-6">
        {/* Connection Status */}
        <div className="flex items-center space-x-2">
          <div className={`w-3 h-3 rounded-full ${isConnected ? 'bg-green-500' : 'bg-red-500'}`}></div>
          <span className="text-sm text-gray-600">
            {isConnected ? 'Emotion recognition enabled' : 'Emotion recognition disconnected'}
          </span>
        </div>
        
        {/* Emotion Display */}
        <div className={`
          w-32 h-32 rounded-full flex items-center justify-center
          ${config ? config.bgColor : 'bg-gray-100'}
          ${config ? config.borderColor : 'border-gray-300'}
          border-4 transition-all duration-500
          ${isRecording ? 'animate-pulse scale-110' : ''}
        `}>
          <IconComponent 
            className={`w-16 h-16 ${config ? config.color : 'text-gray-400'}`}
          />
        </div>
        
        {/* Emotion Label */}
        <div className="text-center">
          <h3 className="text-xl font-semibold text-gray-800">
            {config ? config.label : 'Waiting for voice input...'}
          </h3>
          <p className="text-gray-600 mt-1">
            {config ? config.description : 'Please start speaking to recognize emotions'}
          </p>
        </div>
        
        {/* Recording Status */}
        {isRecording && (
          <div className="flex items-center space-x-2 text-red-600">
            <div className="w-2 h-2 bg-red-500 rounded-full animate-pulse"></div>
            <span className="text-sm">Analyzing emotions...</span>
          </div>
        )}
        
        {/* Emotion Description */}
        <div className="bg-gray-50 rounded-lg p-4 w-full">
          <h3 className="font-semibold text-gray-800 mb-2">Emotion Description</h3>
          <div className="text-sm text-gray-600 space-y-2">
            <p>The system can recognize the following 8 basic emotions:</p>
            <div className="grid grid-cols-2 gap-2 text-xs">
              <div className="flex items-center space-x-1">
                <div className="w-2 h-2 bg-yellow-400 rounded-full"></div>
                <span>Happy</span>
              </div>
              <div className="flex items-center space-x-1">
                <div className="w-2 h-2 bg-blue-400 rounded-full"></div>
                <span>Sad</span>
              </div>
              <div className="flex items-center space-x-1">
                <div className="w-2 h-2 bg-red-400 rounded-full"></div>
                <span>Angry</span>
              </div>
              <div className="flex items-center space-x-1">
                <div className="w-2 h-2 bg-purple-400 rounded-full"></div>
                <span>Fearful</span>
              </div>
              <div className="flex items-center space-x-1">
                <div className="w-2 h-2 bg-orange-400 rounded-full"></div>
                <span>Surprised</span>
              </div>
              <div className="flex items-center space-x-1">
                <div className="w-2 h-2 bg-green-400 rounded-full"></div>
                <span>Disgusted</span>
              </div>
              <div className="flex items-center space-x-1">
                <div className="w-2 h-2 bg-gray-400 rounded-full"></div>
                <span>Calm</span>
              </div>
              <div className="flex items-center space-x-1">
                <div className="w-2 h-2 bg-pink-400 rounded-full"></div>
                <span>Excited</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
} 