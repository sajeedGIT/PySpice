import matplotlib.pyplot as plt
import numpy as np
from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *
from OperationalAmplifier import BasicOperationalAmplifier
circuit = Circuit('Inverting Amplifier')

# Power supplies
circuit.V('CC', 'VCC', circuit.gnd, 15@u_V)
circuit.V('EE', 'VEE', circuit.gnd, -15@u_V)

# Input signal (100 mV peak, 1 kHz)
circuit.SinusoidalVoltageSource(
    'input',
    'Vin',
    circuit.gnd,
    amplitude=100@u_mV,
    frequency=1@u_kHz
)

# Resistors
circuit.R(1, 'Vin', 'N1', 1@u_kΩ)
circuit.R(2, 'OUT', 'N1', 10@u_kΩ)
circuit.R(3, 'N2', circuit.gnd, 0@u_Ω)

# Universal Op-Amp (idealized)
circuit.subcircuit(BasicOperationalAmplifier())
circuit.X('OP','BasicOperationalAmplifier',
    'N2',
    'N1',
    'OUT'
)


# Simulation
simulator = circuit.simulator(
    temperature=25,
    nominal_temperature=25
)

analysis = simulator.transient(
    step_time=10@u_us,
    end_time=5@u_ms
)

# Plot
time = np.array(analysis.time)
vin = np.array(analysis.Vin)
vout = np.array(analysis.OUT)

plt.figure(figsize=(9,4))
plt.plot(time*1000, vin, label='Input')
plt.plot(time*1000, vout, label='Output')

plt.xlabel('Time (ms)')
plt.ylabel('Voltage (V)')
plt.title('Inverting Amplifier (Gain = -10)')
plt.grid(True)
plt.legend()

plt.show()