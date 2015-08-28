import SimpleHTTPServer
import SocketServer
import webbrowser

PORT = 8000

Handler = SimpleHTTPServer.SimpleHTTPRequestHandler

httpd = SocketServer.TCPServer(("", PORT), Handler)

print "serving at port", PORT
webbrowser.open('http://localhost:8000/report.html')
httpd.serve_forever()

