from pydub import AudioSegment
from pydub.playback import play
import pygame
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import os
import pyttsx3
import pycountry

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def getLangName(lang_code):
    language = pycountry.languages.get(alpha_2=lang_code)
    return language.name

def take_voice_input():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("GO ON! I AM LISTENING.")
        r.pause_threshold = 1
        audio = r.listen(source)

    try: 
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"The User said: {query}\n")
        return query.lower()
    except Exception as e:
        print("I DIDN'T GET YOU...")
        return ""

def take_text_input():
    print("Enter the sentence to translate:")
    query = input(">> ")
    return query.lower()

print("Welcome to the translator!")
speak("Welcome to the translator!")
print("Do you want to provide input through voice or text? Say 'voice' or 'text'.")

while True:
    input_mode = take_voice_input()  # Let the user choose voice or text input

    if "voice" in input_mode:
        query = take_voice_input()  # Voice input
    elif "text" in input_mode:
        query = take_text_input()  # Text input
    else:
        print("Invalid input. Please say 'voice' or 'text'.")
        speak("Invalid input. Please say 'voice' or 'text'.")
        continue

    # Break the loop if the user says 'stop'
    if query == 'stop':
        print("Translation stopped.")
        speak("Translation stopped. Exiting.")
        break

    # Detecting the source language
    translator = Translator()
    from_lang = translator.detect(query).lang
    print("Your sentence is in", getLangName(from_lang))

    def destination_language():
        print("What Language do you want me to translate it into (e.g., Hindi, English, Spanish, etc.):")
        to_lang = take_voice_input()  # Let the user provide the destination language via voice input
        while not to_lang:
            to_lang = take_voice_input()
        return to_lang.lower()

    to_lang = destination_language()

    # Check if the destination language is available (case-insensitive)
    languages = [lang.name.lower() for lang in pycountry.languages]
    if to_lang not in languages:
        print("The destination language is currently not available.")
    else:
        # Translating from src to dest
        text_to_translate = translator.translate(query, src=from_lang, dest=to_lang)
        translated_text = text_to_translate.text

        # Using Google Text-to-Speech (gTTS) to speak the translated text in the destination language
        speak(translated_text)
        print(translated_text)

# Clean up temporary files
if os.path.exists("translated_audio.mp3"):
    os.remove("translated_audio.mp3")
