import socket
import sys
import os

def recvAll(sock, numBytes):

    recvBuff = ""
    
    tempBuff = ""

    while len(recvBuff) < numBytes:
        tempBuff = sock.recv(numBytes)

        if not tempBuff:
            break

        recvBuff += tempBuff.decode("utf-8")
    return recvBuff

def main(SERVER_IP, SERVER_PORT):


    # The client's socket
    cliSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #socket created

    # Attempt to connect to the server
    cliSock.connect((SERVER_IP, SERVER_PORT)) #attempts to create at specified IP at specified port
    
    while True:
        #gets command
        msg = input("ftp> ")

        fielData = ""

        recvBuff = ""

        fileSize = 1024

        fileSizeBuff = ""

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
        #--------------------------------------------------------
                 if (msg[0:3] == "get"):
                     completeName = os.path.join(r"C:\Users\dlgun\Desktop\clientFolder", msg[4:])
                     while fileSize >1023:
                         
                         fileSizeBuff = recvAll(extraSock, 10)

                         fileSize = int(fileSizeBuff)

                         print("the filesize is ", fileSize)

                         gFileData = recvAll(extraSock, fileSize)

                         print("the file data is ", gFileData)
                         f = open(completeName, "a")
                         f.write(gFileData)
                     #extraSock.recv(1024)
                     f.close()
                     extraSock.close()
                     print("get data recieved")
        #--------------------------------------------------------
                 elif (msg[0:3] == "put"):
                     filename = msg[4:]

                     numSent = 0

                     fileData = None

                     fileObj = open(filename, "rb")

                     while True:
                        fileData = fileObj.read(1024)

                        if(fileData):

                            dataSizeStr = str(len(fileData))
                            print (dataSizeStr)

                            while len(dataSizeStr) < 10:
                                dataSizeStr = "0" + dataSizeStr

                            fileData = bytes(dataSizeStr, 'utf-8') + fileData

                            numSent = 0

                            print('sending...')

                            while len(fileData) > numSent:
                                print(fileData[numSent:])
                                numSent += extraSock.send(fileData[numSent:])
                               
                                #l = fileObj.read(1024)
                        else:
                            break
                        print("put file sent")
                     extraSock.close()
                     fileObj.close()
                   
if __name__ == "__main__":
    SERVER_MACHINE =  "LAPTOP-SOOL70UB"#sys.argv[1] #"DESKTOP-E5K38H2" #  -argv[1] "LAPTOP-SOOL70UB", 
    SERVER_PORT = sys.argv[2] #65500 
    SERVER_PORT = int(SERVER_PORT)
    SERVER_IP = socket.gethostbyname(SERVER_MACHINE)

    main(SERVER_IP, SERVER_PORT)
