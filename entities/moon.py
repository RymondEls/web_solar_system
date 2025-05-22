from entities.celestial_body import CelestialBody

class Moon(CelestialBody):
    def __init__(self, name, type, mass, position, velocity, color, radius, parent_planet):
        super().__init__(name, type, mass, position, velocity, color, radius)
        self.parent_planet = parent_planet

    def to_dict(self):
        return {
            "name": self.name,
            "type": self.type,
            "mass": self.mass,
            "position": self.position.tolist(),
            "velocity": self.velocity.tolist(),
            "color": self.color,
            "radius": self.radius,
            "parent_planet": self.parent_planet
        }