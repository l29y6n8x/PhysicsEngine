import numpy as np

class body:
    def __init__(self, position, velocity , mass, radius, charge):
        self.mass = mass
        self.radius = radius
        self.charge = charge
        self.state = np.array([position, velocity])
        self.acceleration = np.array([0.0, 0.0, 0.0])