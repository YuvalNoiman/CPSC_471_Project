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


def main(PORT_NUMBER):
   
    #path = "C:\Users\dlgun\Desktop\serverFolder"
    #isExist = os.path.exists(path)
    #if not isExist:
     #   os.makedirs(path)

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

            fileData = ""

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
         #---------------------------------------------------------------
                 if (deMsg[0:3] == "get"):
                     getFilename = deMsg[4:]

                     gNumSent = 0

                     gFileData = None

                     gCompleteName = os.path.join(r"\Users\dlgun\Desktop\serverFolder", deMsg[4:])

                     gFileObj = open(gCompleteName, "rb")

                     while True:
                         gFileData = gFileObj.read(1024)

                         if(gFileData):

                             dataSizeStr = str(len(gFileData))
                             print(dataSizeStr)

                             while len(dataSizeStr) < 10:
                                 dataSizeStr = "0" + dataSizeStr

                             gFileData = bytes(dataSizeStr, 'utf-8') + gFileData

                             numSent = 0

                             print("sending...")

                             while len(gFileData > numSent):
                                 print(gFileData[numSent:])
                                 numSent += extraSock.send(gFileData[numSent:]) 
                         else:
                              break
           
                         print("get sent")
                     extraSock.close()
                     gFileObj.close()
         #---------------------------------------------------------------
                 elif (deMsg[0:3] == "put"):
                     completeName = os.path.join(r"C:\Users\dlgun\Desktop\serverFolder", deMsg[4:])
                     while fileSize > 1023:

                        fileSizeBuff = recvAll(extraSock, 10)

                        fileSize = int(fileSizeBuff)

                        print("the filesize is ", fileSize)

                        fileData = recvAll(extraSock, fileSize)

                        print("the file data is ", fileData)
                        f = open(completeName, "a")
                        #x = extraSock.recv(1024)          
                        f.write(fileData)
                        #f.close()
                        print("file recieved")
                    
         #---------------------------------------------------------------
                 elif (deMsg[0:2] == "ls"):
                     extraSock.send(cliMsg)
                     print("ls sent")
                 f.close()
                 extraSock.close()
                 print("the socket is closed")

if __name__ == "__main__":
    PORT_NUMBER = 65500 #sys.argv[1]

    PORT_NUMBER = int(PORT_NUMBER)

    main(PORT_NUMBER)
