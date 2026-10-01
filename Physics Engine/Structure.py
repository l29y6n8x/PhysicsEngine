from Integration import Integration
import numpy as np
from Collision import collision

class system:
    def __init__(self):
        self.bodies = []
        self.boundry = []
        self.timestep = 0.1
        self.time = 0.0
        self.integration = Integration()

    def add_object(self, body, boundary):
        self.bodies.append(body)
        if boundary is not None and boundary not in self.boundry:
            self.boundry.append(boundary)

    def Differential_Equation(self, DEQ):
        self.DEQ = DEQ

    def Simulation(self):

        for body in self.bodies:

            parameters = {
                **self.parameters,
                "mass": body.mass,
                "charge": body.charge
            }

            body.state = self.integration.RK4(
                self.DEQ,
                self.bodies,
                body.state,
                parameters,
                self.timestep
            )
        if self.boundry:
            for body in self.bodies:
                for boundary in self.boundry:
                    collision(
                        body,
                        boundary,
                        "boundary"
                    ).check_boundary_collision()

        for i in range(len(self.bodies)):
            for j in range(i + 1, len(self.bodies)):

                collision(
                    self.bodies[i],
                    self.bodies[j],
                    "body"
                ).check_body_collision()

    
        self.time += self.timestep

        return self.bodies

    def Graph(self):
        from Visualisation.Graph import Graph
        Graph(self.timestep, self.Simulation)

    def Animation(self):
        from Visualisation.Animation import Animation
        Animation(self.Simulation, self.timestep, self.boundry).loop()