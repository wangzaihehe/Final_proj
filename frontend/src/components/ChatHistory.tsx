'use client'

import { Message, EmotionType } from '@/types/chat'
import { User, Bot, Trash2, Clock } from 'lucide-react'

interface ChatHistoryProps {
  messages: Message[]
  onClear: () => void
}

const emotionColors = {
  [EmotionType.HAPPY]: 'bg-yellow-100 text-yellow-800',
  [EmotionType.SAD]: 'bg-blue-100 text-blue-800',
  [EmotionType.ANGRY]: 'bg-red-100 text-red-800',
  [EmotionType.FEAR]: 'bg-purple-100 text-purple-800',
  [EmotionType.SURPRISE]: 'bg-orange-100 text-orange-800',
  [EmotionType.DISGUST]: 'bg-green-100 text-green-800',
  [EmotionType.NEUTRAL]: 'bg-gray-100 text-gray-800',
  [EmotionType.EXCITED]: 'bg-pink-100 text-pink-800',
}

const emotionLabels = {
  [EmotionType.HAPPY]: 'Happy',
  [EmotionType.SAD]: 'Sad',
  [EmotionType.ANGRY]: 'Angry',
  [EmotionType.FEAR]: 'Fearful',
  [EmotionType.SURPRISE]: 'Surprised',
  [EmotionType.DISGUST]: 'Disgusted',
  [EmotionType.NEUTRAL]: 'Calm',
  [EmotionType.EXCITED]: 'Excited',
}

export default function ChatHistory({ messages, onClear }: ChatHistoryProps) {
  const formatTime = (timestamp: string) => {
    const date = new Date(timestamp)
    return date.toLocaleTimeString('en-US', { 
      hour: '2-digit', 
      minute: '2-digit' 
    })
  }

  return (
    <div className="bg-white rounded-2xl shadow-lg p-6 card-hover">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h2 className="text-2xl font-bold text-gray-800">Chat History</h2>
          <p className="text-gray-600">View your conversation records</p>
        </div>
        {messages.length > 0 && (
          <button
            onClick={onClear}
            className="p-2 text-red-500 hover:bg-red-50 rounded-lg transition-colors"
            title="Clear History"
          >
            <Trash2 className="w-5 h-5" />
          </button>
        )}
      </div>
      
      <div className="space-y-4 max-h-96 overflow-y-auto">
        {messages.length === 0 ? (
          <div className="text-center py-8 text-gray-500">
            <Bot className="w-12 h-12 mx-auto mb-4 text-gray-300" />
            <p>No conversation records</p>
            <p className="text-sm">Start voice chat to see conversation history here</p>
          </div>
        ) : (
          messages.map((message) => (
            <div
              key={message.id}
              className={`flex items-start space-x-3 ${
                message.sender === 'user' ? 'flex-row-reverse space-x-reverse' : ''
              }`}
            >
              {/* Avatar */}
              <div className={`
                w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0
                ${message.sender === 'user' 
                  ? 'bg-blue-500 text-white' 
                  : 'bg-gray-500 text-white'
                }
              `}>
                {message.sender === 'user' ? (
                  <User className="w-4 h-4" />
                ) : (
                  <Bot className="w-4 h-4" />
                )}
              </div>
              
              {/* Message Content */}
              <div className={`
                flex-1 max-w-xs lg:max-w-sm
                ${message.sender === 'user' ? 'text-right' : 'text-left'}
              `}>
                <div className={`
                  inline-block p-3 rounded-lg
                  ${message.sender === 'user' 
                    ? 'bg-blue-500 text-white' 
                    : 'bg-gray-100 text-gray-800'
                  }
                `}>
                  <p className="text-sm">{message.text}</p>
                </div>
                
                {/* Emotion Label */}
                {message.emotion && (
                  <div className="mt-2">
                    <span className={`
                      inline-block px-2 py-1 rounded-full text-xs font-medium
                      ${emotionColors[message.emotion]}
                    `}>
                      {emotionLabels[message.emotion]}
                      {message.confidence && (
                        <span className="ml-1">
                          ({Math.round(message.confidence * 100)}%)
                        </span>
                      )}
                    </span>
                  </div>
                )}
                
                {/* Timestamp */}
                <div className={`
                  mt-1 text-xs text-gray-500 flex items-center
                  ${message.sender === 'user' ? 'justify-end' : 'justify-start'}
                `}>
                  <Clock className="w-3 h-3 mr-1" />
                  {formatTime(message.timestamp)}
                </div>
              </div>
            </div>
          ))
        )}
      </div>
      
      {/* Statistics */}
      {messages.length > 0 && (
        <div className="mt-6 pt-4 border-t border-gray-200">
          <div className="flex justify-between text-sm text-gray-600">
            <span>Total Messages: {messages.length}</span>
            <span>User Messages: {messages.filter(m => m.sender === 'user').length}</span>
            <span>Assistant Messages: {messages.filter(m => m.sender === 'assistant').length}</span>
          </div>
        </div>
      )}
    </div>
  )
} 