import socket
import time

# Client receives token line from server and proceses and responds
script = [
    "Hi, you look familiar",
    "I am from Montana, where are you from?"
    "Me too. Bozeman, Montana",
    "Me too, I am from the room we are currently in Bozeman, Montana",
    "Tango",
    "what are the odds. Two robots run into each other from the same state, and the same town, "
    "and the same room, with the same name?",
    "EOF"
]

def client():
    # Create the TCP / IP Socket
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Connect to the Server first
    clientSocket.connect(('localhost', '9999'))

    try:
        while True:
            # Receive the token to decode
            token = clientSocket.recv(1024).decode()
            print("Testing that client received token from server -------> ", token)
            if token != "your turn":
                print("What happened to the token lol?")
                break
            for line in script:
                print("Message testing, ", line)
                time.sleep(10)
                clientSocket.sendall(token.encode())
                response = clientSocket.recv(1024).decode()
                # Handle the end of the script and change the token to
                if response != "your turn":
                    print("Terminator")
                    break
                if line == "EOF":
                    clientSocket.sendall(b"EOF")
    finally:
        clientSocket.close()

if __name__ == "__main__":
    client()