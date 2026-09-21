from Structure import system
from Setup import setup


System = system()
Setup = setup()

Setup.create_bodies(System)

System.parameters = Setup.get_parameters()
System.Differential_Equation(Setup.get_DEQ())

#System.Graph()

System.Animation() 