import matplotlib.pyplot as plt
import numpy as np
from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *

# 1. Initialize Circuit
circuit = Circuit("BJT Output Characteristics")

# 2. Define the BC547A Transistor Model
circuit.include("BC547A.lib")


# 3. Add Components
# Base current source (I_B) connected between GND and node 'base'
circuit.SinusoidalVoltageSource(
    "IN",
    "vin",
    circuit.gnd,
    dc_offset=0@u_V,
    amplitude=0@u_V,      # ignored during AC analysis
    frequency=1@u_kHz,
    ac_magnitude=20@u_mV
)

# Add the BJT (Collector, Base, Emitter)
circuit.BJT("1", "collector", "base", "emitter", model="BC547A")

# Collector-Emitter voltage source (V_CE) connected between node 'collector' and GND
circuit.C("b", "vin", "base", 10@u_uF)  # Default value, will be swept
circuit.V("CC", "VCC", circuit.gnd, 12@u_V)  # Default value, will be swept
circuit.R("1","base","VCC", 15@u_kΩ)  # Base resistor
circuit.R("2","base",circuit.gnd, 4.7@u_kΩ)  # Base resistor
circuit.R("C", "collector", "VCC", 1@u_kΩ)  # Collector resistor
circuit.R("E", "emitter", circuit.gnd, 1@u_kΩ)  # Emitter resistor
circuit.C("c", "collector", "vout", 10@u_uF)  # Coupling capacitor
circuit.R("L", "vout", circuit.gnd, 10@u_kΩ)
circuit.C("e", "emitter", circuit.gnd, 100@u_uF)  # Bypass capacitor
# 4. Set up the Nested Sweep Configuration
simulator = circuit.simulator(temperature=25)


analysis = simulator.ac(start_frequency=10@u_Hz, stop_frequency=30@u_MHz, number_of_points=100,  variation='dec')

# Extract data arrays
# Plot
frequencies = np.array(analysis.frequency)
vin = np.array(analysis.vin)
vout = np.array(analysis.vout)

plt.figure(figsize=(10,5))
plt.semilogx(frequencies, 20*np.log10(np.abs(vout/vin)), label="Output")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Magnitude (dB)")
plt.title("Frequency Response")
plt.grid(True)
plt.show()
