import socket
import sys
import os

#function that calculates size of data
def recvAll(sock, numBytes):
    #the buffer
    recvBuff = ""
    
    tempBuff = ""

    #keep recieving until all is recieved
    while len(recvBuff) < numBytes:

    #attempt to recieve bytes
        tempBuff = sock.recv(numBytes)

    # the other side has closed the socket
        if not tempBuff:
            break

    #add the received bytes to the buffer
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

        #holds file data as Bytes
        fielData = ""

        #buffer for recieved bytes
        recvBuff = ""

        #size of file to be sent
        fileSize = 1024

        #buffer for file size
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

                 if (msg[0:3] == "get"):

                     #path to store recieved files
                     completeName = os.path.join(r"C:\Users\dlgun\Desktop\clientFolder", msg[4:])

                     #keep recieving while the file hasnt been fully transferred
                     while fileSize >1023:
                         
                         #recieve the first 10 bytes, should be the size of data sent
                         fileSizeBuff = recvAll(extraSock, 10)

                         fileSize = int(fileSizeBuff)

                         print("the filesize is ", fileSize)

                         #recieve the rest of the file
                         gFileData = recvAll(extraSock, fileSize)

                         print("the file data is ", gFileData)

                         #open a file and append to it
                         f = open(completeName, "a")
                         f.write(gFileData)

                     #once file is fully recieved, close connection and file
                     f.close()
                     extraSock.close()
                     print("get data recieved")
        
                 elif (msg[0:3] == "put"):

                     filename = msg[4:]

                     #number of bytes sent
                     numSent = 0

                     fileData = None

                     #file that is opened and edited
                     fileObj = open(filename, "rb")

                     #while the file is not empty
                     while True:

                        #convert contents of file into fileData
                        fileData = fileObj.read(1024)

                        if(fileData):

                            #gets size of data to be sent
                            dataSizeStr = str(len(fileData))

                            print (dataSizeStr)

                            #add a header stating size of file
                            while len(dataSizeStr) < 10:

                                dataSizeStr = "0" + dataSizeStr
                            
                            #convert contents of file to bytes, attach header to front
                            fileData = bytes(dataSizeStr, 'utf-8') + fileData

                            #number of bytes sent
                            numSent = 0

                            print('sending...')

                          
                            while len(fileData) > numSent:
                                print(fileData[numSent:])
                                numSent += extraSock.send(fileData[numSent:])
                               
                        #once the file has been fully sent
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
