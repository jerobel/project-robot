import openai
import speech_recognition as sr
import pyttsx3
import os
import time
import requests
from dotenv import load_dotenv

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Vérifiez que la clé API OpenAI est définie
if not openai.api_key:
    print("Erreur : La clé API OpenAI n'est pas définie. Configurez-la dans le fichier .env.")
    exit()

# Vérification de la connexion Internet
def verifier_connexion_internet():
    try:
        requests.get("https://www.google.com", timeout=5)
        return True
    except requests.ConnectionError:
        return False

if not verifier_connexion_internet():
    print("Erreur : Pas de connexion Internet. La reconnaissance vocale nécessite une connexion active.")
    exit()

# Fonction pour tester la synthèse vocale
def tester_synthese_vocale():
    try:
        print("Test de la synthèse vocale...")
        engine = pyttsx3.init()
        engine.say("Test de la synthèse vocale réussi.")
        engine.runAndWait()
        print("Synthèse vocale : OK")
    except Exception as e:
        print(f"Erreur lors de la synthèse vocale : {e}")
        exit()

tester_synthese_vocale()

# Vérification des périphériques audio disponibles
print("\nListe des périphériques audio disponibles :")
microphones = sr.Microphone.list_microphone_names()

# Vérifier s'il y a des microphones disponibles
if len(microphones) == 0:
    print("Aucun microphone trouvé. Veuillez connecter un microphone.")
    exit()

# Sélectionner automatiquement le premier microphone disponible
device_index = 0  # Utilise le premier périphérique de la liste
print(f"Microphone sélectionné : {microphones[device_index]}")

# Fonction pour capturer l'audio via le microphone avec PyAudio
def capture_audio():
    recognizer = sr.Recognizer()
    try:
        print("\nDites quelque chose...")
        with sr.Microphone(device_index=device_index) as source:
            recognizer.adjust_for_ambient_noise(source, duration=1)  # Ajuster pour le bruit ambiant
            audio = recognizer.listen(source, timeout=5)  # Timeout pour éviter le blocage
            print("Traitement de l'audio...")
            transcription = recognizer.recognize_google(audio, language='fr-FR')  # Reconnaissance
            print(f"Vous avez dit : {transcription}")
            return transcription
    except sr.UnknownValueError:
        print("Je n'ai pas pu comprendre l'audio.")
        return None
    except sr.RequestError as e:
        print(f"Erreur de service de reconnaissance vocale : {e}")
        return None
    except Exception as e:
        print(f"Erreur inconnue lors de la capture audio : {e}")
        return None

# Fonction pour obtenir une réponse d'OpenAI
def obtenir_reponse(question):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Utilisation de GPT-4
            messages=[ 
                {"role": "system", "content": "Tu es un assistant utile."},
                {"role": "user", "content": question}
            ],
            max_tokens=150,
            temperature=0.7
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        print(f"Erreur lors de l'appel à OpenAI : {e}")
        return "Désolé, je n'ai pas pu obtenir de réponse."

# Fonction pour faire parler l'IA via le haut-parleur
def parler_texte(texte):
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)  # Vitesse de la voix
        engine.setProperty('volume', 1)  # Volume
        engine.say(texte)
        engine.runAndWait()
    except Exception as e:
        print(f"Erreur lors de la synthèse vocale : {e}")

# Boucle principale
while True:
    print("\n--- Début d'une nouvelle session ---")
    question = capture_audio()
    if question:
        print(f"Question reçue : {question}")
        reponse = obtenir_reponse(question)
        print(f"Réponse de l'IA : {reponse}")
        parler_texte(reponse)
    else:
        print("Aucune question reçue. Veuillez réessayer.")
