import cherrypy

class HelloWorld:
    @cherrypy.expose
    def index(self):
        # This is the default page that will be displayed
        return """
            <html>
                <body>
                    <h1>Submit a Message</h1>
                    <form method="post" action="/submit">
                        <input type="text" name="message" placeholder="Enter your message" />
                        <button type="submit">Submit</button>
                    </form>
                </body>
            </html>
        """

    @cherrypy.expose
    def submit(self, message=None):
        # This method handles the POST request
        if message:
            return f"Thank you for your message: {message}"
        else:
            return "No message received."

if __name__ == '__main__':
    # Start the CherryPy server
    cherrypy.quickstart(HelloWorld())
    