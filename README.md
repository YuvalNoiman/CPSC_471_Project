# Simplified File Transfer Protocol
### Server and Client
Due: 12/01/2023 on Friday before midnight.

Submitted by only (1) member via Canvas

### Team:
Groups of up to 5 students. No individual work is accepted.

Course: **CPSC 471**. Project with Professor Kurban

_The assignment must be coded in C++, Java, or Python._

Language Chosen: **Python**

Team Members:
> NAME, email
>
> Patton Tang, pattontanges@csu.fullerton.edu
>
> NAME, email
>
> NAME, email
>

# Program Execution Instructions
... (Work In Progress)
...
...

## Overview:
Implement a simplified FTP server and FTP client where the client connects to the server and supports BOTH uploading and downloading files to/from the server.

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

## Specifications:
The server is invoked as follows:
> pythonserv.py<PORTNUMBER>

where <PORTNUMBER> specifies the port the FTP server accepts connection requests.
> Example: pythonserv.py 1234

The FTP client is invoked as follows:
> cli <\servermachine\> <\serverport\>

servermachine is the domain name of the server (ecs.fullerton.edu). Convert into 32-bit IP address using DNS lookup.

serverport example.
> Example: python cli.py ecs.fullerton.edu 1234


The user must be able to execute the following commands.
> ftp> get <\file name\> _(downloads file <file name> from the server)_
>
> ftp> put <\file name\> _(uploads file <file name> to the server)_
>
> ftp> ls _(lists files on the server)_
>
> ftp> quit _(disconnects from the server and exits)_

Be sure to use two connections for each FTP session - control & data
- Control lasts throughout the FTP session
- Control transfers all commands (ls, get, put) from client to server (as well as all status/error messages)
- Data is established for EVERY file transfer using an ephemeral port
- 