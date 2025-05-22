from entities.celestial_body import CelestialBody

class Planet(CelestialBody):
    def __init__(self, name, type, mass, position, velocity, color, radius, atmosphere, surface):
        super().__init__(name, type, mass, position, velocity, color, radius)
        self.atmosphere = atmosphere
        self.surface = surface
    
    def to_dict(self):
        return {
            "name": self.name,
            "type": self.type,
            "mass": self.mass,
            "position": self.position.tolist(),
            "velocity": self.velocity.tolist(),
            "color": self.color,
            "radius": self.radius,
            "atmosphere": self.atmosphere,
            "surface": self.surface
        }