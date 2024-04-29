import RPi.GPIO as GPIO


# DO NOT TOUCH
# Setup of Ultra Sound Sensor
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

TRIG_PIN = 11
ECHO_PIN = 12

GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)
# ----------------------------

# Gets the current distance in front of the ultrasound sensor
# and returns it in cm.
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



