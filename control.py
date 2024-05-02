from maestro import Controller
import time

class Wheels():
    def __init__(self):
        self.control = Controller()
        self.control.setTarget(0, 5900)
        self.control.setTarget(1, 5900)
        self.distance_scale = 42 # represents 42 cm
        self.left_scale = 30
        self.right_scale = 30

    def forward(self, distance=None):
        self.control.setTarget(0, 5200)
        self.control.setTarget(1, 6800)
        if distance:
            time.sleep(distance / self.distance_scale)
            self.stop()

    def reverse(self, distance=None):
        self.control.setTarget(0, 6800)
        self.control.setTarget(1, 5200)
        if distance:
            time.sleep(distance / self.distance_scale)
            self.stop()

    def left(self, angle=None):
        self.control.setTarget(1, 7000)
        self.control.setTarget(0, 5900)
        if angle:
            time.sleep(angle / self.left_scale)
            self.stop()

    def right(self, angle=None):
        self.control.setTarget(0, 4900)
        self.control.setTarget(1, 5900)
        if angle:
            time.sleep(angle / self.right_scale)
            self.stop()

    def stop(self):
        self.control.setTarget(0, 5900)
        self.control.setTarget(1, 5900)

'''
if __name__ == "__main__":
    wheels = Wheels()
    wheels.forward(90)
    time.sleep(1)
    wheels.right(90)
    time.sleep(1)
    wheels.left(90)
    time.sleep(1)
    wheels.stop()
''' 
