'''
-------------W4119 Programming Assignment 1-------------
Created Date:        Sep 14, 2014
File name:           Client.py
Last Modified:       Feb 6, 2017
Language:            Python 2.7.3
Author:              Zhuo (Kevin) Li
------------------All rights reserved------------------
'''
# ---------------------Source Import--------------------
import socket
import sys
import thread
from threading import Thread
import time

# ------------------------Variables---------------------
LOGOUT_FLAG = 'CLOSED'                                # A message to tell the client program that it is about to close the connection
LOGIN_FLAG = 'LOGED IN'                               # A message to tell the client program that it is now logged in
LOGIN_STATUS = False                                  # To mark the user as online or offline
CONNECT_STATUS = False                                # To mark if the server sends logout message to the client
SHUTDOWN_THREAD = False                               # Flag that tells the son threads to exit
validport = False                                     # To mark if the user enters a valid port number
message = ''

# ------------------------Functions---------------------
def recv_from(conn):
    "To receive messages from the server"
    global CONNECT_STATUS, LOGIN_STATUS, LOGOUT_FLAG, LOGIN_FLAG, SHUTDOWN_THREAD

    while SHUTDOWN_THREAD == False:                   # To see if there is a shutting down message from the main thread
        try:
            reply = conn.recv(1024)
            if reply == LOGIN_FLAG:                   # If received a login message
                LOGIN_STATUS = True
            elif reply == LOGOUT_FLAG:                # If received a logout message
                print 'You have logged out successfully'
                CONNECT_STATUS = False
                LOGIN_STATUS = False
                conn.close()
                thread.exit()
            else:                                     # The most common situation is to display what server sends
                print reply,''

        except socket.error:                          # If messages can not be received
            if CONNECT_STATUS == True:                # It is maybe because of the connection broken if the user still marked online
                print 'Receive failed. Remote server may have closed the connection.'
            else:                                     # Or it can be because of the user logged out
                print '\nYou have logged out successfully.'
            sys.exit()

    # If the son thread reaches this sentence, it must be terminated by the main thread
    thread.exit()

    return

def send_to(conn):
    "To send messages to the server"
    global CONNECT_STATUS, SHUTDOWN_THREAD

    while SHUTDOWN_THREAD == False:                   # To see if there is a shutting down message from the main thread
        try:
            message = raw_input()                     # Input messages to send
        except:
            thread.exit()

        try:
            s.send(message)
        except socket.error:                          # If it fails to send the message to the server
            if CONNECT_STATUS == True:                # There may be some problems when the user is still connected to the server
                print 'Send failed'
                sys.exit()
            else:                                     # Or it is because the connection is broken.
                thread.exit()

    # If the son thread reaches this sentence, it must be terminated by the main thread
    thread.exit()

    return

if __name__ == '__main__':

    # To set up a TCP socket
    try:
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    except socket.error, msg:
        print 'Failed to creat socket. Error code:'+str(msg[0])+', Error message:'+ msg[1]
        sys.exit()

    # Instructions for connection
    print '|' + 'DiaosChat Client Terminal'.center(40,'-') + '|' + '\n'
    print 'Please follow the instruction to connect to the server'

    # To enter the hostname and port to connect to the server
    while CONNECT_STATUS == False:
        try:
            HOST = raw_input('HOST>> ')
            while validport == False:                 # To verify that the port input is an integral
                try:
                    PORT = int(raw_input('PORT>> '))
                except ValueError:
                    print 'PORT number should be a integral!'
                else:
                    validport = True

            try:                                      # Try to connect to the server
                s.connect((HOST , PORT))
                print 'Successfully Connected to ' + HOST
                CONNECT_STATUS = True
            except KeyboardInterrupt:                 # In case there is a keyboard interrupt
                print 'The program is terminated by\'Ctrl + C\'.'
                sys.exit()
            except:
                validport = False
                print 'Cannot connect to the server, please check your information and try again!'

        except KeyboardInterrupt:                     # In case there is a keyboard interrupt in this duration
            print 'The program is terminated by \'Ctrl + C\'.'
            sys.exit()

    # Thread for receiving
    new_thread1=Thread(target = recv_from, args = (s,))
    new_thread1.setDaemon(True)
    new_thread1.start()

    # Thread for sending
    new_thread2=Thread(target = send_to, args = (s,))
    new_thread2.setDaemon(True)
    new_thread2.start()

    while True:
        try:
            time.sleep(1)
            if CONNECT_STATUS == False:               # To check if the client is still connected to the server
                sys.exit()
        except KeyboardInterrupt:                     # To catch the Ctrl + C interrupt
            print '\r\bThis program is terminated via \" Ctrl + C\".'
            if LOGIN_STATUS == True:                  # If the client is online
                s.send('logout')                      # then log it out
            else:                                     # Otherwise it will be at username or password entering process
                s.send('prelgout')                    # then pre-logout
            SHUTDOWN_THREAD = True                    # To tell all the son threads to shut down
            time.sleep(0.01)
            sys.exit()
