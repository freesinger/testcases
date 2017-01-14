""""
A simple server.
""""

import socket

s = socket.socket()

host = socket.gethostname()
port = 1234
s.bind((host, port))

s.listen(5)
while True:
    c.addr = s.accept()
    print 'Got Connection from', addr
    c.send('Thank you for Connection!')
    c.close
