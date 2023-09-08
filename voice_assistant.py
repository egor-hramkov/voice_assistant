import webbrowser

import wikipediaapi
from googlesearch import search
import pyttsx3
import requests
from geopy.geocoders import Nominatim

import traceback

import speech_recognition as sr

from config import (
    assistant_language,
    device_index,
    rate,
    volume,
    home_city
)
from exceptions.weather_exceptions import WeatherNotFound
from helpers.weather_code_helper import weather_precipitation_helper, convert_wind_speed_helper


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

    def play_farewell_and_quit(self):
        """
        Проигрывание прощательной речи и выход
        """
        self.play_voice_assistant_speech("Пока")
        self.ttsEngine.stop()
        quit()

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

    def search_for_definition_on_wikipedia(self, search_term: str):
        """
        Поиск в Wikipedia определения с последующим озвучиванием результатов и открытием ссылок
        :param search_term: фраза поискового запроса
        """
        if not search_term:
            return

        # установка языка (в данном случае используется язык, на котором говорит ассистент)
        wiki = wikipediaapi.Wikipedia('voice_assistant (merlin@example.com)', assistant_language)

        # поиск страницы по запросу, чтение summary, открытие ссылки на страницу для получения подробной информации
        wiki_page = wiki.page(search_term)
        try:
            if wiki_page.exists():
                self.play_voice_assistant_speech(f"Вот что удалось найти в википедии по запросу {search_term}")
                webbrowser.get().open(wiki_page.fullurl)

                # чтение ассистентом первых двух предложений summary со страницы Wikipedia
                # (могут быть проблемы с мультиязычностью)
                for sentence in wiki_page.summary.split(".")[:2]:
                    self.play_voice_assistant_speech(sentence)
            else:
                # открытие ссылки на поисковик в браузере в случае, если на Wikipedia не удалось найти ничего по запросу
                self.play_voice_assistant_speech(
                    f"Неудалось найти информацию в википедии, "
                    f"но вот что удалось найти в интернете по запросу {search_term}"
                )
                url = "https://google.com/search?q=" + search_term
                webbrowser.get().open(url)
        except:
            self.play_voice_assistant_speech("Произошла ошибка при поиске, пожалуйста повторите запрос!")
            traceback.print_exc()
            return

    def say_weather(self, search_term: str = None) -> None:
        """Воспроизводит прогноз погоды"""
        try:
            data = self.get_weather_forecast(search_term)
        except WeatherNotFound as e:
            self.play_voice_assistant_speech(e.msg)
            traceback.print_exc()
        except:
            self.play_voice_assistant_speech(
                "При поиске прогноза погоды что-то пошло не так, пожалуйста повторите попытку"
            )
            traceback.print_exc()
        else:
            skies_info = weather_precipitation_helper.get(str(data.get('weathercode')))
            temperature = data.get('temperature')
            wind_info = convert_wind_speed_helper(data.get('windspeed'))
            weather_info = (f"Прогноз на сегодня: {skies_info}, {wind_info}, "
                            f"Температура воздуха - {temperature} градусов цельсия")
            self.play_voice_assistant_speech(weather_info)

    @staticmethod
    def get_weather_forecast(search_term: str = None) -> dict:
        """
        Получение и озвучивание прогноза погоды
        :param search_term: город, по которому должен выполняться запрос
        """
        if not search_term:
            city_name = home_city
        else:
            city_name = search_term

        geolocator = Nominatim(user_agent='voice_assistant')
        location = geolocator.geocode(city_name)
        if not location:
            raise WeatherNotFound

        latitude = location.latitude
        longitude = location.longitude
        url = (f"https://api.open-meteo.com/v1/forecast?latitude={latitude}"
               f"&longitude={longitude}"
               f"&current_weather=true")
        data = requests.get(url).json().get('current_weather')
        return data

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
