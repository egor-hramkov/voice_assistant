import webbrowser
from googlesearch import search
import pyttsx3

import traceback

import speech_recognition as sr

from config import (
    assistant_language,
    device_index
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

    def search_for_term_on_google(self, *args: tuple):
        """
        Поиск в Google с автоматическим открытием ссылок (на список результатов и на сами результаты, если возможно)
        :param args: фраза поискового запроса
        """
        if not args[0]:
            return
        search_term = " ".join(args[0])
        url = "https://google.com/search?q=" + search_term

        # открытие ссылки на поисковик в браузере
        webbrowser.get().open(url)

        # альтернативный поиск с автоматическим открытием ссылок на результаты
        search_results = []
        try:
            for _ in search(search_term,  # что искать
                            tld="com",  # верхнеуровневый домен
                            lang=assistant_language,  # используется язык, на котором говорит ассистент
                            num=1,  # количество результатов на странице
                            start=0,  # индекс первого извлекаемого результата
                            stop=1,
                            # индекс последнего извлекаемого результата (я хочу, чтобы открывался первый результат)
                            pause=1.0,  # задержка между HTTP-запросами
                            ):
                search_results.append(_)
                webbrowser.get().open(_)

        except:
            self.play_voice_assistant_speech("Seems like we have a trouble. See logs for more information")
            traceback.print_exc()
            return

        print(search_results)
        self.play_voice_assistant_speech(f"Here is what I found for {search_term} on google")

    def search_for_video_on_youtube(self, *args: tuple):
        """
        Поиск видео на YouTube с автоматическим открытием ссылки на список результатов
        :param args: фраза поискового запроса
        """
        if not args[0]:
            return
        search_term = " ".join(args[0])
        url = "https://www.youtube.com/results?search_query=" + search_term
        webbrowser.get().open(url)
        self.play_voice_assistant_speech(f"Here is what I found for {search_term} on youtube")
