from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *
import numpy as np
circuit = Circuit('Voltage Divider')

circuit.V('input', 'ip', circuit.gnd, 10@u_V)
circuit.R(1, 'ip', 'out', 1@u_kΩ)
circuit.R(2, 'out', circuit.gnd, 1@u_kΩ)

simulator = circuit.simulator(temperature=25,
                              nominal_temperature=25)

analysis = simulator.operating_point()

print(np.array(analysis.out))
print(np.array(analysis.ip))