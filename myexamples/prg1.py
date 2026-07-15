from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *

circuit = Circuit("RC Circuit")

circuit.V('input', 'vin', circuit.gnd, 5@u_V)
circuit.R(1, 'vin', 'vout', 1@u_kΩ)
circuit.C(1, 'vout', circuit.gnd, 1@u_mF)

simulator = circuit.simulator()

analysis = simulator.transient(
    step_time=10@u_us,
    end_time=10@u_s
)

import matplotlib.pyplot as plt

import numpy as np

time = np.array(analysis.time)
vout = np.array(analysis.vout)

plt.plot(time, vout)
plt.show()