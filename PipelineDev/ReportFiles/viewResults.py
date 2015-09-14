import SimpleHTTPServer
import SocketServer
import webbrowser
import atexit

PORT = 8000

Handler = SimpleHTTPServer.SimpleHTTPRequestHandler

httpd = SocketServer.TCPServer(("", PORT), Handler)

print "serving at port", PORT
webbrowser.open('http://localhost:8000/report.html')
httpd.serve_forever()

atexit.register(exit_handler(httpd))

def exit_handler(httpd):
    httpd.shutdown()