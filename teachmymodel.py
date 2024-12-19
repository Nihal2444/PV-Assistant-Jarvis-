import speech_recognition as sr
import pyttsx3
import json

# Initialize the text-to-speech engine
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen_and_record():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Listening...")
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            speak("Sorry, I did not understand that.")
            print("Sorry, I did not understand that.")
            return None
        except sr.RequestError:
            speak("Sorry, there was an issue with the request.")
            print("Sorry, there was an issue with the request.")
            return None

def load_knowledge_base():
    try:
        with open('model_memory.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_knowledge_base(knowledge_base):
    with open('model_memory.json', 'w') as f:
        json.dump(knowledge_base, f, indent=4)

def teach_model():
    knowledge_base = load_knowledge_base()
    speak("Speak to teach the model.")
    while True:
        print("Speak to teach the model.")
        command = listen_and_record()
        if command is None:
            continue

        if command.strip().lower() == 'stop':
            speak("Teaching stopped.")
            print("Teaching stopped.")
            break
        elif command.strip().lower() == 'continue':
            speak("Continue teaching.")
            print("Continue teaching.")
            # Proceed to record more phrases
            continue
        else:
            speak(f"You said: {command}")
            speak("What does it mean:")
            print("What does it mean:")
            meaning = listen_and_record()
            if meaning:
                knowledge_base[command] = meaning
                speak("Ok Understood.")
                print("Ok Understood.")

    save_knowledge_base(knowledge_base)
    speak("Knowledge base saved to 'model_memory.json'.")
    print("Knowledge base saved to 'model_memory.json'.")

if __name__ == "__main__":
    teach_model()
