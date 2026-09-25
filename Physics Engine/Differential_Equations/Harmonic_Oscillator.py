import numpy as np

def Harmonic_Oscillator(state, constants):

    spring_strength = constants["spring_strength"] 
    mass = constants["mass"]
    damping_ratio = constants["damping_ratio"]


    w = np.sqrt(spring_strength / mass)  # Natural frequency
    damping = 2 * w * damping_ratio

    x_dot = state[1]
    x_ddot = -w**2 * state[0] #- (damping * state[1]) / mass # Damping term
    
    return np.array([x_dot, x_ddot])