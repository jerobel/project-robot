import speech_recognition as sr

# Initialiser le recognizer
recognizer = sr.Recognizer()

# Fonction pour capturer l'audio avec Pocketsphinx
def capture_audio_pocketsphinx():
    with sr.Microphone() as source:
        print("Dites quelque chose...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        print("Reconnaissance en cours...")
        try:
            # Utiliser pocketsphinx pour la reconnaissance locale
            transcription = recognizer.recognize_sphinx(audio, language='fr-FR')
            print(f"Vous avez dit : {transcription}")
            return transcription
        except sr.UnknownValueError:
            print("Je n'ai pas pu comprendre l'audio.")
            return None
        except sr.RequestError as e:
            print(f"Erreur de service : {e}")
            return None

# Boucle principale
while True:
    question = capture_audio_pocketsphinx()
    if question:
        print(f"Question reçue : {question}")
        # Traitement de la question ici
    else:
        print("Aucune question reçue. Veuillez réessayer.")
