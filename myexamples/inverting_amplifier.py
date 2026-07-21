import numpy as np
import matplotlib.pyplot as plt
from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *

circuit = Circuit('Inverting Amplifier')
circuit.include('D:\PySpice\myexamples\lm741.lib')

circuit.SinusoidalVoltageSource('input', 'input', circuit.gnd, amplitude=20@u_mV, frequency=10@u_kHz)
circuit.R(1, 'input', 'inverting_input', 1@u_kΩ)
circuit.R(2, 'inverting_input', 'output', 10@u_kΩ)
circuit.V('pos', 'positive_power_supply', circuit.gnd, 12@u_V)
circuit.V('neg', 'negative_power_supply', circuit.gnd, -12@u_V)
circuit.R(3, 'output', circuit.gnd, 10@u_kΩ)
circuit.R(4, 'non_inverting_input', circuit.gnd, 0@u_kΩ)
circuit.X(
    "1",
    "LM741",
    "non_inverting_input",
    "inverting_input",
    "positive_power_supply",
    "negative_power_supply",
    "output"
)

circuit.simulator(temperature=25, nominal_temperature=25)

analysis = circuit.simulator().transient(step_time=1@u_us, end_time=5@u_ms )

# Extract data arrays
time = np.array(analysis.time)
vin = np.array(analysis.input)
vout = np.array(analysis.output)

# Plot
plt.figure(figsize=(10,5))
plt.subplot(2, 1, 1)
plt.plot(time, vin, label='Input Voltage (V)')
plt.xlabel('Time (s)')
plt.ylabel('Voltage (V)')
plt.title('Input Voltage')
plt.legend()
plt.grid(True)

plt.subplot(2, 1, 2)
plt.plot(time, vout, label='Output Voltage (V)')
plt.xlabel('Time (s)')
plt.ylabel('Voltage (V)')
plt.title('Output Voltage')
plt.legend()
plt.grid(True)
plt.show()

