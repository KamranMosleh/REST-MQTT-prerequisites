import cherrypy
import json
import os

class ContactService:
    exposed = True

    def __init__(self):
        self.file_path = "catalogue.json"
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w") as file:
                json.dump([], file)

    def read_contacts(self):
        """Reads contacts from JSON file."""
        with open(self.file_path, "r") as file:
            data = json.load(file)
        return data if isinstance(data, list) else [data]

    def write_contacts(self, contacts):
        """Writes contacts to JSON file."""
        with open(self.file_path, "w") as file:
            json.dump(contacts, file, indent=4)

    def POST(self):
        """Handles adding a new contact via POST request."""
        content_length = int(cherrypy.request.headers['Content-Length'])
        body = cherrypy.request.body.read(content_length)
        new_contact = json.loads(body)

        contacts = self.read_contacts()
        contacts.append(new_contact)
        self.write_contacts(contacts)

        return "New contact added successfully!"

if __name__ == "__main__":
    conf = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.sessions.on': True,
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'text/plain')],
            'tools.staticdir.root': os.path.abspath(".")
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': "static"
        }
    }
    cherrypy.quickstart(ContactService(), '/', conf)
