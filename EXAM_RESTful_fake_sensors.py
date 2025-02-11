import random
import cherrypy

class Sensor:
    exposed = True

    def __init__(self):
        self.light = None
        self.temp = None

    def lightInq(self):
        self.light = random.randint(0, 1000)

    def tempInq(self):
        self.temp = random.randint(0, 40)

    def GET(self, *uri, **params):
        if len(uri) > 0:
            if uri[0] == "light" and len(uri) == 1:
                self.lightInq()
                if self.light > 500:
                    return f"Light is {self.light} units, what a bright day!"
                else:
                    return f"Light is {self.light} units, what a dark day!"
            elif uri[0] == "temperature" and len(uri) == 1:
                self.tempInq()
                if self.temp > 30:
                    return f"Temperature is {self.temp} degrees, what a hot day!"
                else:
                    return f"Temperature is {self.temp} degrees, what a cool day!"
            else:
                return "Invalid Request"
        else:
            self.tempInq()
            self.lightInq()
            return (
                f"Please use one of the following endpoints:<br> <b>/light</b> or <b>/temperature</b>"

            )

if __name__ == "__main__":
    conf = {
        "/": {
            "request.dispatch": cherrypy.dispatch.MethodDispatcher(),
            "tools.sessions.on": True,
        }
    }
    cherrypy.quickstart(Sensor(), '/', conf)
    # cherrypy.tree.mount(Sensor(), "/", conf)
    # cherrypy.engine.start()
    # cherrypy.engine.block()
