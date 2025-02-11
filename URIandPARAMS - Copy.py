import cherrypy

class HelloWorld(object):
    exposed = True

    def GET(self, *uri, **params):
        # Standard output
        output = "Hello World"

        # Check the uri in the requests
        # <br> is just used to append the content in a new line
        # (<br> is the \n for HTML)
        print(uri)
        print(type(uri))
        if len(uri) != 0:
            output += '<br>uri: ' + ', '.join(uri)

        # Check the parameters in the request
        # <br> is just used to append the content in a new line
        # (<br> is the \n for HTML)
        print(params)
        print(type(params))
        if params != {}:
            output += '<br>params: ' + str(params)

        return output


if __name__ == "__main__":
    # Standard configuration to serve the url "localhost:8080"
    conf = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.sessions.on': True
        }
    }
    cherrypy.quickstart(HelloWorld(), '/', conf)

# test with http://127.0.0.1:8080/I/have/some/parameters/4u?a=135&b=ciao