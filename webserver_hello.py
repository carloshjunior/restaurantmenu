# Building a Server with BaseHTTPServer
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

# Listening requisitions
class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/hello"):
                # Response
                self.send_response(200)
                self.send_header("Content-Type", "text/html")
                self.end_headers()
                # Message of response
                output = ""
                output += "<html><body>"
                output += "<h1>Hello!</h1>"
                output += '''<form method='POST' enctype='multipart/form-data'
                            action='/hello'>
                            <h2>What would you like me to say?</h2>
                            <input name="message" type="text" >
                            <input type="submit" value="Submit">
                            </form>'''
                output += " </body></html>"
                self.wfile.write(output)
                # Can be usefull to help in debug
                print(output)
                return


            if self.path.endswith("/hola"):
                # Response
                self.send_response(200)
                self.send_header("Content-Type", "text/html")
                self.end_headers()
                # Message of response
                output = ""
                output += "<html><body>"
                output += "<h1>&#161 Hola !</h1>"
                output += '''<form method='POST' enctype='multipart/form-data'
                            action='/hello'>
                            <h2>What would you like me to say?</h2>
                            <input name="message" type="text" >
                            <input type="submit" value="Submit">
                            </form>'''
                output += " </body></html>"
                self.wfile.write(output)
                # Can be usefull to help in debug
                print(output)
                return


        except IOError:
            self.send_error(404,"File Not Found %s" % self.path)

    def do_POST(self):
        try:
            self.send_response(301)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            ctype, pdict = cgi.parse_header(
                self.headers.getheader('content-type'))
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('message')
            output = ""
            output += "<html><body>"
            output += "<h2> Okay, how about this: </h2>"
            output += "<h1> %s </h1>" % messagecontent[0]
            output += '''<form method='POST' enctype='multipart/form-data'
                        action='/hello'><h2>What would you like me to say?</h2>
                        <input name="message" type="text" >
                        <input type="submit" value="Submit">
                        </form>'''
            output += " </body></html>"
            self.wfile.write(output)
            print output
        except:
            pass



# Initialize Web Server and Stop methods
def main():

    # Start new server
    try:
        port = 8080
        server = HTTPServer(("",port), webserverHandler)
        print("Web Server running on port %s" % port)
        server.serve_forever()

    # Stop the server when press Ctrl+C
    except KeyboardInterrupt:
        print("^C entered, stopping web server...")
        server.socket.close()

# Start the main method after compilation
if  __name__ == "__main__":
    main()
