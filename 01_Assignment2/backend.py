from flask import *
import tkinter as tk
from tkinter import ttk
from maestro import *
import time


###   HOW TO USE THIS PROGRAM   ###
# 1. Open up a terminal
# 2. Enter the command: sudo /etc/init.d/apache2 stop
#       This ends an apache server that runs on boot. When running, it uses port 80,
#       which is the port we want to use with this program.
# 3. Connect to the wifi network: Lenovo PHAB2 Pro
#       This is only necessary if you are running this script at the MSU campus.
#       MSU's firewall stops the flask server from serving the webpage for some reason.
#       The important thing is that you can run the script while connected to network
#       That won't prevent you from serving the webpage.
# 4. Run this script in the terminal
#       The exact command depends on where the file is located, but the current command is
#       sudo  python3 ROBOT/01_Assignment2/backend.py
# 5. If you receive no errors after running the command in the terminal, open a browser
#       and enter the IP address of the Pi. You can find the IP address by hover the mouse
#       over the wifi symbol in the top right of the screen.
# 6. To stop the flask server, press 'Ctrl-c' while focused on the terminal.
# _________________________________________________________________________________________


# Port numbers for the Maestro Contoller
LEFTWHEEL = 0
RIGHTWHEEL = 1
# In order to send commands to the wheels, you first need to give an initializing value of
# 5900. This can be done by executing "self.tango.setTarget([PORTNUMBER], 5900)"
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


# This provides the flask server with the webpage to be served.
# The server will serve the html file whose name matches the string
# argument given in render_template function below (Contained in the
# return statement). In addition to giving the name of the html file,
# the html file you wish to serve must be found in a folder titled
# "templates" and the folder must be right next to this python file
# In your file organizer.
app = Flask(__name__)
@app.route("/")
def index():
    return render_template('webPage.html')

# This route will run whenever data is received via the 'POST' method.
# Currently, the webpage posts data whenever any slider or the joystick is moved.
@app.route("/receive-data", methods=['POST'])
def receive_data():
    # Data is passed in the form "value;sliderNumber;inputCode",
    # e.g. "-2;1;torsoOrHead"


    # Below is a test you can uncomment to verify that data is being sent from
    # the webpage to this python script. If data is being correctly sent,
    # moving the second slider into the -2 position should cause a blank
    # tkinter window to pop up immediately.
    '''
    # BEGIN TEST
    if data == "-2;1;torsoOrHead":
        root = tk.Tk()
        root.mainloop()
    # END TEST
    '''

    
    data = request.form['data']
    positionAndMotorPair = data.split(";")
    bodyPartCode = positionAndMotorPair[2]
                # This body part code is how the logic of the python script will know
                # what type of motor input it is dealing with. There is a seperate track
                # for dealing with a wheel motor input than for the torso or head motors.
    if bodyPartCode == "torsoOrHead":
        motor = int(positionAndMotorPair[1])
        motor += 2      # This shists the given slider number to fit its motor number.
                        # The slider numbers are. top to bottom, 0, 1, and 2. The corresponding
                        # motor numbers for the sliders are, respectively, 2, 3, and 4.
        position = int(positionAndMotorPair[0])
        position += 5   # This shifts the position input from a range of -5 to 5 into a range
                        # of 0 to 10, which will be used to get values from a list later.
    elif bodyPartCode == "wheels":
        offsetX = int(positionAndMotorPair[0])
        offsetY = int(positionAndMotorPair[1])
            
    
    class Tango():
        def __init__(self):

            self.tango = Controller()
        
            self.tango.setTarget(0, 5900)  # This initializes the wheel motors so that
            self.tango.setTarget(1, 5900)  # they will spin when they receive instruction



            # MOVEMENT FUNCTIONS __________________________________________________
            
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

            def rotateBodyPart(motor, position):
                positions = [3900,4300,4700,5100,5500,5900,6300,6700,7100,7500,7900]
                self.tango.setTarget(motor, positions[position])

            def drive(offsetX, offsetY):
                x = offsetX - 50
                y = (offsetY - 50)*(-1)

                if y == 0:
                    stop()
                else:
                    c = Conductor(x, y)
                    motorInputList = c.handleMovement()
                    self.tango.setTarget(0, int(motorInputList[0]))
                    # print(motorInputList[0])
                    self.tango.setTarget(1, int(motorInputList[1]))
                    # print(motorInputList[1])
            

                
            # MOTOR INPUT PARSER _________________________________________________________

            if bodyPartCode == "torsoOrHead":
                rotateBodyPart(motor, position)
            elif bodyPartCode == "wheels":
                drive(offsetX, offsetY)
                

    t = Tango()
    
    return 'Data received successfully'

        
if __name__ == '__main__':
    app.run(debug=True,port=80,host='192.168.43.166')
