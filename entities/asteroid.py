from entities.celestial_body import CelestialBody

class Asteroid(CelestialBody):
    def __init__(self, name, type, mass, position, velocity, color, radius, composition):
        super().__init__(name, type, mass, position, velocity, color, radius)
        self.composition = composition

    def to_dict(self):
        return {
            "name": self.name,
            "type": self.type,
            "mass": self.mass,
            "position": self.position.tolist(),
            "velocity": self.velocity.tolist(),
            "color": self.color,
            "radius": self.radius,
            "composition": self.composition
        }