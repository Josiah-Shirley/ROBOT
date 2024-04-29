import tkinter as tk
import random
import numpy as np
import time
import threading
import pyttsx3
from maestro import *
from openai import OpenAI
import speech_recognition as sr
import RPi.GPIO as GPIO
from speechEngine import *
from RobotBrainForSensorFinding import *

# DO NOT TOUCH
# Setup of Ultra Sound Sensor
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
TRIG_PIN = 11
ECHO_PIN = 12
GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)
destinations = { 'starting quadrant': 0, 'charing station': 1, 'hunters office': 2, 'restrooms': 3 }

class Greeter:

    def __init__():
        self.tango = Controller()
        # self.brain.ravioliRavioliGiveMeTheDistanceolis()
        # The above line will return a dictionary of the distances from
        # each anchor -> {"a": 0, "b": 0, "c": 0, "d": 0}
        self.brain = RobotBrainForSensorFinding()
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 135)
        self.grid = np.array(grid, dytype=int)
        
    def respond(self, prompt):
        response = prompt + " and please limit your response to 20 words or less."
        completion = client.chat.completions.create(
            model='gpt-3.5-turbo',
            messages=[
                {'role': 'user', 'content': response}
            ],
            temperature=0,
            max_tokens=25
        )
        self.engine.say(completion.choices[0].message.content)
        self.engine.runAndWait()


    # Gets the current distance in front of the ultrasound sensor
    # and returns it in cm.
    def get_distance(self):
        print("Getting distance...")
        GPIO.output(TRIG_PIN, False)
        time.sleep(0.01)


        GPIO.output(TRIG_PIN, True)
        time.sleep(0.0001)
        GPIO.output(TRIG_PIN, False)

        timeout = time.time()
        while GPIO.input(ECHO_PIN) == 0:
            if (time.time() - timeout) > 3:
                print("Timeout error")
                return None
            
        pulse_start = time.time()
        timeout = time.time()
        while GPIO.input(ECHO_PIN) == 1:
            if (time.time() - timeout) > 3:
                print("pulse start error")
                return None
        pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration*17150

        return distance


    def checkForPedestrians(self):
        dist = self.get_distance()
        while dist > 150:
            print("Nothing in the way")
            time.sleep(1)
            dist = self.get_distance()
        self.haveConversation()

    def haveConversation(self):
        dt = DialogueTemplate("dialogTestFile.txt")
        dt.interpretLines()
        self.engine.say("Are you lost? You look lost.")
        self.engine.runAndWait()
    
        while True:
            with sr.Microphone() as source:
                r = sr.Recognizer()
                r.adjust_for_ambient_noise(source)
                r.dynamic_energy_threshold = 3000
                try:
                    print("---------------------")
                    print("listening, go ahead...")
                    audio = r.listen(source)
                    print("Got audio...")
                    user_input = r.recognize_google(audio)
                    print(user_input)
                    if user_input in self.destination.keys():
                        self.turn_to_destination(user_input)
                    response = dt.findResponse(user_input)
                    if response == "invalid input for text file":
                        self.respond(user_input)
                    else:
                        self.engine.say(response)
                        self.engine.runAndWait()
                    if user_input == "goodbye":
                        break
                except sr.UnknownValueError:
                    print("That may not be a valid English word...")

    def grid(self):
        self.grid = np.zeros((2, 2), dtype=int), 
        self.row = len(self.grid)
        self.cols = len(self.grid[0])

    def turn_to_destination():
        # Get current position

if __name__ == "__main__":
    reginold = Greeter()
    reginold.checkForPedestrians()

    grid = [
        [],[],[],[]
        ]
    


    

