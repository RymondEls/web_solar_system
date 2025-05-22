from entities.spacecraft import Spacecraft

def launch_spacecraft(bodies, name, mass, position, velocity, mission):
    spacecraft = Spacecraft(name, "spacecraft", mass, position, velocity, (255, 255, 255), 1, mission)
    bodies.append(spacecraft)
    print(f"Космический аппарат {name} запущен с миссией: {mission}")