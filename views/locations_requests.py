LOCATIONS = [
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

def get_all_locations():
    '''Shows all objects within the LOCATIONS array.'''
    return LOCATIONS

def get_single_location(id):
    '''Shows a single object within the LOCATIONS array.'''
    requested_location = None

    for location in LOCATIONS:
        if location["id"] == id:
            requested_location = location

    return requested_location

def create_location(location):
    '''Get the id value of the last location in the list.'''
    max_id = LOCATIONS[-1]["id"]
    new_id = max_id + 1
    location ["id"] = new_id
    LOCATIONS.append(location)
    return location
