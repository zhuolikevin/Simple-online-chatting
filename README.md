Simple-online-chatting
======================
a. A brief description of the code

This is a chatting program based on socket programming and multi-thread processing.It contains two code files (Server.py & Client.py) and a txt file which is used to store the combination of usernames and passwords. The client can use different commands (whoelse, wholasthr, broadcast, message, logintime, logout, etc.) to chat with other clients or know some of the chat room status. The server can use several commands to change parameters and monitor the server status as well. The brief structure of the two files are as follows.

Server.py:
The main thread first read the txt file and created a TCP socket to wait for requests from client. At the same time, it sets up a son thread to continuously respond to the command entered by the server controller. For each connection built up, the server sets up a son thread to verify the user with password and then respond to the different commands.

Client.py:
This code is quite simple. Two threads are set up to seperately deal with receiving the message from the server and sending the command to the server. The main thread is used to check the connection flag and catch the keyboard interrupt.


b. Details on development environment

Operating System:       Mac OS X 10.9.4
programming language:   Python 2.7.3
IDE:                    Eclipse 4.4.1


c. Instructions on how to run the code

Put Server.py and user_pass.txt together and run Server.py in the host machine while then Client.py in the users’ machines.

Terminals （such as Shell in Linux) can be used to run the code. First find the file location and then use “python Server.py” and “python Client.py” to run the code.

Then the Server program will display its IP and port and you can follow the instructions on Client to enter the IP and port to connect to the server. After connect to the server, the Client need to enter the username and password to be verified. And what remains is just use the commands to do what you want to do. (P.S: For both Server and Client program, you can enter ‘help’ to see what commands you can made.)



