import socket
import ipaddress
import sys
import select
import threading
import queue
import time
import os
from threading import Thread

#initiliaze IP, port and name
SIZE = 1024
PORT = int(sys.argv[1])
NAME = sys.argv[2]
COUNT = 0
ip  = socket.gethostbyname(socket.gethostname())
HOST = ip

openservers = []
openservers.append(HOST)
respondservers = []
respondservers.append(HOST)




#listen UDP packets
def listenUDP():
    global COUNT
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('', PORT))
    while True:
        data, addr = s.recvfrom(SIZE)
        if data:
            data = str(data)
            
            if data[2:10] == 'discover':
                # parsing if the received data is a discover
                bracIndex = data.find('[')
                bracStop = data.find(',', bracIndex)
                otherName = data [bracIndex + 1:bracStop]
                otherIPStop = data.find(',', bracStop + 1)
                otherIP = data[bracStop + 1:otherIPStop]
                duplicate = False
                for x in openservers:
                    if (x == otherIP):
                        duplicate = True
                if not duplicate and HOST != otherIP:
                    print('From ', otherIP,', ',  otherName + ' : DISCOVER ME!')
                    openservers.append(otherName)
                resp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                resp.settimeout(2)
                COUNT = COUNT + 1
                if COUNT > 2:
                    openservers.clear()
                    respondservers.clear()
                    openservers.append(HOST)
                    respondservers.append(HOST)
                    COUNT = 0
                
                

                resp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                resp.settimeout(2)
                try:
                    if HOST != otherIP:
                        resp.connect((addr[0], PORT))
                        msg = 'response,broadcast TCP,[' + NAME + ',' + HOST + ',' + 'response' + ']'
                        msg = msg.encode('ascii')
                        resp.sendall(bytes(msg))
                        resp.close()
                except:
                    print('err 2')

           
#listen TCP packets
def listenTCP():
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp.bind(('',PORT))
    while True:
        tcp.listen()
        conn, addr = tcp.accept()
        data = conn.recv(SIZE)
        if data:
            data = str(data)
            if data [2:9] == 'message':
            # parsing if the received data is a massage
                nameIndex = data.find('[')
                nameStop = data.find(',', nameIndex)
                name = data [nameIndex + 1:nameStop]
                msgIndex = data.find(',', nameStop+1 )
                msgIndex = data.find(',', msgIndex+1 )
                msgStop = data.find(']', msgIndex+1 )
                msg = data[msgIndex + 1 : msgStop]
                print('From ', addr,', ',  name + ' : ' + msg)

            elif data [2:10] == 'response':
                # parsing if the received data is a response
                nameIndex = data.find('[')
                nameStop = data.find(',', nameIndex)
                name = data [nameIndex + 1:nameStop]
                otherIPStop = data.find(',', nameStop + 1)
                otherIP = data[nameStop + 1:otherIPStop]
                duplicate = False
                for x in respondservers:
                    if (x == otherIP):
                        duplicate = True
                if not duplicate and name != NAME:
                    print('From ', otherIP,', ',  name + ' : RESPONDED')
                    respondservers.append(otherIP)
             

def main():
    global HOST
    ThreadUDP = Thread(target=listenUDP)
    ThreadTCP = Thread(target=listenTCP)
    ThreadUDP.start()
    ThreadTCP.start()
    
    # try to send discover message to open servers
    try:
        
        ann = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        ann.bind(('',0))
        ann.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST,1)
        
        #ann.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        msg = 'discover,broadcast UDP,[' + NAME + ',' + HOST + ',' + 'announce' + ']'
        msg = msg.encode('ascii')
        #broadcast 3 times to cover up losses
        for x in range(3):
            ann.sendto(msg,('<broadcast>', PORT))
        bcast = '192.168.1.'
        #for some reason the sendto() function with <broadcast> is not sent to 
        #all ip addresses accross the network, 
        #so it is done with the for loop below
        for y in range(256):
            bcastTO = bcast + str(y)
            for x in range(3):
                ann.sendto(msg,(bcastTO, PORT))

        ann.close()
    except socket.error as socketerror:
        print('Error happened :(') 
   
print('Your server is now open on : ', HOST,':', PORT)


if __name__ == ("__main__"):
    main()






