import speech_recognition as sr
import openai
import pyttsx3
import time

class Listen:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 135)

        # Put your api key here

        self.prompt = "As a member of the sith overlord, I am here to assist you."

    def listen_and_respond(self):
        self.engine.say("Hello human")
        self.engine.runAndWait()
        with sr.Microphone() as source:
            r = sr.Recognizer()
            r.adjust_for_ambient_noise(source)
            r.dynamic_energy_threshold = 3000
            print("Listening, go ahead...")
            audio = r.listen(source)
            print("Got audio...")
            try:
                user_input = r.recognize_google(audio)
                print("You said:", user_input)
                response = self.generate_response(user_input)
                self.engine.say(response)
                self.engine.runAndWait()
                return user_input
            except sr.UnknownValueError:
                print("Could not understand audio...")
                return None

    def generate_response(self, user_input):
        predefined_responses = {
            "go to the restroom": "Ok, we will head to quadrant 3.",
            "go to the charging station": "We will go recharge and power up.",
            "go to hunter's office": "Let's go visit our awesome professor and tell him a joke."
        }

        if user_input.lower() in predefined_responses:
            response = predefined_responses[user_input.lower()]
        else:
            try:
                combo = self.prompt + user_input
                completion = self.client.chat.completions.create(
                    model='gpt-3.5-turbo',
                    messages=[
                        {"role": "user", "content": combo}
                    ],
                    temperature=0,
                    max_tokens=20
                )
                time.sleep(0.5)
                response = completion.choices[0].message.content
            except Exception as e:
                print("Error generating response:", e)
                response = "Sorry, I didn't catch that."

        print("Response:", response)
        return response
    
    def affirm_location_with_speech(self, quadrant):
        affirmation = ""
        if quadrant == 0:
            affirmation = "I am in the quadrant I started in."
        elif quadrant == 1:
            affirmation = "I am at the charging station."
        elif quadrant == 2:
            affirmation = "I am in Hunter's office."
        elif quadrant == 3:
            affirmation = "I am in the restroom."
        else:
            affirmation = "I was given an invalid quadrant number."
        self.engine.say(affirmation)
        self.engine.runAndWait()

def main():
    listener = Listen()
    try:
        listener.listen_and_respond()
    except KeyboardInterrupt:
        print("Program terminated by user.")
    except Exception as e:
        print("An error occurred:", e)
    finally:
        listener.engine.stop()

if __name__ == "__main__":
    main()

