#!/usr/bin/env python3
##
## EPITECH PROJECT, 2024
## projet robot epitech digital 
## File description:
## projet robot epitech digital
##

import openai
import speech_recognition as sr
import pyttsx3

from keys import secret

openai.api_key = secret

def capture_audio():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Dites quelque chose...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        print("Vous avez dit : " + recognizer.recognize_google(audio))
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        print("Je n'ai pas pu comprendre l'audio.")
        return None
    except sr.RequestError as e:
        print(f"Erreur de service de reconnaissance vocale {e}")
        return None
def obtenir_reponse(question):
    response = openai.Completion.create(
        engine="gpt-4", 
        prompt=question,
        max_tokens=150
    )
    return response.choices[0].text.strip()
def parler_texte(texte):
    engine = pyttsx3.init()
    engine.say(texte)
    engine.runAndWait()
while True:
    question = capture_audio()
    if question:
        print(f"Question reçue : {question}")
        reponse = obtenir_reponse(question)
        print(f"Réponse de l'IA : {reponse}")
        parler_texte(reponse)
