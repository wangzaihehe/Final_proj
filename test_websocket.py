#!/usr/bin/env python3
import asyncio
import websockets
import json
import base64
import time

async def test_websocket_connection():
    """Test WebSocket connection and message exchange"""
    uri = "ws://localhost:8000/ws/chat"
    
    try:
        async with websockets.connect(uri) as websocket:
            print("✅ WebSocket connection successful")
            
            # Wait a moment to ensure connection is stable
            await asyncio.sleep(1)
            
            # Send a test audio message (mock data)
            test_audio_data = b"mock_audio_data_for_testing"
            
            print(f"📤 Sending test audio data: {len(test_audio_data)} bytes")
            await websocket.send(test_audio_data)
            
            # Wait for response
            print("⏳ Waiting for response...")
            response = await websocket.recv()
            
            # Parse response
            response_data = json.loads(response)
            print(f"📝 User text: {response_data.get('user_text', 'N/A')}")
            print(f"🤖 Assistant response: {response_data.get('assistant_text', 'N/A')}")
            print(f"😊 Detected emotion: {response_data.get('emotion', 'N/A')}")
            print(f"📊 Emotion confidence: {response_data.get('emotion_confidence', 'N/A')}")
            
            # Test with text message
            text_message = {
                "type": "text",
                "message": "Hello, how are you today?"
            }
            
            print(f"📤 Sending text message: {text_message}")
            await websocket.send(json.dumps(text_message))
            
            # Wait for response
            response = await websocket.recv()
            response_data = json.loads(response)
            print(f"📝 User text: {response_data.get('user_text', 'N/A')}")
            print(f"🤖 Assistant response: {response_data.get('assistant_text', 'N/A')}")
            print(f"😊 Detected emotion: {response_data.get('emotion', 'N/A')}")
            
            print("✅ Test completed successfully")
            
    except websockets.exceptions.ConnectionClosed:
        print("❌ WebSocket connection closed unexpectedly")
    except Exception as e:
        print(f"❌ Test failed: {e}")

async def test_multiple_messages():
    """Test sending multiple messages"""
    uri = "ws://localhost:8000/ws/chat"
    
    try:
        async with websockets.connect(uri) as websocket:
            print("✅ WebSocket connection established for multiple message test")
            
            messages = [
                "Hello, I'm feeling happy today!",
                "Actually, I'm a bit sad now...",
                "I'm getting excited about this conversation!"
            ]
            
            for i, message in enumerate(messages, 1):
                print(f"\n--- Message {i} ---")
                print(f"📤 Sending: {message}")
                
                # Send as text message
                text_message = {
                    "type": "text",
                    "message": message
                }
                
                await websocket.send(json.dumps(text_message))
                
                # Wait for response
                response = await websocket.recv()
                response_data = json.loads(response)
                
                print(f"📝 User text: {response_data.get('user_text', 'N/A')}")
                print(f"🤖 Assistant response: {response_data.get('assistant_text', 'N/A')}")
                print(f"😊 Detected emotion: {response_data.get('emotion', 'N/A')}")
                
                # Wait between messages
                await asyncio.sleep(2)
            
            print("\n✅ Multiple message test completed")
            
    except Exception as e:
        print(f"❌ Multiple message test failed: {e}")

if __name__ == "__main__":
    print("🧪 Testing stable version WebSocket connection...")
    
    # Run basic connection test
    asyncio.run(test_websocket_connection())
    
    # Run multiple message test
    asyncio.run(test_multiple_messages()) 