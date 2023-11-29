# Bytes for the size of the header
HEADERSIZE = 4 #keep long enough for Max_Sent to fit
defaultEncoding = "utf-8"
queueAmount = 5
#Max bytes sent at a time
Max_Sent = 1024

#function that calculates size of data
def recvAll(sock, numBytes):
    #the buffer
    recvBuff = ""
    
    tempBuff = ""

    #keep receiving until all is received
    while len(recvBuff) < numBytes:
        #attempt to receive bytes
        tempBuff = sock.recv(numBytes)

        # the other side has closed the socket
        if not tempBuff:
            break

        #add the received bytes to the buffer
        recvBuff += tempBuff.decode(defaultEncoding)
    return recvBuff

#sendsData
def sendData(msg, sock):
    #gets size of data to be sent
    dataSizeStr = str(len(msg))
    #print(dataSizeStr)

    #add a header stating size of file
    while len(dataSizeStr) < HEADERSIZE:
        dataSizeStr = "0" + dataSizeStr

    #convert contents of file to bytes, attach header to front
    msg = dataSizeStr.encode(defaultEncoding) + msg

    #number of bytes sent
    numSent = 0

    print("sending...")

    while (len(msg) > numSent):
        #print(msg[numSent:])
        numSent += sock.send(msg[numSent:])


#recievesData
def receiveData(sock):
    msgSize = Max_Sent
    #keep receiving while the msg hasn't been fully transferred
    while msgSize > Max_Sent-1:
        #receive Header bytes, should be size of data sent
        msgBuff = recvAll(sock, HEADERSIZE)
        msgSize = int(msgBuff)
        print("the message size is ", msgSize)
        #receive the rest of the file
        data = recvAll(sock, msgSize)
        print("the message data is ", data)
        #return data

#sends File data
def sendFile(file_name, sock):
    try:
        #file that is opened and edited
        file_obj = open(file_name, "rb")
        #while the file is not empty
        while True:
            #converts contents of file into fileData
            file_data = file_obj.read(Max_Sent)
            if (file_data):
                sendData(file_data, sock)
            #once the file has been fully sent
            else:
                break
        file_obj.close()
        print("file data sent")
    #if file does not exist
    except:
        DNE = "File does not exist!!!"
        print(DNE)
        sock.send(DNE.encode(defaultEncoding))

#receives File data
def recvFile(msg, sock):
    file_exists = True
    file_name = msg[4:]
    fileSize = Max_Sent
    #keep receiving while the file hasn't been fully transferred
    while fileSize > Max_Sent-1:
        #receive Header bytes, should be size of data sent
        fileSizeBuff = recvAll(sock, HEADERSIZE)
        try:
            fileSize = int(fileSizeBuff)
        #if file does not exist lets both know
        except:
            print("File does not exist!!!")
            file_exists = False
            break
        print("the file size is ", fileSize)
        #receive the rest of the file
        file_data = recvAll(sock, fileSize)
        print("the file data is ", file_data)
        #open a file and append to it
        file = open(file_name, "a")
        file.write(file_data)
    #if file exists it will close connection and file
    if file_exists:
        file.close()
        print("file data received")
    #file_exists = True
