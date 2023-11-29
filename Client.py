import socket
import sys
from data import *

def ephemeral_port(cliSock):
    #creates new socket
    extraSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #gets port number from ephemeral socket
    port = cliSock.recv(1024)
    port = int(str(port.decode(defaultEncoding)))
    #connects new socket to port
    extraSock.connect((SERVER_IP, port))
    #sends data
    print("extra socket connected")
    return extraSock

def main(SERVER_IP, SERVER_PORT):


    # The client's socket
    cliSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #socket created

    # Attempt to connect to the server
    cliSock.connect((SERVER_IP, SERVER_PORT)) #attempts to create at specified IP at specified port
    
    while True:
        #gets command
        msg = input("ftp> ")

        #ends if quit command
        if (msg == "quit"):
            #sends command to server
            en_msg = msg.encode(defaultEncoding)
            cliSock.send(en_msg)
            break     
        #receives file if get command
        elif (msg[0:3] == "get"):
            #sends command to server
            en_msg = msg.encode(defaultEncoding)
            cliSock.send(en_msg)
            extraSock = ephemeral_port(cliSock)
            recvFile(msg, extraSock)
        #sends file if put command
        elif (msg[0:3] == "put"):
            #sends command to server
            en_msg = msg.encode(defaultEncoding)
            cliSock.send(en_msg)
            extraSock = ephemeral_port(cliSock)
            file_name = msg[4:]
            sendFile(file_name, extraSock)
        #receives ls data if ls command
        elif (msg[0:2] == "ls"):
            #sends command to server
            en_msg = msg.encode(defaultEncoding)
            cliSock.send(en_msg)
            extraSock = ephemeral_port(cliSock)
            ls_data = recvAll(extraSock, 10000)
            print(ls_data)
            print("ls data received")
        else:
            print("Invalid Input!!! Please try again!")
                     
if __name__ == "__main__":
    SERVER_MACHINE = sys.argv[1]
    SERVER_PORT = sys.argv[2]
    SERVER_PORT = int(SERVER_PORT)
    SERVER_IP = socket.gethostbyname(SERVER_MACHINE)

    main(SERVER_IP, SERVER_PORT)
