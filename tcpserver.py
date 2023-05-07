from socket import *
import sys

serverSocket = socket(AF_INET, SOCK_STREAM)

# Prepare a server socket
serverPort = 80 # Port number for HTTP
serverSocket.bind(('', serverPort))
serverSocket.listen(1)

while True:
    # Establish the connection
    print('Ready to serve...')
    connectionSocket, addr = serverSocket.accept()
    try:
        message = connectionSocket.recv(1024).decode()
        filename = message.split()[1]
        f = open(filename[1:])
        outputdata = f.read()
        f.close()
        
        # Send one HTTP header line into socket
        response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n<html><title>HALO!!!</title><header><h1>TUBES JARKOM</h1></header></html>"
        connectionSocket.send(response.encode())

        # Send the content of the requested file to the client
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].upper().encode())
        connectionSocket.send("\r\n".encode())
        connectionSocket.close()
    except IOError:
        # Send response message for file not found
        response = "HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\n"
        connectionSocket.send(response.encode())
        connectionSocket.send("<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n".encode())
        connectionSocket.close()

serverSocket.close()
sys.exit()
