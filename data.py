# Bytes for the size of the header
HEADERSIZE = 4 #keep long enough for Max_Sent to fit
defaultEncoding = "utf-8"  #png and pdf use "ISO-8859-1"
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
    full_data = ""
    #keep receiving while the msg hasn't been fully transferred
    while msgSize > Max_Sent-1:
        #receive Header bytes, should be size of data sent
        msgBuff = recvAll(sock, HEADERSIZE)
        try:
            msgSize = int(msgBuff)
        except:
            return False
        print("the message size is ", msgSize)
        #receive the rest of the file
        data = recvAll(sock, msgSize)
        full_data += data
        print("the message data is ", data)
    return full_data

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
    file_name = msg[4:]
    file_data = receiveData(sock)
    if file_data == False:
        print("File does not exist!!!")
        return False
    file = open(file_name, "wb")
    file_data = file_data.encode(defaultEncoding)
    file.write(file_data)
    file.close()
    print("file data received")
    print("file is called: ", file_name)
    print("bytes received is: ", len(file_data))
