'use client'

import { useState, useEffect } from 'react'
import VoiceChat from '@/components/VoiceChat'
import Header from '@/components/Header'
import EmotionDisplay from '@/components/EmotionDisplay'
import ChatHistory from '@/components/ChatHistory'
import { Message, EmotionType } from '@/types/chat'

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([])
  const [currentEmotion, setCurrentEmotion] = useState<EmotionType | null>(null)
  const [isConnected, setIsConnected] = useState(false)
  const [isRecording, setIsRecording] = useState(false)

  const addMessage = (message: Message) => {
    setMessages(prev => [...prev, message])
  }

  const updateEmotion = (emotion: EmotionType) => {
    setCurrentEmotion(emotion)
  }

  const clearHistory = () => {
    setMessages([])
  }

  return (
    <main className="min-h-screen">
      <Header />
      
      <div className="container mx-auto px-4 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Left: Emotion Display */}
          <div className="lg:col-span-1">
            <EmotionDisplay 
              emotion={currentEmotion}
              isRecording={isRecording}
              isConnected={isConnected}
            />
          </div>
          
          {/* Center: Voice Chat */}
          <div className="lg:col-span-1">
            <VoiceChat
              onMessage={addMessage}
              onEmotionUpdate={updateEmotion}
              onConnectionChange={setIsConnected}
              onRecordingChange={setIsRecording}
            />
          </div>
          
          {/* Right: Chat History */}
          <div className="lg:col-span-1">
            <ChatHistory 
              messages={messages}
              onClear={clearHistory}
            />
          </div>
        </div>
      </div>
    </main>
  )
} 