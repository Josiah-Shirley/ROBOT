import math
import time
from RobotBrainForSensorFinding import *
from maestro import *
import RPi.GPIO as GPIO
import pyttsx3


engine = pyttsx3.init()
engine.setProperty('rate', 145)
engine.setProperty('voice', "english+f4")

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

TRIG_PIN = 11
ECHO_PIN = 12

GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)

def get_distance():
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

def checkForPedestrians():
    dist = get_distance()
    while dist < 150:
        print("Move it or lose it!")
        engine.say("Move it or lose it!")
        engine.runAndWait()
        time.sleep(1)
        dist = get_distance()

t = Controller()
giveItSomeMoreJuice = 0
robocop = RobotBrainForSensorFinding(t)
distances = robocop.ravioliRavioliGiveMeTheDistanceolis()
print(distances)
for key, value in distances.items():
    distances[key] = int(value)
min_key = min(distances, key=distances.get)
robocop.setTargetAnchor(min_key)
del distances[min_key]
next_min = min(distances, key=distances.get)
print("I am in quadrant:", min_key)
engine.say("I am in quadrant " + min_key)
engine.runAndWait()
print("I am the next closest quadrant:", next_min)
premoveDistance = robocop.ravioliRavioliGiveMeTheDistanceolis()[min_key] # k
checkForPedestrians()
robocop.tentativelyMoveForward()
time.sleep(1)
postmoveDistance = robocop.ravioliRavioliGiveMeTheDistanceolis()[min_key] # g
print("Pre-move:",premoveDistance)
print("Post-move:",postmoveDistance)
if premoveDistance > postmoveDistance:
    checkForPedestrians()
    robocop.continueOnToAnchor()
else:
    testDistance = robocop.getTestMoveDistance()    # h
    angle = (math.pow(premoveDistance, 2) + math.pow(testDistance, 2) - math.pow(postmoveDistance, 2)) / (2 * premoveDistance * postmoveDistance)  
    print("Radians", angle)
    if angle < 0:
        angle = (2*math.pi) + angle
    arcLength = angle*robocop.getRobotRadius()
    speed = testDistance/robocop.getTestMoveTime()
    timeToMoveFor = arcLength/speed
    robocop.t.setTarget(0,5900-robocop.getTestMovePowerLevel()-giveItSomeMoreJuice)
    time.sleep(timeToMoveFor)
    robocop.t.setTarget(0,5900)
    time.sleep(1)
    checkForPedestrians()
    robocop.continueOnToAnchor()
engine.say("Exited!")
engine.runAndWait()


