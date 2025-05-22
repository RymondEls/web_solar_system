from utils.physics import rk4_step

def simulate_orbits(bodies, dt, time_scale):
    for _ in range(int(time_scale)):
        rk4_step(bodies, dt)