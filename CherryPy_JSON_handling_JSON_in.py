## (json_in): Deserializing JSON Request Body
# This snippet demonstrates how to handle JSON data sent in an HTTP request body.
## cherrypy.request.json automatically parses the JSON data from the request body and converts it into a Python dictionary.

import cherrypy
import json

class MyService:
    @cherrypy.expose
    def update_data(self):
        try:
            request_data = cherrypy.request.json  # Parse JSON from request body
            temperature = request_data.get('temperature')
            humidity = request_data.get('humidity')

            if temperature is not None and humidity is not None:
                # Process the received data (e.g., store in database)
                print(f"Received data: Temperature={temperature}, Humidity={humidity}")
                return json.dumps({"status": "success", "message": "Data updated"}) # Return the JSON string

            else:
                return json.dumps({"status": "error", "message": "Missing 'temperature' or 'humidity'"})

        except ValueError:  # Handle cases where the request body is not valid JSON
            return json.dumps({"status": "error", "message": "Invalid JSON data"})

if __name__ == '__main__':
    cherrypy.config.update({'server.socket_host': '0.0.0.0',
                            'server.socket_port': 8080})
    cherrypy.quickstart(MyService())