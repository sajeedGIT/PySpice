import numpy as np
import matplotlib.pyplot as plt
from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *

circuit = Circuit('Inverting Amplifier')
circuit.include(r'D:\PySpice\myexamples\lm741.lib')
circuit.include(r"D:\PySpice\myexamples\1N4007.lib")
circuit.PieceWiseLinearVoltageSource(
    'VIN',
    'input',
    circuit.gnd,
    values=[
        (0@u_ms,   -9@u_V),
        (0.5@u_ms,  9@u_V),
        (1.0@u_ms, -9@u_V),

        (1.5@u_ms,  9@u_V),
        (2.0@u_ms, -9@u_V),

        (2.5@u_ms,  9@u_V),
        (3.0@u_ms, -9@u_V),

        (3.5@u_ms,  9@u_V),
        (4.0@u_ms, -9@u_V),

        (4.5@u_ms,  9@u_V),
        (5.0@u_ms, -9@u_V),
    ]
)
#circuit.SinusoidalVoltageSource('input', 'input', circuit.gnd, amplitude=9@u_V, frequency=1@u_kHz)
circuit.R(1, 'input', 'inverting_input', 1@u_kΩ)
circuit.R(5, 'anode', circuit.gnd, 10@u_kΩ)
circuit.R(6, 'cathode', 'inverting_input', 0@u_kΩ)
circuit.R(2, 'inverting_input', 'output', 1@u_kΩ)
circuit.V('pos', 'positive_power_supply', circuit.gnd, 12@u_V)
circuit.V('neg', 'negative_power_supply', circuit.gnd, -12@u_V)
circuit.R(3, 'output', circuit.gnd, 10@u_kΩ)
circuit.R(4, 'non_inverting_input', circuit.gnd, 0@u_kΩ)

circuit.D(1, 'anode', 'cathode', model='1N4007')
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
vdut = np.array(analysis.anode) 
# Plot
plt.figure(figsize=(10,5))
plt.subplot(2, 1, 1)
plt.plot(time, vout, label='Input Voltage (V)')
plt.xlabel('Time (s)')
plt.ylabel('Voltage (V)')
plt.title('Input Voltage')
plt.legend()
plt.grid(True)

plt.subplot(2, 1, 2)
plt.plot(vdut*1000, vout, label='Output Voltage (V)')
plt.xlabel('V (mV)')
plt.ylabel('Voltage (V)')
plt.title('Output Voltage')
plt.legend()
plt.grid(True)
plt.show()

