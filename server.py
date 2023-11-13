import socket
import sys


def main(PORT_NUMBER):


    # Create a socket
    serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Associate the socket with the port
    serverSock.bind(('',PORT_NUMBER))

    serverSock.listen(100)

    while True:
        print("Waiting for clients to connect...")

        # Accept a waiting connection
        cliSock, cliInfo = serverSock.accept()

        print("Client connected from: " + str(cliInfo))

        # Receive the command the client has to send.
        # This will receive at most 1024 bytes
        while True:
            cliMsg = cliSock.recv(1024)
            deMsg = str(cliMsg.decode())
            #prints client command
            print("Client sent " + deMsg)
            if (deMsg == "quit"):
                 cliSock.close()
                 break
            elif (deMsg[0:3] == "get" or deMsg[0:3] == "put" or deMsg[0:2] == "ls"):
                 #creates extra socket
                 extraSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                 extraSock.bind(('',0))
                 extraSock.listen(100)
                 print("Waiting for extra clients to connect...")
                 #gets emepheral port number
                 port = str(extraSock.getsockname()[1])
                 #sends port to client to send data
                 cliSock.send(port.encode())
                 extraSock, cliInfo = extraSock.accept()
                 print("Extra client connected from: " + str(cliInfo))
                 if (deMsg[0:3] == "get"):
                     extraSock.send(cliMsg)
                     print("get sent")
                 elif (deMsg[0:3] == "put"):
                     extraSock.recv(1024)
                     print("file recived")
                 elif (deMsg[0:2] == "ls"):
                     extraSock.send(cliMsg)
                     print("ls sent")
                 extraSock.close()


if __name__ == "__main__":
    PORT_NUMBER = sys.argv[1]

    PORT_NUMBER = int(PORT_NUMBER)

    main(PORT_NUMBER)
