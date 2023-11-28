import socket
import settings


# server.py
def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((socket.gethostname(), 1234))  # 1234 is serverPort
    s.listen(settings.queueAmount)  # queue amount
    localHeaderSize = settings.HEADERSIZE
    localUtfEncoding = settings.defaultEncoding

    # Note: since we need(2) connections (one constant, one ephemeral, we may need to thread the former)
    while True:
        # now our endpoint knows about the OTHER endpoint.
        clientSocket, address = s.accept()
        print(f"Connection from {address} has been established.")  # Success, need a conditional if failed

        # May need an if statement here, depending on command
        outboundMessage = "This is the server speaking."
        outboundMessage = f"{len(outboundMessage):<{localHeaderSize}}" + outboundMessage
        '''
        # FORMAT:
        message = "STRING"
        message = len(STRING):<HEADERSIZE + STRING
        '''

        # Here is where you'd add logic for sending multiple messages instead of just (1)
        clientSocket.send(bytes(outboundMessage, localUtfEncoding))

        clientSocket.close()
        # end while
    # end while


# import system
# will need sys.argv for commands > len(1)
'''
try: serverSocket.bind(", serverPort)
except socket.error, msg: {
    print(f"Error: {msg}")
    sys.exit()
    }

command = ""
while True:
    # Prompt command
    if command == "quit": sys.exit() or return 0 (?)
    elif command == "put": # print "receiving file FROM client"
        listenPort = 1001  # temporary port on which to listen
        cToS_WelcSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cToS_WelcSock.bind(('', listenPort))
        cToS_WelcSock.listen(1)


        def recvAll(sock, numBytes):
            recvBuff = ""
            tmpBuff = ""

            while len(recvBuff) < numBytes:
                tmpBuff = sock.recv(numBytes)

                if not tmpBuff:
                    break
                recvBuff += tmpBuff

            return recvBuff

        while True:
            print "Waiting for connection..."

            clientSock, addr = cToS_Welcome.accept()

            print "Accepted connection from client: ", addr
            print "\n"

            fileData = ""
            recvBuff = ""
            fileSize = 0
            fileSizeBuff = ""

            fileSizeBuff = recvAll(clientSock, 10)
            fileSize = int(fileSizeBuff)

            print "The file size is ", fileSize

            fileData = recvAll(clientSock, fileSize)

            print "SUCCESS"
            print "The file data is: "
            print fileData

            clientSock.close
    cToS_WelcSock.close
    
    elif command == "get": # print "sending file TO client"
    elif command == "ls":  # print directory, code given from Professor in .rar file
        for line in commands.getstatusoutput('ls -l'):
    	    print line # since we want to send strings to client, will need to condense/store info
    else: print("Command not valid. Try again.\n")
'''
