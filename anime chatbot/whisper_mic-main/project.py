import requests
import os
import websockets
import json
import time
import asyncio
from whisper_mic import WhisperMic  # Assuming you already have this set up

# API Keys and URLs
ELEVEN_LABS_API_KEY = "sk_5725ce13d8e3e67390bc79c2c1f8d0d179b777dc1ebff90b"  # Replace with your Eleven Labs API key
HUGGINGFACE_API_KEY = "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"  # Replace with your Hugging Face API key
VTube_WS_URL = "ws://localhost:8001"  # Adjust if necessary for VTube Studio WebSocket URL

# Set up WhisperMic instance for speech recognition
mic = WhisperMic()

# Hugging Face API URL for chatbot
API_URL = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"  # Example model, replace with your desired model
headers = {
    "Authorization": f"Bearer {HUGGINGFACE_API_KEY}"
}

# Function to generate speech using Eleven Labs API
def generate_speech(text, voice="Dorothy"):
    headers = {
        "Authorization": f"Bearer {ELEVEN_LABS_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "text": text,
        "voice": voice,
        "model_id": "eleven_monolingual_v1"
    }

    response = requests.post("https://api.elevenlabs.io/v1/text-to-speech/generate", json=payload, headers=headers)

    if response.status_code == 200:
        audio_content = response.content
        with open("output.mp3", "wb") as f:
            f.write(audio_content)
        print("Audio generated and saved as 'output.mp3'.")
        return "output.mp3"
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

# Function to interact with Hugging Face chatbot API
def query_hugging_face(prompt):
    try:
        response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
        if response.status_code == 200:
            response_data = response.json()
            return response_data[0]["generated_text"]
        else:
            print(f"Error: {response.status_code} - {response.json().get('error', 'Unknown error')}")
            return "Sorry, I couldn't process your request."
    except Exception as e:
        print(f"Error interacting with Hugging Face API: {e}")
        return "An error occurred while processing your request."

# WebSocket function to send lip-sync request to VTube Studio
async def send_lipsync_request():
    async with websockets.connect(VTube_WS_URL) as websocket:
        message = {
            "event": "SetLipSync",
            "parameters": {
                "value": "anime",  # You can adjust this based on your needs
                "duration": 5.0  # Duration to match the lip sync
            }
        }
        await websocket.send(json.dumps(message))

        response = await websocket.recv()
        print("Received response from VTube Studio:", response)

# Function to listen to audio using Whisper
def listen_and_transcribe():
    print("Listening for your input...")
    transcribed_text = mic.listen()  # Adjust to your WhisperMic method
    if transcribed_text:
        print(f"You said: {transcribed_text}")
        return transcribed_text
    return None

# Main function
def main():
    print("Starting voice interaction system with Whisper, Hugging Face, Eleven Labs, and VTube Studio...")

    while True:
        # Listen for speech and transcribe it
        user_input = listen_and_transcribe()

        if user_input:
            # Get chatbot response from Hugging Face
            response = query_hugging_face(user_input)

            # Generate speech from Eleven Labs
            audio_file = generate_speech(response)

            if audio_file:
                # Play the generated speech
                os.system(f"start {audio_file}")  # For Windows, change this for other OS
                time.sleep(1)  # Wait for audio to start

                # Sync the avatar's lip sync with the speech
                asyncio.get_event_loop().run_until_complete(send_lipsync_request())

        else:
            print("No speech detected, waiting for input...")

if __name__ == "__main__":
    main()
