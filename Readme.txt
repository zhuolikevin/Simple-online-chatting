*****************************************************************************************
IMPORTANT NOTICE: Thanks for referring to the README.txt. Please take minutes to read this file, especially c and d sections and the P.S./ Note in each section before running the code.

Author:            Zhuo(Kevin) Li
Email:             lizhuogo@gmail.com
Last modification: Oct 2nd 2014

All rights reserved.
*****************************************************************************************


a. A brief description of your code

This is a chatting program based on socket programming and multi-thread processing.It contains two code files (Server.py & Client.py) and a txt file which is used to store the combination of usernames and passwords. The client can use different commands (whoelse, wholasthr, broadcast, message, logintime, logout, etc.) to chat with other clients or know some of the chat room status. The server can use several commands to change parameters and monitor the server status as well. The brief structure of the two files are as follows.

Server.py:
The main thread first read the txt file and created a TCP socket to wait for requests from client. At the same time, it sets up a son thread to continuously respond to the command entered by the server controller. For each connection built up, the server sets up a son thread to verify the user with password and then respond to the different commands.

Client.py:
This code is quite simple. Two threads are set up to seperately deal with receiving the message from the server and sending the command to the server. The main thread is used to check the connection flag and catch the keyboard interrupt.

————————————————————————————————————————————————————————————————————————————————————————
b. Details on development environment

Operating System:       Mac OS X 10.9.4
programming language:   Python 2.7.3
IDE:                    Eclipse 4.4.1

————————————————————————————————————————————————————————————————————————————————————————
c. Instructions on how to run your code

Put Server.py and user_pass.txt together and run Server.py in the host machine while then Client.py in the users’ machines.

Terminals （such as Shell in Linux) can be used to run the code. First find the file location and then use “python Server.py” and “python Client.py” to run the code.

Then the Server program will display its IP and port and you can follow the instructions on Client to enter the IP and port to connect to the server. After connect to the server, the Client need to enter the username and password to be verified. And what remains is just use the commands to do what you want to do. (P.S: For both Server and Client program, you can enter ‘help’ to see what commands you can made.)

Examples will be shown in next d section.

————————————————————————————————————————————————————————————————————————————————————————
d. Sample commands in invoke your code

For Server:
|-------------DiaosChat Server Control Terminal--------------|

[NOTICE] Preparation completed
[CONFIGURATION] 
--------------------------------------------------
Server IP address         160.39.234.31
Server port number        4119
--------------------------------------------------
[PARAMETER]              
--------------------------------------------------
BLOCK_TIME                60     s
LAST_HOUR                 1      hr(s)
TIME_OUT                  30     min(s)
--------------------------------------------------
[NOTICE] Now listening for clients ...
[NOTICE] Connected with 160.39.234.31:50651 at 30,Sep,2014 20:23:52
Command>> 
[NOTICE]  google is now logged in from IP: 160.39.234.31 ( 50651 )
[LOGIN LIST] 
--------------------------------------------------
google           IP:  160.39.234.31 : 50651
--------------------------------------------------
Command>> 
[NOTICE] Connected with 160.39.234.31:50674 at 30,Sep,2014 20:30:26
Command>> 
[NOTICE]  facebook is now logged in from IP: 160.39.234.31 ( 50674 )
[LOGIN LIST] 
--------------------------------------------------
google           IP:  160.39.234.31 : 50651
facebook         IP:  160.39.234.31 : 50674
--------------------------------------------------
Command>> 
[NOTICE]  google  logged out at  Tue Sep 30 20:33:49 2014
[LOGIN LIST] 
--------------------------------------------------
facebook         IP:  160.39.234.31 : 50674
--------------------------------------------------
Command>> 
help
------------------------------------------------------------------------------
COMMAND                   FUNCTIONALITY
------------------------------------------------------------------------------
change BLOCK_TIME         To change the block time for 3 consecutive failures
change LAST_HOUR          To change the last_hour time
change TIME_OUT           To change the no-action auto-logging out time
showconfig                To show the current parameters configuration
showstatus                To show the current Server status
kickoff                   To force a current online user offline
blacklist                 To change the permanent black list
'Ctrl + C'                To terminate the Server program
------------------------------------------------------------------------------
Command>> change BLOCK_TIME
Please input BLOCK_TIME value (Unit: second): ABC
Your input must be a float or int value
Please input BLOCK_TIME value (Unit: second): 15
BLOCK_TIME is changed as:  15.0 s
Command>> showconfig
------------------------------
PARAMETER       VALUE
------------------------------
BLOCK_TIME      15.0  s
LAST_HOUR       1  hr(s)
TIME_OUT        30  min(s)
------------------------------
Command>> showstatus 
------------------------------------------------------------------------------
[Server IP address]       160.39.234.31
[Server port number]      4119
[Current User]           
facebook           IP:  160.39.234.31 : 50674
[Blocked User]           
------------------------------------------------------------------------------
Command>>

For Client.py:
dyn-160-39-234-31:haha Kevin$ python Client.py
|-------DiaosChat Client Terminal--------|

Please follow the instruction to connect to the server
HOST>> 160.39.234.31
PORT>> 4119
Successfully Connected to 160.39.234.31
|----------Welcome to DiaosChat----------|  
Username>>   
google
Password>>   
hasglasses
|----------Welcome back! google----------|  
Command>>   
<System Message> (broadcast) 30,Sep,2014 20:30:57 :
facebook is now logged in!  
Command>>   
<facebook> (broadcast) 30,Sep,2014 20:32:00 :
Hello, everyone  
Command>>   
<facebook> (private) 30,Sep,2014 20:32:33 :
hi!  
Command>>   
message<facebook><Hi, how are you?>
Command>>   
message<columbia><Call me when you are online>
columbia is not online now. He/She will receive the message when logging in  
Command>>   
help
------------------------------------------------------------------------------  
COMMAND                       FUNCTIONALITY 
------------------------------------------------------------------------------
whoelse                       Display name of other connected users 
wholasthr                     Display name of only those users that connected 
                              within the last hour 
broadcast<message>            Broadcasts <message> to all connected users 
message<user><message>        Private <message> to a <user> 
logintime                     Display how long you have been logged in
block<user>                   Put a user into your personal block list
unblock<user>                 Take a user out of your personal block list
showblockls                   Display your current block list
logout                        Logout this user  
------------------------------------------------------------------------------  
Command>>   
logintime
You have logged in for 0 h 9 min 41 s  
Command>>   
logout
|------------Goodbye, google!------------|
 
You have logged out successfully

Note:
The client command ‘broadcast<message>’ and ‘message<user><message>’, you should input ’<‘ & ‘>’. And there is no space between each of the three parts. (e.g. message<columbia><Call me when you are online>) So is that for ‘block<user>’ and ‘unblock<user>’

————————————————————————————————————————————————————————————————————————————————————————
e. Description of any additional functionalities and how they should be executed/tested

1) Display login time

[DESCRIPTION] To display the time duration from the user logged in in “ X h X min X s” format.

[TEST]  Input ‘logintime’ in the Client.py program whenever you can input commands.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
2) Messages marked with time

[DESCRIPTION] All the messages that every user receives will be marked with a time. This includes the time a user logging in and out.

[TEST] You can see the effects when you are testing  other broadcast or private message functionalities.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
3) User login and logout notification

[DESCRIPTION] When a new user logs in or a current user logs out, the server will send every ONLINE users a notification to tell them who is now change their online/offline status.

[TEST] Log a user in with valid username and password (for example, let facebook online). Then log another user in (for example, google). The first online user (refers to facebook) will see the notification as a system broadcast to tell him that google is online now. Similarly, when two users are online (facebook and google), log one of them out (let us log google out). Then the still online user (facebook) will receive a notification as a system broadcast message to tell him that google is now logged out.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
4) Offline messages

[DESCRIPTION] Online users can use ‘message<user><message>’ (NOTE: remember to use ’<‘ and ‘>’ when use this command. This is the signal that program will identify) command to send messages to users that is not online. The message is stored in the Server. When the offline user logs in, he/she will receive the message instantly.

[TEST] Log a user in with valid username and password (for example, let facebook online). Then let the user send a message use ‘message<user><message>’ command to an offline user (for example, google). Then log the user (google) in. Now the user (google) will see the message from the sender (facebook) with the sending time.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
5) block/unblock certain user in the user’s block list

[DESCRIPTION]If a user do not want to receive the message from another certain user, he can just use the ‘block<user>’ command to block another user. This blocking is PERMANENT that will stored in the Server. Even the user logs out and logs in again, his block list will still be the same, unless he use the ‘unblock<user>’. However, the block is not bidirectional, which means when google blocked facebook, he can not RECEIVE messages from facebook, but he can still SEND messages to facebook. The client can use ’showblockls’ to see who is in his block list as well.

[TEST]To test this functionality, you can first log in two users (e.g. google & facebook).  Then you can send messages between the two users. There will be no blocking in this situation. And when you input ‘block<facebook>’ in google’s terminal. google will no longer receive broadcast or private messages from facebook, unless he input ‘unblock<facebook>’. You can also use ‘showblockls’ to see who’s in your personal block list

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
6) Server commands (change PARAMETERS\showSTATUS&CONFIG\kickoff user\blacklist, etc.)

[DESCRIPTION] You can enter command in the Server console to change parameters or check the current configurations. For kickoff command, you can use the server program to kick an online client off.BUT HE CAN STILL BE ABLE TO LOG IN AGAIN. However, for blacklist command, you can ALWAYS block a username as long as it is in the BLACK_LIST. You can also add or remove usernames to or from the BLACK_LIST.

[TEST] You can enter ‘help’ to see what command you can make. Then just follow the instructions to change the parameter or do other things. For kickoff user and blacklist command, you can just log a user in and try the command on the server.

*****************************************************************************************
Thanks for reading the README.txt. Because of time limited, quite a lot other essential functionalities I came up with (e.g. user register/deregister, Server save some of the data like USER_BLOCK_LIST in a txt file in case of accidentally shutting down, etc.) can not be completed. And there is also possible to have some BUGs I haven’t found out. It needs the feedback from the user experiences. But I am sure there will be no big problems in the program.

Kevin Li
2ND OCT 2014 
*****************************************************************************************

