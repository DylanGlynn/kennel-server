import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from views import get_all_animals, get_single_animal
from views import create_animal, delete_animal, update_animal
from views import get_all_locations, get_single_location
from views import create_location, delete_location, update_location
from views import get_all_employees, get_single_employee
from views import create_employee, delete_employee, update_employee
from views import get_all_customers, get_single_customer
from views import create_customer, update_customer

# Here's a class. It inherits from another class.
# For now, think of a class as a container for functions that
# work together for a common purpose. In this case, that
# common purpose is to respond to HTTP requests from a client.

method_mapper = {
    "animals": {"single": get_single_animal, "all": get_all_animals},
    "locations": {"single": get_single_location, "all": get_all_locations},
    "employees": {"single": get_single_employee, "all": get_all_employees},
    "customers": {"single": get_single_customer, "all": get_all_customers}
}

class HandleRequests(BaseHTTPRequestHandler):
    """Controls the functionality of any GET, PUT, POST, DELETE requests to the server
    """

    def parse_url(self, path):
        ''' Just like splitting a string in JavaScript. If the '''
        # path is "/animals/1", the resulting list will
        # have "" at index 0, "animals" at index 1, and "1"
        # at index 2.
        path_params = path.split("/")
        resource = path_params[1]
        id = None

        # Try to get the item at index 2
        try:
            # Convert the string "1" to the integer 1
            # This is the new parseInt()
            id = int(path_params[2])
        except IndexError:
            pass  # No route parameter exists: /animals
        except ValueError:
            pass  # Request had trailing slash: /animals/

        return (resource, id)  # This is a tuple
    # This is a Docstring it should be at the beginning of all classes and functions
    # It gives a description of the class or function

    # Here's a class function

    # Here's a method on the class that overrides the parent's method.
    # It handles any GET request.
    def get_all_or_single(self, resource, id):
        ''' Determines if GET is for a single object within or an entire dictionary. '''
        if id is not None:
            response = method_mapper[resource]["single"](id)

            if response is not None:
                self._set_headers(200)
            else:
                self._set_headers(404)
                response = ''
        else:
            self._set_headers(200)
            response = method_mapper[resource]["all"]()

        return response

    def do_GET(self):
        ''' Handles GET requests to the server. '''
        response = None
        (resource, id) = self.parse_url(self.path)
        response = self.get_all_or_single(resource, id)
        self.wfile.write(json.dumps(response).encode())

    # def do_GET(self):
    #    ''' Handles GET requests to the server. '''
    #    self._set_headers(200)
    #    response = {}  # Default response

        # Parse the URL and capture the tuple that is returned
    #    (resource, id) = self.parse_url(self.path)

    #    if resource == "animals":
    #        if id is not None:
    #            response = get_single_animal(id)
    #            if response is None:
    #                self._set_headers(404)
    #                response = ''
    #            else:
    #                self._set_headers(200)

    #        else:
    #            response = get_all_animals()

    #    elif resource == "locations":
    #        if id is not None:
    #            response = get_single_location(id)
    #            if response is None:
    #                self._set_headers(404)
    #                response = ''
    #            else:
    #                self._set_headers(200)

    #        else:
    #            response = get_all_locations()

    #    elif resource == "employees":
    #        if id is not None:
    #            response = get_single_employee(id)
    #            if response is None:
    #                self._set_headers(404)
    #                response = ''
    #            else:
    #                self._set_headers(200)
    #        else:
    #            response = get_all_employees()

    #    elif resource == "customers":
    #        if id is not None:
    #            response = get_single_customer(id)
    #            if response is None:
    #                self._set_headers(404)
    #                response = ''
    #            else:
    #                self._set_headers(200)
    #        else:
    #            response = get_all_customers()

    #    else:
    #        response = {}

    #    self.wfile.write(json.dumps(response).encode()) """

    # Here's a method on the class that overrides the parent's method.
    # It handles any POST request.
    def do_POST(self):
        '''Post method.'''
        self._set_headers(000)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)

        # Convert JSON string to a Python dictionary
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        # Initialize new animal
        new_employee = None
        new_customer = None
        created_resource = None

        # Add a new animal to the list. Don't worry about
        # the orange squiggle, you'll define the create_animal
        # function next.
        if resource == "animals":
            if "name" in post_body and "species" in post_body and "locationId" in post_body and "customerId" in post_body and "status" in post_body:
                self._set_headers(201)
                created_resource = create_animal(post_body)
        # Encode the new animal and send in response
            else:
                self._set_headers(400)
                created_resource = {
                    "message": f'{"name is required." if "name" is not post_body else ""} {"species is required." if "species" is not post_body else ""} {"Location is required." if "locationId" is not post_body else ""} {"Customer is required." if "customerId" is not post_body else ""} {"Status is required." if "status" is not post_body else ""}'}

        if resource == "locations":
            if "name" in post_body and "address" in post_body:
                self._set_headers(201)
                created_resource = create_location(post_body)
            else:
                self._set_headers(400)
                created_resource = {
                    "message": f'{"name is required." if "name" is not post_body else ""} {"address is required." if "address" is not post_body else ""}'}

        if resource == "employees":
            new_employee = create_employee(post_body)
        self.wfile.write(json.dumps(new_employee).encode())

        if resource == "customers":
            new_customer = create_customer(post_body)
        self.wfile.write(json.dumps(new_customer).encode())

        self.wfile.write(json.dumps(created_resource).encode())

    # A method that handles any PUT request.
    def do_PUT(self):
        '''Handles PUT requests.'''
        self._set_headers(204)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        # Delete a single animal from the list
        if resource == "animals":
            update_animal(id, post_body)

        # Encode the new animal and send in response
        self.wfile.write("".encode())

        if resource == "customers":
            update_customer(id, post_body)
        self.wfile.write("".encode())

        if resource == "employees":
            update_employee(id, post_body)
        self.wfile.write("".encode())

        if resource == "locations":
            update_location(id, post_body)
        self.wfile.write("".encode())

    def _set_headers(self, status):
        # Notice this Docstring also includes information about the arguments passed to the function
        """Sets the status code, Content-Type and Access-Control-Allow-Origin
        headers on the response

        Args:
            status (number): the status code to return to the front end
        """
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    # Another method! This supports requests with the OPTIONS verb.
    def do_OPTIONS(self):
        """Sets the options headers
        """
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods',
                         'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers',
                         'X-Requested-With, Content-Type, Accept')
        self.end_headers()

    def do_DELETE(self):
        '''Delete method'''
        # Set a 204 response code
        self._set_headers(204)

    # Parse the URL
        (resource, id) = self.parse_url(self.path)
        response = {}

    # Delete a single animal from the list
        if resource == "animals":
            delete_animal(id)

    # Encode the new animal and send in response
        self.wfile.write("".encode())

        if resource == "locations":
            delete_location(id)
        self.wfile.write("".encode())

        if resource == "employees":
            delete_employee(id)
        self.wfile.write("".encode())

        if resource == "customers":
            self._set_headers(400)
            response = ''
        self.rfile.write(json.dumps(response).encode())

# This function is not inside the class. It is the starting
# point of this application.


def main():
    """Starts the server on port 8088 using the HandleRequests class
    """
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()
