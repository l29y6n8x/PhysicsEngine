import numpy as np

class Differential_Equation:
    def __init__(self, DEQ):
        self.Equations = [DEQ] if isinstance(DEQ, str) else DEQ
        
        

    def Harmonic_Oscillator(self, state, constants):

        spring_strength = constants["spring_strength"] 
        mass = constants["mass"]
        damping_ratio = constants["damping_ratio"]


        w = np.sqrt(spring_strength / mass)  # Natural frequency
        damping = 2 * w * damping_ratio

        x_dot = state[1]
        x_ddot = -w**2 * state[0] - (damping * state[1]) / mass # Damping term

        return np.array([x_dot, x_ddot])

    def Newtonian_Gravity(self, bodies, state, constants):
        G = constants["G"]
        m = constants["mass"]
        self.energy = 0.0
        
        length_scale = constants["length_scale"]
        force = np.zeros(3)

        for body in bodies:
            if body.state[0] is not state[0]:
                r = body.state[0] - state[0]
                distance = np.linalg.norm(r)
                if distance <= 1:
                    continue

                force += G * m * body.mass * (r / distance**3) * (1/ length_scale**2)

        for i in range(len(bodies)):
            self.energy += 0.5 * bodies[i].mass * np.linalg.norm(bodies[i].state[1])**2  # Kinetic energy
            for j in range(i + 1, len(bodies)):
                r = bodies[j].state[0] - bodies[i].state[0]
                distance = np.linalg.norm(r)
                if distance <= 1:
                    continue
                self.energy += G * bodies[j].mass * bodies[i].mass / distance

        print("Energy:", self.energy)

        x_dot = state[1]
        x_ddot = force / m
        #print("Force:", force)
        return np.array([x_dot, x_ddot])



    def Electrostatic(self, bodies, state, constants):
        k = constants["k"]
        m = constants["mass"]
        q = constants["charge"]
        length_scale = constants["length_scale"]
        self.energy = 0.0
        force = np.zeros(3)

        for body in bodies:
            if body.state[0] is not state[0]:
                r = body.state[0] - state[0]
                distance = np.linalg.norm(r)
                if distance <= 1:
                    continue

                force -= k * q * body.charge * (r / distance**3) * (1 / length_scale**2)

        x_dot = state[1]
        x_ddot = force / m

        return np.array([x_dot, x_ddot])

    def Magnetic(self, bodies, state, constants):
        return 

        

    def execute(self, bodies, state, constants):
        self.output = np.array([state[1], [0.0, 0.0, 0.0]])
        for DEQ in self.Equations:
            if DEQ == "Harmonic_Oscillator":
                self.output[1] += self.Harmonic_Oscillator(state, constants)[1]
            if DEQ == "Newtonian_Gravity":
                self.output[1] += self.Newtonian_Gravity(bodies, state, constants)[1]
            if DEQ == "Electromagnetism":
                self.output[1] += self.Electrostatic(bodies, state, constants)[1]
              #  self.output[1] += self.Magnetic(bodies, state, constants)[1]
        self.acceleration = self.output[1]
        return self.output