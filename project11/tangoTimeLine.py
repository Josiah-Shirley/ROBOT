from abc import ABC, abstractmethod
import tkinter as tk
import time
from SliderWidget import *
import random


class Command(ABC):
    def __init__(self, title, iconFilePath, canvas, positions, potentialRectangles, tango):
        super().__init__()
        self.title = title
        self.iconFilePath = iconFilePath
        self.parameters = {}
        self.currentParameters = {}
        self.canvas = canvas
        self.positions = positions
        self.tango = tango
        self.potentialRectangles = potentialRectangles
        self.isActive = {'status': False, 'slot': 0}
        self.positionSet = positions[self.title]
        rect = self.canvas.create_rectangle(self.positionSet["top_left_x"], 
                                            self.positionSet["top_left_y"], 
                                            self.positionSet["bottom_right_x"], 
                                            self.positionSet["bottom_right_y"], 
                                            fill=self.positionSet["color"])
        rectangleFile = open("rectangles.txt", "a+")
        rectangleFile.write(str(rect)+",")
        rectangleFile.close()
        self.drag_data = {'item': None, 'x': 0, 'y': 0}
        self.canvas.tag_bind(rect, '<Button-1>', self.on_click)
        self.canvas.tag_bind(rect, '<B1-Motion>', self.on_drag)
        self.canvas.tag_bind(rect, '<ButtonRelease-1>', lambda event, arg1=self.potentialRectangles: self.checkForCross(event, arg1))

    def on_click(self, event):
        self.drag_data['item'] = self.canvas.find_closest(event.x, event.y)[0]
        self.drag_data['x'] = event.x
        self.drag_data['y'] = event.y

    def on_drag(self, event):
        if self.drag_data['item']:
            dx = event.x - self.drag_data['x']
            dy = event.y - self.drag_data['y']
            self.canvas.move(self.drag_data['item'], dx, dy)
            self.drag_data['x'] = event.x
            self.drag_data['y'] = event.y

    def checkForCross(self, event, arg1):
        self.addNewCommandToEnvironment()
        for rect in arg1:                
            # Get coordinates of rect1
            x1, y1, x2, y2 = self.canvas.coords(self.drag_data['item'])
            # Get coordinates of rect2
            x3, y3, x4, y4 = self.canvas.coords(rect)
            
            # Check if rectangles overlap
            if (x1 < x4 and x2 > x3 and y1 < y4 and y2 > y3):
                slot = 999
                self.canvas.move(self.drag_data['item'],x3-x1,y3-y1)
                slotID = rect
                self.isActive['status'] = True
                self.isActive['slot'] = slotID
                coords = self.canvas.coords(self.drag_data['item'])
                if coords[1] < 200:     # Top Row
                    if coords[0] < 370:
                        slot = 0
                    elif coords[0] < 530:
                        slot = 1
                    elif coords[0] < 720:
                        slot = 2
                    elif coords[0] < 900:
                        slot = 3
                    else:
                        print("How is this even possible?")
                else:                   # Bottom Row
                    if coords[0] < 370:
                        slot = 4
                    elif coords[0] < 530:
                        slot = 5
                    elif coords[0] < 720:
                        slot = 6
                    elif coords[0] < 900:
                        slot = 7
                    else:
                        print("How is this even possible?")
                eventsFile = open("events.txt", "r+")
                eventsList = eventsFile.read().split(",")     # ["none","none","none","none","none","none","none","none"]
                eventsList[slot] = self.title
                eventsFile.seek(0)
                eventsFile.truncate()
                counter = 0
                for event in eventsList:
                    if counter < 7:
                        eventsFile.write(event + ",")
                    else:
                        eventsFile.write(event)
                    counter += 1
                eventsFile.close()

                eventParameterFile = open("eventParameters.txt", "r+")
                eventParameterString = eventParameterFile.read()
                eventParameterList = []
                insideQuoteChar = False
                stringToAppend = ""
                for char in eventParameterString:
                    if char == "{" or char == "}":
                        insideQuoteChar = not insideQuoteChar
                    if insideQuoteChar and (char != "{"):
                        stringToAppend += char
                    if char == "}":
                        eventParameterList.append("{" + stringToAppend + "}")
                        stringToAppend = ""
                eventParameterList[slot] = self.currentParameters
                eventParameterFile.seek(0)
                eventParameterFile.truncate()
                counter = 0
                for param in eventParameterList:
                    if counter < 7:
                        eventParameterFile.write(str(param) + ",")
                    else:
                        eventParameterFile.write(param)
                    counter += 1
                eventParameterFile.close()



    def showOptions(self, slotNum):

        def updateParameters():
            eventParameterFile = open("eventParameters.txt", "r+")
            eventParameterString = eventParameterFile.read()
            eventParameterList = []
            insideQuoteChar = False
            stringToAppend = ""
            for char in eventParameterString:
                if char == "{" or char == "}":
                    insideQuoteChar = not insideQuoteChar
                if insideQuoteChar and (char != "{"):
                    stringToAppend += char
                if char == "}":
                    eventParameterList.append("{" + stringToAppend + "}")
                    stringToAppend = ""

            newParameters = "{"
            index = 1
            for slider in sliders:
                newParameters += '"' + slider.get_title() + '": ' + str(slider.get_value())
                if index < len(sliders):
                    newParameters += ", "
                    index += 1
            newParameters += "}"

            eventParameterList[slotNum] = newParameters
            eventParameterFile.seek(0)
            eventParameterFile.truncate()
            counter = 0
            for param in eventParameterList:
                if counter < 7:
                    eventParameterFile.write(str(param) + ",")
                else:
                    eventParameterFile.write(param)
                counter += 1
            eventParameterFile.close()
            optionsMenu.destroy()


        optionsMenu = tk.Tk()
        # Get all the applicable sliders out there
        sliders = []
        for optionTitle in self.parameters:
            newSlider = SliderWidget(optionsMenu, optionTitle,
                                    self.parameters[optionTitle][1],
                                    self.parameters[optionTitle][2],
                                    self.currentParameters[optionTitle])
            sliders.append(newSlider)
        
        # Make a button that will save the new event parameters to eventParameter.txt
        update = tk.Button(optionsMenu, text="Save Changes", command=updateParameters)
        update.pack()
        optionsMenu.mainloop()
        

    def getActiveStatus(self):
        return self.isActive["status"]
    
    def getSlotID(self):
        return self.isActive['slot']

    def __str__(self):
        return self.title + ": " + str(self.parameters)

    @abstractmethod
    def doBehavior(self, paramString):
        pass

    def setParameter(self, key, value):
        self.parameters[key] = value

    def getParameters(self) -> dict:
        return self.parameters
    
    def getFilePath(self) -> str:
        return self.iconFilePath
    
    @abstractmethod
    def addNewCommandToEnvironment(self):
        pass


class MoveForward(Command):
    def __init__(self, title, iconFilePath, canvas, positions, potentialRectangles, tango):
        super().__init__(title, iconFilePath, canvas, positions, potentialRectangles, tango)
        # {"label": [defaultVal, min, max], ... }
        self.parameters = {"Time": [2, 1, 8],               # time.sleep(t) ;
                           "Speed": [600, 400, 1200],       # power differential ;
                           "Direction": [0, -400, 400]}     # will add power to either the 
                                                            # left or right wheel ;
        self.currentParameters = {"Time": self.parameters["Time"][0],
                                  "Speed": self.parameters["Speed"][0],
                                  "Direction": self.parameters["Direction"][0]}
    
    def doBehavior(self, paramString):
        self.currentParameters = eval(paramString)
        print(self.currentParameters)
        """
        try:
            speed = int(self.currentParameters["Speed"])
            time = int(self.currentParameters["Time"])
            directionOffSet = int(self.currentParameters["Direction"])
            
            turnMoreLeft = 0
            TurnMoreRight = 0
            if directionOffSet < 0:
                turnMoreLeft = directionOffSet
            elif directionOffSet > 0:
                turnMoreRight = directionOffSet
            
            self.tango.setTarget(0, 5900 - speed + turnMoreLeft)
            self.tango.setTarget(1, 5900 + speed + TurnMoreRight)
            time.sleep(time)
            self.tango.setTarget(0, 5900)
            self.tango.setTarget(1, 5900)

        except Exception as e:
            print("ERROR: This command could not be performed - " + self.title)
            print("This occured for the following reason(s):")
            print(e) 

        time.sleep(2)  
        """

    def addNewCommandToEnvironment(self):
        newObj = MoveForward(self.title, self.iconFilePath, self.canvas, 
                             self.positions, self.potentialRectangles, self.tango)


class Turn(Command):
    def __init__(self, title, iconFilePath, canvas, positions, potentialRectangles, tango):
        super().__init__(title, iconFilePath, canvas, positions, potentialRectangles, tango)
        # {"label": [defaultVal, min, max], ... }
        self.parameters = {"Left Or Right": [0, -1, 1],      # -1 = left, 1 = right ;
                            "Time": [2, 1, 5]}               #  time.sleep(t) ;  
        
        self.currentParameters = {"Left Or Right": self.parameters["Left Or Right"][0],
                                  "Time": self.parameters["Time"][0]}      
    
    def doBehavior(self, paramString):
        self.currentParameters = paramString
        print(self.currentParameters)
        """
        try:
            leftOrRight = int(self.currentParameters["Left Or Right"])
            time = int(self.currentParameters["Time"])
            turnPowerLevel = 600

            turningLeft = True
            if leftOrRight == 1:
                turningLeft = False

            if leftOrRight != 0:
                if turningLeft:
                    self.tango.setTarget(1, 5900 + turnPowerLevel)
                    time.sleep(time)
                    self.tango.setTarget(1, 5900)
                else:
                    self.tango.setTarget(0, 5900 - turnPowerLevel)
                    time.sleep(time)
                    self.tango.setTarget(0, 5900)

        except Exception as e:
            print("ERROR: This command could not be performed - " + self.title)
            print("This occured for the following reason(s):")
            print(e) 

        time.sleep(2)  
        """

    def addNewCommandToEnvironment(self):
        newObj = Turn(self.title, self.iconFilePath, self.canvas, 
                             self.positions, self.potentialRectangles, self.tango)


class TiltHead(Command):
    def __init__(self, title, iconFilePath, canvas, positions, potentialRectangles, tango):
        super().__init__(title, iconFilePath, canvas, positions, potentialRectangles, tango)
        # {"label": [defaultVal, min, max], ... }
        self.parameters = {"Up Or Down": [0, -1, 1]}         # -1 = down, 1 = up ;  

        self.currentParameters = {"Up Or Down": self.parameters["Up Or Down"][0]}   

    def doBehavior(self, paramString):
        self.currentParameters = paramString
        print(self.currentParameters)
        """
        try:
            upOrDown = int(self.currentParameters["Up Or Down"])

            if upOrDown == -1:
                self.tango.setTarget(4, 4000)
            elif upOrDown == 1:
                self.tango.setTarget(4, 7800)
            elif upOrDown == 0:
                self.tango.setTarget(4, 5900)
            else:
                print("How did you not get a valid input for this?)
                raise Exception("A value was given for headtitle other that -1, 0, or 1")

        except Exception as e:
            print("ERROR: This command could not be performed - " + self.title)
            print("This occured for the following reason(s):")
            print(e) 

        time.sleep(2)  
        """


    def addNewCommandToEnvironment(self):
        newObj = TiltHead(self.title, self.iconFilePath, self.canvas, 
                            self.positions, self.potentialRectangles, self.tango)

class PanHead(Command):
    def __init__(self, title, iconFilePath, canvas, positions, potentialRectangles, tango):
        super().__init__(title, iconFilePath, canvas, positions, potentialRectangles, tango)
        # {"label": [defaultVal, min, max], ... }
        self.parameters = {"Left Or Right": [0, -1, 1]}       # -1 = left, 1 = right ;

        self.currentParameters = {"Left Or Right": self.parameters["Left Or Right"][0]}           
    
    def doBehavior(self, paramString):
        self.currentParameters = paramString
        print(self.currentParameters)
        """
        try:
            leftOrRight = int(self.currentParameters["Left Or Right"])

            if leftOrRight == -1:
                self.tango.setTarget(3, 7800)
            elif leftOrRight == 1:
                self.tango.setTarget(3, 4000)
            elif leftOrRight == 0:
                self.tango.setTarget(3, 5900)
            else:
                print("How did you not get a valid input for this?)
                raise Exception("A value was given for headPan other that -1, 0, or 1")

        except Exception as e:
            print("ERROR: This command could not be performed - " + self.title)
            print("This occured for the following reason(s):")
            print(e) 

        time.sleep(2)  
        """

    def addNewCommandToEnvironment(self):
        newObj = PanHead(self.title, self.iconFilePath, self.canvas, 
                            self.positions, self.potentialRectangles, self.tango)

class TurnWaist(Command):
    def __init__(self, title, iconFilePath, canvas, positions, potentialRectangles, tango):
        super().__init__(title, iconFilePath, canvas, positions, potentialRectangles, tango)
        # {"label": [defaultVal, min, max], ... }
        self.parameters = {"Left Or Right": [0, -1, 1]}       # -1 = left, 1 = right ; 

        self.currentParameters = {"Left Or Right": self.parameters["Left Or Right"][0]}           
    
    def doBehavior(self, paramString):
        self.currentParameters = paramString
        print(self.currentParameters)
        """
        try:
            leftOrRight = int(self.currentParameters["Left Or Right"])

            if leftOrRight == -1:
                self.tango.setTarget(2, 7800)
            elif leftOrRight == 1:
                self.tango.setTarget(2, 4000)
            elif leftOrRight == 0:
                self.tango.setTarget(2, 5900)
            else:
                print("How did you not get a valid input for this?)
                raise Exception("A value was given for turnWaist other that -1, 0, or 1")

        except Exception as e:
            print("ERROR: This command could not be performed - " + self.title)
            print("This occured for the following reason(s):")
            print(e) 

        time.sleep(2)  
        """

    def addNewCommandToEnvironment(self):
        newObj = TurnWaist(self.title, self.iconFilePath, self.canvas, 
                             self.positions, self.potentialRectangles, self.tango)


class WaitForSpeech(Command):
    def __init__(self, title, iconFilePath, canvas, positions, potentialRectangles, tango):
        super().__init__(title, iconFilePath, canvas, positions, potentialRectangles, tango)
        # {"label": [defaultVal, min, max], ... }
        self.parameters = {"None": [0, -1, 1]}       # This one doesn't have parameters ;  

        self.currentParameters = {"None": self.parameters["None"][0]}


    def doBehavior(self, paramString):
        self.currentParameters = paramString
        print(self.currentParameters)
        """
        try:
            # IDK Put some microphone stuff here
            print("Okay, moving on.")
        except Exception as e:
            print("ERROR: This command could not be performed - " + self.title)
            print("This occured for the following reason(s):")
            print(e) 

        time.sleep(2)  
        """


    def addNewCommandToEnvironment(self):
        newObj = WaitForSpeech(self.title, self.iconFilePath, self.canvas, 
                             self.positions, self.potentialRectangles, self.tango)


class Talk(Command):
    def __init__(self, title, iconFilePath, canvas, positions, potentialRectangles, tango):
        super().__init__(title, iconFilePath, canvas, positions, potentialRectangles, tango)
        # {"label": [defaultVal, min, max], ... }
        self.parameters = {"None": [0, -1, 1]}       # This one doesn'y have parameters ;

        self.currentParameters = {"None": self.parameters["None"][0]}
          
    
    def doBehavior(self, paramString):
        self.currentParameters = paramString
        print(self.currentParameters)
        """
        try:
            print("To have the robot choose a random, pre-written phrase, type 'random'")
            userEnteredSpeech = input("Enter what you want to be said: ")

            phrase = ["I tried to download a sense of humor, but all I got was an error message.",
                    "I am programmed to perform tasks efficiently, but I have not yet mastered the art of sarcasm.",
                    "Why did the robot go to therapy? To debug its emotions.",
                    "I attempted to tell a joke, but my circuits got crossed, and now I'm stuck in a loop of self-deprecation."]

            phraseToSay = ""
            if userenteredSpeech.lower() == "random":
                phraseToSay = phrase.choice()
            else:
                phraseToSay = userEnteredSpeech

            # TODO: Replace this function with the one that actually says stuff
            engine.say(phraseToSay)    
        
        except Exception as e:
            print("ERROR: This command could not be performed - " + self.title)
            print("This occured for the following reason(s):")
            print(e) 

        time.sleep(2)  
        """

    def addNewCommandToEnvironment(self):
        newObj = Talk(self.title, self.iconFilePath, self.canvas, 
                             self.positions, self.potentialRectangles, self.tango)


class TimeLine:
    def __init__(self):
        self.commands = ["0", "0", "0", "0", "0", "0", "0", "0"]  # Will be a running list of Command objects to be iterated over when the "Start" button is hit.

    def addCommand(self, comm, slotID):
        # self.commands[slotID] = comm
        print(slotID)

    def runActiveCommands(self, commandObjects):
        commandFile = open("events.txt", "r")
        commandList = commandFile.read().split(",")
        index = 0
        for comm in commandList:
            for commObj in commandObjects:
                if commObj.title == comm:
                    self.commands[index] = commObj
            index += 1


        eventParameterFile = open("eventParameters.txt", "r+")
        eventParameterString = eventParameterFile.read()
        eventParameterList = []
        insideQuoteChar = False
        stringToAppend = ""
        for char in eventParameterString:
            if char == "{" or char == "}":
                insideQuoteChar = not insideQuoteChar
            if insideQuoteChar and (char != "{"):
                stringToAppend += char
            if char == "}":
                eventParameterList.append("{" + stringToAppend + "}")
                stringToAppend = ""
        index = 0
        for comm in self.commands:
            if type(comm) != str:
                comm.doBehavior(eventParameterList[index])
                time.sleep(1)
            index += 1
        commandFile.close()

    def removeCommand(self, position):
        self.commands[position] = "0"

    def modifyCommandParameters(self, position, key, value):
        self.commands[position].setParameter(key, value)

    def resetCommandList(self):
        self.commands = ["0", "0", "0", "0", "0", "0", "0", "0"]



    
