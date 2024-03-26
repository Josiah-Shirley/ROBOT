import math
import time
# import serial

class RobotBrainForSensorFinding():
    # t is a tango Object
    def __init__(self, t) -> None:
        self.t = t
        self.distances = {}

    def mainloop(self):
        pass
        # Do this once to get some data to pass
        """
        try:
            ser = serial.Serial()
            ser.port = '/dev/ttyUSB0'
            ser.baudrate = 115200
            ser.bytesize = serial.EIGHTBITS 
            ser.parity =serial.PARITY_NONE 
            ser.stopbits = serial.STOPBITS_ONE 
            ser.timeout = 1
            ser.open()
            time.sleep(1)
            ser.close()
        except Exception as e:
            print(e)
            pass

        ser.open()
        operating = True
        while operating:
            try:
                data=str(ser.readline())
                print(data)
                self.decideWhatToDo(data)
                time.sleep(0.1)
            except Exception as e:
                print(e)
                pass
            except KeyboardInterrupt:
                ser.close()
        """

    def decideWhatToDo(self, data):
        print("Oh boy! Here I go moving again!")
        directionIsKnown = False
        isMovingTowardsAnchor = False
        while not directionIsKnown:
            # get and parse the data repeatedly while figuring things out
            print("What direction am I pointing?...")
            
            directionIsKnown = self.findDirection()

    # takes in distance from anchor in the form of '00000###' 
    # and returns distance in mm as a float.
    def interpretDistance(self, dist) -> float:
        valueList = list(dist)
        toConvert = '0'
        for val in valueList:
            if val != '0':
                toConvert += val
        toReturn = int(toConvert, 16)
        return toReturn
    
    def findDirection(self, cur) -> bool:
        print("hmmm...")
        currentDistanceFromTargetAnchor = cur
        self.t.setTarget(0, 6600)
        self.t.setTarget(1, 6600)
        time.sleep(1)
        self.t.setTarget(0, 5900)
        self.t.setTarget(1, 5900)

    # This method updates the distances dictionary with the current
    # distances from each anchor.
    def getCurrentDistances():
        pass

        
    


robot = RobotBrainForSensorFinding()
print(robot.interpretDistance('00000663'))
