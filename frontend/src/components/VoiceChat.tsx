'use client'

import { useState, useEffect, useRef } from 'react'
import { Mic, MicOff, Volume2, Loader2 } from 'lucide-react'
import { Message, EmotionType, ChatResponse } from '@/types/chat'
import toast from 'react-hot-toast'

interface VoiceChatProps {
  onMessage: (message: Message) => void
  onEmotionUpdate: (emotion: EmotionType) => void
  onConnectionChange: (connected: boolean) => void
  onRecordingChange: (recording: boolean) => void
}

export default function VoiceChat({
  onMessage,
  onEmotionUpdate,
  onConnectionChange,
  onRecordingChange
}: VoiceChatProps) {
  const [isRecording, setIsRecording] = useState(false)
  const [isProcessing, setIsProcessing] = useState(false)
  const [isConnected, setIsConnected] = useState(false)
  const [mediaRecorder, setMediaRecorder] = useState<MediaRecorder | null>(null)
  const [audioChunks, setAudioChunks] = useState<Blob[]>([])
  
  const wsRef = useRef<WebSocket | null>(null)
  const streamRef = useRef<MediaStream | null>(null)

  useEffect(() => {
    connectWebSocket()
    return () => {
      if (wsRef.current) {
        wsRef.current.close()
      }
      if (streamRef.current) {
        streamRef.current.getTracks().forEach(track => track.stop())
      }
    }
  }, [])

  const connectWebSocket = () => {
    const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL || 'ws://localhost:8000'
    const ws = new WebSocket(`${backendUrl.replace('http', 'ws')}/ws/chat`)
    
    ws.onopen = () => {
      console.log('WebSocket connection established')
      setIsConnected(true)
      onConnectionChange(true)
      toast.success('Connected to server')
    }
    
    ws.onmessage = async (event) => {
      try {
        const data: ChatResponse = JSON.parse(event.data)
        
        // Add user message
        const userMessage: Message = {
          id: Date.now().toString(),
          text: data.user_text,
          sender: 'user',
          emotion: data.emotion,
          confidence: data.emotion_confidence,
          timestamp: new Date().toISOString()
        }
        onMessage(userMessage)
        
        // Update emotion
        onEmotionUpdate(data.emotion)
        
        // Add assistant message
        const assistantMessage: Message = {
          id: (Date.now() + 1).toString(),
          text: data.assistant_text,
          sender: 'assistant',
          timestamp: new Date().toISOString()
        }
        onMessage(assistantMessage)
        
        // Play audio response
        if (data.audio_data) {
          playAudioResponse(data.audio_data)
        }
        
        setIsProcessing(false)
        
      } catch (error) {
        console.error('Failed to process WebSocket message:', error)
        toast.error('Failed to process message')
        setIsProcessing(false)
      }
    }
    
    ws.onclose = () => {
      console.log('WebSocket connection closed')
      setIsConnected(false)
      onConnectionChange(false)
      toast.error('Connection disconnected')
    }
    
    ws.onerror = (error) => {
      console.error('WebSocket error:', error)
      toast.error('Connection error')
    }
    
    wsRef.current = ws
  }

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
      streamRef.current = stream
      
      const recorder = new MediaRecorder(stream, {
        mimeType: 'audio/webm;codecs=opus'
      })
      
      console.log('MediaRecorder MIME type:', recorder.mimeType)
      console.log('MediaRecorder state:', recorder.state)
      
      const chunks: Blob[] = []
      
      recorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          chunks.push(event.data)
        }
      }
      
      recorder.onstop = async () => {
        const audioBlob = new Blob(chunks, { type: 'audio/webm' })
        console.log('Recording stopped, audio blob size:', audioBlob.size, 'bytes')
        console.log('Audio blob type:', audioBlob.type)
        await sendAudioData(audioBlob)
      }
      
      recorder.start()
      setMediaRecorder(recorder)
      setAudioChunks(chunks)
      setIsRecording(true)
      onRecordingChange(true)
      
      toast.success('Recording started')
      
    } catch (error) {
      console.error('Failed to start recording:', error)
      toast.error('Cannot access microphone')
    }
  }

  const stopRecording = () => {
    if (mediaRecorder && mediaRecorder.state === 'recording') {
      mediaRecorder.stop()
      setIsRecording(false)
      onRecordingChange(false)
      setIsProcessing(true)
      
      if (streamRef.current) {
        streamRef.current.getTracks().forEach(track => track.stop())
      }
      
      toast.success('Recording stopped, processing...')
    }
  }

  const sendAudioData = async (audioBlob: Blob) => {
    if (!wsRef.current || wsRef.current.readyState !== WebSocket.OPEN) {
      toast.error('Connection disconnected, please reconnect')
      return
    }
    
    try {
      const arrayBuffer = await audioBlob.arrayBuffer()
      console.log('Sending audio data, size:', arrayBuffer.byteLength, 'bytes')
      wsRef.current.send(arrayBuffer)
      console.log('Audio data sent')
    } catch (error) {
      console.error('Failed to send audio data:', error)
      toast.error('Failed to send audio')
      setIsProcessing(false)
    }
  }

  const playAudioResponse = (audioData: string) => {
    try {
      const audio = new Audio(`data:audio/mpeg;base64,${audioData}`)
      audio.play().catch(error => {
        console.error('Failed to play audio:', error)
      })
    } catch (error) {
      console.error('Failed to create audio object:', error)
    }
  }

  const handleToggleRecording = () => {
    if (isRecording) {
      stopRecording()
    } else {
      startRecording()
    }
  }

  return (
    <div className="bg-white rounded-2xl shadow-lg p-6 card-hover">
      <div className="text-center mb-6">
        <h2 className="text-2xl font-bold text-gray-800 mb-2">Voice Chat</h2>
        <p className="text-gray-600">Click the microphone to start voice chat</p>
      </div>
      
      <div className="flex flex-col items-center space-y-6">
        {/* Connection Status */}
        <div className="flex items-center space-x-2">
          <div className={`w-3 h-3 rounded-full ${isConnected ? 'bg-green-500' : 'bg-red-500'}`}></div>
          <span className="text-sm text-gray-600">
            {isConnected ? 'Connected' : 'Disconnected'}
          </span>
        </div>
        
        {/* Recording Button */}
        <button
          onClick={handleToggleRecording}
          disabled={!isConnected || isProcessing}
          className={`
            w-20 h-20 rounded-full flex items-center justify-center text-white text-2xl
            transition-all duration-300 transform hover:scale-105
            ${isRecording 
              ? 'bg-red-500 hover:bg-red-600 animate-pulse' 
              : 'bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700'
            }
            ${(!isConnected || isProcessing) ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}
          `}
        >
          {isProcessing ? (
            <Loader2 className="w-8 h-8 animate-spin" />
          ) : isRecording ? (
            <MicOff className="w-8 h-8" />
          ) : (
            <Mic className="w-8 h-8" />
          )}
        </button>
        
        {/* Status Text */}
        <div className="text-center">
          {isProcessing && (
            <div className="flex items-center space-x-2 text-blue-600">
              <Loader2 className="w-4 h-4 animate-spin" />
              <span>Processing your voice...</span>
            </div>
          )}
          {isRecording && (
            <div className="flex items-center space-x-2 text-red-600">
              <div className="w-2 h-2 bg-red-500 rounded-full animate-pulse"></div>
              <span>Recording...</span>
            </div>
          )}
        </div>
        
        {/* Usage Tips */}
        <div className="bg-gray-50 rounded-lg p-4 w-full">
          <h3 className="font-semibold text-gray-800 mb-2">Usage Tips</h3>
          <ul className="text-sm text-gray-600 space-y-1">
            <li>• Ensure microphone permission is enabled</li>
            <li>• Maintain appropriate volume when speaking</li>
            <li>• The system will automatically recognize your emotions</li>
            <li>• The assistant will adjust responses based on emotions</li>
          </ul>
        </div>
      </div>
    </div>
  )
} 