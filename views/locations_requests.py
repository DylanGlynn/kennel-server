import sqlite3
import json
from models import Location

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
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        sql_to_execute = """
        SELECT l.id, l.name, l.address, COUNT(*) AS `Total_Animals`
        FROM Location l
        JOIN Animal a
        ON l.id = a.location_id
        GROUP BY a.location_id;
        """

        db_cursor.execute(sql_to_execute)

        locations = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            location = Location(row['id'], row['name'], row['address'], row['Total_Animals'])

            locations.append(location.__dict__)

    return locations

def get_single_location(id):
    '''Shows a single object within the LOCATIONS array.'''
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            l.id,
            l.name,
            l.address,
            l.animals
        FROM location l
        WHERE a.id = ?
        """, ( id, ))

        data = db_cursor.fetchone()

        location = Location(data['id'], data['name'], data['address'], data['animals'])

        return location.__dict__

def create_location(location):
    '''Get the id value of the last location in the list.'''
    max_id = LOCATIONS[-1]["id"]
    new_id = max_id + 1
    location ["id"] = new_id
    LOCATIONS.append(location)
    return location

def delete_location(id):
    '''Handles the DELETE requests.'''
    location_index = -1
    for index, location in enumerate(LOCATIONS):
        if location["id"] == id:
            location_index = index
    if location_index >= 0:
        LOCATIONS.pop(location_index)

def update_location(id, new_location):
    '''Handles the PUT request.'''
    for index, location in enumerate(LOCATIONS):
        if location["id"] == id:
            LOCATIONS[index] = new_location
            break
