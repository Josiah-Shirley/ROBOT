import speech_recognition as sr
import random
import pyttsx3



#----------------------------------------------------------------
# ROBOT INTERPRETS SPEECH HERE


def haveConversation():
    dt = DialogueTemplate("dialogTestFile.txt")
    dt.interpretLines()
    engine = pyttsx3.init()
    engine.setProperty('rate', 125)
    # dt.printPrimaryInputPairs()

    while True:
        with sr.Microphone() as source:
            r = sr.Recognizer()
            r.adjust_for_ambient_noise(source)
            r.dynamic_energy_threshold = 3000
            try:
                print("---------------------")
                print("listening, go ahead...")
                audio = r.listen(source)
                print("Got audio...")
                user_input = r.recognize_google(audio)
                print(user_input)
                response = dt.findResponse(user_input)
                engine.say(response)
                engine.runAndWait()
                if user_input == "goodbye":
                    break
            except sr.UnknownValueError:
                print("That may not be a valid English word...")

    """
        listening = True
        while listening:
            for phrase in LiveSpeech():
                print(phrase)
                response = dt.findResponse(phrase.__str__())
                engine.say(response)
                engine.runAndWait()
    """
    """
    # The following block of code is for testing without a micriphone
    listening = True
    while listening:
        print("Ready To Test...     *say 'stop' to end the loop*")
        word = input(">>> ")
        if word == "stop":
            break
        response = dt.findResponse(word)
        engine.say(response)
        engine.runAndWait()
    # End microphoneless testing block
    """
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
        for unProcessedline in dialogueFile:
            try:
                line = self.removeLeadingSpaces(unProcessedline)
                # tokens = ['#', '~', 'u']
                # "If it isn't a blank line..."
                if self.checkForSpaces(line):
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
                    elif firstChar == "#":
                        pass
                    else:
                        print("This is a weird line...")
                        print(line)
            except Exception as e:
                print("There was a problem reading this line:")
                print(unProcessedline)
                print(str(e))
        for pair in self.primaryInputPairs:
            self.activeUserInputPairs.append(pair)
        dialogueFile.close()
        for pair in self.allInputPairs:
            pair.setVariablesList(self.variablesList)

    def checkForSpaces(self, given):
        return any(char.isalpha() for char in given)

    def removeLeadingSpaces(self, text):
        return text.lstrip()

    def printPrimaryInputPairs(self):
        for pair in self.primaryInputPairs:
            print(pair)

    def printActiveInputPairs(self):
        for pair in self.activeUserInputPairs:
            print(pair)

    def findResponse(self, userInput) -> str:
        response = ""
        print("Finding the right response...")
        foundResponse = False
        # Check all active pairs for a valid user input
        for pair in self.activeUserInputPairs:
            # This will iterate through a list of possible inputs within the 
            # current input-response pair being evaluated. The list will only
            # contain one input unless there are variable inputs assigned to 
            # the pair in the script.
            for input in pair.getPossibleInputs():
                # GLOBAL VARIABLE: NO TOUCHY!
                indexOfUnderscore = 0
                # if an _ is in the possible input, it is a piece of user info
                # and should be handled in a special way. If the user has entered
                # a sentence that goes to an input with an _, it is handled here.
                if "_" in input:
                    # Also test if the entered input is the same length as the 
                    # script input, because if they are not, we shouldn't waste time
                    # checking for a match.
                    inputList = input.split(" ")
                    userInputList = userInput.split(" ")
                    if len(inputList) == len(userInputList):
                        # The following for loop and if/else statements find the index
                        # position (assuming each word is a position) of the _
                        currentIndex = 0
                        for word in inputList:
                            if word != "_":
                                currentIndex += 1
                            else:
                                indexOfUnderscore = currentIndex
                        # inputToTest is the predetermined input given in the script
                        inputToTest = input.split(" ")
                        # The idea of the following code is to take the underscore out
                        # of the possible user input and then also take whatever word 
                        # is at the same index position in the entered input. At that
                        # point, the two can be compared for a match.
                        inputToTest.pop(indexOfUnderscore)
                        inputWithoutSpaces = "".join(inputToTest)
                        # userInputToTest is the entered user input.
                        possibleUserInputObjectValue = userInputList.pop(indexOfUnderscore)
                        userInputWithoutSpaces = "".join(userInputList)
                        if userInputWithoutSpaces == inputWithoutSpaces:
                            userInputObjectName = ""
                            possibleResponse = pair.getResponseWithVariableName()
                            responseList = possibleResponse.split(" ")
                            for word in responseList:
                                # This quick check of the word's length protects against
                                # a possible error that occurs when the script contains
                                # two spaces next to eachother. The two spaces would result
                                # in the value of 'word' being "" at some point during the
                                # iteration of this for each loop, resuling in an index out
                                # of range exception in the following if statement.
                                if len(word) > 0:
                                    if word[0] == "$":
                                        userInputObjectName = word[1:]
                            self.setUserInfoObjectValue(userInputObjectName, possibleUserInputObjectValue)
                            for eachpair in self.allInputPairs:
                                nameOfUserInfo = self.removeCharacterGroup(userInputObjectName, "\n")
                                eachpair.addUserInfoObjectValue(nameOfUserInfo, possibleUserInputObjectValue)
                            response = pair.getResponses()
                            foundResponse = True
                            # If the latest input is a primary input, deactivate all previous subpairs.
                            if pair in self.primaryInputPairs:
                                self.activeUserInputPairs.clear()
                                for irp in self.primaryInputPairs:
                                    self.activeUserInputPairs.append(irp)
                            # Activate any subpairs of the current pair.
                            #print("Here are all the subpairs for the current IRP:", pair.getSubpairs())
                            subpairs = pair.getSubpairs()
                            for subPair in subpairs:
                                #print("Current subpair being added to active IRP list:", subPair)
                                self.activeUserInputPairs.append(subPair)
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
            print("Could not find a valid response for this input...")
        else:
            print("Found one!")
        return response
    
    def removeCharacterGroup(self, word, group):
        result = ''
        i = 0
        while i < len(word):
            if word[i:i+2] == group:
                i += 2
            else:
                result += word[i]
                i += 1
        return result
    
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
    
    def removeCharacterGroup(self, word, group):
        result = ''
        i = 0
        while i < len(word):
            if word[i:i+2] == group:
                i += 2
            else:
                result += word[i]
                i += 1
        return result

    
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
            variableObject = self.getVariableByName(self.removeCharacterGroup(self.responses[1:], "\n"))
            toReturn = variableObject.getRandomValue()
        else:
            try:
                responseList = self.responses.split(" ")
                for word in responseList:
                    if word[0] == "$":
                        key = word[1:]
                        key = self.removeCharacterGroup(key, "\n")
                        toReturn += self.userInfoDict[key]
                    else:
                        toReturn += word
                    toReturn += " "
            except Exception as e:
                toReturn = "You have asked for user information that has not yet been defined..."
                print("ERROR:", e)
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
    
    def getResponseWithVariableName(self) -> str:
        return self.responses

    def getResponses(self) -> str:
        toReturn = ""
        responseWithVariable = self.responses
        responseList = responseWithVariable.split(" ")
        for word in responseList:
            if len(word) > 0:
                if word[0] == "$":
                    toReturn += self.getUserInfoObject().getCurrentValue()
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
