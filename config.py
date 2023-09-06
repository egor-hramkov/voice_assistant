import speech_recognition as sr

assistant_name = ''
assistant_sex = 'female'
assistant_language = 'ru'
recognition_language = "ru-RU"
device_index = 1


def get_microphone_list():
    microphones = sr.Microphone.list_microphone_names()
    for index, name in enumerate(microphones):
        print("Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(index, name))


if __name__ == "__main__":
    get_microphone_list()
