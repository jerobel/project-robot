import openai
import speech_recognition as sr
import pyttsx3
import os
<<<<<<< HEAD
import time
from dotenv import load_dotenv

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Vérifiez que la clé API est définie
if not openai.api_key:
    print("Erreur : La clé API OpenAI n'est pas définie. Configurez-la dans les variables d'environnement ou dans le script.")
    exit()
=======

openai.api_key = os.getenv("open_api_key")
>>>>>>> 7df3183af606220c08263a0eea7f37ee96899295

# Fonction pour capturer l'audio via le microphone Jabra
def capture_audio():
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone(device_index=1) as source:  # Assurez-vous que l'index du microphone Jabra est correct
            print("Dites quelque chose...")
            time.sleep(1)  # Délai pour permettre à l'utilisateur de se préparer
            recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = recognizer.listen(source)
            print("Traitement de l'audio...")
            transcription = recognizer.recognize_google(audio, language='fr-FR')
            print(f"Vous avez dit : {transcription}")
            return transcription
    except sr.UnknownValueError:
        print("Je n'ai pas pu comprendre l'audio.")
        return None
    except sr.RequestError as e:
        print(f"Erreur de service de reconnaissance vocale : {e}")
        return None
    except Exception as e:
        print(f"Erreur inconnue : {e}")
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
        # Récupération de la réponse dans le format correct
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        print(f"Erreur lors de l'appel à OpenAI : {e}")
        return "Désolé, je n'ai pas pu obtenir de réponse."

# Fonction pour faire parler l'IA via le haut-parleur Jabra
def parler_texte(texte):
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)  # Vitesse de la voix (optionnel)
        engine.setProperty('volume', 1)  # Volume (optionnel)
        engine.say(texte)
        engine.runAndWait()
    except Exception as e:
        print(f"Erreur lors de la synthèse vocale : {e}")

# Boucle principale
while True:
    question = capture_audio()
    if question:
        print(f"Question reçue : {question}")
        reponse = obtenir_reponse(question)
        print(f"Réponse de l'IA : {reponse}")
        parler_texte(reponse)  # La réponse de l'IA est maintenant lue à haute voix
    else:
        print("Aucune question reçue, réessayez.")
