import speech_recognition as sr

listening = True
r = sr.Recognizer()

while listening:
    with sr.Microphone() as source:
        # r.adjust_for_ambient_noise(source)
        r.dynamic_energy_threshold = 300

        try:
            print("listening...")
            audio = r.listen(source)
            print("{processing audio...}")
            word = r.recognize_google(audio)
            print(word)
        except sr.UnknownValueError:
            print("..Unknown Word..")