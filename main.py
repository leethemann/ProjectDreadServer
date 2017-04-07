import socket
import sys
from thread import *

def ClientThread(conn):
    conn.send('Welcome to the server. Type something and hit enter.\n')
    participate = True

    while participate:
        data = conn.recv(1024)

        #I think really what I want here is that the client is going to send of either a json or xml blob,
        #   and we'll end up doing the right thing with it via a case statement.
        if "attack" in data:
            reply = "You attacked your enemy!\n"
        elif "spy" in data:
            reply = "Your enemy is 10,000 warriors strong!\n"
        elif "sabatoge" in data:
            reply = "You poisoned the enemies water supply, their warriors look weak!\n"
        elif "quit" in data:
            break
        else:
            reply = "Command not recognized!\n"
        if not data:
            break

        conn.sendall(reply)

    conn.close()
#ENDING FUNCTIONS

HOST = ''
PORT = 8888

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'

try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print 'Bind failed. Error Code: ' + str(msg[0]) + 'Message ' + msg[1]
    sys.exit

print 'Socket bind complete'

s.listen(10)
print 'Socket now listening'

while 1:
    conn, addr = s.accept()
    print 'Connected with ' + addr[0] + ':' + str(addr[1])

    start_new_thread(ClientThread, (conn,))

s.close()


