from maestro import *
import time


class Tango:
    def __init__(self):
        self.tango=Controller()
        self.turn = 5900
        self.tango.setTarget(0,self.turn)
        self.tango.setTarget(1,self.turn)

        def dab():
            self.tango.setTarget(2, 4000) # Torso
            self.tango.setTarget(3, 4000) # Head
            self.tango.setTarget(4, 4000) # Head Pitch
            self.tango.setTarget(5, 10000) # Right Shoulder
            self.tango.setTarget(6, 7500) # Right Chicken Wing
            self.tango.setTarget(7, 7000) # Right Elbow
            self.tango.setTarget(8, 7500) # Right Wrist Pitch
            self.tango.setTarget(10, 7500) # Right Claw
            self.tango.setTarget(11, 2000) # Left Shoulder
            self.tango.setTarget(12, 3000) # Left Chicken Wing
            self.tango.setTarget(13, 15000) # Left Elbow
            self.tango.setTarget(14, 5000) # Left Wrist Pitch
            self.tango.setTarget(16, 4000) # Left Claw
        
        speed = 5900
        rotate = 5900
        proceed = True
        while proceed:
            print("R = stop : W = forward : s = backward : B = break")
            print("D = right : A = left")
            user = input(">>> ")
            if user.lower() == 'r':
                speed = 5900
                rotate = 5900
                print(speed)
            elif user.lower() == 'w':
                speed -= 700
                print(speed)
            elif user.lower() == 's':
                speed += 500
                print(speed)
            elif user.lower() == 'd':
                rotate -= 200
            elif user.lower() == 'a':
                rotate += 200
            elif user.lower() == "k":
                dab()
            elif user.lower() == 'g':
                for num in range(2,17):
                    self.tango.setTarget(num, 6000)
            else:
                speed = 5900
                rotate = 5900
                proceed = False
            self.tango.setTarget(0,speed)
            self.tango.setTarget(1,rotate)

        '''
        for num in range(2,17):
            self.tango.setTarget(num,self.turn)
            pasue = input("Press enter to continue")
        '''
t = Tango()

