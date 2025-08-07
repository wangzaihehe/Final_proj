# Emotion-Aware Voice Chat Assistant

An AI-powered emotional intelligence voice chat application that can recognize emotions in user voice and respond accordingly.

## Project Features

- 🎭 **Voice Emotion Recognition**: Real-time analysis of user voice emotional states
- 🧠 **Intelligent Conversation**: Context understanding based on GPT-4 and other large language models
- 🎤 **Voice Interaction**: Support for voice input and voice output
- 💬 **Real-time Communication**: Low-latency real-time conversation via WebSocket
- 🎨 **Modern UI**: Responsive interface based on Next.js and TailwindCSS
- 🔒 **Privacy Protection**: Local emotion recognition to protect user privacy

## Tech Stack

### Backend
- **FastAPI**: High-performance Python web framework
- **WebSocket**: Real-time bidirectional communication
- **Librosa**: Audio processing and feature extraction
- **PyTorch**: Deep learning framework
- **Whisper**: Speech-to-text conversion
- **ElevenLabs**: Text-to-speech conversion

### Frontend
- **Next.js 14**: React full-stack framework
- **TailwindCSS**: Utility-first CSS framework
- **TypeScript**: Type-safe JavaScript
- **Socket.io**: Client-side WebSocket communication

### AI/ML
- **OpenAI GPT-4**: Large language model
- **Emotion Recognition Model**: Audio feature-based emotion classification

## Project Structure

```
FinalProj/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── models/         # Data models
│   │   ├── services/       # Business logic
│   │   ├── api/           # API routes
│   │   └── utils/         # Utility functions
│   ├── requirements.txt
│   └── main.py
├── frontend/               # Next.js frontend
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── pages/        # Pages
│   │   ├── styles/       # Style files
│   │   └── utils/        # Utility functions
│   ├── package.json
│   └── next.config.js
├── models/                # Pre-trained models
└── README.md
```

## Quick Start

### Requirements
- Python 3.8+
- Node.js 18+
- FFmpeg (for audio processing)

### Installation Steps

1. **Clone the project**
```bash
git clone <repository-url>
cd FinalProj
```

2. **Install backend dependencies**
```bash
cd backend
pip install -r requirements.txt
```

3. **Install frontend dependencies**
```bash
cd frontend
npm install
```

4. **Configure environment variables**
```bash
# Backend .env
OPENAI_API_KEY=your_openai_api_key
ELEVENLABS_API_KEY=your_elevenlabs_api_key

# Frontend .env.local
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
```

5. **Start services**
```bash
# Start backend
cd backend
uvicorn main:app --reload

# Start frontend
cd frontend
npm run dev
```

## Usage Instructions

1. Open browser and visit `http://localhost:3000`
2. Allow microphone permissions
3. Click the start conversation button
4. Speak and the system will automatically recognize emotions and respond accordingly

## Features

- **Real-time Emotion Recognition**: Analyze 8 basic emotions in voice
- **Contextual Conversation**: Remember conversation history for coherent communication
- **Emotion Adaptation**: Adjust response style based on user emotions
- **Voice Synthesis**: Natural voice output
- **Multi-language Support**: Support for English and other languages

## Contributing

Welcome to submit Issues and Pull Requests to improve this project!

## License

MIT License 