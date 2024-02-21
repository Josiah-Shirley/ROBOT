# This is an understudy for the part of the maestro driven controller (Currently played
# by the part of 'backend.py'.) The point of this program is to provide an
# easy interface for debugging and testing conductor.py

from conductor import Conductor
import time

while True:
    # USER INPUT MODE FOR TESTING
    coordinates = input(">>> ")
    if coordinates == "stop":
        break
    else:
        coordinatesList = coordinates.split(",")
        xCor = int(coordinatesList[0])
        yCor = int(coordinatesList[1])
        # END TEST COMPONENT SECTION


        # START OF INTEGRATION READY BLOCK
        c = Conductor(xCor, yCor)
        spinAdjustmentList = c.handleSpinInstruction()
        if spinAdjustmentList[0] != 0 and spinAdjustmentList[1] != 0 and spinAdjustmentList[2] != 0:
            print("Spinning!")
            # self.tango.setTarget(0, spinAdjustmentList[0])
            print(spinAdjustmentList[0])
            # self.tango.setTarget(1, spinAdjustmentList[1])
            print(spinAdjustmentList[1])
            time.sleep(spinAdjustmentList[2])
            # self.tango.setTarget(0, 5900)
            # self.tango.setTarget(1, 5900)
            print("Done spinning!")
        motorInputList = c.handleForwardAndBackwardMovement()
        # self.tango.setTarget(0, motorInputList[0])
        print(motorInputList[0])
        # self.tango.setTarget(1, motorInputList[1])
        print(motorInputList[1])
        # END OF INTEGRATION READY BLOCK

        # TODO: !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # put this in the stop function of the backend.py so that it runs
        # when the user lifts their finger.
        # expectingInstructionsState()
        # TODO: !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
