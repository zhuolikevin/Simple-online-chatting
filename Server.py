'''
-------------W4119 Programming Assignment 1-------------
Created Date:        Sep 15, 2014
Last Modified:       Feb 6, 2017
File name:           Server.py
Language:            Python 2.7.3
Author:              Zhuo (Kevin) Li
------------------All rights reserved------------------
'''
# ---------------------Source Import--------------------
import socket
import sys
from time import strftime
import time
import thread
from threading import Thread

# ------------------------Variables---------------------
LOGOUT_FLAG = 'CLOSED'                                # A message to tell the client program that it is about to close the connection
LOGIN_FLAG = 'LOGED IN'                               # A message to tell the client program that it is now logged in
MANU_TERMINATION = False                              # Flag that tells the son threads to shut down when the main shuts down
user_password = []                                    # To store all the user-password combination in the list
USER_TOTAL = 0                                        # Number of all accounts in the txt file
BLOCK_TIME = 60                                       # Login failure blocking time, can be changed for testing, unit: second
LOGIN_LIST = []                                       # To record current online users
ELSE_ONLINE = ''                                      # String for displaying other online users
MESSAGE_LIST = []                                     # To store the messages for all users
USER_ADDR = []                                        # To store the addresses of users
LOGIN_TIME = []                                       # To record the time when a user logged in
LOGOUT_TIME = []                                      # To record the time when a user logged out
LASTHOUR_LIST = []                                    # To list the users in last one hour
LAST_HOUR = 1                                         # Can be changed for testing, unit: hour
TIME_OUT = 30                                         # Automatically log out time, unit: minute
BLOCK_LIST = []                                       # To record the blocked combination of username and IP address
KICKOFF_NAME = ''                                     # The name of user that will be kicked off by the server
BLACK_LIST = []                                       # To block users from log in the chatting room
USER_BLOCKLIST = []                                   # To record the user defined block list

# ------------------------Functions---------------------
def SERVER_COMMAND(HOST, PORT):
    "To deal with command for server"
    global BLOCK_TIME, LAST_HOUR, TIME_OUT, MANU_TERMINATION, USER_ADDR, LOGIN_LIST # To modify the global variables
    global user_password, KICKOFF_NAME, BLACK_LIST

    while MANU_TERMINATION == False:
        try:
            message = raw_input('Command>> ')         # To get command
        except:
            thread.exit()

        if message == 'change BLOCK_TIME':
            while True:
                try:
                    BLOCK_TIME = float(raw_input('Please input BLOCK_TIME value (Unit: second): '))
                except ValueError:
                    print 'Your input must be a float or int value'
                except:
                    thread.exit()
                else:
                    print 'BLOCK_TIME is changed as: ', BLOCK_TIME, 's'
                    break
        elif message == 'change LAST_HOUR':
            while True:
                try:
                    LAST_HOUR = float(raw_input('Please input LAST_HOUR value (Unit: hour): '))
                except ValueError:
                    print 'Your input must be a float or int value'
                except:
                    thread.exit()
                else:
                    print 'LAST_HOUR is changed as: ', LAST_HOUR, 'hr(S)'
                    break
        elif message == 'change TIME_OUT':
            while True:
                try:
                    TIME_OUT = float(raw_input('Please input TIME_OUT vale (Unit: minute): '))
                except ValueError:
                    print 'Your input must be a float or int value'
                except:
                    thread.exit()
                else:
                    print 'TIME_OUT is changed as: ', TIME_OUT, 'min(s)'
                    break
        elif message == 'showconfig':
            print '-' * 30
            print 'PARAMETER'.ljust(15), 'VALUE'
            print '-' * 30
            print 'BLOCK_TIME'.ljust(15), BLOCK_TIME, ' s'
            print 'LAST_HOUR'.ljust(15), LAST_HOUR, ' hr(s)'
            print 'TIME_OUT'.ljust(15), TIME_OUT, ' min(s)'
            print '-' * 30
        elif message == 'showstatus':
            print '-' * 78
            print '[Server IP address]'.ljust(25), HOST
            print '[Server port number]'.ljust(25), PORT
            print '[Current User]'.ljust(25)
            for element in LOGIN_LIST:
                for number in range(len(user_password)):
                    if element == user_password[number][0]:
                        print element.ljust(15), ' IP: ', USER_ADDR[number][0], ':', USER_ADDR[number][1]
            print '[Blocked User]'.ljust(25)
            for number in range(len(BLOCK_LIST)):
                print BLOCK_LIST[number][0].ljust(15), 'blocked IP:', BLOCK_LIST[number][1]
            print '-' * 78
        elif message == 'kickoff':
            print '-' * 78
            print '[Current User]'
            for element in LOGIN_LIST:
                for number in range(len(user_password)):
                    if element == user_password[number][0]:
                        print element.ljust(15), ' IP: ', USER_ADDR[number][0], ':', USER_ADDR[number][1]
            print '-' * 78
            KICKOFF_NAME = raw_input('Please enter the user name in the above list you want to kick off: ')
            while KICKOFF_NAME not in LOGIN_LIST:
                KICKOFF_NAME = raw_input('There is no user named ' + KICKOFF_NAME +' online, please try again:')
            time.sleep(1)
            KICKOFF_NAME = ''
        elif message == 'blacklist':
            output_count = 0
            print '-' * 78
            print '[Registered Users]'
            for element in user_password:
                output_count = output_count +1
                print element[0].ljust(10),
                if output_count == 4:
                    print ''
                    output_count = 0
            if output_count != 0:
                print ''
            print '-' * 78
            output_count = 0
            print '[BLACK LIST]'
            for element in BLACK_LIST:
                output_count = output_count +1
                print element.ljust(10),
                if output_count == 4:
                    print ''
                    output_count = 0
            if output_count != 0:
                print ''
            print '-' * 78

            ARfinish = False
            while ARfinish == False:
                ad_or_rm = raw_input('Do you want to add or remove a user to or from the BLACK LIST? (a/r): ')
                if ad_or_rm == 'a':
                    non_register_user = True
                    new_blackname = ''
                    while non_register_user == True or new_blackname in BLACK_LIST:
                        new_blackname = raw_input('Please input the username you want to add to the BLACK LIST: ')
                        #print new_blackname
                        for element in user_password:
                            if element[0] == new_blackname: non_register_user = False
                        if non_register_user == True:
                            print new_blackname, 'is not a registered username.'
                        elif non_register_user == False and new_blackname in BLACK_LIST:
                            print new_blackname, 'is already in the BLACK LIST.'

                    #print new_blackname
                    BLACK_LIST.append(new_blackname)
                    KICKOFF_NAME = new_blackname
                    time.sleep(1)
                    KICKOFF_NAME = ''
                    print '[NOTICE] ', new_blackname, 'is now added to the BLACK LIST'
                    ARfinish = True
                elif ad_or_rm == 'r':
                    non_register_user = True
                    rm_blackname = ''
                    while non_register_user == True or rm_blackname not in BLACK_LIST:
                        rm_blackname = raw_input('Please input the username you want to remove from the BLACK LIST: ')
                        for element in user_password:
                            if element[0] == rm_blackname: non_register_user = False
                        if non_register_user == True:
                            print rm_blackname, 'is not a registered username.'
                        elif non_register_user == False and rm_blackname not in BLACK_LIST:
                            print rm_blackname, 'is not in the BLACK LIST.'

                    BLACK_LIST.remove(rm_blackname)
                    print '[NOTICE] ', rm_blackname, 'is now removed from the BLACK LIST'
                    ARfinish = True
                else:
                    print 'Please enter \'a\' to add a black name, or \'r\' to remove a black name!'

            print '-' * 78
            output_count = 0
            print '[BLACK LIST]'
            for element in BLACK_LIST:
                output_count = output_count +1
                print element.ljust(10),
                if output_count == 4:
                    print ''
                    output_count = 0
            if output_count != 0:
                print ''
            print '-' * 78

        elif message == 'help':
            print '-' * 78
            print 'COMMAND'.ljust(25), 'FUNCTIONALITY'
            print '-' * 78
            print 'change BLOCK_TIME'.ljust(25), 'To change the block time for 3 consecutive failures'
            print 'change LAST_HOUR'.ljust(25), 'To change the last_hour time'
            print 'change TIME_OUT'.ljust(25), 'To change the no-action auto-logging out time'
            print 'showconfig'.ljust(25), 'To show the current parameters configuration'
            print 'showstatus'.ljust(25), 'To show the current Server status'
            print 'kickoff'.ljust(25), 'To force a current online user offline'
            print 'blacklist'.ljust(25), 'To change the permanent black list'
            print '\'Ctrl + C\''.ljust(25), 'To terminate the Server program'
            print '-' * 78
        else:
            print 'We cannot understand your command. Please type \'help\' for help.'

    # This means the MANU_TERMINATION is true, then kill the thread
    thread.exit()

    return

def pre_setting():
    "To read the file and initialize the variables"
    try:
        userlist = open("user_pass.txt","r")
    except:
        print 'Cannot find corresponding file'

    allusers = userlist.readlines()                       # Read file in lines
    i = 0
    usernumber = len(allusers)
    user_password=[0]*usernumber                          # Initialize a list to store users and passwords
    for singleuser in allusers:
        user_password[i] = (singleuser.strip()).split()   # Cut the string with space
        i = i + 1

    for num in range(0,usernumber):
        MESSAGE_LIST.append([])
        USER_ADDR.append(())
        LOGIN_TIME.append(0)
        LOGOUT_TIME.append(0)
        USER_BLOCKLIST.append([])

    userlist.close()

    return (usernumber, user_password, MESSAGE_LIST, USER_ADDR, LOGIN_LIST, LOGIN_TIME)

def update_lasthr():
    "To update the list of last_hour online users"
    global LASTHOUR_LIST

    if len(LASTHOUR_LIST) != 0:
        for number in range(len(LOGIN_TIME)):
            if LOGIN_TIME[number] != 0:
                if (time.time() - LOGOUT_TIME[number]) > (LAST_HOUR * 3600) and (user_password[number][0] not in LOGIN_LIST):
                    if user_password[number][0] in LASTHOUR_LIST:
                        LASTHOUR_LIST.remove(user_password[number][0])
                        print '[NOTICE] Users in the past', LAST_HOUR, 'hr(s):', LASTHOUR_LIST
                        print '\bCommand>> '
    return

def update_blocklist():
    "To update the block list"
    global BLOCK_LIST

    for element in BLOCK_LIST:
        if time.time() - element[2] >= BLOCK_TIME:
            BLOCK_LIST.remove(element)

    return

def command_whoelse(name_num, conn):
    "To deal with 'whoelse' command"
    if len(LOGIN_LIST) == 1:
        conn.send('\r\bOnly you are online now!')
    else:
        elseonline = ''
        for element in LOGIN_LIST:
            if element != user_password[name_num][0]:
                elseonline = elseonline + element + ' '
        conn.send('\r\bOther online user(s): ' + elseonline)

    return

def command_wholasthr(name_num, conn):
    "To deal with 'wholasthr' command"
    if len(LASTHOUR_LIST) == 1:
        conn.send('\r\bOnly you are online in the past ' + str(LAST_HOUR) + ' hour !')
    else:
        elselasthr = ''
        for element in LASTHOUR_LIST:
            if element != user_password[name_num][0]:
                elselasthr = elselasthr + element + ' '
        conn.send('\r\bOther user(s) in the past ' + str(LAST_HOUR) + ' hr(s): ' + elselasthr)

    return

def command_broadcast(name_num, username, br_message):
    "To deal with broadcast message sending"
    for element in LOGIN_LIST:
        if element != user_password[name_num][0]:
            for number in range(len(user_password)):
                if element in user_password[number]:
                    message_num = number
                    MESSAGE_LIST[message_num].append('\r\b<' + username + '> (broadcast) ' + strftime("%d,%b,%Y %H:%M:%S", time.localtime()) + ' :\n\b' + br_message)

    return

def command_private(receiver_name, pr_message, username, conn):
    "To deal with private message sending"
    onlist_receiver = False
    online_receiver = False

    for number in range(len(user_password)):
        if user_password[number][0] == receiver_name:
            message_num = number
            onlist_receiver = True

    if onlist_receiver == False:
        conn.send('\r\bThere is no user whose name is ' + receiver_name)
    else:

        for number in range(len(LOGIN_LIST)):
            if LOGIN_LIST[number] == receiver_name:
                online_receiver = True

        if online_receiver == False:
            MESSAGE_LIST[message_num].append('\r\b<' + username + '> (private) ' + strftime("%d,%b,%Y %H:%M:%S", time.localtime()) + ' :\n\b' + pr_message)
            conn.send('\b' + receiver_name + ' is not online now. He/She will receive the message when logging in')
        else:
            MESSAGE_LIST[message_num].append('\r\b<' + username + '> (private) ' + strftime("%d,%b,%Y %H:%M:%S", time.localtime()) + ' :\n\b' + pr_message)

    return

def command_block(name_num, bl_name, conn):
    "To deal with blocking a certain user"
    global USER_BLOCKLIST

    wr_blname = True
    re_blname = False

    for element in user_password:
        if element[0] == bl_name: wr_blname = False
    if bl_name in USER_BLOCKLIST[name_num]: re_blname = True

    if wr_blname == True:
        conn.send(bl_name + ' is not a registered username! Please confirm and retry your command.')
    elif wr_blname == False and re_blname == True:
        conn.send(bl_name + ' is already in your block list!')
    else:
        USER_BLOCKLIST[name_num].append(bl_name)
        conn.send(bl_name + ' is now blocked!')

    return

def command_unblock(name_num, ubl_name, conn):
    "To deal with unblocking a blocked user"
    global USER_BLOCKLIST

    wr_ublname = True
    no_ublname = False

    for element in user_password:
        if element[0] == ubl_name: wr_ublname = False
    if ubl_name not in USER_BLOCKLIST[name_num]: no_ublname = True

    if wr_ublname == True:
        conn.send(ubl_name + ' is not a registered username! Please confirm and retry your command')
    elif wr_ublname == False and no_ublname == True:
        conn.send(ubl_name + ' is not in your block list!')
    else:
        USER_BLOCKLIST[name_num].remove(ubl_name)
        conn.send(ubl_name + ' is now unblocked')

    return

def user_logout(name_num, conn):
    "To deal with logging out process"

    global LOGIN_LIST

    LOGIN_LIST.remove(user_password[name_num][0])
    time.sleep(0.1)
    conn.send(LOGOUT_FLAG)
    LOGOUT_TIME[name_num] = time.time()
    ConnStatus = False
    command_broadcast(name_num, 'System Message', user_password[name_num][0] + ' is now logged out!')
    print '\r\b[NOTICE] ', user_password[name_num][0], ' logged out at ', time.ctime(time.time())
    print '[LOGIN LIST] '
    print '-' * 50
    for element in LOGIN_LIST:
        for number in range(len(user_password)):
            if element == user_password[number][0]:
                print element.ljust(15), ' IP: ', USER_ADDR[number][0], ':', USER_ADDR[number][1]
    print '-' * 50
    print '\r\bCommand>> '
    conn.close()

    return ConnStatus

def clientthread(conn,addr):
    "To control the new client thread"

    global BLOCK_LIST

    conn.send('|' + 'Welcome to DiaosChat'.center(40,'-') + '|')
    time.sleep(0.1)
    conn.send('\bUsername>> ')

    # Variables used in the thread
    validname = False
    validpassword = False
    relogin = False
    countinvalidpw = 0
    ConnStatus = True
    blocklogin = False
    inblocklist = False
    commandfinish = False
    name_num = 0
    blocklist = []

    # >>>>>>>>>>>>>>>>>>>>>>>>>To get username<<<<<<<<<<<<<<<<<<<<<<<<<
    while validname == False:

        conn.settimeout(1)
        try:
            username = conn.recv(1024)
            if not username: break
        except socket.timeout:
            # This is for the situation that the server terminates when the client is still entering the username
            if MANU_TERMINATION == True:
                conn.send('Server is about to close, now automatically logging out!\n')
                time.sleep(0.1)
                conn.send(LOGOUT_FLAG)
                ConnStatus = False
                thread.exit()
        except:
            thread.exit()
        else:
            if MANU_TERMINATION == False:
                # To find if the client terminated before entering the username
                if username == 'prelgout':
                    print '[NOTICE] ', addr[0], ':', addr[1], ' terminated before logging in.'
                    print 'Command>> '
                    thread.exit()

                # To find if the username and IP are in the BLOCK_LIST
                inblocklist = False
                for element in BLOCK_LIST:
                    if element[0] == username and element[1] == addr[0]:
                        inblocklist = True

                # If the username and IP are in the BLOCK_LIST
                if inblocklist == True:
                    conn.send('You are still in the block list!\n')
                    time.sleep(0.1)
                    conn.send('Username>> ')
                    blocklogin = True
                else:
                    blocklogin = False

                # If it is not in the BLOCK_LIST, this is the normal process to verify username
                if blocklogin == False and username not in BLACK_LIST:
                    # Check if the entered username in the record and in the LOGIN_LIST
                    for number in range(USER_TOTAL):
                        if user_password[number][0] == username and username not in LOGIN_LIST:
                            if blocklogin == False:
                                name_num = number                        # Record the number of username in the list
                                validname = True
                                conn.send('Password>> ')

                        elif user_password[number][0] == username and username in LOGIN_LIST:
                            conn.send('\rThis username has already logged in, it cannot be logged in again!\n' + \
                            'Please try another username!\n')
                            time.sleep(0.1)
                            conn.send('\rUsername>> ')
                            relogin = True                               # Marked as relogin

                    if validname == False and relogin == False and blocklogin == False:
                        conn.send('\rThis username does not match our records! Please confirm and enter again:')
                        time.sleep(0.1)
                        conn.send('\rUsername>> ')

                if username in BLACK_LIST:
                    conn.send('\rThis username are in the Server BLACK LIST, you can not log in!')
                    time.sleep(0.1)
                    conn.send('\rUsername>> ')
            else:
                conn.send('Server is about to close, now automatically logging out!')
                time.sleep(0.1)
                conn.send(LOGOUT_FLAG)
                ConnStatus = False
                thread.exit()

    # >>>>>>>>>>>>>>>>>>>>>>>>>To get password<<<<<<<<<<<<<<<<<<<<<<<<<
    while validpassword == False:

        conn.settimeout(1)
        try:
            password = conn.recv(1024)
            if not password: break
        except socket.timeout:
            # This is for the situation that the server terminates when the client is still entering the password
            if MANU_TERMINATION == True:
                conn.send('Server is about to close, now automatically logging out!')
                time.sleep(0.1)
                conn.send(LOGOUT_FLAG)
                ConnStatus = False
                thread.exit()
        except:
            thread.exit()
        else:
            if MANU_TERMINATION == False:
                # To find if the client terminated before entering the password
                if password == 'prelgout':
                    print '[NOTICE] ', addr[0], ':', addr[1], ' terminated before logging in.'
                    print 'Command>> '
                    thread.exit()

                # To find if the username and IP are in the BLOCK_LIST
                inblocklist = False
                for element in BLOCK_LIST:
                    if element[0] == username and element[1] == addr[0]:
                        inblocklist = True

                # If the username and IP are in the BLOCK_LIST
                if inblocklist == True:
                    conn.send('\rYou are still in the block list!')
                    time.sleep(0.1)
                    conn.send('\rPassword>> ')
                    blocklogin = True
                else:
                    blocklogin = False

                # If it is not in the BLOCK_LIST, this is the normal process to verify password
                if blocklogin == False:
                    # Check if the password is correct
                    if password == user_password[name_num][1] and username not in LOGIN_LIST:          # The password is correct, log the user in
                        validpassword = True
                        conn.send('\r|' + ('Welcome back! ' + user_password[name_num][0]).center(40,'-') + '|')
                        time.sleep(0.1)
                        conn.send(LOGIN_FLAG)
                        LOGIN_LIST.append(user_password[name_num][0])                                  # Add the user to currently logined user list
                        command_broadcast(name_num, 'System Message', user_password[name_num][0] + ' is now logged in!')

                        USER_ADDR[name_num] = addr
                        LOGIN_TIME[name_num] = time.time()
                        LASTHOUR_LIST.append(user_password[name_num][0])

                        print '[NOTICE] ', user_password[name_num][0], 'is now logged in from IP:', addr[0], '(', addr[1], ')', 'at ', strftime("%d,%b,%Y %H:%M:%S", time.localtime())
                        print '[LOGIN LIST] '
                        print '-' * 50
                        for element in LOGIN_LIST:
                            for number in range(len(user_password)):
                                if element == user_password[number][0]:
                                    print element.ljust(15), ' IP: ', USER_ADDR[number][0], ':', USER_ADDR[number][1]
                        print '-' * 50
                        print '\rCommand>> '

                        commandfinish = True
                        firstcommand = True
                        count = 0

                        countinvalidpw = 0
                    elif password != user_password[name_num][1]:
                        countinvalidpw = countinvalidpw + 1

                        if countinvalidpw == 1 or countinvalidpw == 2:               # Warning and penalty for 3 consecutive failure
                            conn.send('\rThe password does not match your username! Please confirm and enter again!\n' + \
                            'You still have ' + str(3-countinvalidpw) + ' chance(s) to try!')
                            time.sleep(0.1)
                            conn.send('\rPassword>> ')
                        else:
                            conn.send('\rBecause of 3 consecutive failure, you will be blocked from logging in DiaoChat for ' + str(BLOCK_TIME) +' seconds!')

                        if countinvalidpw == 3:
                            blocktime = time.time()
                            BLOCK_LIST.append([user_password[name_num][0],addr[0],blocktime])
                            print '[NOTICE] ', user_password[name_num][0], 'is now blocked from IP:', addr[0]
                            print '[BLOCK LIST] '
                            print '-' * 50
                            for number in range(len(BLOCK_LIST)):
                                print (BLOCK_LIST[number][0]).ljust(15), 'blocked from IP:', BLOCK_LIST[number][1]
                            print '-' * 50

                            conn.send('\rPassword>> ')
                            countinvalidpw = 0

                    else:
                        conn.send('\rThis username has already logged in, it cannot be logged in again!\n' + \
                        'Please use \'Ctrl + C\' to terminate the program. And connect again to try another username!')
                        time.sleep(0.1)


    # >>>>>>>>>>>>>>>>>>>>>>>>>After log in<<<<<<<<<<<<<<<<<<<<<<<<<
    while ConnStatus == True :
        # If the server is terminated manually, then log out the user and terminate the thread
        if MANU_TERMINATION == True:
            conn.send('Server is about to close, now automatically logging out!')
            LOGIN_LIST.remove(user_password[name_num][0])
            time.sleep(0.1)
            conn.send(LOGOUT_FLAG)
            LOGOUT_TIME[name_num] = time.time()
            ConnStatus = False
            command_broadcast(name_num, 'System Message', user_password[name_num][0] + ' is now logged out!')
            thread.exit()

        # If the user is kicked off by the server, then log it out
        if user_password[name_num][0] == KICKOFF_NAME:
            conn.send('You have been kicked off by the administrator! Now being forcely terminated...')
            LOGIN_LIST.remove(user_password[name_num][0])
            time.sleep(0.1)
            conn.send(LOGOUT_FLAG)
            LOGOUT_TIME[name_num] = time.time()
            ConnStatus = False
            command_broadcast(name_num, 'System Message', user_password[name_num][0] + ' is now kicked off by the administrator!')
            print '[NOTICE]', user_password[name_num][0], 'is now kicked off successfully.'
            thread.exit()

        # To broadcast or send private messages
        if MESSAGE_LIST[name_num] != 0:
            for element in MESSAGE_LIST[name_num]:
                blackedone = False
                for name in USER_BLOCKLIST[name_num]:
                    if element[(element.find('<') + 1):element.find('>')] == name: blackedone = True
                if blackedone == False:
                    conn.send('\r' + element)
                    time.sleep(0.1)
                    if firstcommand != True:
                        conn.send('Command>> ')
            MESSAGE_LIST[name_num] = []
        firstcommand = False

        command = ''

        if commandfinish == True:
            time.sleep(0.1)
            conn.send('Command>> ')

        # To set timeout for socket with specific client
        conn.settimeout(1)

        try:
            command = conn.recv(1024)
        except socket.timeout:
            commandfinish = False
            count = count + 1
        except socket.error:
            pass
        else:
            commandfinish = True
            count = 0

        # To deal with no activities for a long time
        if count >= (TIME_OUT *60):
            conn.send('\rWe found you are inactive for ' + str(TIME_OUT) + ' minutes. To ensure the safety of your account, we are now logging you out!')
            ConnStatus = user_logout(name_num, conn)

#-------------------------Check Commands---------------------------#
        # Command for checking other connected users
        if command == 'whoelse':
            command_whoelse(name_num, conn)

        # Command for displaying the other users that connected within one hour
        elif command == 'wholasthr':
            command_wholasthr(name_num, conn)

        # Command for broadcast messages to everyone online
        elif command.find('broadcast<', 0, 10) == 0 and command.find('>', 10) != -1:
            br_message = command[10:command.find('>', 10)]
            command_broadcast(name_num, username, br_message)
            #print MESSAGE_LIST

        # Command for sending private messages to a specific person
        elif command.find('message<', 0, 8) == 0 and command.find('><', 8) != -1 and (command.rfind('>')>command.rfind('<')) == True:
            receiver_name = command[8:command.find('><', 8)]
            pr_message = command[(command.rfind('<')+1):command.rfind('>')]
            command_private(receiver_name, pr_message, username, conn)

        # Command for display the login time
        elif command == 'logintime':
            logintime = time.time() - LOGIN_TIME[name_num]
            conn.send('\rYou have logged in for ' + str(int(logintime/3600)) + ' h ' + str(int((logintime%3600)/60)) + ' min ' + str(int(logintime%60)) + ' s')

        # Command for blocking another user's message
        elif command.find('block<', 0, 6) == 0 and command.find('>', 6) != -1:
            bl_name = command[6:command.find('>', 6)]
            command_block(name_num, bl_name, conn)

        # Command for unblocking another user's message
        elif command.find('unblock<', 0, 8) == 0 and command.find('>', 8) != -1:
            showlist = ''
            for element in USER_BLOCKLIST[name_num]:
                showlist = showlist + element + ' '
            conn.send('-' * 78 + '\n' + \
                      '[BLOCK LIST] ' + '\n' + \
                      showlist + '\n' + \
                      '-' * 78)
            ubl_name =command[8:command.find('>', 8)]
            command_unblock(name_num, ubl_name, conn)

        # Command for displaying the user's block list
        elif command == 'showblockls':
            showlist = ''
            for element in USER_BLOCKLIST[name_num]:
                showlist = showlist + element + ' '
            conn.send('-' * 78 + '\n' + \
                      '[BLOCK LIST] ' + '\n' + \
                      showlist + '\n' + \
                      '-' * 78)

        # Command for logging out
        elif command == 'logout':
            conn.send('\r' +'|' + ('Goodbye, ' + user_password[name_num][0] + '!').center(40,'-') + '|' + '\n')
            ConnStatus = user_logout(name_num, conn)

        # Command for listing all the valid commands
        elif command == 'help':
            conn.send('-' * 78)
            time.sleep(0.1)
            conn.send('COMMAND'.ljust(30) + 'FUNCTIONALITY \n' + \
                      '-' * 78 + '\n' + \
                      'whoelse'.ljust(30) + 'Display name of other connected users \n' + \
                      'wholasthr'.ljust(30) + 'Display name of only those users that connected \n' +\
                      ' '.ljust(30) + 'within the last hour \n' + \
                      'broadcast<message>'.ljust(30)  + 'Broadcasts <message> to all connected users \n' + \
                      'message<user><message>'.ljust(30)  + 'Private <message> to a <user> \n' + \
                      'logintime'.ljust(30) + 'Display how long you have been logged in\n' + \
                      'block<user>'.ljust(30) + 'Put a user into your personal block list\n' + \
                      'unblock<user>'.ljust(30) + 'Take a user out of your personal block list\n' + \
                      'showblockls'.ljust(30) + 'Display your current block list\n' + \
                      'logout'.ljust(30)  + 'Logout this user')
            time.sleep(0.1)
            conn.send('-' * 78)

        # For no command, just pass
        elif command == '':
            pass

        # For unknown command
        else:
            conn.send('\r\bWe cannot understand your action. Please type "help" for help.')

    # If it reaches this sentence, it means the connection is broken, the son thread can be terminated
    thread.exit()

    return

if __name__ == "__main__":

    print '|' + 'DiaosChat Server Control Terminal'.center(60,'-') + '|' + '\n'

    # File read and variable initialization
    (USER_TOTAL,user_password, MESSAGE_LIST, USER_ADDR, LOGIN_LIST, LOGIN_TIME) = pre_setting()

    # Define the name of host and the port #
    HOST = socket.gethostbyname(socket.gethostname())
    PORT = 4118

    # Create a TCP socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # bind socket with host and port
    try:
        s.bind((HOST, PORT))
    except socket.error , msg:
        print 'Bind failed. Error Code: ' + str(msg[0]) + ' Message ' + msg[1]
        sys.exit()

    # Display current server status
    print '[NOTICE] Preparation completed'
    print '[CONFIGURATION] '
    print '-' * 50
    print 'Server IP address'.ljust(25), HOST
    print 'Server port number'.ljust(25), PORT
    print '-' * 50
    # Display current parameter setting
    print '[PARAMETER]'.ljust(25)
    print '-' * 50
    print 'BLOCK_TIME'.ljust(25), str(BLOCK_TIME).ljust(5), ' s'
    print 'LAST_HOUR'.ljust(25), str(LAST_HOUR).ljust(5), ' hr(s)'
    print 'TIME_OUT'.ljust(25), str(TIME_OUT).ljust(5), ' min(s)'
    print '-' * 50

    # listen to connection requests from clients
    s.listen(10)
    print '[NOTICE] Now listening for clients ...'

    # This thread are for receiving and dealing with server command
    command_thread = Thread(target = SERVER_COMMAND, args = (HOST, PORT,))
    command_thread.setDaemon(True)
    command_thread.start()

    while MANU_TERMINATION == False:

        havedone = False

        # Set timeout for listening socket
        s.settimeout(1)
        try:
            conn, addr = s.accept()
            print '\r[NOTICE] Connected with ' + addr[0] + ':' + str(addr[1]) + ' at ' + strftime("%d,%b,%Y %H:%M:%S", time.localtime())
            print 'Command>> '

            # Create a new son thread for each of the connected clients
            new_thread = Thread(target = clientthread, args = (conn,addr,))
            new_thread.setDaemon(True)
            new_thread.start()


        except socket.timeout:
            pass
        except KeyboardInterrupt:                                    # To catch keyboard interrupt
            print '\r\b[NOTICE] This program is about to terminate via \" Ctrl + C\".'
            MANU_TERMINATION = True                                  # Set up flag to shut all the son threads down
            time.sleep(1)                                            # Waiting for all the son threads to be shut down
            print '[NOTICE] Successfully logged all the clients out'
            havedone = True

        if havedone == False:
            try:
                # Update the list of users that connected within one hour
                update_lasthr()
                # Update the block list
                update_blocklist()
            except KeyboardInterrupt:
                print '\r\b[NOTICE] This program is about to terminate via \" Ctrl + C\".'
                MANU_TERMINATION = True                                  # Set up flag to shut all the son threads down
                time.sleep(1)                                            # Waiting for all the son threads to be shut down
                print '[NOTICE] Successfully logged all the clients out'

    # This means the MANU_TERMINATION is true, so shut the program down
    s.close()
    sys.exit()
