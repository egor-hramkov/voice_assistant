from voice_assistant import VoiceAssistant

if __name__ == "__main__":
    VoiceAssistant().setup_assistant_voice()
    while True:
        # старт записи речи с последующим выводом распознанной речи
        voice_input = VoiceAssistant().record_and_recognize_audio()
        print(voice_input)
