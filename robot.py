import pyaudio
import speech_recognition as sr
import pyttsx3
import os
import requests
from dotenv import load_dotenv

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# Vérifiez que la clé API OpenAI est définie
if not openai_api_key:
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

# Initialiser PyAudio
p = pyaudio.PyAudio()

# Liste des périphériques disponibles
devices = []
for i in range(p.get_device_count()):
    device_info = p.get_device_info_by_index(i)
    devices.append(device_info)

print("Liste des périphériques audio disponibles :")
for device in devices:
    print(f"ID : {device['index']} | Nom : {device['name']}")

# Assurez-vous que vous utilisez le bon index pour le microphone Jabra
device_index = 2  # Remplacez par l'index correct de votre microphone Jabra
print(f"Microphone sélectionné : {devices[device_index]['name']}")

# Fonction pour capturer l'audio via le microphone
recognizer = sr.Recognizer()

def capture_audio(device_index):
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
        import openai
        openai.api_key = openai_api_key
        response = openai.ChatCompletion.create(  # Utilisation de la méthode correcte
            model="gpt-4",  # Utilisation de GPT-4
            messages=[ 
                {"role": "system", "content": "Tu es un assistant utile."},
                {"role": "user", "content": question}
            ],
            max_tokens=150,
            temperature=0.7
        )
        return response['choices'][0]['message']['content'].strip()  # Utilisation du bon champ pour la réponse
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
    question = capture_audio(device_index)
    if question:
        print(f"Question reçue : {question}")
        reponse = obtenir_reponse(question)
        print(f"Réponse de l'IA : {reponse}")
        parler_texte(reponse)
    else:
        print("Aucune question reçue. Veuillez réessayer.")
