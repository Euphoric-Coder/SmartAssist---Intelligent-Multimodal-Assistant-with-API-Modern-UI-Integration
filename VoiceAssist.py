from datetime import datetime
from nltk.chat.util import Chat, reflections
from input_pattern import pairs
import speech_recognition as sr
import time
import tkinter as tk
from announcer import speak


def get_greeting():
    """
    This function is usesd to get current time in hours to greet the user
    """
    Time = datetime.now()
    Time = Time.hour

    if Time > 5 and Time < 12:
        return "Good morning"
    elif Time > 12 and Time < 18:
        return "Good afternoon"
    else:
        return "Good evening"


def get_command():

    audio = sr.Recognizer()

    # Use the default microphone as the audio source
    with sr.Microphone() as source:
        print("Please say something...")
        audio.adjust_for_ambient_noise(source)  # To adjust for ambient noise
        audio_data = audio.listen(source)  # Will listen for 10 seconds

    try:
        print("Recognizing...")
        # Using the Google Web Speech API for speech recognition
        text = audio.recognize_google(audio_data)
        print(f"You said: {text}")
        return text

    except sr.UnknownValueError:
        print("Sorry, could not understand audio.")
        return None
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return None


def main():
    greetings = get_greeting()
    salutation = " Sire,"
    chatbot = Chat(pairs, reflections)

    speak(greetings + salutation + " How may i help you ?")
    # Start the conversation
    while True:
        user_input = get_command()
        time.sleep(3)
        try:
            if user_input.lower() in ["quit"]:
                speak("Goodbye!")
                break
            else:
                response = chatbot.respond(user_input)
                if response == None:
                    speak("Not Clear please repeat")
                else:
                    speak(response)
        except:
            pass


if __name__ == "__main__":
    main()
