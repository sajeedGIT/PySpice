import numpy as np
import matplotlib.pyplot as plt
from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *

circuit = Circuit('Weinbridge Oscillator')
circuit.include('D:\PySpice\myexamples\lm741.lib')


circuit.R(1, 'inverting_input',circuit.gnd, 4.7@u_kΩ)
circuit.R(2, 'inverting_input', 'output', 10@u_kΩ)
circuit.V('pos', 'positive_power_supply', circuit.gnd, 12@u_V)
circuit.V('neg', 'negative_power_supply', circuit.gnd, -12@u_V)
#circuit.R(3, 'output', circuit.gnd, 10@u_kΩ)
circuit.R(5, 'output', 'cn1', 4.7@u_kΩ)
circuit.C(1, 'cn1', 'non_inverting_input', 0.1@u_uF)
circuit.R(4, 'non_inverting_input', circuit.gnd, 4.7@u_kΩ)
circuit.C(2, 'non_inverting_input', circuit.gnd, 0.1@u_uF)
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

analysis = circuit.simulator().transient(step_time=1@u_us, start_time=200@u_ms, end_time=280@u_ms )

# Extract data arrays
time = np.array(analysis.time)

vout = np.array(analysis.output)

# Plot
plt.figure(figsize=(10,5))
plt.plot(time, vout, label='Output Voltage (V)')
plt.xlabel('Time (s)')
plt.ylabel('Voltage (V)')
plt.title('Output Voltage')
plt.legend()
plt.grid(True)
plt.show()

