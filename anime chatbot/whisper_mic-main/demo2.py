import requests
import pyttsx3
from whisper_mic import WhisperMic
from gtts import gTTS
import pygame
import os
import websocket
import json
import threading

# Set up WhisperMic instance for speech-to-text
mic = WhisperMic()

# Hugging Face API Setup for BlenderBot
API_URL = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"
API_TOKEN = "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"  # Replace with your Hugging Face API token
headers = {
    "Authorization": f"Bearer {API_TOKEN}"
}

# VTube Studio WebSocket details
VTS_WS_URL = "ws://127.0.0.1:8001"  # Default WebSocket URL for VTube Studio
vts_connected = False  # Connection status for VTube Studio WebSocket

# Connect to VTube Studio WebSocket
def connect_to_vts():
    def on_open(ws):
        print("Connected to VTube Studio WebSocket.")
        global vts_connected
        vts_connected = True

        # Authenticate with VTube Studio
        auth_request = {
            "apiName": "VTubeStudioPublicAPI",
            "apiVersion": "1.0",
            "requestID": "auth-request",
            "messageType": "AuthenticationTokenRequest",
            "data": {
                "pluginName": "Chatbot Integration",
                "pluginDeveloper": "Your Name or Team",
                "pluginIcon": ""  # Optional: Add base64 image of your plugin icon
            }
        }
        ws.send(json.dumps(auth_request))

    def on_message(ws, message):
        print("VTube Studio Response:", message)

    def on_error(ws, error):
        print("VTube Studio WebSocket Error:", error)

    def on_close(ws, close_status_code, close_msg):
        print("Disconnected from VTube Studio WebSocket.")
        global vts_connected
        vts_connected = False

    # Establish WebSocket connection
    ws = websocket.WebSocketApp(
        VTS_WS_URL,
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )
    threading.Thread(target=ws.run_forever, daemon=True).start()
    return ws

# Function to send lip-sync data to VTube Studio
def send_lip_sync(ws, text):
    if vts_connected:
        lip_sync_request = {
            "apiName": "VTubeStudioPublicAPI",
            "apiVersion": "1.0",
            "requestID": "lip-sync-request",
            "messageType": "TextToSpeechRequest",
            "data": {
                "text": text,
                "pitch": 1.0,
                "speed": 1.0,
                "volume": 1.0,
                "characterName": ""  # Optional: Target specific VTube Studio character
            }
        }
        ws.send(json.dumps(lip_sync_request))

# Function to interact with Hugging Face API (BlenderBot model)
def query_hugging_face(prompt):
    try:
        payload = {
            "inputs": prompt
        }
        response = requests.post(API_URL, headers=headers, json=payload)

        if response.status_code == 200:
            response_data = response.json()
            return response_data[0]["generated_text"]
        else:
            print(f"Error: {response.status_code} - {response.json()}")
            return "Sorry, I couldn't process your request."
    except Exception as e:
        print(f"Error interacting with Hugging Face API: {e}")
        return "An error occurred while processing your request."

# Text-to-Speech (Optional)
def speak_text(text):
    tts = gTTS(text=text, lang='ja', slow=False)  # Use Japanese language (ja)
    temp_file = "response.mp3"
    tts.save(temp_file)
    
    pygame.mixer.init()
    pygame.mixer.music.load(temp_file)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.music.stop()
    pygame.mixer.quit()
    os.remove(temp_file)

# Main loop for voice interaction
def main():
    print("Starting interactive chatbot with BlenderBot...")
    ws = connect_to_vts()  # Connect to VTube Studio WebSocket

    while True:
        print("Listening for your input...")
        transcribed_text = mic.listen()

        if transcribed_text:
            print(f"You said: {transcribed_text}")
            response = query_hugging_face(transcribed_text)

            if response:
                print(f"AI Response: {response}")
                speak_text(response)  # Optionally, speak out the response
                send_lip_sync(ws, response)  # Send lip-sync data to VTube Studio
            else:
                print("No response received.")
        else:
            print("No speech detected. Listening again...")

if __name__ == "__main__":
    main()
