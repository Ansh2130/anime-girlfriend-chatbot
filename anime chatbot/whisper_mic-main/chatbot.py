    
import openai
from whisper_mic import WhisperMic

# Set up WhisperMic instance
mic = WhisperMic()

# OpenAI API Key (replace with your API key)
OPENAI_API_KEY = "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"
openai.api_key = OPENAI_API_KEY

# Function to interact with ChatGPT using the updated API
def interact_with_chatgpt(prompt, model="gpt-3.5-turbo"):
    try:
        # Use the updated `openai.ChatCompletion.create` function
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},  # Optional system message
                {"role": "user", "content": prompt}
            ]
        )
        reply = response['choices'][0]['message']['content']
        return reply
    except Exception as e:
        print(f"Error interacting with ChatGPT: {e}")
        return None

# Main loop for voice interaction
def main():
    print("Starting voice interaction system with ChatGPT...")
    for transcribed_text in mic.listen_continuously():
        if transcribed_text:
            print(f"You said: {transcribed_text}")

            # Send the transcribed text to ChatGPT
            gpt_response = interact_with_chatgpt(transcribed_text)

            if gpt_response:
                print(f"ChatGPT response: {gpt_response}")
                # Optional: Convert response to speech (Text-to-Speech)
            else:
                print("Failed to get a response from ChatGPT.")
        else:
            print("Waiting for input...")

if __name__ == "__main__":
    main()

