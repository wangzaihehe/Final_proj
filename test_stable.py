#!/usr/bin/env python3
import asyncio
import websockets
import json
import base64
import time

async def test_stable_websocket():
    """Test stable WebSocket connection and message exchange"""
    uri = "ws://localhost:8000/ws/chat"
    
    try:
        async with websockets.connect(uri) as websocket:
            print("✅ WebSocket connection successful")
            
            # Wait a moment to ensure connection is stable
            await asyncio.sleep(1)
            
            # Test 1: Send binary audio data (simulate frontend)
            print("\n=== Test 1: Send binary audio data ===")
            mock_audio = b"mock_webm_audio_data" * 50  # Simulate webm audio
            
            await websocket.send(mock_audio)
            print("✅ Binary data sent")
            
            try:
                response = await asyncio.wait_for(websocket.recv(), timeout=15.0)
                print("✅ Response received")
                try:
                    response_data = json.loads(response)
                    print(f"📝 User text: {response_data.get('user_text', 'N/A')}")
                    print(f"🤖 Assistant response: {response_data.get('assistant_text', 'N/A')}")
                    print(f"😊 Detected emotion: {response_data.get('emotion', 'N/A')}")
                    print(f"📊 Confidence: {response_data.get('emotion_confidence', 'N/A')}")
                except:
                    print("⚠️ Response is not JSON format")
                    print(f"Raw response: {response[:200]}...")
            except asyncio.TimeoutError:
                print("❌ Response timeout")
            
            # Wait a moment
            await asyncio.sleep(2)
            
            # Test 2: Send JSON format data
            print("\n=== Test 2: Send JSON format data ===")
            test_data = {
                "audio": base64.b64encode(mock_audio).decode(),
                "timestamp": time.time()
            }
            
            await websocket.send(json.dumps(test_data))
            print("✅ JSON data sent")
            
            try:
                response = await asyncio.wait_for(websocket.recv(), timeout=15.0)
                print("✅ Response received")
                try:
                    response_data = json.loads(response)
                    print(f"📝 User text: {response_data.get('user_text', 'N/A')}")
                    print(f"🤖 Assistant response: {response_data.get('assistant_text', 'N/A')}")
                    print(f"😊 Detected emotion: {response_data.get('emotion', 'N/A')}")
                    print(f"📊 Confidence: {response_data.get('emotion_confidence', 'N/A')}")
                except:
                    print("⚠️ Response is not JSON format")
                    print(f"Raw response: {response[:200]}...")
            except asyncio.TimeoutError:
                print("❌ Response timeout")
            
            # Test 3: Test heartbeat mechanism
            print("\n=== Test 3: Test heartbeat mechanism ===")
            print("Waiting 30 seconds to test heartbeat...")
            try:
                response = await asyncio.wait_for(websocket.recv(), timeout=35.0)
                print("✅ Heartbeat response received")
                try:
                    response_data = json.loads(response)
                    if response_data.get('type') == 'heartbeat':
                        print("✅ Heartbeat mechanism working normally")
                    else:
                        print(f"Received other response: {response_data}")
                except:
                    print("⚠️ Heartbeat response is not JSON format")
            except asyncio.TimeoutError:
                print("❌ Heartbeat test timeout")
                
    except Exception as e:
        print(f"❌ WebSocket test failed: {e}")

if __name__ == "__main__":
    print("🧪 Testing stable version WebSocket connection...")
    asyncio.run(test_stable_websocket()) 