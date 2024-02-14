from maestro import *
import time
import tkinter as tk
from tkinter import ttk

FWDREV = 0
LEFTRIGHT = 1
WAIST = 2
HEADTILT = 3
HEADTURN = 4
RIGHTSHDR = 5
RIGHTBICEP = 6
RIGHTELBOW = 7
RIGHTFOREARM = 8
RIGHTWRIST = 9
RIGHTGRIPCLOSE = 10
LEFTSHDR = 11
LEFTBICEP = 12
LEFTELBOW = 13
LEFTFOREARM = 14
LEFTWRIST = 15
LEFTGRIPCLOSE = 16

WHEELS = 0

class Tango():
    def __init__(self):
        self.gear = 0
        self.speeds = [5200, 4500, 4000]
        self.tango = Controller()
    
        self.tango.setTarget(0, 5900)  # This initializes the wheel motors so that
        self.tango.setTarget(1, 5900)  # they will sping when they receive instruction

        def forward(event):
            self.tango.setTarget(0, self.speeds[self.gear])
            print("Forward " + str(self.speeds[self.gear]))

        def backward(event):
            self.tango.setTarget(0, 7000)

        def left(event):
            self.tango.setTarget(1, 7000)

        def right(event):
            self.tango.setTarget(1, 4800)

        def stop(event):
            self.tango.setTarget(0, 5900)
            self.tango.setTarget(1, 5900)

        def dab(event):
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
            time.sleep(3)
            reset()

        def reset():
            for num in range(2,17):
                self.tango.setTarget(num, 6000)

        def shiftUp(event):
            if self.gear < 2:
                self.gear += 1
                self.tango.setTarget(0, self.speeds[self.gear])

        def shiftDown(event):
            if self.gear > 0:
                self.gear -= 1
                self.tango.setTarget(0, self.speeds[self.gear])


        root = tk.Tk()

        btn = ttk.Button(root, text='Awaiting Commands...')
        btn.bind('<Up>', forward)
        btn.bind('<Down>', backward)
        btn.bind('<Left>', left)
        btn.bind('<Right>', right)
        btn.bind('<space>', stop)
        btn.bind('<Return>', dab)
        btn.bind('<Shift_R>', shiftUp)
        btn.bind('<Shift_L>', shiftDown)
        

        btn.focus()
        btn.pack(expand=True)


        root.mainloop()


t = Tango()
