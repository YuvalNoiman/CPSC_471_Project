import socket
import settings
FileSegmentSize = 8  # bytes


# client.py
def main():
    # Connect to server
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect((socket.gethostname(), 1234))  # serverPort

    localFileSegmentSize = FileSegmentSize
    print(receiveMessage(clientSocket, localFileSegmentSize))


# Receive messages
# File segment size can be extracted from the first (10) bytes of the buffer(?)
# FSS can be 8, 16, etc... defined by client when sending the message? / depending on size of file sent?
def receiveMessage(clientSocket, fileSegmentSize):
    localHeaderSize = settings.HEADERSIZE
    while True:
        fullMessage = ""
        _buffer = ""
        isNewMessage = True
        while True:
            _buffer = clientSocket.recv(fileSegmentSize)  # file segment size ...
            if isNewMessage:
                messageLength = int(_buffer[:localHeaderSize])
                isNewMessage = False

            fullMessage += _buffer.decode(settings.defaultEncoding)
            print(f'Bytes sent: {len(fullMessage)}\n')

            # wait until full message is received, subtracting header information
            if (len(fullMessage)-localHeaderSize) == messageLength:
                print(f'Full message:')
                print(fullMessage[localHeaderSize:])  # We may want to instead write to a file
                isNewMessage = True
                fullMessage = ""
        # end While
    # end While
