from flask import *
import tkinter as tk
from tkinter import ttk
from maestro import *
import time


# If you get an error stating that port 80 is currently being used,
# Then the apache server is running. run the command
# sudo /etc/init.d/apache2 stop
# to stop the server.


# The command to start the flask server is
# sudo  python3 ROBOT/02_Assignment3/backend.py



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


app = Flask(__name__)
@app.route("/")
def index():
    return render_template('webPage.html')

@app.route("/receive-data", methods=['POST'])
def receive_data():
    # Data is passed in the form "value;sliderNumber",
    # e.g. "-2;1"
    '''
    # This is just to test that we have received the data
    if data == "-2;1":
        root = tk.Tk()
        root.mainloop()
    # End test
    '''
    data = request.form['data']
    positionAndMotorPair = data.split(";")
    position = int(positionAndMotorPair[0])
    position += 5   # This shifts the position input from a range of -5 to 5 into a range
                    # of 0 to 10, which will be used to get values from a list later.
    motor = int(positionAndMotorPair[1])
    motor += 2
    bodyPartCode = positionAndMotorPair[2]

    
    class Tango():
        def __init__(self):
            self.gear = 0
            self.speeds = [5200, 4500, 4000]
            self.tango = Controller()
        
            self.tango.setTarget(0, 5900)  # This initializes the wheel motors so that
            self.tango.setTarget(1, 5900)  # they will spin when they receive instruction

            def forward():
                self.tango.setTarget(0, self.speeds[self.gear])

            def backward():
                self.tango.setTarget(0, 7000)

            def left():
                self.tango.setTarget(1, 7000)

            def right():
                self.tango.setTarget(1, 4800)

            def stop():
                self.tango.setTarget(0, 5900)
                self.tango.setTarget(1, 5900)

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
                time.sleep(3)
                reset()

            def reset():
                for num in range(2,17):
                    self.tango.setTarget(num, 6000)

            def shiftUp():
                self.gear += 1
                self.tango.setTarget(0, self.speeds[self.gear])

            def shiftDown():
                self.gear -= 1
                self.tango.setTarget(0, self.speeds[self.gear])

            def rotateBodyPart(motor, position):
                positions = [3900,4300,4700,5100,5500,5900,6300,6700,7100,7500,7900]
                self.tango.setTarget(motor, positions[position])
                self.tango.setTarget(0,6700)


            if bodyPartCode == "torsoOrHead":
                rotateBodyPart(motor, position)
                

    t = Tango()
    
    return 'Data received successfully'

        
if __name__ == '__main__':
    app.run(debug=True,port=80,host='192.168.43.166')

