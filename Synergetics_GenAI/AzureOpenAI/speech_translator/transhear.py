import azure.cognitiveservices.speech as speech_sdk

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

target_Language = ""
while target_Language != 'quit':
    target_Language = input("\nEnter a target language:\n fr=French\n es=Spanish\n hi=Hindi\n ar=Arabic\n kn=Kannada\n mr=Marathi\nEnter 'quit' to stop\n").lower()

    if target_Language in translation_config.target_languages:
        audio_config = speech_sdk.AudioConfig(use_default_microphone=True)
        translator = speech_sdk.translation.TranslationRecognizer(translation_config, audio_config=audio_config)

        print("Speak now...")
        result = translator.recognize_once_async().get()

        print('Translating "{}"'.format(result.text))

        # Check if the key exists in the translations dictionary
        translation = result.translations.get(target_Language, "Translation not available for the selected language.")
        print(translation)

        voices = {
            "ar": 'ar-SA-NaayfNeural',
            "fr": 'fr-French-HenriNeural',
            "es": 'es-Es-ElviraNeural',
            "hi": 'hi-IN-MadhurNeural',
            "kn": 'kn-IN-ChitraNeural',  # Update with the correct Kannada voice
            "mr": 'mr-IN-AarohiNeural'  # Update with the correct Marathi voice
        }

        speech_config.speech_synthesis_voice_name = voices.get(target_Language)
        speech_synthesizer = speech_sdk.SpeechSynthesizer(speech_config)
        speak = speech_synthesizer.speak_text_async(translation).get()
    elif target_Language != 'quit':
        print("Unsupported language. Please try again.")
