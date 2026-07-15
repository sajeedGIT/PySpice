import matplotlib.pyplot as plt
import numpy as np

from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *

# Create circuit
circuit = Circuit("Diode IV Characteristics")

# Define diode model
circuit.include("1N4007.lib")

# Voltage source
circuit.V('input', 'vin', circuit.gnd, 0@u_V)

# Series resistor
circuit.R(1, 'vin', 'anode', 1@u_kΩ)

# Diode
circuit.D(1, 'anode', circuit.gnd, model='1N4007')

# Simulator
simulator = circuit.simulator(
    temperature=25,
    nominal_temperature=25
)

# DC Sweep
analysis = simulator.dc(
    Vinput=slice(0, 1.0, 0.01)
)

# Voltage across diode
vd = np.array(analysis.anode)

# Current through voltage source
current = -np.array(analysis.Vinput)

# Plot
plt.figure(figsize=(7,5))
plt.plot(vd, current*1000)

plt.grid(True)
plt.xlabel("Diode Voltage (V)")
plt.ylabel("Diode Current (mA)")
plt.title("Diode I-V Characteristics")
plt.show()