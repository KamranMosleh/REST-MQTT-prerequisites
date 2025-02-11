import cherrypy

class Student:
    exposed = True

    def __init__(self):
        self.name = None
        self.surname = None
        self.id = None

    def POST(self, name, surname, id):
        self.name = name
        self.surname = surname
        self.id = id
        return f"Student {self.name} {self.surname} with ID {self.id} has been registered"


if __name__ == "__main__":
    conf = {
        "/": {
            "request.dispatch": cherrypy.dispatch.MethodDispatcher(),
            "tools.sessions.on": True,
        }
    }
    cherrypy.quickstart(Student(), '/', conf)
