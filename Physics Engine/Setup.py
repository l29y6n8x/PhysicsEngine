from Body import body


class setup:
    def __init__(self):
        self.bodies = [
            [[50.0, 600.0, 10.0],
             [0.0, 0.0, 0.0],
             1.0,
             100],
            [[100.0, 60.0, 0.0],
             [0.0, 0.0, 0.0],
             5.0,
             100]

        ]

    def create_bodies(self, system):
        for data in self.bodies:
            Body = body(
                data[0],
                data[1],
                data[2],
                data[3]
            )

            system.add_body(Body)

    def get_DEQ(self):
        return "Harmonic_Oscillator"

    def get_parameters(self):
        return {
            "spring_strength": 5.0,
            "damping_ratio": 0.0
        }