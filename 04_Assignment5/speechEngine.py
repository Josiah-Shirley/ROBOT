import speech_recognition as sr


#----------------------------------------------------------------
# ROBOT INTERPRETS SPEECH HERE

def readFile(file) -> str:
    toSay = " "
    for line in file:
        toSay = interpretLine(line)
        if toSay != " ":
            break
    return toSay

class DialogueLine():

    def __init__(self, line) -> None:
        self.line = line
        self.firstChar = list(line)[0]

    def getLineDepth(self) -> int:
        if list(self.line)[1] != ":":
            toReturn = int(list(self.line)[1])
            return toReturn
        else:
            return 0
        
    # Parse out the speech input/output here

def interpretLine(line) -> str:
    toSay = " "
    # tokens = ['#', '~', 'u']
    if line != "\n":
        firstChar = list(line)[0]
        if firstChar == "~":
            toSay = " "    # <-- Handle variable user inputs here
        elif firstChar == "u":
            dl = DialogueLine(line)
    return toSay

#----------------------------------------------------------------
# ROBOT LISTENS HERE

listening = True
r = sr.Recognizer()

while listening:
    with sr.Microphone() as source:
        # r.adjust_for_ambient_noise(source)
        r.dynamic_energy_threshold = 500

        try:
        # Listen for user input
            print("listening...")
            ### audio = r.listen(source)
            print("{processing audio...}")
        # Process user input
            ### word = r.recognize_google(audio)        # <-- "testing testing 123"
        # Write most recent user input to a text file
            word = "testing"
            userInputFile = open("userInput.txt", "w+")
            userInputFile.truncate()
            userInputFile.write(word)
            userInputFile.close()
        # Apply input to a dialogue file
            dialogueFile = open("dialogTestFile.txt", "r")
            toSay = readFile(dialogueFile)
            dialogueFile.close()
        # Give a reply
            ### print(toSay)    # <-- Replace with TTS
        except sr.UnknownValueError:
            print("..Unknown Word..")

    listening = False   # <-- Just for testing purposes.
