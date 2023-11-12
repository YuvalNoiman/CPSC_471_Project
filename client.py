import socket
fileSegmentSize = 8 # bytes
import settings


# client.py
def main():
    # Connect to server
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect((socket.gethostname(), 1234))  # serverPort

    print(receiveMessage(clientSocket, fileSegmentSize))

# Receive messages
# File segment size can be extracted from the first (10) bytes of the buffer(?)
# FSS can be 8, 16, etc... defined by client when sending the message? / depending on size of file sent?
def receiveMessage(clientSocket, fileSegmentSize):
    while True:
        fullMessage = ""
        _buffer = ""
        isNewMessage = True
        while True:
            _buffer = clientSocket.recv(fileSegmentSize) # file segment size ...
            if isNewMessage:
                messageLength = int(_buffer[:settings.HEADERSIZE])
                isNewMessage = False

            fullMessage += _buffer.decode(settings.defaultEncoding)
            print(f'Bytes sent: {len(fullMessage)}\n')

            # wait until full message is received, subtracting header information
            if (len(fullMessage)-settings.HEADERSIZE) == messageLength:
                print(f'Full message:')
                print(fullMessage[settings.HEADERSIZE:])  # We may want to instead write to a file
                newMessage = True
                fullMessage = ""
        # end While
    # end While
