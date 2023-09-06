import pyttsx3
import speech_recognition as sr

from config import (
    assistant_name,
    assistant_sex,
    assistant_language,
    recognition_language,
    device_index
)


class VoiceAssistant:
    ttsEngine = pyttsx3.init()
    recognizer = sr.Recognizer()
    microphone = sr.Microphone(device_index=device_index)
    name = ""
    sex = ""
    speech_language = ""
    recognition_language = ""

    def setup_assistant_voice(self) -> None:
        """
        Установка голоса по умолчанию (индекс может меняться в
        зависимости от настроек операционной системы)
        """
        self.name = assistant_name
        self.sex = assistant_sex
        self.speech_language = assistant_language
        self.recognition_language = recognition_language
        voices = self.ttsEngine.getProperty("voices")
        self.ttsEngine.setProperty("voice", voices[0].id)

    def record_and_recognize_audio(self, *args: tuple):
        """
        Запись и распознавание аудио
        """
        with self.microphone:
            recognized_data = ""

            # регулирование уровня окружающего шума
            self.recognizer.adjust_for_ambient_noise(self.microphone, duration=2)

            try:
                print("Listening...")
                audio = self.recognizer.listen(self.microphone, 5, 5)

            except sr.WaitTimeoutError:
                print("Can you check if your microphone is on, please?")
                return

            # использование online-распознавания через Google
            try:
                print("Started recognition...")
                recognized_data = self.recognizer.recognize_google(audio, language="ru").lower()

            except sr.UnknownValueError:
                pass

            # в случае проблем с доступом в Интернет происходит выброс ошибки
            except sr.RequestError:
                print("Check your Internet Connection, please")

            return recognized_data
