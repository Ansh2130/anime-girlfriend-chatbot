import requests
import pyttsx3  # Optional for Text-to-Speech
from whisper_mic import WhisperMic  # Assuming Whisper setup is correct

# Hugging Face API Setup
API_URL = "https://api-inference.huggingface.co/models/deepset/roberta-base-squad2"  # Replace with the model you want to use
API_TOKEN = "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 "  # Replace with your API token

headers = {
    "Authorization": f"Bearer {API_TOKEN}"
}

# Initialize Whisper Mic
mic = WhisperMic()

# Text-to-Speech (Optional)
def speak_text(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# Function to interact with Hugging Face
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

# Function to format conversation history
conversation_history = []
def format_conversation_history(user_input):
    global conversation_history
    conversation_history.append(f"Human: {user_input}")
    formatted_prompt = "\n".join(conversation_history)
    return formatted_prompt

# Main loop for voice interaction
def main():
    print("Starting interactive chat...")

    while True:
        print("Listening for your input...")
        transcribed_text = mic.listen()  # Replace with your Whisper listen method

        if transcribed_text:
            print(f"You said: {transcribed_text}")

            # Format input with conversation history
            prompt = format_conversation_history(transcribed_text)
            print(f"Sending prompt:\n{prompt}")

            # Query Hugging Face API
            response = query_hugging_face(prompt)

            if response:
                conversation_history.append(f"AI: {response}")
                print(f"AI Response: {response}")

                # Speak response (optional)
                speak_text(response)
            else:
                print("No response received.")
        else:
            print("No speech detected. Listening again...")

if __name__ == "__main__":
    main()
