from Body import body


class setup:
    def __init__(self):
        self.bodies = [
            [[0.0, 80.0, 80.0],
             [0.0, 0.0, 100.0],
             1.0,
             10],
            [[0.0, 80.0, 0.0],
             [0.0, 0.0, 30.0],
             2.0,
             10]
        ]

        self.boundary = {"type": "cube", "size": 100.0}

    def create_objects(self, system):
        for data in self.bodies:
            Body = body(
                data[0],
                data[1],
                data[2],
                data[3]
            )

            system.add_object(Body, self.boundary)

    def get_DEQ(self):
        return "Harmonic_Oscillator"

    def get_parameters(self):
        return {
            "spring_strength": 5.0,
            "damping_ratio": 0.0
        }