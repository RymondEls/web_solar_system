import numpy as np

G = 6.67430e-11

def compute_acceleration(bodies, index):
    acceleration = np.zeros(2)
    for i, body in enumerate(bodies):
        if i != index:
            r = body.position - bodies[index].position
            r_norm = np.linalg.norm(r)
            if r_norm > 0:
                acceleration += G * body.mass / r_norm**3 * r
    return acceleration

def rk4_step(bodies, dt):
    new_positions = []
    new_velocities = []
    for i, body in enumerate(bodies):
        k1_v = compute_acceleration(bodies, i) * dt
        k1_r = body.velocity * dt
        k2_v = compute_acceleration(bodies, i) * dt
        k2_r = (body.velocity + k1_v / 2) * dt
        k3_v = compute_acceleration(bodies, i) * dt
        k3_r = (body.velocity + k2_v / 2) * dt
        k4_v = compute_acceleration(bodies, i) * dt
        k4_r = (body.velocity + k3_v) * dt
        new_position = body.position + (k1_r + 2*k2_r + 2*k3_r + k4_r) / 6
        new_velocity = body.velocity + (k1_v + 2*k2_v + 2*k3_v + k4_v) / 6
        new_positions.append(new_position)
        new_velocities.append(new_velocity)
    for i, body in enumerate(bodies):
        body.update_position(new_positions[i])
        body.velocity = new_velocities[i]