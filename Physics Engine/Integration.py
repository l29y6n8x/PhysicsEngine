import numpy as np
from Differential_Equations import Differential_Equation

class Integration:
    def __init__(self):
        self.eq = None

    def Eulers_Method(self, DEQ, bodies, state, constants, dt): 
        if self.eq is None:    
            self.eq = Differential_Equation(DEQ)

        return self.eq.execute(bodies, state, constants) * dt + state

    def RK4(self, DEQ, bodies, state, constants, dt):
        if self.eq is None:
            self.eq = Differential_Equation(DEQ)
        
            
        
        k1 = self.eq.execute(bodies, state, constants)
        k2 = self.eq.execute(bodies, state + (dt / 2) * k1, constants)
        k3 = self.eq.execute(bodies, state + (dt / 2) * k2, constants)
        k4 = self.eq.execute(bodies, state + dt * k3, constants)

        return state + (dt / 6) * (k1 + 2 * k2 + 2 * k3 + k4)

