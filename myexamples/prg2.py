import matplotlib.pyplot as plt

from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *

# Create circuit
circuit = Circuit('RC Charging Circuit')

# Pulse voltage source
circuit.PulseVoltageSource(
    'input',
    'input',
    circuit.gnd,
    initial_value=0@u_V,
    pulsed_value=5@u_V,
    pulse_width=20@u_ms,
    period=40@u_ms,
    rise_time=1@u_us,
    fall_time=1@u_us
)

# Components
circuit.R(1, 'input', 'out', 1@u_kΩ)
circuit.L(2,'out', 'capout', 4@u_mH)
circuit.C(1, 'capout', circuit.gnd, 0.1@u_uF)

# Simulator
simulator = circuit.simulator(temperature=25,
                              nominal_temperature=25)

analysis = simulator.transient(
    step_time=10@u_us,
    end_time=5@u_ms
)

# Plot
plt.figure(figsize=(8,4))

plt.plot(analysis.time,
         analysis.input,
         label='Input')

plt.plot(analysis.time,
         analysis.capout,
         label='Capacitor Voltage')

plt.xlabel("Time (s)")
plt.ylabel("Voltage (V)")
plt.title("RC Charging Transient Response")
plt.grid(True)
plt.legend()

plt.show()