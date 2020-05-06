# zeroconf-Chat

Python zeroconf chat. Server with UDP listener for broadcast discovery, and TCP listener for p2p messaging. The servers starts both TCP & UDP listener sockets. Then sends broadcast UDP packets into the network and receives responds from open servers according to the protocol, which is :  
* message_type, UDP/TCP, [name, HOST, message_type, message] 

The client code establishes TCP connection to the HOST specified in command line. Opens socket to the server, sends TCP packets to the server, closes it afterwards.


# Usage:

echo_server.py:

    python echo_server.py PORT NAME
  
  
echo_client.py:

    python echo_client.py HOST PORT NAME
  
  
# Test:
Tested on Windows 10, with Python 3.7.4 on 3 different computers.
