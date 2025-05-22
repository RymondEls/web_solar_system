from entities.celestial_body import CelestialBody

class Spacecraft(CelestialBody):
    def __init__(self, name, type, mass, position, velocity, color, radius, mission):
        super().__init__(name, type, mass, position, velocity, color, radius)
        self.mission = mission

    def to_dict(self):
        return {
            "name": self.name,
            "type": self.type,
            "mass": self.mass,
            "position": self.position.tolist(),
            "velocity": self.velocity.tolist(),
            "color": self.color,
            "radius": self.radius,
            "mission": self.mission
        }