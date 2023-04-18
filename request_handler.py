from urllib.parse import urlparse, parse_qs
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from views import get_all_animals, get_single_animal, create_animal
from views import delete_animal, update_animal, get_animals_by_location, get_animals_by_status
from views import get_all_locations, get_single_location, create_location
from views import delete_location, update_location
from views import get_all_employees, get_single_employee, create_employee
from views import delete_employee, update_employee, get_employees_by_location
from views import get_all_customers, get_single_customer, create_customer
from views import delete_customer, update_customer, get_customers_by_email


# Here's a class. It inherits from another class.
# For now, think of a class as a container for functions that
# work together for a common purpose. In this case, that
# common purpose is to respond to HTTP requests from a client.


class HandleRequests(BaseHTTPRequestHandler):
    """Controls the functionality of any GET, PUT, POST, DELETE requests to the server
    """
    # replace the parse_url function in the class

    def parse_url(self, path):
        """Parse the url into the resource and id"""
        url_components = urlparse(path)
        path_params = url_components.path.strip("/").split("/")
        query_params = []

        if url_components.query != "":
            query_params = url_components.query.split("&")

        resource = path_params[0]
        id = None

        try:
            id = int(path_params[1])
        except IndexError:
            pass
        except ValueError:
            pass
        print(f'{resource}, {id}, {query_params}')
        return (resource, id, query_params)


    # Here's a class function

    # Here's a method on the class that overrides the parent's method.
    # It handles any GET request.
    def do_GET(self):
        """ Handles the GET requests. """
        self._set_headers(200)
        response = {}
        # Parse the URL and capture the tuple that is returned
        parsed = self.parse_url(self.path)

        if '?' not in self.path:
            (resource, id, query_params) = parsed

            if resource == "animals":
                if id is not None:
                    response = get_single_animal(id)

                else:
                    response = get_all_animals(query_params)

            elif resource == "locations":
                if id is not None:
                    response = get_single_location(id)

                else:
                    response = get_all_locations()

            elif resource == "employees":
                if id is not None:
                    response = get_single_employee(id)

                else:
                    response = get_all_employees()

            elif resource == "customers":
                if id is not None:
                    response = get_single_customer(id)
                else:
                    response = get_all_customers()

        else:
            (resource, id, query_params) = parsed

            if query_params.__contains__('email') and resource == 'customers':
                response = get_customers_by_email(query_params['email'][0])

            elif query_params.__contains__('location_id') and resource == 'employees':
                response = get_employees_by_location(query_params['location_id'][0])

            elif query_params.__contains__('status') and resource == 'animals':
                response = get_animals_by_status(query_params['status'][0])

            elif resource == 'animals' and query_params[0] == '_sortBy=location_id':
                response = get_all_animals(query_params)

            elif query_params.__contains__('location_id') and resource == 'animals':
                response = get_animals_by_location(query_params['location_id'][0])

        self.wfile.write(json.dumps(response).encode())

    # Here's a method on the class that overrides the parent's method.
    # It handles any POST request.
    def do_POST(self):
        '''Post method.'''
        self._set_headers(201)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)

        # Convert JSON string to a Python dictionary
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id, query_params) = self.parse_url(self.path)

        # Initialize new animal
        new_animal = None
        new_location = None
        new_employee = None
        new_customer = None

        # Add a new animal to the list. Don't worry about
        # the orange squiggle, you'll define the create_animal
        # function next.
        if resource == "animals":
            new_animal = create_animal(post_body)
        # Encode the new animal and send in response
        self.wfile.write(json.dumps(new_animal).encode())

        if resource == "locations":
            new_location = create_location(post_body)
        self.wfile.write(json.dumps(new_location).encode())

        if resource == "employees":
            new_employee = create_employee(post_body)
        self.wfile.write(json.dumps(new_employee).encode())

        if resource == "customers":
            new_customer = create_customer(post_body)
        self.wfile.write(json.dumps(new_customer).encode())

    # A method that handles any PUT request.
    def do_PUT(self):
        '''Handles PUT requests.'''

        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id, query_params) = self.parse_url(self.path)

        success = False

        # Delete a single animal from the list
        if resource == "animals":
            success = update_animal(id, post_body)

        elif resource == "customers":
            success = update_customer(id, post_body)

        elif resource == "employees":
            success = update_employee(id, post_body)

        elif resource == "locations":
            success = update_location(id, post_body)

        if success:
            self._set_headers(204)
        else:
            self._set_headers(404)

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
        (resource, id, query_params) = self.parse_url(self.path)

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
            delete_customer(id)
        self.wfile.write("".encode())


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
