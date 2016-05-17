import http.server
import socketserver
import webbrowser

PORT = 8000
httpd = "";


def createrServer(PORT):
    httpd = False
    try:
        Handler = http.server.SimpleHTTPRequestHandler

        httpd = socketserver.TCPServer(("", PORT), Handler)

        print("serving at port", PORT)
        webbrowser.open('http://localhost:' + str(PORT) + '/report.html')

        httpd.serve_forever()

    except KeyboardInterrupt:
        httpd.server_close()
        print("Server Stopped")

    except:
        print('Error')
        createrServer(PORT + 1)

    return httpd


httpd = createrServer(PORT)

if (httpd != False):
    httpd.server_close()
    print("Server Stopped")
