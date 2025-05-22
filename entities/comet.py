from entities.celestial_body import CelestialBody

class Comet(CelestialBody):
    def __init__(self, name, type, mass, position, velocity, color, radius, tail_length):
        super().__init__(name, type, mass, position, velocity, color, radius)
        self.tail_length = tail_length

    def to_dict(self):
        return {
            "name": self.name,
            "type": self.type,
            "mass": self.mass,
            "position": self.position.tolist(),
            "velocity": self.velocity.tolist(),
            "color": self.color,
            "radius": self.radius,
            "tail_length": self.tail_length
        }