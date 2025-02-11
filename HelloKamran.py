import cherrypy


class HelloKamran:
    @cherrypy.expose
    # exposed = True

    def index(self):
        return "Hello Kamran! :D"

# cherrypy.config.update({'server.socket_port': 9090})
cherrypy.quickstart(HelloKamran())
