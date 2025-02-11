import json
import cherrypy

class Student:
    def __init__(self, id, name, surname):
        self.id = id
        self.name = name
        self.surname = surname
        self.grades = {}  # Dictionary to store grades by subject

class GradeService:
    exposed = True
    def __init__(self):
        self.students = {}

    def POST(self, *uri, **params):
        try:
            if len(uri) == 0:  # Register student
                data = json.loads(cherrypy.request.body.read().decode('utf-8'))
                if not all(key in data for key in ('id', 'name', 'surname')):
                    raise ValueError("Missing required fields for student registration.")

                if data['id'] in self.students:
                    raise ValueError("Student with this ID already exists.")

                student = Student(data['id'], data['name'], data['surname'])
                self.students[data['id']] = student
                cherrypy.response.status = 201  # Created
                cherrypy.response.headers['Location'] = f'/students/{data["id"]}'
                return json.dumps({"message": "Student registered successfully."})

            elif len(uri) == 2 and uri[1] == 'grades':  # Register grades
                student_id = uri[0]
                if student_id not in self.students:
                    raise ValueError("Student not found.")

                data = json.loads(cherrypy.request.body.read().decode('utf-8'))
                if not all(key in data for key in ('subject', 'grades')):
                    raise ValueError("Missing required fields for grade registration.")

                student = self.students[student_id]
                subject = data['subject']
                grades = data['grades']

                if subject not in student.grades:
                    student.grades[subject] = grades
                else:
                    student.grades[subject].extend(grades) # Append new grades to existing ones.

                cherrypy.response.status = 201 # Created
                return json.dumps({"message": "Grades registered successfully."})
            else:
                raise ValueError("Invalid endpoint for POST request.")

        except ValueError as e:
            cherrypy.response.status = 400  # Bad Request
            return json.dumps({"error": str(e)})
        except json.JSONDecodeError:
            cherrypy.response.status = 400 # Bad Request
            return json.dumps({"error": "Invalid JSON data."})
        except Exception as e:
            cherrypy.response.status = 500  # Internal Server Error
            return json.dumps({"error": "An internal server error occurred."})


    def GET(self, *uri, **params):
        try:
            if len(uri) == 0:  # Get all students
                student_list = []
                for student in self.students.values():
                    student_list.append({"id": student.id, "name": student.name, "surname": student.surname})
                return json.dumps(student_list)

            elif len(uri) == 1:  # Get student by ID
                student_id = uri[0]
                if student_id not in self.students:
                    raise ValueError("Student not found.")
                student = self.students[student_id]
                return json.dumps({"id": student.id, "name": student.name, "surname": student.surname})

            elif len(uri) == 2 and uri[1] == 'grades':  # Get grades for a student
                student_id = uri[0]
                if student_id not in self.students:
                    raise ValueError("Student not found.")

                student = self.students[student_id]
                if 'subject' in params:
                    subject = params['subject']
                    if subject in student.grades:
                        return json.dumps({"id": student_id, "grades": {subject: student.grades[subject]}})
                    else:
                        return json.dumps({"id": student_id, "grades": {}}) # Return empty if subject not found
                else:
                    return json.dumps({"id": student_id, "grades": student.grades})

            else:
                raise ValueError("Invalid endpoint for GET request.")
        except ValueError as e:
            cherrypy.response.status = 404 if "Student not found" in str(e) else 400 # Not found or bad request
            return json.dumps({"error": str(e)})
        except Exception as e:
            cherrypy.response.status = 500  # Internal Server Error
            return json.dumps({"error": "An internal server error occurred."})



if __name__ == '__main__':
    conf = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.sessions.on': True,
            'tools.json_in.on': True,  # Enable automatic JSON input parsing
            'tools.json_out.on': True  # Enable automatic JSON output encoding
        }
    }
    cherrypy.quickstart(GradeService(), '/', conf)