# Building a Server with BaseHTTPServer
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

# Libs for CRUD operations using sqlite and sqlalchemy
from database_setup import Base, Restaurant, MenuItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Create session and connect to DB
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind=engine
DBSession = sessionmaker(bind = engine)
session = DBSession()


class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # Create confirmation page to Delete a Restaurant
            if self.path.endswith("/delete"):
                restIDPath = self.path.split("/")[2]
                myRest = session.query(Restaurant).filter_by(
                    id=restIDPath).one()

                if myRest:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()

                    output = "<html><body>"
                    output += "<h1>Are you sure want to delete "
                    output += "%s?</h1>" % (myRest.name,)
                    output += "<form method='POST' enctype='multipart/form-data'"
                    output += " action = '/restaurants/%s/delete' >" % restIDPath
                    output += "<input type='submit' value='Yes'>"
                    output += "<a href='/restaurants'>No</a>"
                    output += "</form>"
                    output += "</body></html>"
                    self.wfile.write(output)
                    print(output)
                    return

            # Create a page to Edit Restaurants
            if self.path.endswith("/edit"):
                restIDPath = self.path.split("/")[2]
                myRest = session.query(Restaurant).filter_by(
                    id=restIDPath).one()
                if myRest:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output = "<html><body>"
                    output += "<h1>"
                    output += myRest.name
                    output += "</h1>"
                    output += "<form method='POST' enctype='multipart/form-data' action = '/restaurants/%s/edit' >" % restIDPath
                    output += "<input name='name' type='text' placeholder='%s' >" % myRest.name
                    output += "<input type='submit' value='Rename'>"
                    output += "</form>"
                    output += "</body></html>"

                    self.wfile.write(output)
                    print(output)
                    return

            # Create a page Insert a new Restaurants
            if self.path.endswith("/restaurants/new"):
                # Response
                self.send_response(200)
                self.send_header("Content-Type", "text/html")
                self.end_headers()
                # Message of response
                output = ""
                output += "<html><body>"
                output += "<h1>Restaurants</h1>"
                output += '''<form method='POST' enctype='multipart/form-data'
                action='/restaurants'>'''
                output += "<h2>New Restaurant</h2>"
                output += "<input type='text' name='name'>"
                output += "<input type='submit' value='Submit'>"
                output += "</form> </body></html>"
                self.wfile.write(output)
                # Can be usefull to help in debug
                print(output)
                return


            # Create a page to list all restaurants
            if self.path.endswith("/restaurants"):
                # Response
                self.send_response(200)
                self.send_header("Content-Type", "text/html")
                self.end_headers()
                # Message of response
                output = ""
                output += "<html><body>"
                output += "<h1>Restaurants</h1>"
                output += '''<form method='POST' enctype='multipart/form-data'
                            action='/restaurants'>'''
                items = session.query(Restaurant).all()
                for item in items:
                    output += "<p>%s<br/>" % (item.name,)
                    output += "<a href='restaurants/%s/edit'>" % (item.id,)
                    output += "Edit</a> / "
                    output += "<a href='restaurants/%s/delete'>" % (item.id,)
                    output += "Delete</a><br>"
                output += "</p></br>"
                output += "<a href='/restaurants/new'>"
                output += "Make a new Restaurant Here</a>"
                output += "</form></body></html>"
                self.wfile.write(output)
                # Can be usefull to help in debug
                print(output)
                return

        except IOError:
            self.send_error(404,"File Not Found %s" % self.path)


    def do_POST(self):
        try:
            #Return page after Delete Restaurant
            if self.path.endswith("/delete"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('name')
                    restIDPath = self.path.split("/")[2]

                myRest = session.query(Restaurant).filter_by(
                        id=restIDPath).one()
                if myRest != []:
                    session.delete(myRest)
                    session.commit()

                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location','/restaurants')
                    self.end_headers()


            # Return page after Update a Restaurant
            if self.path.endswith("/edit"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('name')
                    restIDPath = self.path.split("/")[2]

                myRest = session.query(Restaurant).filter_by(
                        id=restIDPath).one()
                if myRest != []:
                    myRest.name = messagecontent[0]
                    session.add(myRest)
                    session.commit()

                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location','/restaurants')
                    self.end_headers()


            # Return Page afer Insert a new Restaurant
            if self.path.endswith("/restaurants/new"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('name')

                newRestaurant = Restaurant(name = "%s" % (messagecontent[0],))
                session.add(newRestaurant)
                session.commit()

                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location','/restaurants')
                self.end_headers()


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
        print(" entered, stopping web server...")
        server.socket.close()

# Start the main method after compilation
if  __name__ == "__main__":
    main()
