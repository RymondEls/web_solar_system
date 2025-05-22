from entities.celestial_body import CelestialBody

class Star(CelestialBody):
    def __init__(self, name, type, mass, position, velocity, color, radius, temperature):
        super().__init__(name, type, mass, position, velocity, color, radius)
        self.temperature = temperature

    def to_dict(self):
        return {
            "name": self.name,
            "type": self.type,
            "mass": self.mass,
            "position": self.position.tolist(),
            "velocity": self.velocity.tolist(),
            "color": self.color,
            "radius": self.radius,
            "temperature": self.temperature
        }