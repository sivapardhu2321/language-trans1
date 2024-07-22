from flask import Flask, render_template, request
import speech_recognition as sr
from googletrans import Translator

app = Flask(__name__)

# Function to recognize speech using Google Speech Recognition
def recognize_speech():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak something...")
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return "Google Speech Recognition could not understand audio"
    except sr.RequestError as e:
        return f"Could not request results from Google Speech Recognition service; {e}"

# Function to translate text using Google Translate API
def translate_text(text, dest_lang='en'):
    translator = Translator()
    translation = translator.translate(text, dest=dest_lang)
    return translation.text

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    if request.method == 'POST':
        recognized_text = recognize_speech()
        if recognized_text:
            translations = {}
            languages = ['te', 'hi', 'ta', 'bn', 'gu', 'mr', 'pa', 'ur', 'ja', 'ko', 'es', 'de', 'ne', 'fr']
            for lang in languages:
                translated_text = translate_text(recognized_text, dest_lang=lang)
                translations[lang] = translated_text

            return render_template('translate.html', original_text=recognized_text, translations=translations)

if __name__ == '__main__':
    app.run(debug=True)
