import cherrypy
import json

class HelloWorld:
    @cherrypy.expose
    def index(self):
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
        if cherrypy.request.method == 'POST':
            # Handle JSON data
            if cherrypy.request.headers['Content-Type'] == 'application/json':
                raw_data = cherrypy.request.body.read()
                data = json.loads(raw_data)
                message = data.get('message', None)

        if message:
            return f"Thank you for your message: {message}"
        else:
            return "No message received."

if __name__ == '__main__':
    cherrypy.quickstart(HelloWorld())