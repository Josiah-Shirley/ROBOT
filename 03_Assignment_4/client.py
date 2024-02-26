import socket
import pickle

# Define host and port
HOST = '192.168.43.166'
PORT = 5002

# Sample data to send
data_to_send = {'message': 'Hello, server!'}

# Create a socket object
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # Connect to the server
    s.connect((HOST, PORT))
    # Pickle the data to send
    serialized_data = pickle.dumps(data_to_send)
    # Send the pickled data
    s.sendall(serialized_data)
    # Receive data from the server
    received_data = s.recv(4096)
    # Unpickle the received data
    obj = pickle.loads(received_data)
    print("Received from server:", obj)
