import numpy as np
import pygame

class CelestialBody:
    def __init__(self, name, type, mass, position, velocity, color, radius):
        self.name = name
        self.type = type
        self.mass = mass
        self.position = np.array(position, dtype=float)
        self.velocity = np.array(velocity, dtype=float)
        self.color = color
        self.radius = radius
        self.trajectory = []

    def update_position(self, new_position):
        self.position = new_position
        self.trajectory.append(self.position.copy())

    def draw(self, screen, scale, offset, font):
        x = int(self.position[0] * scale + offset[0])
        y = int(self.position[1] * scale + offset[1])
        display_radius = max(1, int(self.radius * scale * 2))
        pygame.draw.circle(screen, self.color, (x, y), max(1, int(self.radius * scale * 2)))
        if self.name:
            text = font.render(self.name, True, (255,255,255))
            screen.blit(text, (x + display_radius, y + display_radius))