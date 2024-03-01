import speech_recognition as sr


#----------------------------------------------------------------
# ROBOT INTERPRETS SPEECH HERE

def haveConversation():
    dt = dialogueTemplate("dialogTestFile.txt")
    dt.interpretLines()
    # dt.printPrimaryInputPairs()

    listening = True
    r = sr.Recognizer()

    while listening:
        with sr.Microphone() as source:
            # r.adjust_for_ambient_noise(source)
            r.dynamic_energy_threshold = 500

            try:
            # Listen for user input
                print("listening...")
                word = input(">>> ")
                if word == "stop":
                    break
                ###audio = r.listen(source)
                print("{processing audio...}")
            # Process user input
                ###word = r.recognize_google(audio)
                ###print(word)        # <-- "testing testing 123"
                ###word = "hello"
            # Figure out which reply to give
                response = dt.findResponse(word)
            # Give a reply
                print(response)    # <-- Replace print with TTS
            except sr.UnknownValueError:
                print("..Unknown Word..")




class dialogueTemplate():
    def __init__(self, textFile):
        self.textFile = textFile
        self.primaryInputPairs = []
        self.activeUserInputPairs = []

    def __str__(self):
        toReturn = "{"
        for pair in self.primaryInputPairs:
            toReturn += pair
        toReturn += "}"
        return toReturn
        
    def interpretLines(self):
        dialogueFile = open(self.textFile, "r")
        for line in dialogueFile:
            # tokens = ['#', '~', 'u']
            if line != "\n":
                firstChar = list(line)[0]
                if firstChar == "~":
                    pass        # <-- handle variable inputs here
                elif firstChar == "u":
                    irp = InputResponsePair(line)
                    nextChar = list(line)[1]
                    if nextChar == ":":
                        self.primaryInputPairs.append(irp)
                    else:
                        currentPair = self.primaryInputPairs[len(self.primaryInputPairs)-1]
                        currentPair.addSubPair(irp)
        for pair in self.primaryInputPairs:
            self.activeUserInputPairs.append(pair)
        dialogueFile.close()

    def printPrimaryInputPairs(self):
        for pair in self.primaryInputPairs:
            print(pair)

    def findResponse(self, userInput) -> str:
        response = ""
        # Check all active pairs for a valid user input possibility
        for pair in self.activeUserInputPairs:
            if userInput in pair.getPossibleInput():
                response = pair.getResponses()
                # If the latest input is a primary input, deactivate all previous subpairs.
                if pair in self.primaryInputPairs:
                    self.activeUserInputPairs.clear()
                    for pair in self.primaryInputPairs:
                        self.activeUserInputPairs.append(pair)
                # Activate any subpairs of the current pair.
                for subPair in pair.subPairs:
                    print("THIS HAPPENED")
                    self.activeUserInputPairs.append(subPair)
            print(pair)
        return response


class InputResponsePair():
    def __init__(self, line) -> None:
        self.line = line
        self.lineComponents = self.line.split(":")
        self.userInput = self.lineComponents[1]
        self.responses = self.lineComponents[2]
        self.subPairs = []      # <-- This will be a list of InputResponsePair objects

    def __str__(self):
        return self.line

    def getLineDepth(self) -> int:
        if list(self.line)[1] != ":":
            toReturn = int(list(self.line)[1])
            return toReturn
        else:
            return 0
        
    def getPossibleInput(self) -> list:
        tempList = self.userInput.split("(")
        anotherTempList = tempList[1].split(")")
        userInput = anotherTempList[0]   
        userInputList = [userInput]  
        return userInputList
    
    def getResponses(self) -> str:
        return self.responses
    
    def getSubpairs(self):
        return self.subPairs
    
    def addSubPair(self, irp):
        self.subPairs.append(irp)

    def printAllSubPairs(self):
        for pair in self.subPairs:
            print(pair)



haveConversation()