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
circuit.V("BE", "VBB", circuit.gnd, 0@u_uV)  # Default value, will be overridden

# Add the BJT (Collector, Base, Emitter)
circuit.BJT("1", "collector", "base", "emitter", model="BC547A")

# Collector-Emitter voltage source (V_CE) connected between node 'collector' and GND
circuit.V("CE", "VCC", circuit.gnd, 10@u_V)  # Default value, will be swept
circuit.R("B", "VBB", "base", 10@u_kΩ)  # Base resistor
circuit.R("C", "collector", 'VCC', 1@u_kΩ)  # Collector resistor
circuit.R("E", "emitter", circuit.gnd, 1@u_kΩ)  # Emitter resistor
# 4. Set up the Nested Sweep Configuration
vcesw = [0,3,9]  # Collector-Emitter voltages in volts (V)

plt.figure(figsize=(10, 6))

# Loop through each Base Current (Outer Sweep)
for vce_val in vcesw:
    # Dynamically update the base current value in the netlist
    circuit["VCE"].dc_value = vce_val @ u_V

    # Set up simulator
    simulator = circuit.simulator(temperature=25)

    # Sweep V_CE from 0V to 5V in steps of 0.05V (Inner Sweep)
    analysis = simulator.dc(VBE=slice(0, 10, 0.01))

    # Extract data arrays
    v_be_axis = np.array(analysis.base - analysis.emitter)  # Swept voltage vector
    i_b_axis = -np.array(analysis.vbe) * 1000  # Convert Amperes to mA

    # Plot the curve for the current I_B step
    plt.plot(v_be_axis, i_b_axis, label=f"Vce = {vce_val} V")

# 5. Format and Show Plot
plt.title("BC547A BJT Output Characteristics ($I_B$ vs $V_{BE}$)")
plt.xlabel("Base-Emitter Voltage $V_{BE}$ (V)")
plt.ylabel("Base Current $I_B$ (mA)")
plt.grid(True)
plt.legend()
plt.show()
