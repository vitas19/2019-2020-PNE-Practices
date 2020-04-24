import http.server
import socketserver
import termcolor
from pathlib import Path


# Define the Server's port
PORT = 8080

# -- This is for preventing the error: "Port already in use"
socketserver.TCPServer.allow_reuse_address = True


# Class with our Handler. It is a called derived from BaseHTTPRequestHandler
# It means that our class inheritates all his methods and properties
class TestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        """This method is called whenever the client invokes the GET method
        in the HTTP protocol request"""

        # Print the request line
        termcolor.cprint(self.requestline, 'green')

        req_line = self.requestline.split(' ')

        path = req_line[1]

        path = path[1:]

        type_content = "text/html"

        # Message to send back to the client
        if path == "":
            path = "index.html"
        if path == "index.html":
            contents = Path(path).read_text()
            status = 200
        else:
            contents = Path("Error.html").read_text()
            status = 404

        # Generating the response message
        self.send_response(status)  # -- Status line: OK!

        # Define the content-type header:
        self.send_header('Content-Type', type_content)
        self.send_header('Content-Length', len(contents.encode()))

        # The header is finished
        self.end_headers()

        # Send the response message
        self.wfile.write(contents.encode())

        return


# ------------------------
# - Server MAIN program
# ------------------------
# -- Set the new handler
Handler = TestHandler

# -- Open the socket server
with socketserver.TCPServer(("", PORT), Handler) as httpd:

    print("Serving at PORT", PORT)

    # -- Main loop: Attend the client. Whenever there is a new
    # -- clint, the handler is called
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("")
        print("Stoped by the user")
        httpd.server_close()
