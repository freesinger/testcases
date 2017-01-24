# A simple server based om SocketServer

from SocketServer import TCPServer, StreamRequestHandler

class Handler(StreamRequestHandler):

    def handle(self):
        addr = self.request.getpeername()
        print 'Got connection from', addr
        self.wfile.write('Thanks for connection')

server = TCPServer(('', 1024), Handler)
server.serve_forever()