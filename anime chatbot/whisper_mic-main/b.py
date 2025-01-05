import requests
import pyttsx3
from whisper_mic import WhisperMic

# Set up WhisperMic instance for speech-to-text
mic = WhisperMic()

# Hugging Face API Setup for BlenderBot
API_URL = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"
API_TOKEN = "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"  # Replace with your Hugging Face API token
headers = {
    "Authorization": f"Bearer {API_TOKEN}"
}

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
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# Main loop for voice interaction
def main():
    print("Starting interactive chatbot with BlenderBot...")

    while True:
        print("Listening for your input...")
        transcribed_text = mic.listen()  # Use your WhisperMic method to capture speech

        if transcribed_text:
            print(f"You said: {transcribed_text}")

            # Query Hugging Face API (BlenderBot) with transcribed text
            response = query_hugging_face(transcribed_text)

            if response:
                print(f"AI Response: {response}")
                speak_text(response)  # Optionally, speak out the response
            else:
                print("No response received.")
        else:
            print("No speech detected. Listening again...")

if __name__ == "__main__":
    main()
