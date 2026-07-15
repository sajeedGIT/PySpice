import matplotlib.pyplot as plt
import numpy as np
from PySpice.Doc.ExampleTools import find_libraries
from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *
from PySpice.Spice.Library import SpiceLibrary
# 1. Initialize Circuit
circuit = Circuit("BJT Output Characteristics")

# 2. Define the BC547A Transistor Model
libraries_path = find_libraries()
print("Libraries path:", libraries_path)
spice_library = SpiceLibrary(libraries_path)

circuit.include(spice_library['BC547A'])

# 3. Add Components
circuit.SinusoidalVoltageSource(
    "IN",
    "vin",
    circuit.gnd,
    amplitude=20@u_mV,
    frequency=1@u_kHz
) # Default value, will be overridden

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


analysis = simulator.transient( step_time=10@u_us, end_time=5@u_ms)

# Extract data arrays
# Plot
time = np.array(analysis.time) * 1000

vin = np.array(analysis.vin)
vout = np.array(analysis.vout)

plt.figure(figsize=(10,5))
plt.subplot(2, 1, 1)
plt.plot(time, vin, label="Input")
plt.xlabel("Time (ms)")
plt.ylabel("Input Voltage (Vin)")
plt.title("Common Emitter Amplifier")
plt.grid(True)
plt.subplot(2, 1, 2)
plt.plot(time, vout, label="Output")
plt.xlabel("Time (ms)")
plt.ylabel("Voltage (Vout)")
plt.title("Common Emitter Amplifier")
plt.grid(True)


plt.show()
