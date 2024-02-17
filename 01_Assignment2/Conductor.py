import math


class Conductor:
    def __init__(self, x, y, r=2000):
        self.x = x
        self.y = y
        self.range = r
        # These values are placeholders and should be replaced with the real world values
        # once they are calculated
        self.speed = 2.2  # <-- measured in ft/s
        self.wheelDiameter = 2.1  # <-- measured in ft
        self.spinPowerAdjustment = 500  # <-- this is the amount of power that will be
        #     given to the wheels while spinning in place

    def setRange(self, r):
        self.range = r

    # This function handles the forward and backward movement signal
    # which need to be sent to the robot. The function takes in the
    # 'y' coordinate and turns it into the proper motor inputs
    # and returns a list containing those motor impulses.
    # The list should be used in the backend controller like this:
    #
    # motorInputList = handleForwardAndBackwardMovement(y) <-- Be sure that this is the post
    # self.tango.setTarget(0, motorInputList[0])                adjustment y value (i.e. 50
    # self.tango.setTarget(1, motorInputList[1])                has already been subtracted.)
    #
    def handleForwardAndBackwardMovement(self, y) -> list:
        powerLevel = y / 50
        powerAdjustment = powerLevel * self.range
        rightPowerLevel = 5900 + powerAdjustment
        leftPowerLevel = 5900 - powerAdjustment
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
    def handleSpinInstruction(self, x, y) -> list:
        angleMeasureRadians = math.atan(y / x)
        angleMeasureDegrees = angleMeasureRadians * (180 / math.pi)
        if x < 0 and y < 0:  # Then we are in the third quadrant.
            angleMeasureDegrees -= 180
        arcLength = 2 * math.pi * (self.wheelDiameter / 2) * (angleMeasureDegrees / 360)
        time = arcLength / self.speed
        leftPowerLevel = 5900
        rightPowerLevel = 5900
        if (x > 0 and y > 0) or (x < 0 and y < 0):  # Then we are in the first or third quadrant.
            leftPowerLevel -= self.spinPowerAdjustment
            rightPowerLevel += self.spinPowerAdjustment
        elif (x > 0 > y) or (x < 0 < y):
            leftPowerLevel += self.spinPowerAdjustment
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
        return [leftPowerLevel, rightPowerLevel, time]
    