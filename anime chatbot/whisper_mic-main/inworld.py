import requests
import pyttsx3  # For Text-to-Speech (optional)
from whisper_mic import WhisperMic  # Assuming you have WhisperMic setup

# Wit.ai API Setup
WIT_API_KEY = "XA6LGWI2JFLSI2KDSQXUUELMOXXKTYFX"  # Replace with your Wit.ai API Key
WIT_API_URL = "  https://api.wit.ai/message?v=20250105&q="

# Authorization headers
headers = {
    "Authorization": f"Bearer {WIT_API_KEY}"
}

# Initialize Whisper Mic
mic = WhisperMic()

# Text-to-Speech Function (Optional)
def speak_text(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# Function to interact with Wit.ai
def query_wit_ai(message):
    try:
        response = requests.get(WIT_API_URL, headers=headers, params={"q": message})
        if response.status_code == 200:
            response_data = response.json()
            # Extract intent or text from response
            if "text" in response_data:
                return response_data["text"]
            return "I couldn't understand your request."
        else:
            print(f"Error: {response.status_code} - {response.json().get('error', 'Unknown error')}")
            return "Sorry, I couldn't process your request."
    except Exception as e:
        print(f"Error interacting with Wit.ai: {e}")
        return "An error occurred while processing your request."

# Main Loop for Voice Interaction
def main():
    print("Starting voice-based chatbot with Wit.ai...")

    for transcribed_text in mic.listen_continuously():
        if transcribed_text:
            print(f"You said: {transcribed_text}")

            # Query Wit.ai with the transcribed text
            wit_response = query_wit_ai(transcribed_text)

            if wit_response:
                print(f"Wit.ai Response: {wit_response}")
                # Optional: Convert response to speech
                speak_text(wit_response)
            else:
                print("Failed to get a response from Wit.ai.")
        else:
            print("No speech detected. Listening again...")

if __name__ == "__main__":
    main()
