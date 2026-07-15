import matplotlib.pyplot as plt
import numpy as np

from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *

# Create circuit
circuit = Circuit("Half Wave Rectifier")

# Diode Model
circuit.model(
    'D4148',
    'D',
    IS=4.352e-9,
    RS=0.6458,
    N=1.906,
    BV=100,
    IBV=0.0001
)

# AC Source (10 V peak, 50 Hz)
circuit.SinusoidalVoltageSource(
    'input',
    'input',
    circuit.gnd,
    amplitude=10@u_V,
    frequency=50@u_Hz
)

# Diode
circuit.D(1, 'input', 'out', model='D4148')

# Load Resistor
circuit.R(1, 'out', circuit.gnd, 1@u_kΩ)

# Simulator
simulator = circuit.simulator(
    temperature=25,
    nominal_temperature=25
)

# Transient Analysis
analysis = simulator.transient(
    step_time=100@u_us,
    end_time=60@u_ms
)

# Convert to NumPy arrays
time = np.array(analysis.time)
vin = np.array(analysis.input)
vout = np.array(analysis.out)

# Plot
plt.figure(figsize=(10,5))

plt.plot(time*1000, vin, label='Input Voltage')
plt.plot(time*1000, vout, linewidth=2, label='Output Voltage')

plt.xlabel("Time (ms)")
plt.ylabel("Voltage (V)")
plt.title("Half-Wave Rectifier")
plt.grid(True)
plt.legend()

plt.show()