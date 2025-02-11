import cherrypy
import json


class WordFinderService:
    exposed = True

    def POST(self, *uri, **params):
        try:
            # Parse the JSON payload
            input_data = cherrypy.request.body.read().decode('utf-8')
            data = json.loads(input_data)

            # Extract the word to find and the list of words
            word_to_find = data.get('word')
            word_list = data.get('word_list')

            # Validate inputs
            if not isinstance(word_to_find, str) or not isinstance(word_list, list):
                raise ValueError("Invalid input format: 'word' must be a string and 'word_list' must be a list.")

            # Search for the word in the list
            if word_to_find in word_list:
                position = word_list.index(word_to_find)
                updated_list = [word for word in word_list if word != word_to_find]
                return json.dumps({
                    "message": f"Word '{word_to_find}' found at position {position}",
                    "updated_list": updated_list
                })
            else:
                return json.dumps({"message": "Word not found."})

        except (json.JSONDecodeError, ValueError) as e:
            # Handle JSON decoding errors and invalid input formats
            cherrypy.response.status = 400
            return json.dumps({"error": str(e)})


if __name__ == "__main__":
    # Configuration for the CherryPy server
    conf = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.sessions.on': True,
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'application/json')]
        }
    }
    cherrypy.quickstart(WordFinderService(), '/', conf)
