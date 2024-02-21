# This is a helper object that allows easier debugging and testing
# of the driving component of backend.py

import math


class Conductor:
    def __init__(self, x, y, r=1400):
        self.x = x
        self.y = y
        self.range = r
        # self.speed = 2.5  # <-- measured in ft/s
        # self.wheelDiameter = 1.375  # <-- measured in ft
        # self.spinPowerAdjustment = 1200  # <-- this is the amount of power that will be
        #     given to the wheels while spinning in place

    def setRange(self, r):
        self.range = r

    # This function handles the forward and backward movement signal
    # which need to be sent to the robot. The function takes in the
    # 'y' coordinate and turns it into the proper motor inputs
    # and returns a list containing those motor impulses.
    # The list should be used in the backend controller like this:
    #
    # motorInputList = handleForwardAndBackwardMovement() <-- Be sure that this is the post
    # self.tango.setTarget(0, motorInputList[0])                adjustment y value (i.e. 50
    # self.tango.setTarget(1, motorInputList[1])                has already been subtracted.)
    #
    def handleMovement(self) -> list:
        x = self.x
        y = self.y
        powerLevel = y / 50
        powerAdjustment = powerLevel * self.range
        if y < 0:
            powerAdjustment *= 0.70
        rightPowerLevel = 5900
        leftPowerLevel = 5900
        if x > 0:
            rightPowerLevel += (0.6)*powerAdjustment
            leftPowerLevel -= powerAdjustment
        elif x < 0:
            rightPowerLevel += powerAdjustment
            leftPowerLevel -= (0.6)*powerAdjustment
        elif x == 0 and y != 0:
            rightPowerLevel -= powerAdjustment
            leftPowerLevel += powerAdjustment
        return [leftPowerLevel, rightPowerLevel]

    # This function takes in the x and y coordinates of the joy stick and
    # rotates the robot accordingly. Any input in the first or third quadrant
    # will result in the robot turning the right, and any input in the
    # second or forth quadrant will result in the robot turning to the
    # left. This functions returns a list that contains the following
    # information: [leftMotorInput, rightMotorInput, duration]
    # and should be used in the backend script like this:
    #
    # spinAdjustmentList = handleSpinInstruction(x, y)
    # self.tango.setTarget(0, spinAdjustmentList[0])
    # self.tango.setTarget(1, spinAdjustmentList[1])
    # Time.sleep(spinAdjustmentList[2])
    # self.tango.setTarget(0, 5900)
    # self.tango.setTarget(1, 5900)
    #
    '''
    def handleSpinInstruction(self) -> list:
        statusFile = open("status.txt", "r")
        statusFileContents = statusFile.read()
        statusFileContentList = statusFileContents.split(";")
        # ['turning status';'current joystick quadrant']
        statusFile.close()
        if statusFileContentList[0] == "is turning":
            return [0, 0, 0]
        else:
            joystickIsInCurrentQuadrant = self.checkQuadrant()
            needsNewTurn = True
            if joystickIsInCurrentQuadrant:
                needsNewTurn = False
            if not needsNewTurn:
                return [0, 0, 0]
            else:
                x = self.x
                y = self.y
                angleMeasureRadians = math.atan(x / y)
                angleMeasureDegrees = angleMeasureRadians * (180 / math.pi)
                if x < 0 and y < 0:  # Then we are in the third quadrant.
                    angleMeasureDegrees -= 180
                arcLength = 2 * math.pi * (self.wheelDiameter / 2) * (angleMeasureDegrees / 360)
                if arcLength < 0:
                    arcLength *= (-1)
                time = arcLength / self.speed
                leftPowerLevel = 5900
                rightPowerLevel = 5900
                if (x > 0 and y > 0) or (x < 0 and y < 0):  # Then we are in the first or third quadrant.
                    leftPowerLevel += self.spinPowerAdjustment
                    rightPowerLevel += self.spinPowerAdjustment
                elif (x > 0 > y) or (x < 0 < y):
                    leftPowerLevel -= self.spinPowerAdjustment
                    rightPowerLevel -= self.spinPowerAdjustment
                elif x == 0:
                    pass
                elif y == 0:
                    if x > 0:
                        leftPowerLevel -= self.spinPowerAdjustment
                        rightPowerLevel += self.spinPowerAdjustment
                    elif x < 0:
                        leftPowerLevel += self.spinPowerAdjustment
                        rightPowerLevel -= self.spinPowerAdjustment
                x = self.x
                y = self.y
                quadrant = 0
                if x > 0 and y > 0:
                    quadrant = 1
                elif x > 0 and y < 0:
                    quadrant = 2
                elif x < 0 and y < 0:
                    quadrant = 3
                elif x < 0 and y > 0:
                    quadrant = 4
                statusFile = open("status.txt", "w")
                statusFile.write("is turning;"+str(quadrant))
                statusFile.close()
                return [leftPowerLevel, rightPowerLevel, time*4]

    def checkQuadrant(self) -> bool:
        statusFile = open("status.txt", "r")
        statusFileContents = statusFile.read()
        statusFileContentsList = statusFileContents.split(";")
        # ['turning status';'current joystick quadrant']
        currentQuadrant = statusFileContentsList[1]
        statusFile.close()
        x = self.x
        y = self.y
        quadrant = 0
        if x > 0 and y > 0:
            quadrant = 1
        elif x > 0 and y < 0:
            quadrant = 2
        elif x < 0 and y < 0:
            quadrant = 3
        elif x < 0 and y > 0:
            quadrant = 4
        if str(quadrant) == currentQuadrant:
            return True
        else:
            return False

    '''
