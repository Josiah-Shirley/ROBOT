import RPi.GPIO as GPIO
import time

class UltrasonicSensor:
    def __init__(self, trigger_pin, echo_pin):
        self.trigger_pin = trigger_pin
        self.echo_pin = echo_pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.trigger_pin, GPIO.OUT)
        GPIO.setup(self.echo_pin, GPIO.IN)

    def measure_distance(self):
        GPIO.output(self.trigger_pin, True)
        time.sleep(0.00001)
        GPIO.output(self.trigger_pin, False)

        timeout = time.time()
        while GPIO.input(self.echo_pin) == 0:
            if (time.time() - timeout) > 3:
                print("Timeout error")
                return None

        pulse_start = time.time()
        timeout = time.time()
        while GPIO.input(self.echo_pin) == 1:
            if (time.time() - timeout) > 3:
                print("Pulse start error")
                return None
        pulse_end = time.time()
            
        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration*17150

        return distance

    def cleanup(self):
        GPIO.cleanup([self.trigger_pin, self.echo_pin])


def main():
    trigger_pin = 18
    echo_pin = 24
    GPIO.setwarnings(False)
    ultrasonic_sensor = UltrasonicSensor(trigger_pin, echo_pin)
    try:
        while True:
            distance = ultrasonic_sensor.measure_distance()
            if distance is not None:
                print("Distance:", distance, "cm")
            else:
                print("Error measuring distance")
            time.sleep(0.2) 
    finally:
        ultrasonic_sensor.cleanup()

if __name__ == "__main__":
    main()

