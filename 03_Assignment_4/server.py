import socket
import pickle
import time

# Define host and port
# HOST = '192.168.43.166' # <-- This is the IP address when connected to the Tango phone's hot spot
HOST = '192.168.1.14' # <-- Desktop IP address
PORT = 5002

def resetLineNumberFile():
    f = open("lineNumber", "w")
    f.write("0")
    f.close()

resetLineNumberFile()

def speakThenSerializeData():

    # SPEAKING INSTRUCTIONS GO HERE
    script = open("script.txt", "r+")
    scriptLines = script.readlines()
    script.close()
    lineNumber = getCurrentLineNumber()
    toSay = scriptLines[lineNumber]
    currentLine = lineNumber + 1
    lineNumberFile = open("lineNumber.txt", "w")
    lineNumberFile.write(str(currentLine))
    lineNumberFile.close()

    # toSay.speak()
    print(toSay)

    time.sleep(2)

    # THIS SENDS THE TOKEN BACK TO THE OTHER ROBOT
    messageFile = open("message.txt", "r")
    dataToSend = messageFile.read()
    serialized_data = pickle.dumps(dataToSend)
    messageFile.close()
    return serialized_data

def getCurrentLineNumber() -> int:
    lineNumberFile = open("lineNumber.txt", "r+")
    lineNumber = int(lineNumberFile.read())
    lineNumberFile.close()
    return lineNumber

def openTokenFile() -> str:
    f = open("token.txt", "a+")
    f.seek(0)
    content = f.read()
    f.close()
    return content

def checkForToken():
    if openTokenFile() == "your turn":
        return True
    else:
        return False
    
def addTokenToOutgoingMessage():
    f = open("message.txt", "w")
    f.write(openTokenFile())
    f.truncate()
    f.close()

def resetToken(token):
    f = open("message.txt", "a+")
    f.truncate()
    f.write(token)
    f.close()

# Create a socket object
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # Bind the socket to the address
    s.bind((HOST, PORT))
    # Listen for incoming connections
    s.listen()
    print(f"Server listening on {HOST}:{PORT}")
    # Accept a connection
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")  
        # Receive data from the client
        while getCurrentLineNumber() <= 6:
            if checkForToken():
                addTokenToOutgoingMessage()
                # Echo the received data back to the client
                conn.sendall(speakThenSerializeData())
            data = conn.recv(4096)
            # Unpickle the received data
            token = pickle.loads(data)
            resetToken(token)
            # print("Received:", obj)


# I want to hold onto this in case I need it later
"""
    data = conn.recv(4096)
    # Unpickle the received data
    obj = pickle.loads(data)
    print("Received:", obj)
"""