## dumps --> Serializing/converting dictionary to a JSON formatted String
import json

data = {'temperature': 25.5, 'humidity': 60}
json_string = json.dumps(data) 
print(json_string)  # Output: {"temperature": 25.5, "humidity": 60}

# In a CherryPy service:
import cherrypy

class MyService:
    @cherrypy.expose
    def get_data(self):
        data = {'temperature': 25.5, 'humidity': 60}
        return json.dumps(data)  # Return the JSON string

    @cherrypy.expose
    def index(self):
        return """
        <html>
        <head>
        <title>My IoT Data</title>
        </head>
        <body>
        <p>Check Temperature and Humidity</p>
        </body>
        </html>
        """

if __name__ == '__main__':
    cherrypy.quickstart(MyService())