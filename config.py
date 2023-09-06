import speech_recognition as sr

microphones = sr.Microphone.list_microphone_names()
for index, name in enumerate(microphones):
    print("Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(index, name))
