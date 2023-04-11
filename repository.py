import json
from urllib.parse import urlparse
from http.server import BaseHTTPRequestHandler, HTTPServer


DATABASE = {
    "ANIMALS": [
        {
            "id": 1,
            "name": "Snickers",
            "species": "Dog",
            "locationId": 1,
            "customerId": 1,
            "status": "Admitted"
        },
        {
            "id": 2,
            "name": "Eleanor",
            "species": "Dog",
            "locationId": 1,
            "customerId": 2,
            "status": "Admitted"
        },
        {
            "id": 3,
            "name": "Blue",
            "species": "Cat",
            "locationId": 2,
            "customerId": 1,
            "status": "Admitted"
        }
    ],
    "CUSTOMERS": [
        {
            "id": 1,
            "name": "Ryan Tanay"
        },
        {
            "id": 2,
            "name": "AJ Nua"
        }
    ],
    "EMPLOYEES": [
        {
            "id": 1,
            "name": "Jenna Solis"
        }
    ],
    "LOCATIONS": [
        {
            "id": 1,
            "name": "Nashville North",
            "address": "8422 Johnson Pike"
        },
        {
            "id": 2,
            "name": "Nashville South",
            "address": "209 Emory Drive"
        }
    ]
}


class HandleRequests(BaseHTTPRequestHandler):
    """Controls the functionality of any GET, PUT, POST, DELETE requests to the server"""

#    def parse_url(self, path):
#    url_components = urlparse(path)
#    path_params = url_components.path.strip("/").split("/")
#    query_params = url_components.query.split("&") # ? instead of & maybe?
#    resource = path_params[0]
#    id = None

#    try:
#        id = int(path_params[1])
#    except IndexError:
#        pass
#    except ValueError:
#        pass

#    return (resource, id, query_params)


def all(resources):
    """For GET requests to collection"""
    return DATABASE[resources]


def retrieve(resources, id):
    """For GET requests to a single resource"""
    requested_resource = None
    for resource in DATABASE[resources]:
        # Dictionaries in Python use [] notation to find a key
        # instead of the dot notation that JavaScript used.
        if resource["id"] == id:
            requested_resource = resource.copy

    return requested_resource


def create_resource(resources, resource):
    '''Get the id value of the last entry in the list'''
    max_id = DATABASE[resources][-1]["id"]
    new_id = max_id + 1
    resource["id"] = new_id
    DATABASE[resources].append(resource)
    return resource


def create(self, resource):
    """For POST requests to a collection"""
    content_len = int(self.headers.get('content-length', 0))
    post_body = self.rfile.read(content_len)

    # Convert JSON string to a Python dictionary
    post_body = json.loads(post_body)

    # Parse the URL
    (resource) = self.parse_url(self.path)
    created_resource = None
    self._set_headers(201)
    created_resource = create_resource(resource, post_body)
    self.wfile.write(json.dumps(created_resource).encode())


#    if resource == "animals":
#        if "name" in post_body and "species" in post_body and "locationId" in post_body and "customerId" in post_body and "status" in post_body:
#            self._set_headers(201)
#            created_resource = create_resource(resource, post_body)
    # Encode the new animal and send in response
#        else:
#            self._set_headers(400)
#            created_resource = {
#                "message": f'{"name is required." if "name" is not post_body else ""} {"species is required." if "species" is not post_body else ""} {"Location is required." if "locationId" is not post_body else ""} {"Customer is required." if "customerId" is not post_body else ""} {"Status is required." if "status" is not post_body else ""}'}

#    if resource == "locations":
#        if "name" in post_body and "address" in post_body:
#            self._set_headers(201)
#            created_resource = create_location(post_body)
#        else:
#            self._set_headers(400)
#            created_resource = {
#                "message": f'{"name is required." if "name" is not post_body else ""} {"address is required." if "address" is not post_body else ""}'}

#    if resource == "employees":
#        new_employee = create_employee(post_body)
#    self.wfile.write(json.dumps(new_employee).encode())

#    if resource == "customers":
#        new_customer = create_customer(post_body)
#    self.wfile.write(json.dumps(new_customer).encode())

#    self.wfile.write(json.dumps(created_resource).encode())


def update():
    """For PUT requests to a single resource"""
    pass


def delete(self, resource):
    """For DELETE requests to a single resource"""

    def delete_resource(resource, id):
        '''Handles the DELETE requests.'''
        resource_index = -1
        for index, entry in enumerate(DATABASE[resource]):
            if entry["id"] == id:
                resource_index = index
        if resource_index >= 0:
            DATABASE[resource].pop(resource_index)

# Parse the URL
    (resource, id) = self.parse_url(self.path)
    response = {}

    if resource == "customers":
        self._set_headers(400)
        response = ''
    else:
        self._set_headers(204)
        delete_resource(id)
        response = {f'Entry deleted from {resource}.'}
        self.rfile.write(json.dumps(response).encode())
