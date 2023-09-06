from voice_input import VoiceInput

if __name__ == "__main__":
    while True:
        # старт записи речи с последующим выводом распознанной речи
        voice_input = VoiceInput().record_and_recognize_audio()
        print(voice_input)
