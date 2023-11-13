import socket
import sys

def main(SERVER_IP, SERVER_PORT):


    # The client's socket
    cliSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #socket created

    # Attempt to connect to the server
    cliSock.connect((SERVER_IP, SERVER_PORT)) #attempts to create at specified IP at specified port
    
    while True:
        #gets command
        msg = input("ftp> ")

        #sends command to server
        en_msg = msg.encode()
        cliSock.send(en_msg)

        #ends if quit command
        if (msg == "quit"):
        	break     
        #if get,put, or ls command create extra port to send data
        elif (msg[0:3] == "get" or msg[0:3] == "put" or msg[0:2] == "ls"):
                 #creates new socket
                 extraSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                 #gets port number from emphemeral socket
                 port = cliSock.recv(1024)
                 port = int(str(port.decode()))
                 #connects new socket to port
                 extraSock.connect((SERVER_IP, port))
                 #sends data
                 print("extra socket connected")
                 if (msg[0:3] == "get" or msg[0:2] == "ls"):
                     extraSock.recv(1024)
                     print("get/ls data recived")
                 elif (msg[0:3] == "put):
                     extraSock.send(en_msg)
                     print("put file sent")
                     
if __name__ == "__main__":
    SERVER_MACHINE = sys.argv[1]
    SERVER_PORT = sys.argv[2]
    SERVER_PORT = int(SERVER_PORT)
    SERVER_IP = socket.gethostbyname(SERVER_MACHINE)

    main(SERVER_IP, SERVER_PORT)
