    import pyttsx3
    import json
    import speech_recognition as sr
    import os

    model_name = "Jarvis"
    user_name = "Human Being"

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
        file_path = 'C:\\Users\\nihal\\PycharmProjects\\JarvisTry90\\model_memory.json'
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                return data
        except FileNotFoundError:
            speak("No model data found. Please teach the model first.")
            print("File not found. No model data found.")
            return {}
        except json.JSONDecodeError:
            speak("Error decoding the model data. Please check the file.")
            print("Error decoding JSON. Please check the file.")
            return {}

    def save_model_name(new_name):
        global model_name
        model_name = new_name
        speak(f"Model name changed to {model_name} as per your command.")
        print(f"Model name changed to {model_name} as per your command.")

    def get_user_name():
        global user_name
        speak(f"Hello, I am {model_name}, your personal voice assistant. Please say your name to get started.")
        print(f"\nHello, I am {model_name}, your personal voice assistant. Please say your name to get started.")
        print("\n")
        user_name = listen_and_record()
        if user_name:
            speak(f"Nice to meet you, {user_name}!")
            print(f"Nice to meet you, {user_name}!")

    def test_model():
        global model_name, user_name
        data = load_knowledge_base()
        if not data:
            return

        if user_name == "Human Being":
            get_user_name()

        speak(f"Hello, {user_name}. I am {model_name}. Your personal voice assistant. How can I help you?")
        last_input = None
        while True:
            user_input = listen_and_record()
            if user_input:
                if 'please change the model name' in user_input.lower():
                    speak("Ok, please say a new name for the model.")
                    new_name = listen_and_record()
                    if new_name:
                        save_model_name(new_name)
                    continue

                # Check if the input starts with 'what is'
                if user_input.lower().startswith('what is '):
                    query = user_input.lower().split('what is ', 1)[1].strip()
                    if query in data:
                        response = f"{query} is {data[query]}"
                    else:
                        response = f"Sorry , I don't know what '{query}' means."
                else:
                    # Process other inputs normally
                    if user_input in data:
                        response = f"{user_name}, I understand '{user_input}'. {data[user_input]}"
                    else:
                        response = f"{user_name}, I don't know what '{user_input}' means. Please say again ."

                speak(response)
                print(response)
                last_input = user_input

                speak("Say 'exit' to stop or 'repeat' to repeat my response.")
                action = listen_and_record().strip().lower()
                if action == 'exit' or action == 'please stop running the model':
                    speak(f"Okay , It was nice meeting you {user_name}, Thank You for using me. See you again...!")
                    print(f"Okay, It was nice meeting you {user_name}, Thank You for using me. See you again...!")
                    break
                elif action == 'repeat' and last_input:
                    # Repeat the last response
                    speak(response)
                    print(response)

    if __name__ == "__main__":
        test_model()