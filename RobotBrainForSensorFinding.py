import math
import time
import serial

# TODO:
#   1. Measure how far the robot goes when given a power differential of 600 for time.sleep(1)
#       and put that in for self.testDistance

class RobotBrainForSensorFinding():
    # t is a tango Object
    def __init__(self, tango) -> None:
        self.t = tango
        self.targetAnchor = ""
        # These are the bindings for which index position the distance from each anchor can
        # be found at. "self.A = 2" means that the distance to anchor A is found at position
        # 2 (i.e. is the first anchor distance given when the string of all distances is fetched.)
        self.A = 2
        self.B = 3
        self.C = 4
        self.D = 5
        # This needs to be updated with the actual distance traveled by the bot in mm
        self.testDistance = 220
        # NO TOUCHY!!!
        self.testMovePowerLevel = 900   # mm
        self.testMoveDuration = 1       # second(s)
        # The distance between the outer edges of the robots two front wheels in mm
        self.robotDiameter = 442.9125
        # Didn't turn all the way? Increase this value to give her some more juice!
        self.giveHerSomeMoreJuice = 150
        self.minimumCloseness = 2000    # mm

    def setTargetAnchor(self, anchor):
        self.targetAnchor = anchor

    def getTestMoveDistance(self):
        return self.testDistance

    def getRobotRadius(self):
        return self.robotDiameter/2

    def getTestMoveTime(self):
        return self.testMoveDuration

    def getTestMovePowerLevel(self):
        return self.testMovePowerLevel

    def mainloop(self, anchor):
        try:
            self.targetAnchor = anchor.lower()
            preMoveDistance = self.fetchDistances()[self.targetAnchor]
            if preMoveDistance == "ERROR: NOT GETTING SINGAL FROM THIS ANCHOR":
                print("Something is wrong with the target anchor...")
                print("Target Anchor:", self.targetAnchor)
            else:
                # NOTE: If it moves backwards instead of forwards at this point, switch the plus and minus
                self.tentativelyMoveForward()
                postMoveDistance = self.fetchDistances()[self.targetAnchor]
                if postMoveDistance == "ERROR: NOT GETTING SINGAL FROM THIS ANCHOR":
                    self.throwAnchorError()
                self.shamefullyMoveBackwards()
                # Law of Cosines:
                numerator = ((self.testDistance**2) + (preMoveDistance**2)) - (postMoveDistance**2)
                print("test dist:",self.testDistance)
                print("Pre-move dist:",preMoveDistance)
                print("Post-move dist:",postMoveDistance)
                denominator = 2 * self.testDistance * preMoveDistance
                print("Numerator:", numerator)
                print("Denominator:",denominator)
                radians = math.acos(numerator/denominator)
                angle = radians * (180 / math.pi)
                distanceToTurn = radians*(self.robotDiameter/2)
                print("Distance to turn:",distanceToTurn)
                print("Angle (radians):",radians)
                print("Angle (degrees):",angle)
                self.makeTurn(distanceToTurn)
                status = "failure"
                preMoveDistance = self.fetchDistances()[self.targetAnchor]
                self.tentativelyMoveForward()
                postMoveDistance = self.fetchDistances()[self.targetAnchor]
                if postMoveDistance >= preMoveDistance:
                    # Move back to where you started
                    self.shamefullyMoveBackwards()
                    # Rotate twice
                    self.makeTurn(((2*math.pi)-(2*radians))*(self.robotDiameter/2))
                    preMoveDistance = self.fetchDistances()[self.targetAnchor]
                    self.tentativelyMoveForward()
                    postMoveDistance = self.fetchDistances()[self.targetAnchor]
                    if postMoveDistance >= preMoveDistance:
                        print("HHHHHEEEEEEEEELLLLLLLLLLLPPPPPPPPP!!!!!!!!")
                    else:
                        self.continueOnToAnchor()
                else:
                    result = self.tryTheOtherWayToMakeSure(postMoveDistance, radians, distanceToTurn)
                    if result:
                        self.continueOnToAnchor()
        except Exception as e:
            self.t.setTarget(0, 5900)
            self.t.setTarget(1, 5900)
            print("Something went wrong with mainloop:")
            print(e)

    def tryTheOtherWayToMakeSure(self, pmd, radians, dtt):
        # Move back to where you started
        self.shamefullyMoveBackwards()
        # Rotate twice
        self.makeTurn(((2*math.pi)-(2*radians))*(self.robotDiameter/2))
        preMoveDistance = self.fetchDistances()[self.targetAnchor]
        self.tentativelyMoveForward()
        postMoveDistance = self.fetchDistances()[self.targetAnchor]
        if pmd > postMoveDistance:
            self.continueOnToAnchor()
            return False
        else:
            self.makeTurn(dtt*2)
            return True


    def tentativelyMoveForward(self):
        self.t.setTarget(0, 5900 - self.testMovePowerLevel)
        self.t.setTarget(1, 5900 + self.testMovePowerLevel)
        time.sleep(self.testMoveDuration)
        self.t.setTarget(0, 5900)
        self.t.setTarget(1, 5900)

    def shamefullyMoveBackwards(self):        
        self.t.setTarget(0, 5900 + self.testMovePowerLevel)
        self.t.setTarget(1, 5900 - self.testMovePowerLevel)
        time.sleep(self.testMoveDuration)
        self.t.setTarget(0, 5900)
        self.t.setTarget(1, 5900)

    def makeTurn(self, distanceToTurn):
        speed = self.testDistance/self.testMoveDuration
        timeToMoveFor = distanceToTurn/speed
        self.t.setTarget(0, 5900 - self.testMovePowerLevel - self.giveHerSomeMoreJuice)
        print("Time to turn for:", timeToMoveFor)
        time.sleep(abs(timeToMoveFor))
        self.t.setTarget(0, 5900)
        self.t.setTarget(1, 5900)

    def notThatWayTryTheOtherWay(self, distanceToTurn):
        speed = self.testDistance/self.testMoveDuration
        timeToMoveFor = distanceToTurn/speed
        for _ in range(2):
            self.t.setTarget(0, 5900 - self.testMovePowerLevel - self.giveHerSomeMoreJuice)
            time.sleep(timeToMoveFor)
            self.t.setTarget(0, 5900)
            self.t.setTarget(1, 5900)

    def continueOnToAnchor(self):
        remainingDistance = self.fetchDistances()[self.targetAnchor]
        print("RemainingDistance:",remainingDistance)
        speed = self.testDistance/self.testMoveDuration
        print("Speed:",speed)
        timeToMoveFor = remainingDistance/speed
        print("Time to move for:",timeToMoveFor)
        self.t.setTarget(0, 5900 - self.testMovePowerLevel)
        self.t.setTarget(1, 5900 + self.testMovePowerLevel)
        time.sleep(timeToMoveFor/2.3)
        self.t.setTarget(0, 5900)
        self.t.setTarget(1, 5900)
        currentDistance = self.fetchDistances()[self.targetAnchor]
        print("Final Distance:",currentDistance)
        print("EXITED!")

    # takes in distance from anchor in the form of '00000###' 
    # and returns distance in mm as a float.
    def interpretDistance(self, dist) -> int:
        if dist == "ffffffff":
            self.throwAnchorError()
        dist = dist.lstrip("0")  # Remove leading zeros
        if not dist:  # If the string becomes empty after stripping zeros
            dist = "0"  # Set it to "0" to represent zero
        return int(dist, 16)

    def getCurrentDistances(self) -> dict:
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
            print("ERROR IN FIRST TRY OF GET DISTANCES:",e)
            pass
        ser.open()
        searching = True
        toReturn = {}
        while searching:
            try:
                # data looks like this when it first gets here
                # mc 0f 00000663 000005a3 00000512 000004cb  ffffffff ffffffff ffffffff 095f c1 00146fb7 a0:0 22be
                # 0  1  2        3        4        5        6        7        8        9        10   11 12       13   14
                data=str(ser.readline())
                # print(data)
                dataList = data.split(" ")
                status = "failure"
                if "ffffffff" not in dataList:
                    status = "success"
                toReturn = {
                    "a":self.interpretDistance(dataList[self.A]),
                    "b":self.interpretDistance(dataList[self.B]),
                    "c":self.interpretDistance(dataList[self.C]),
                    "d":self.interpretDistance(dataList[self.D])
                    }
                return toReturn
            except Exception as e:
                print("ERROR IN SECOND TRY IN GET DISTANCES:",e)
            except KeyboardInterrupt:
                ser.close()

    def fetchDistances(self):
        distances = {}
        gettingTargetDistance = True
        while gettingTargetDistance:
            distances = self.getCurrentDistances()
            gettingTargetDistance = False            
            for value in distances:
                if value == 4294967295:
                    gettingTargetDistance = True
        return distances

    def ravioliRavioliGiveMeTheDistanceolis(self):
        dict1 = self.fetchDistances()
        dict2 = self.fetchDistances()
        dict3 = self.fetchDistances()
        dict4 = self.fetchDistances()
        dict5 = self.fetchDistances()

        dictToReturn = {"a": 0, "b": 0, "c": 0, "d": 0}
        for key in dictToReturn:
            val1 = dict1[key]
            val2 = dict1[key]
            val3 = dict1[key]
            val4 = dict1[key]
            val5 = dict1[key]
            toAdd = (val1 + val2 + val3 + val4 + val5)/5
            dictToReturn[key] = toAdd
        return dictToReturn

    def throwAnchorError(self):
        print("*******************************************************")
        print("A signal could not be received from at least one anchor")
        print("*******************************************************")
