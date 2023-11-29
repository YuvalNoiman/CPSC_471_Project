import socket
import sys
import os

#function to determine filesize
def recvAll(sock, numBytes):

    recvBuff = ""
    
    tempBuff = ""

    while len(recvBuff) < numBytes:
        tempBuff = sock.recv(numBytes)

        if not tempBuff:
            break

        recvBuff += tempBuff.decode("utf-8")
    return recvBuff


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

            #holds file data
            fileData = ""

            #buffer for recieved data
            recvBuff = ""

            fileSize = 1024

            fileSizeBuff = ""

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

                     getFilename = deMsg[4:]

                     #number of bytes sent
                     gNumSent = 0

                     #data from file in bytes
                     gFileData = None

                     gCompleteName = os.path.join(r"\Users\dlgun\Desktop\serverFolder", deMsg[4:])

                     #file that is being appended to
                     gFileObj = open(gCompleteName, "rb")

                     #while there is data to be read from file
                     while True:

                         gFileData = gFileObj.read(1024)

                         #if there is data to be sent, send it
                         if(gFileData):

                             #size of data to be sent
                             dataSizeStr = str(len(gFileData))
                             print(dataSizeStr)

                             #creates header for data size
                             while len(dataSizeStr) < 10:
                                 dataSizeStr = "0" + dataSizeStr

                             #stores file data as bytes
                             gFileData = bytes(dataSizeStr, 'utf-8') + gFileData
                             gNumSent = 0

                             print("sending...")

                             while len(gFileData) > gNumSent:
                                 print(gFileData[gNumSent:])
                                 gNumSent += extraSock.send(gFileData[gNumSent:]) 
                         else:
                              break
           
                         print("get sent")
                     extraSock.close()
                     gFileObj.close()
        
                 elif (deMsg[0:3] == "put"):

                     completeName = os.path.join(r"C:\Users\dlgun\Desktop\serverFolder", deMsg[4:])

                     #while there is still content left in the file
                     while fileSize > 1023:

                        #recieve header for file size
                        fileSizeBuff = recvAll(extraSock, 10)

                        fileSize = int(fileSizeBuff)
                        print("the filesize is ", fileSize)

                        #stores recieved data of file
                        fileData = recvAll(extraSock, fileSize)
                        print("the file data is ", fileData)

                        #open file to append to
                        f = open(completeName, "a")
                             
                        f.write(fileData)
                        f.close()
                        print("file recieved")
                    
                 elif (deMsg[0:2] == "ls"):
                     extraSock.send(cliMsg)
                     print("ls sent")
                 #f.close()
                 extraSock.close()
                 print("the socket is closed")

if __name__ == "__main__":
    PORT_NUMBER = 65500 #sys.argv[1]

    PORT_NUMBER = int(PORT_NUMBER)

    main(PORT_NUMBER)
