from Body import body
import numpy as np


class setup:
    def __init__(self):
        #self.bodies = [
        #    [[100.0, 130.0, 0.0],
        #     [0.0, 0.0, 2.0],
        #     1.989e12,
        #     4.0,
        #     0.0],
        #    [[0.0, 150.0, 0.0], #in mrd m
        #     [0.0, 2.0, 0.5], #in m/s
        #     5.972e12,
        #     4.7,
        #     0.0],
        #    [[0.0, 172.0, 50.0], #in mrd m
        #     [3.0, 0.0, 0.0], #in m/s
        #     7.348e12,
        #     5.0,
        #     0.0]
        #]

        self.bodies = []

        self.number_of_bodies = 20

        self.boundary = None#{"type": "cube", "size": 100.0}  # in mrd m

        self.celestial_bodies = {"sun": {"mass": 1.989e30, "charge": 0.0},
                                 "earth": {"mass": 5.972e24, "charge": 0.0},
                                 "moon": {"mass": 7.348e22, "charge": 0.0}}

        self.particles = {"electron": {"mass": 9.10938356e-31, "charge": -1.602176634e-19},
                          "proton": {"mass": 1.6726219e-27, "charge": 1.602176634e-19},
                          "neutron": {"mass": 1.674927471e-27, "charge": 0.0}}

    def create_objects(self, system):
        for i in range(self.number_of_bodies):
            if self.boundary: 
                size = self.boundary["size"] 
            else: 
                size = 100.0

            random_position = [np.random.uniform(-size, size), np.random.uniform(-size, size), np.random.uniform(-size, size)]
            if i % 2 == 0:
                Body = body(
                    random_position,
                    [0.0, 0.0, 0.0],
                    self.particles["proton"]["mass"],
                    5.0,
                    self.particles["proton"]["charge"]
                )
            else:    
                Body = body(
                    random_position,
                    [0.0, 0.0, 0.0],
                    self.particles["electron"]["mass"],
                    5.0,
                    self.particles["electron"]["charge"]
                )
            system.add_object(Body, self.boundary)


    def get_DEQ(self):
        return "Electromagnetism"

    def get_parameters(self):
        return {
            "length_scale": 1.0,
            "spring_strength": 5.0,
            "damping_ratio": 0.1,
            "G": 6.67430e-11,   
            "k": 8.9875517923e9
        }   