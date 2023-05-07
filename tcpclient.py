import sys
from socket import *

# Get the command-line arguments
server_host = sys.argv[1]
server_port = int(sys.argv[2])
filename = sys.argv[3]

# Create a client socket
client_socket = socket(AF_INET, SOCK_STREAM)

# Connect to the server
client_socket.connect((server_host, server_port))

# Send the request to the server
request = f"GET /{filename} HTTP/1.1\r\nHost: {server_host}\r\n\r\n"
client_socket.send(request.encode())

# Receive the response from the server
response = client_socket.recv(1024)
while response:
    print(response.decode(), end="")
    response = client_socket.recv(1024)

# Close the socket
client_socket.close()
