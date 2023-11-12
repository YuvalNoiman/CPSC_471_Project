import socket
import settings
import time


# server.py
def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((socket.gethostname(), 1234))  # 1234 is serverPort
    s.listen(settings.queueAmount)  # queue amount

    # Note: since we need(2) connections (one constant, one ephemeral, we may need to thread the former)
    while True:
        # now our endpoint knows about the OTHER endpoint.
        clientSocket, address = s.accept()
        print(f"Connection from {address} has been established.")  # Success, need a conditional if failed

        # May need an if statement here, depending on command
        outboundMessage = "This is the server speaking."
        outboundMessage = f"{len(outboundMessage):<{settings.HEADERSIZE}}" + outboundMessage
        '''
        # FORMAT:
        message = "STRING"
        message = len(STRING):<HEADERSIZE + STRING
        '''

        # Here is where you'd add logic for sending multiple messages instead of just (1)
        clientSocket.send(bytes(outboundMessage, settings.defaultEncoding))

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
    elif command == "get": # print "sending file TO client"
    elif command == "ls":  # print directory, code given from Professor in .rar file
        for line in commands.getstatusoutput('ls -l'):
    	    print line # since we want to send strings to client, will need to condense/store info
    else: print("Command not valid. Try again.\n")
'''