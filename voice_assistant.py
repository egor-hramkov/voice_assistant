import webbrowser
from googlesearch import search
import pyttsx3

import traceback

import speech_recognition as sr

from config import (
    assistant_language,
    device_index,
    rate,
    volume
)


class VoiceAssistant:
    ttsEngine = pyttsx3.init()
    recognizer = sr.Recognizer()
    microphone = sr.Microphone(device_index=device_index)

    def setup_assistant_voice(self) -> None:
        """
        Установка голоса по умолчанию (индекс может меняться в
        зависимости от настроек операционной системы)
        """
        voices = self.ttsEngine.getProperty("voices")
        self.ttsEngine.setProperty("voice", voices[0].id)
        self.ttsEngine.setProperty('rate', rate + 30)
        self.ttsEngine.setProperty('volume', volume)

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

    def play_voice_assistant_speech(self, text_to_speech: str):
        """
        Проигрывание речи ответов голосового ассистента (без сохранения аудио)
        :param text_to_speech: текст, который нужно преобразовать в речь
        """
        self.ttsEngine.say(str(text_to_speech))
        self.ttsEngine.runAndWait()

    def search_for_term_on_google(self, search_term: str):
        """
        Поиск в Google с автоматическим открытием ссылок (на список результатов и на сами результаты, если возможно)
        :param search_term: фраза поискового запроса
        """
        if not search_term:
            return
        url = "https://google.com/search?q=" + search_term
        webbrowser.get().open(url)
        self.play_voice_assistant_speech(f"Вот что мне удалось найти по запросу {search_term}")

    def search_for_video_on_youtube(self, search_term: str):
        """
        Поиск видео на YouTube с автоматическим открытием ссылки на список результатов
        :param search_term: фраза поискового запроса
        """
        if not search_term:
            return
        url = "https://www.youtube.com/results?search_query=" + search_term
        webbrowser.get().open(url)
        self.play_voice_assistant_speech(f"Вот что мне удалось найти на ютубе по запросу {search_term}")

    def alternative_google_search(self, search_term: str):
        # альтернативный поиск с автоматическим открытием ссылок на результаты
        search_results = []
        try:
            for website in search(search_term, lang=assistant_language, num_results=3):
                search_results.append(website)
                webbrowser.get().open(website)
            self.play_voice_assistant_speech(f"Вот что мне удалось найти по запросу {search_term}")
        except Exception:
            self.play_voice_assistant_speech("Произошла ошибка при поиске, пожалуйста повторите запрос!")
            traceback.print_exc()
            return

