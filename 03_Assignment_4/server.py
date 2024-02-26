import socket
import pickle

# Define host and port
HOST = '192.168.43.166'
PORT = 5002

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
        while True:
            # Receive data from the client
            data = conn.recv(4096)
            if not data:
                break
            # Unpickle the received data
            obj = pickle.loads(data)
            print("Received:", obj)
            # Echo the received data back to the client
            conn.sendall(data)
