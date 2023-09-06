from voice_input import VoiceAssistant

if __name__ == "__main__":
    while True:
        # старт записи речи с последующим выводом распознанной речи
        VoiceAssistant().setup_assistant_voice()
        voice_input = VoiceAssistant().record_and_recognize_audio()
        print(voice_input)
