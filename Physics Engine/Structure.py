from Integration import Integration
import numpy as np
from Collision import collision

class system:
    def __init__(self):
        self.bodies = []
        self.boundry = []
        self.timestep = 0.01
        self.time = 0.0
        self.integration = Integration()

    def add_object(self, body, boundary):
        self.bodies.append(body)
        self.boundry.append(boundary)

    def Differential_Equation(self, DEQ):
        self.DEQ = DEQ

    def Simulation(self):
        for body in self.bodies:

            parameters = {
                **self.parameters,
                "mass": body.mass
            }

            body.state = self.integration.RK4(
                self.DEQ,
                body.state,
                parameters,
                self.timestep
            )

            for boundry in self.boundry:
                    collision(body, boundry, "boundary").check_collision()
                            
            for body2 in self.bodies:
                if body2 != body:
                    collision(body, body2, "body").check_collision()
            
            

        self.time += self.timestep

        return (
            self.bodies
            #self.time
        )

    def Graph(self):
        from Visualisation.Graph import Graph
        Graph(self.timestep, self.Simulation)

    def Animation(self):
        from Visualisation.Animation import Animation
        Animation(self.Simulation, self.timestep, self.boundry).loop()