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
circuit.I("B", circuit.gnd, "base", 10@u_uA)  # Default value, will be overridden

# Collector-Emitter voltage source (V_CE) connected between node 'collector' and GND
circuit.V("CE", "collector", circuit.gnd, 0@u_V)  # Default value, will be swept

# Add the BJT (Collector, Base, Emitter)
circuit.BJT("1", "collector", "base", circuit.gnd, model="BC547A")

# 4. Set up the Nested Sweep Configuration
base_currents = [10, 20, 30, 40, 50]  # Base currents in microamperes (uA)

plt.figure(figsize=(10, 6))

# Loop through each Base Current (Outer Sweep)
for ib_val in base_currents:
    # Dynamically update the base current value in the netlist
    circuit["IB"].dc_value = ib_val @ u_uA

    # Set up simulator
    simulator = circuit.simulator(temperature=25)

    # Sweep V_CE from 0V to 5V in steps of 0.05V (Inner Sweep)
    analysis = simulator.dc(VCE=slice(0, 5.0, 0.05))

    # Extract data arrays
    v_ce_axis = np.array(analysis.collector)  # Swept voltage vector
    i_c_axis = -np.array(analysis.VCE) * 1000  # Convert Amperes to mA

    # Plot the curve for the current I_B step
    plt.plot(v_ce_axis, i_c_axis, label=f"Ib = {ib_val} µA")

# 5. Format and Show Plot
plt.title("BC547A BJT Output Characteristics ($I_C$ vs $V_{CE}$)")
plt.xlabel("Collector-Emitter Voltage $V_{CE}$ (V)")
plt.ylabel("Collector Current $I_C$ (mA)")
plt.grid(True)
plt.legend()
plt.show()
