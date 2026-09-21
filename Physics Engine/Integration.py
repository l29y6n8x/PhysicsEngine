import numpy as np
import importlib

class Integration:
    def __init__(self):
        self.eq = None

    def get_DEQ(self, DEQ):
        path = f"Differential_Equations.{DEQ}" 
        equation_module = importlib.import_module(path)
        self.eq = getattr(equation_module, DEQ)

    def Eulers_Method(self, DEQ, state, constants, dt): 
        if self.eq is None:
            self.get_DEQ(DEQ)
        return self.eq(state, constants) * dt + state

    def RK4(self, DEQ, state, constants, dt):
        if self.eq is None:
            self.get_DEQ(DEQ)
        
        k1 = self.eq(state, constants)
        k2 = self.eq(state + (dt / 2) * k1, constants)
        k3 = self.eq(state + (dt / 2) * k2, constants)
        k4 = self.eq(state + dt * k3, constants)

        return state + (dt / 6) * (k1 + 2 * k2 + 2 * k3 + k4)

