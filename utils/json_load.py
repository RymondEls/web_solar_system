import json
from entities.star import Star
from entities.planet import Planet
from entities.moon import Moon
from entities.comet import Comet
from entities.asteroid import Asteroid
from entities.spacecraft import Spacecraft


def load_bodies_from_json(file_path):
    with open(file_path, "r") as file:
        data = json.load(file)
    bodies = []
    for body_data in data:
        if body_data["type"] == "star":
            bodies.append(Star(**body_data))
        elif body_data["type"] == "planet":
            bodies.append(Planet(**body_data))
        elif body_data["type"] == "moon":
            bodies.append(Moon(**body_data))
        elif body_data["type"] == "comet":
            bodies.append(Comet(**body_data))
        elif body_data["type"] == "asteroid":
            bodies.append(Asteroid(**body_data))
        elif body_data["type"] == "spacecraft":
            bodies.append(Spacecraft(**body_data))
    return bodies


def save_bodies_to_json(file_path, bodies):
    data = []
    for body in bodies:
        data.append(body.to_dict())
    
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)