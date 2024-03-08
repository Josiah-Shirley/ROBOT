import time
import tkinter as tk
import threading
import math
import random
from time import sleep
from TTS import *
import speech_recognition as sr

class Face(tk.Tk):
    def __init__(self):
        super().__init__()
        self.attributes('-fullscreen', True)
        self.canvas = tk.Canvas(self, bg='white')
        self.bind('<Escape>', lambda e: self.destroy())
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.width = self.winfo_screenwidth()
        self.height = self.winfo_screenheight()

        # Eye attributes
        self.eye_radius = 80
        self.eye_size = 300
        self.eye_spacing = 500
        self.eye_color = 'black'
        self.eye1_x = self.width // 2 - self.eye_spacing // 2
        self.eye1_y = self.height // 2 - 50
        self.eye2_x = self.width // 2 + self.eye_spacing // 2
        self.eye2_y = self.height // 2 - 50
        # Pupil attributes
        self.pupil_radius = 30
        self.pupil_color = 'white'
        self.pupil1_x = self.eye1_x
        self.pupil1_y = self.eye1_y
        self.pupil2_x = self.eye2_x
        self.pupil2_y = self.eye2_y
        # Mouth attributes
        self.mouth_width = 200
        self.mouth_height = 100
        self.mouth_color = 'red'
        self.mouth_y = self.height // 2 + 200

        # Create eyes
        self.eye1 = self.canvas.create_oval(self.eye1_x - self.eye_size // 2, self.eye1_y - self.eye_size // 2,
                                            self.eye1_x + self.eye_size // 2, self.eye1_y + self.eye_size // 2,
                                            fill=self.eye_color, outline='')
        self.eye2 = self.canvas.create_oval(self.eye2_x - self.eye_size // 2, self.eye2_y - self.eye_size // 2,
                                            self.eye2_x + self.eye_size // 2, self.eye2_y + self.eye_size // 2,
                                            fill=self.eye_color, outline='')
        # Create pupils
        self.pupil1 = self.canvas.create_oval(self.pupil1_x - self.pupil_radius, self.pupil1_y - self.pupil_radius,
                                               self.pupil1_x + self.pupil_radius, self.pupil1_y + self.pupil_radius,
                                               fill=self.pupil_color, outline='')
        self.pupil2 = self.canvas.create_oval(self.pupil2_x - self.pupil_radius, self.pupil2_y - self.pupil_radius,
                                               self.pupil2_x + self.pupil_radius, self.pupil2_y + self.pupil_radius,
                                               fill=self.pupil_color, outline='')
        # Create Mouth
        self.mouth = self.canvas.create_rectangle(self.width // 2 - self.mouth_width // 2,
                                                  self.mouth_y - self.mouth_height // 2,
                                                  self.width // 2 + self.mouth_width // 2,
                                                  self.mouth_y + self.mouth_height // 2,
                                                  fill=self.mouth_color, outline='')

        # Start threads for animations
        threading.Thread(target=self.listenAnimation, daemon=True).start()
        threading.Thread(target=self.talkAnimation, daemon=True).start()
        threading.Thread(target=self.walkingAnimation, daemon=True).start()
        threading.Thread(target=self.speechEngine, daemon=True).start()

        self.isTalking = False
        self.isWalking = False
        self.isPupils = False

        self.sweating_image = tk.PhotoImage(file="sweat.png")
        self.smaller_image = self.sweating_image.subsample(7, 7)
        self.sweat_droplets = []

    def speechEngine(self):
        def haveConversation():
            dt = DialogueTemplate("dialogTestFile.txt")
            dt.interpretLines()
            # dt.printPrimaryInputPairs()

            # Uncomment the following for final product...
            """
            listening = True
            r = sr.Recognizer()

            while listening:
                with sr.Microphone() as source:
                    r.adjust_for_ambient_noise(source)
                    r.dynamic_energy_threshold = 500

                    try:
                    # Listen for user input
                        print("listening...")
                        audio = r.listen(source)
                        print("{processing audio...}")
                    # Process user input
                        word = r.recognize_google(audio)
                    # Figure out which reply to give
                        response = dt.findResponse(word)
                    # Give a reply
                        print(response)    # <-- Replace print with TTS
                    except sr.UnknownValueError:
                        print("..Unknown Word..")
            """
            # The following block of code is for testing without a micriphone
            listening = True
            while listening:
                print("Ready To Test...")
                word = input(">>> ")
                if word == "stop":
                    break
                response = dt.findResponse(word)
                print(response)
            # End microphoneless testing block
            

        class DialogueTemplate():
            def __init__(self, textFile):
                self.textFile = textFile
                self.primaryInputPairs = []
                self.activeUserInputPairs = []
                self.allInputPairs = []
                self.variablesList = []
                self.userInputObjectList = []

            def __str__(self):
                toReturn = "{"
                for pair in self.primaryInputPairs:
                    toReturn += pair + " | "
                toReturn += "}"
                return toReturn
                
            def interpretLines(self):
                dialogueFile = open(self.textFile, "r")
                # "For each line in the dialogue text file..."
                for line in dialogueFile:
                    # tokens = ['#', '~', 'u']
                    # "If it isn't a blank line..."
                    if line != "\n":
                        # "Take the first character in the line..."
                        firstChar = list(line)[0]
                        # "If that first charater is a tilda..."
                        if firstChar == "~":
                            variableObject = Variable(line)
                            self.variablesList.append(variableObject)
                        # "If that first character is a 'u' (Dont worry if it has a number or not just yet)..."
                        elif firstChar == "u":
                            irp = ""
                            hasUserInput = False
                            for word in line:
                                if word == "_":
                                    irp = InputResponsePairWithUserInfo(line)
                                    self.userInputObjectList.append(irp.getUserInfoObject())
                                    hasUserInput = True
                            if not hasUserInput:    
                                irp = InputResponsePair(line)
                            # "Make an input response pair object with that line..."
                            self.allInputPairs.append(irp)
                            # "Get the second character in the line..."
                            nextChar = list(line)[1]
                            # "If it is a ':' it means that it is the highest level of possible user inputs
                            # and should always be listened for..."
                            if nextChar == ":":
                                # "So add it to the primary input pair list (A list of these highest level
                                # possible user inputs.)"
                                self.primaryInputPairs.append(irp)
                            # "Otherwise, it is some lower level of user input and should sometimes be listened for..."
                            else:
                                #print("Oh boy! Here comes a subpair!")
                                pointer = self.primaryInputPairs[len(self.primaryInputPairs)-1]
                                #print("pointer is currently pointing to:", pointer)
                                for _ in range(int(nextChar)-1):
                                    pointer = pointer.getSubpairs()[len(pointer.getSubpairs())-1]
                                #print("pointer is now pointing to:", pointer)
                                #print("The IRP that was just added to pointer was:", irp)
                                pointer.addSubpair(irp)
                                #print("Pointer's subpairs are:")
                for pair in self.primaryInputPairs:
                    self.activeUserInputPairs.append(pair)
                dialogueFile.close()
                for pair in self.allInputPairs:
                    pair.setVariablesList(self.variablesList)

            def printPrimaryInputPairs(self):
                for pair in self.primaryInputPairs:
                    print(pair)

            def printActiveInputPairs(self):
                for pair in self.activeUserInputPairs:
                    print(pair)

            def findResponse(self, userInput) -> str:
                response = ""
                foundResponse = False
                # Check all active pairs for a valid user input
                for pair in self.activeUserInputPairs:
                    for input in pair.getPossibleInputs():
                        indexOfUnderscore = 0
                        if "_" in input:
                            currentIndex = 0
                            inputList = input.split(" ")
                            for word in inputList:
                                if word != "_":
                                    currentIndex += 1
                                else:
                                    indexOfUnderscore = currentIndex
                        inputToTest = input.split(" ")
                        inputToTest.pop(indexOfUnderscore)
                        inputWithoutSpaces = "".join(inputToTest)
                        userInputToTest = userInput.split(" ")
                        possibleUserInputObjectValue = userInputToTest.pop(indexOfUnderscore)
                        userInputWithoutSpaces = "".join(userInputToTest)
                        if userInputWithoutSpaces == inputWithoutSpaces:
                            userInputObjectName = ""
                            possibleResponse = pair.getResponses()
                            responseList = possibleResponse.split(" ")
                            for word in responseList:
                                if len(word) > 0:     
                                    if word[0] == "$":
                                        userInputObjectName = word[1:]
                            self.setUserInfoObjectValue(userInputObjectName, possibleUserInputObjectValue)
                            for pair in self.allInputPairs:
                                pair.addUserInfoObjectValue(userInputObjectName, possibleUserInputObjectValue)
                            response = pair.getResponses()
                            foundResponse = True
                    #print("Current pair being checked:", pair)
                    #print("Here are all the subpairs for the current IRP:", pair.getSubpairs())
                    subpairs = pair.getSubpairs()
                    if userInput in pair.getPossibleInputs():
                        foundResponse = True
                        #print("It's a match! Here's all the possible responses:", pair.getResponses())
                        response = pair.getResponses()
                        # If the latest input is a primary input, deactivate all previous subpairs.
                        if pair in self.primaryInputPairs:
                            self.activeUserInputPairs.clear()
                            for irp in self.primaryInputPairs:
                                self.activeUserInputPairs.append(irp)
                        # Activate any subpairs of the current pair.
                        #print("Here are all the subpairs for the current IRP:", pair.getSubpairs())
                        for subPair in subpairs:
                            #print("Current subpair being added to active IRP list:", subPair)
                            self.activeUserInputPairs.append(subPair)
                if not foundResponse:
                    response = "This does not appear to be an input I am prepared to handle..."
                    response += "\n" + "'" + userInput + "'"
                return response
            
            def setUserInfoObjectValue(self, name, value) -> bool:
                for userInfoObject in self.userInputObjectList:
                    if userInfoObject.getName()[1:] == name:
                        userInfoObject.setCurrentValue(value)
                        return True
                return False

            def getUserInfoObject(self, name):
                for userInfoObject in self.userInputObjectList:
                    if userInfoObject.getName() == name:
                        return userInfoObject

        class InputResponsePair():
            def __init__(self, line) -> None:
                # A line looks like this:
                # u:(user input):robot response
                self.line = line
                # This results in a list that looks like this:
                # ["u","(user input)","robot response"]
                self.lineComponents = self.line.split(":")
                # This should be: "(user input)"
                self.userInput = self.lineComponents[1]
                # This should be: "robot response"
                self.responses = self.lineComponents[2]
                self.subPairs = []      # <-- This will be a list of InputResponsePair objects
                self.variablesList = []
                self.userInfoDict = {}

            def __str__(self):
                return self.line

            def getLineDepth(self) -> int:
                if list(self.line)[1] != ":":
                    toReturn = int(list(self.line)[1])
                    return toReturn
                else:
                    return 0
                
            def getPossibleInputs(self) -> list:
                unprocessedPossibleInputs = self.userInput.strip(")(")
                if unprocessedPossibleInputs[0] == "~":
                    variableObject = self.getVariableByName(unprocessedPossibleInputs.strip("~"))
                    possibleInputs = variableObject.getValues()
                else:
                    possibleInputs = [unprocessedPossibleInputs] 
                return possibleInputs
            
            def getResponses(self) -> str:
                toReturn = ""
                if self.responses[0] == "[":
                    values = []
                    tempList = self.responses.replace("[","").replace("]","").split(",")
                    for value in tempList:
                        toAppend = ""
                        valueList = list(value)
                        if '"' in valueList:
                            toAppend = value[1:len(value)-1]
                            if toAppend[0] == '"':
                                toAppend = toAppend[1:]
                        else:
                            toAppend = value[1:len(value)]
                        tempString = toAppend.split("\n")
                        toAppend = "".join(tempString)
                        values.append(toAppend)
                    toReturn = random.choice(values)
                elif self.responses[0] == "~":
                    variableObject = self.getVariableByName(self.responses[1:])
                    toReturn = variableObject.getRandomValue()
                else:
                    responseList = self.responses.split(" ")
                    for word in responseList:
                        if word[0] == "$":
                            key = word[1:]
                            toReturn += self.userInfoDict[key]
                        else:
                            toReturn += word
                        toReturn += " "
                return toReturn
            
            def getSubpairs(self):
                return self.subPairs
            
            def addSubpair(self, irp):
                self.subPairs.append(irp)

            def printAllSubpairs(self):
                for pair in self.subPairs:
                    print(pair)

            def setVariablesList(self, l):
                self.variablesList = l

            def getVariableByName(self, n):
                for var in self.variablesList:
                    if var.getName() == n:
                        return var

            def addUserInfoObjectValue(self, name, value):
                self.userInfoDict[name] = value


        class InputResponsePairWithUserInfo(InputResponsePair):
            def __init__(self, line) -> None:
                super().__init__(line)
                userInfoName = ""
                append = False
                for char in self.responses:
                    if char == "$":
                        append = True
                    if char == " ":
                        append = False
                    if append:
                        userInfoName += char
                ui = UserInfo(userInfoName)
                self.userInfoObject = ui

            def getUserInfoObject(self):
                return self.userInfoObject
            
            def getResponses(self) -> str:
                toReturn = ""
                if self.userInfoObject.getCurrentValue() == "":
                    toReturn = "\n" + "()()()This response contains a variable whose value has not been set yet()()()" + "\n"
                else:
                    line = self.responses
                    lineList = line.split(" ")
                    for word in lineList:
                        if word[0] == "$":
                            toReturn += self.userInfoObject.getCurrentValue()
                        else:
                            toReturn += word
                        toReturn += " "
                return toReturn

        class UserInfo():
            def __init__(self, name) -> None:
                self.name = name
                self.value = ""
            
            def setCurrentValue(self, v) -> None:
                self.value = v

            def getCurrentValue(self) -> str:
                return self.value
            
            def getName(self) -> str:
                return self.name


        class Variable():
            def __init__(self, line):
                self.componentList = line.split(":")
                self.values = []
                tempString = self.componentList[1]
                tempList = tempString.replace("[","").replace("]","").split(",")
                for value in tempList:
                    toAppend = ""
                    valueList = list(value)
                    if '"' in valueList:
                        tempString = value.strip('"')
                        toAppend = tempString[1:len(value)-1]
                        if toAppend[0] == '"':
                            toAppend = toAppend[1:]
                    else:
                        toAppend = value[1:len(value)]
                    tempString = toAppend.split("\n")
                    toAppend = "".join(tempString)
                    self.values.append(toAppend)
                self.name = self.componentList[0].strip("~")
            
            def __str__(self) -> str:
                return self.name + ": " + str(self.values)
            
            def getValues(self):
                return self.values
            
            def getName(self):
                return self.name
            
            def getRandomValue(self):
                return random.choice(self.values)



        haveConversation()
        
    def idleFace(self):
        self.isTalking = False
        self.isPupils = True
        self.reset_pupils()

    def reset_pupils(self):
        self.canvas.coords(self.pupil1, self.pupil1_x - self.pupil_radius,
                           self.pupil1_y - self.pupil_radius,
                           self.pupil1_x + self.pupil_radius, self.pupil1_y + self.pupil_radius)
        self.canvas.coords(self.pupil2, self.pupil2_x - self.pupil_radius,
                           self.pupil2_y - self.pupil_radius,
                           self.pupil2_x + self.pupil_radius, self.pupil2_y + self.pupil_radius)

    def talkingFace(self):
        self.isWalking = False
        self.isTalking = True

    def walkingFace(self):
        self.isTalking = False
        self.isWalking = True

    def listenAnimation(self):
        while True:
            # Randomly move pupils if in idle state
            if self.isPupils:
                self.move_pupil(self.eye1, self.pupil1, self.eye1_x, self.eye1_y)
                self.move_pupil(self.eye2, self.pupil2, self.eye2_x, self.eye2_y)
            sleep(0.4)  # Adjust the speed of pupil movement here

    def move_pupil(self, eye, pupil, eye_x, eye_y):
        if self.isPupils:
            # Calculate the center of the eye
            eye_center_x, eye_center_y = eye_x + self.eye_size // 2, eye_y + self.eye_size // 2

            # Calculate the angle at which the pupil should move
            angle = random.uniform(0, 2 * math.pi)

            # Calculate the new pupil position along the perimeter of the eye
            new_x = eye_center_x + (self.eye_radius - self.pupil_radius) * math.cos(angle)
            new_y = eye_center_y + (self.eye_radius - self.pupil_radius) * math.sin(angle)

            # Update the pupil position
            self.canvas.coords(pupil, new_x - self.pupil_radius, new_y - self.pupil_radius,
                               new_x + self.pupil_radius, new_y + self.pupil_radius)

            # Update the canvas to reflect the changes
            self.update()

    def talkAnimation(self):
        while True:
            time.sleep(0.01)
            if self.isTalking:
                self.talk()

    def talk(self):
        # Adjust mouth height
        new_height = random.randint(10, 50)
        self.canvas.coords(self.mouth, self.width // 2 - self.mouth_width // 2,
                       self.mouth_y - new_height // 2,
                       self.width // 2 + self.mouth_width // 2,
                       self.mouth_y + new_height // 2)

        self.update()
        sleep(random.uniform(0.05, 0.5))  # Adjust the speed of mouth movement

    def walkingAnimation(self):
        while True:
            time.sleep(0.01)
            if self.isWalking:
                self.walk()

    def walk(self):
        # Delete previous sweat droplets
        for drop in self.sweat_droplets:
            self.canvas.delete(drop)
        self.sweat_droplets = []

        # Calculate the x-coordinates for the droplets
        droplet_width = self.sweating_image.width()  # Get the width of the droplet image
        droplet_spacing = (self.width - droplet_width * 3) / 4  # Calculate spacing between droplets
        droplet_positions = [(i * (droplet_width + droplet_spacing) + droplet_spacing, 0) for i in range(3)]

        # Simulate sweating with smaller water droplets
        for initial_x, initial_y in droplet_positions:
            drop = self.canvas.create_image(initial_x, initial_y, image=self.sweating_image, anchor=tk.NW)
            self.sweat_droplets.append(drop)

        # Animate droplets falling
        self.animate_droplets_fall()

    def animate_droplets_fall(self):
        while self.sweat_droplets:
            for drop in self.sweat_droplets:
                x, y = self.canvas.coords(drop)
                # Move the droplet downwards
                y += random.randint(4, 12)  # Adjust the falling speed
                self.canvas.scale(drop, x, y, 0.005, 0.005)
                # Check if droplet reached the bottom
                if y >= self.height:
                    # Remove droplet from the canvas and the list
                    self.canvas.delete(drop)
                    self.sweat_droplets.remove(drop)
            self.update()
            sleep(0.03)  # Adjust the animation speed

    def stopWalking(self):
        self.isWalking = False

if __name__ == "__main__":
    face = Face()
    face.bind('<KeyPress-y>', lambda e: face.idleFace())
    face.bind('<KeyPress-t>', lambda e: face.talkingFace())
    face.bind('<KeyPress-u>', lambda e: face.walkingFace())
    face.mainloop()

main()
