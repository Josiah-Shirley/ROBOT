import pyttsx3
import threading

class TTS(threading.Thread):
    def __init__(self):
        self.engine = pyttsx3.init()

    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

def main():
    tts = TTS()

    start = "Text to Speech from the shell"
    tts.speak(start)

    while True:
        text = input()

        if text.lower() == 'quit':
            break

        tts.speak(text)

if __name__ == "__main__":
    main()
