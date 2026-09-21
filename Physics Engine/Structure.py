from Integration import Integration


class system:
    def __init__(self):
        self.bodies = []
        self.timestep = 0.01
        self.time = 0.0
        self.integration = Integration()

    def add_body(self, body):
        self.bodies.append(body)

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
        Animation(self.Simulation, self.timestep).loop()