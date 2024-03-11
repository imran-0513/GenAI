from flask import Flask, render_template, request
import azure.cognitiveservices.speech as speech_sdk

app = Flask(__name__)

cog_key = "2328ec43179f4401a82199e32f449746"
cog_reg = "eastus"

translation_config = speech_sdk.translation.SpeechTranslationConfig(cog_key, cog_reg)
translation_config.speech_recognition_language = 'en-US'
translation_config.add_target_language('ar')
translation_config.add_target_language('fr')
translation_config.add_target_language('es')
translation_config.add_target_language('hi')
translation_config.add_target_language('kn')  # Kannada
translation_config.add_target_language('mr')  # Marathi

speech_config = speech_sdk.SpeechConfig(cog_key, cog_reg)

voices = {
    "ar": 'ar-SA-NaayfNeural',
    "fr": 'fr-French-HenriNeural',
    "es": 'es-Es-ElviraNeural',
    "hi": 'hi_IN-MadhurNeural',
    "kn": 'kn-IN-ChitraNeural',  # Update with the correct Kannada voice
    "mr": 'mr-IN-AarohiNeural'  # Update with the correct Marathi voice
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    target_language = request.form['target_language']

    if target_language in translation_config.target_languages:
        audio_config = speech_sdk.AudioConfig(use_default_microphone=True)
        translator = speech_sdk.translation.TranslationRecognizer(translation_config, audio_config=audio_config)

        print("Speak now...")
        result = translator.recognize_once_async().get()

        print('Translating "{}"'.format(result.text))

        translation = result.translations.get(target_language, "Translation not available for the selected language.")

        speech_config.speech_synthesis_voice_name = voices.get(target_language)
        speech_synthesizer = speech_sdk.SpeechSynthesizer(speech_config)
        speak = speech_synthesizer.speak_text_async(translation).get()

        return render_template('result.html', translation=translation)
    else:
        return "Unsupported language. Please try again."

if __name__ == '__main__':
    app.run(debug=True)
