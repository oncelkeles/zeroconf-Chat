import socket
import sys
import os

SIZE = 1024
HOST = sys.argv[1]
PORT = int(sys.argv[2])
NAME = sys.argv[3]


try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(3)
    s.connect((HOST, PORT))
    print('You can send messages to server: ' + HOST)
except socket.error as socketerror:
    print('The server you tired to reach might have been closed.')

while True:
    user = input()
    if user:
        # '-close' will terminate the script
        if user == '-close' :
            os._exit(1)

        #establish connection to server, send message, then close the connection
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((HOST, PORT))
            user = 'message,unicast TCP,[' + NAME + ',' + HOST + ',' + 'message' + ',' + user + ']'
            user = user.encode('ascii')
            s.sendall(bytes(user))
            s.close()
            print('Message sent!')
        except socket.error as socketerror:
            print('Lost connection to server: ' + HOST + '. It might have been closed.')










