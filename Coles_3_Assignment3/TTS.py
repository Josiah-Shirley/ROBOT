import pyttsx3
import threading
import time

class TTS(threading.Thread):

    #
    def __int__(self):
        super(TTS, self).__init__()
        # Initialize the TTS engine
        self.engine = pyttsx3.init()
        # Set the speaking rate
        self.engine.setProperty('rate', 150)

    def run(self):
        # Start the TTS engine loop
        self.engine.startLoop(False)

    def say(self, text):
        # Speak the input string
        self.engine.say(text)
        # Non-blocking "manner" to proces the input string apart from TTS engine
        self.engine.iterate()

    def stop(self):
        # End the TTS engine loop
        self.engine.endLoop()

def main():
    tts = TTS()

    # Starts the TTS thread
    tts.start()

    # Testing
    tts.say("Hello, Josiaih I am your robot........Here me roar!")

    # More Testing
    while True:
        try:
            text = input("Enter text to speak: ")
            if text == "EOF":
                break
            tts.say(text)
            # delay to prevent interference
            time.sleep(.02)
        except KeyboardInterrupt:
            # Handle keyboard interrupt
            print("Interrupt. Stopping")
            break
        except Exception as e:
            # Handle other
            print("An error occurred,", e)

    tts.stop()
    # Check to make sure
    print("Stopped")

if __name__ == "__main__":
    main()
