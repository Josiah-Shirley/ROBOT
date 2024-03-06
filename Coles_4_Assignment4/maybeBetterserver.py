import socket
import time

# Server starts with Token and starts the conversation
script = [
    "Hi. ",
    "I was just going to say the same thing about you. Where are you from?",
    "Me too. Bozeman, Montana",
    "Me too, I am from the room we are currently in Bozeman Montana.",
    "Your not going to believe this, but my name is Tango also.",
    "Looking around the room I'd say pretty high."
]

def server():

    # create the TCP/IP socket
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind(('localhost', '9999'))

    # Listening and Accepting the connection from the client
    serverSocket.listen(5)
    print("Server waiting 5 seconds for the client request")
    # Accept the request from the client
    client_message, address = serverSocket.accept()
    print("Connected by: ", address)

    try:
        # Send token to start conversation
        token = "your turn"
        client_message.sendall(token.encode())
        for line in script:
            # Setting a pause before we release the token
            time.sleep(2)
            print("Testing the conversation ", line)
            # listening for the request
            token = client_message.recv(1024).decode()
            if token != "your turn":
                print("Check token value")
                break
            client_message.sendall(token.encode())
    # No more lines in the script and waiting for EOF message
    finally:
        token = client_message.recv(1024).decode()
        if token == "EOF":
            client_message.sendall(b"EOF")
            client_message.close()
            serverSocket.close()
            print("Valid acknowledgment")
        else:
            print("Connection not closed")

if __name__ == "__main__":
    server()