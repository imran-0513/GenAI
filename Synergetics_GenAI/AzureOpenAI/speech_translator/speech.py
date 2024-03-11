##pip install azure-cognitiveservices-speech==1.30.0

import azure.cognitiveservices.speech as speech_sdk

cog_key = "2328ec43179f4401a82199e32f449746"
cog_reg = "eastus"

translation_config = speech_sdk.translation.SpeechTranslationConfig(cog_key,cog_reg)

translation_config.speech_recognition_language='en-US'

translation_config.add_target_language('fr')
translation_config.add_target_language('es')
translation_config.add_target_language('hi')

speech_config = speech_sdk.SpeechConfig(cog_key, cog_reg)

target_language =""
while target_language!='quit':
    target_language = input("\nenter a target language\n fr= Frecnh\n es=Spanish\n hi=hindi \n enter anything to stop\n").lower()
    audio_config = speech_sdk.AudioConfig(use_default_microphone=True)
    translator = speech_sdk.translation.TranslationRecognizer(translation_config,audio_config=audio_config)

    print("Speak now...")
    result = translator.recognize_once_async().get()

    print('Translating"{}"'.format(result.text))
    translation = result.translations[target_language]
    print(translation)
    voices = {
        "fr":'fr-French-HenriNeural',
        "es":'es-Es-ElviraNeural',
        "hi":'hi_IN-MadhurNeural'

    }

    speech_config.speech_synthesis_voice_name=voices.get(target_language)
    speech_synthesizer=speech_sdk.SpeechSynthesizer(speech_config)
    speech_synthesizer.speak_text_async(translation).get()
    target_language = 'quit'


