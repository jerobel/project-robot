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
import os

openai.api_key = os.getenv("open_api_key")

def capture_audio():
    recognizer = sr.Recognizer()

    # Liste des périphériques audio disponibles
    mic_list = sr.Microphone.list_microphone_names()
    print("Microphones disponibles:", mic_list)

    # Vous pouvez essayer d'identifier votre microphone en utilisant l'index correspondant à votre microphone
    mic_index = None
    for index, name in enumerate(mic_list):
        if "nom_de_votre_microphone" in name:  # Remplacez par le nom de votre microphone
            mic_index = index
            break

    if mic_index is not None:
        with sr.Microphone(device_index=mic_index) as source:
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
    else:
        print("Microphone non trouvé.")
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

    # Liste des périphériques audio disponibles
    audio_devices = engine.getProperty('audiooutput')
    print("Périphériques audio disponibles:", audio_devices)
    
    # Remplacez 'index_pour_votre_haut_parleur' par l'index réel de votre périphérique Jabra
    engine.setProperty('audiooutput', 'index_pour_votre_haut_parleur')

    engine.say(texte)
    engine.runAndWait()

while True:
    question = capture_audio()
    if question:
        print(f"Question reçue : {question}")
        reponse = obtenir_reponse(question)
        print(f"Réponse de l'IA : {reponse}")
        parler_texte(reponse)
