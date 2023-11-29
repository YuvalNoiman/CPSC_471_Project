import socket
import sys
import subprocess
from data import *

def ephemeral_port(cliSock):
    #creates extra socket
    extraSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    extraSock.bind(('',0))
    extraSock.listen(100)
    print("Waiting for extra clients to connect...")
    #gets ephemeral port number
    port = str(extraSock.getsockname()[1])
    #sends port to client to send data
    cliSock.send(port.encode(defaultEncoding))
    extraSock, cliInfo = extraSock.accept()
    print("Extra client connected from: " + str(cliInfo))
    return extraSock

def main(PORT_NUMBER):


    # Create a socket
    serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Associate the socket with the port
    serverSock.bind(('',PORT_NUMBER))

    serverSock.listen(queueAmount)

    while True:
        print("Waiting for clients to connect...")

        # Accept a waiting connection
        cliSock, cliInfo = serverSock.accept()

        print("Client connected from: " + str(cliInfo))

        # Receive the command the client has to send.
        # This will receive at most 1024 bytes
        while True:
            cliMsg = cliSock.recv(1024)
            deMsg = str(cliMsg.decode(defaultEncoding))
            #prints client command
            print("Client sent " + deMsg)
            if (deMsg == "quit"):
                 cliSock.close()
                 break
            elif (deMsg[0:3] == "get"):
                 extraSock = ephemeral_port(cliSock)
                 file_name = deMsg[4:]
                 sendFile(file_name, extraSock)
            elif (deMsg[0:3] == "put"):
                 extraSock = ephemeral_port(cliSock)
                 recvFile(deMsg, extraSock)
            elif (deMsg[0:2] == "ls"):
                 extraSock = ephemeral_port(cliSock)
                 ls_message = ""
                 for line in subprocess.getstatusoutput(cliMsg):
                    if (line != 0):
                        ls_message += str(line) + "\n"
                 increment = Max_Sent
                 while True:
                     message = ls_message[increment-Max_Sent:increment]
                     if (message):
                          sendData(message.encode(defaultEncoding), extraSock)
                          increment += Max_Sent
                     else:
                          break
                 print("ls message sent")
            extraSock.close()
            print("ephemeral socket closed")


if __name__ == "__main__":
    PORT_NUMBER = sys.argv[1]

    PORT_NUMBER = int(PORT_NUMBER)

    main(PORT_NUMBER)
