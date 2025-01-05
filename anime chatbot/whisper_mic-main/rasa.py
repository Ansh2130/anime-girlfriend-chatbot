import requests
from whisper_mic import WhisperMic

# Rasa API endpoint
RASA_URL = "http://localhost:5005/webhooks/rest/webhook"  # Default Rasa REST webhook

# Function to send user input to Rasa and get a response
def interact_with_rasa(prompt):
    try:
        # Send the prompt to Rasa
        response = requests.post(RASA_URL, json={"sender": "user", "message": prompt})
        if response.status_code == 200:
            rasa_responses = response.json()
            if rasa_responses:
                # Combine all responses from Rasa into a single string
                return " ".join(resp.get("text", "") for resp in rasa_responses)
            else:
                return "No response from Rasa."
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return "Failed to process your request."
    except Exception as e:
        print(f"Error interacting with Rasa: {e}")
        return "An error occurred while processing your request."

# Main loop for voice interaction
def main():
    print("Starting voice interaction system with Rasa...")
    mic = WhisperMic()  # Initialize WhisperMic instance

    # Continuously listen for transcribed speech and interact with Rasa
    for transcribed_text in mic.listen_continuously():
        if transcribed_text:
            print(f"You said: {transcribed_text}")

            # Send the transcribed text to Rasa
            rasa_response = interact_with_rasa(transcribed_text)

            if rasa_response:
                print(f"Rasa response: {rasa_response}")
                # Optional: Convert response to speech (Text-to-Speech)
            else:
                print("Failed to get a response from Rasa.")
        else:
            print("Waiting for input...")

if __name__ == "__main__":
    main()
