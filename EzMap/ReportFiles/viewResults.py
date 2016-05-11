import SimpleHTTPServer
import SocketServer
import webbrowser
import atexit
import random

def exit_handler(httpd):
    httpd.shutdown()

def accessReport (PORT):
    try:
        Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
        httpd = SocketServer.TCPServer(("", PORT), Handler)

        print "serving at port", PORT
        webbrowser.open('http://localhost:' + str(PORT) + '/report.html')
        httpd.serve_forever()

        atexit.register(exit_handler(httpd))
    except SocketServer.socket.error as e:
        accessReport(PORT+1)

PORT = 8000
accessReport(PORT)