from Structure import system
from Setup import setup

print("Starting simulation...")
System = system()
Setup = setup()

Setup.create_objects(System)

System.parameters = Setup.get_parameters()
System.Differential_Equation(Setup.get_DEQ())

#System.Graph()

System.Animation() 