<div align="center">

# Simplified File Transfer Protocol

</div>

## Overview:
Implement a simplified FTP server and FTP client where the client connects to the server and supports BOTH uploading and downloading files to/from the server.


## Program Execution Instructions
Invoke the server and then invoke the client before sending any commands.
### Invoke Server
```sh
python3 -m Server 1234
```
### Invoke Client
```sh
python3 -m Client localhost 1234
```

## Using Command-Line Arguments
### GET
Find file from server, and then send to client.
```sh
ftp> get FILENAME
```

### PUT
Send file from client to server.
```sh
ftp> put FILENAME
```

### LS
List all files in the current directory.
```sh
ftp> ls
```

### QUIT
Close connection between client and server.
```sh
ftp> quit
```

### Problems:
1. Not all data may arrive at the same time
2. rec() returns after emptying the receive buffer of the socket
3. What kinds of messages will be exchanged across the control channel?
4. How should the other side respond to the messages?
5. What sizes/formats will the messages have?
6. What message exchanges have to take place in order to set up a file transfer
   channel?
7. How will the receiving side know when to start/stop receiving the file?
8. How to avoid overflowing TCP buffers?

## Technical Specifications:
The server is invoked as follows:
```sh
pythonserv.py<PORTNUMBER>
```

where <PORTNUMBER> specifies the port the FTP server accepts connection requests.
```sh
Example: pythonserv.py 1234
```

The FTP client is invoked as follows:
```sh
cli <servermachine> <serverport>
```

servermachine is the domain name of the server (ecs.fullerton.edu). Convert into 32-bit IP address using DNS lookup.

serverport example.
> Example: python cli.py ecs.fullerton.edu 1234


The user must be able to execute the following commands.
```sh
ftp> get <file name> (downloads file <file name> from the server)
ftp> put <file name> (uploads file <file name> to the server)
ftp> ls (lists files on the server)
ftp> quit (disconnects from the server and exits)
```

Be sure to use two connections for each FTP session - control & data
- Control lasts throughout the FTP session
- Control transfers all commands (ls, get, put) from client to server (as well as all status/error messages)
- Data is established for EVERY file transfer using an ephemeral port

Server should () with each message:
1. Print out message
2. Indicate Success or Failure of command
3. Print fileName, and numberOfBytesTransferred

### Submission Specifications
Due: 12/01/2023 on Friday before midnight.

Submitted by only (1) member via Canvas

Groups of up to 5 students. No individual work is accepted.

_The assignment must be coded in C++, Java, or Python._

## Meta
Course: **CPSC 471**. Project with Professor Kurban.

Language Chosen: **Python**

https://github.com/YuvalNoiman/CPSC_471_Project/

### Team Members:
```sh
Dylan Gunter, dgunter@csu.fullerton.edu
Yuval Noiman, yuvalnoiman@csu.fullerton.edu
Angel Zambrano, AngelZ@fullerton.edu
Patton Tang, pattontanges@csu.fullerton.edu
```
