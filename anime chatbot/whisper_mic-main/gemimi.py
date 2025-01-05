
import requests
from whisper_mic import WhisperMic
import pyttsx3  # Optional: For Text-to-Speech

# Set up WhisperMic instance
mic = WhisperMic()

# Google Gemini API Key and URL (replace with your actual API key)
GEMINI_API_KEY = "AIzaSyAZ4gI_Vmd_NAsJNe5JbDZ2zxMpM28mUIg"  # Replace with your Gemini API key
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta2/models/text-bison-001:generateText"

# Function to interact with Google Gemini API
def interact_with_gemini(prompt):
    try:
        # Prepare the request payload
        payload = {
            "prompt": {"text": prompt},
            "temperature": 0.7,  # Controls randomness (0.0 is deterministic, 1.0 is highly random)
            "maxOutputTokens": 256,  # Maximum length of the response
            "topP": 0.95,  # Controls diversity (higher is more diverse)
        }
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {GEMINI_API_KEY}",  # Use Bearer authentication
        }

        # Send the request to Gemini API
        response = requests.post(GEMINI_API_URL, headers=headers, json=payload)
        response.raise_for_status()  # Raise an error for HTTP issues

        # Parse the response and return the output text
        response_data = response.json()
        return response_data.get("candidates", [{}])[0].get("output", "No response from Gemini.")
    except requests.exceptions.RequestException as e:
        print(f"Error interacting with Gemini API: {e}")
        return "An error occurred while processing your request."

# Optional: Text-to-Speech Function
def speak_text(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# Main loop for voice interaction
def main():
    print("Starting voice interaction system with Google Gemini...")
    for transcribed_text in mic.listen_continuously():  # Transcribe continuously using Whisper
        if transcribed_text:
            print(f"You said: {transcribed_text}")

            # Send the transcribed text to Gemini API
            gemini_response = interact_with_gemini(transcribed_text)

            if gemini_response:
                print(f"Gemini response: {gemini_response}")
                # Optional: Speak the Gemini response
                speak_text(gemini_response)
            else:
                print("Failed to get a response from Gemini.")
        else:
            print("Waiting for input...")

if __name__ == "__main__":
    main()
