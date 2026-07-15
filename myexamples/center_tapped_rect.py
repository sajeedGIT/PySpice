import matplotlib.pyplot as plt
import numpy as np
from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *



# 1. Initialize Circuit
circuit = Circuit("Center-Tapped Full-Wave Rectifier")

# 2. Add Diode Models (Standard 1N4148)
circuit.include("1N4007.lib")  # Ensure you have the diode model file in the same directory or provide the correct path

# 3. Primary Side (AC Input Source & Primary Inductor)
# 230V RMS @ 50Hz -> Peak voltage = 230 * sqrt(2) ≈ 325V
circuit.AcLine("input", "in_pos", "in_neg", rms_voltage=230@u_V, frequency=50@u_Hz)
circuit.L(1, "in_pos", "in_neg", 1@u_H)
circuit.L(2, "sec_top", "center_tap", 40@u_mH)
circuit.L(3, "center_tap", "sec_bot", 40@u_mH)
circuit.CoupledInductor('K1', 'L1', 'L2', 0.999)
circuit.CoupledInductor('K2', 'L1', 'L3', 0.999)
circuit.CoupledInductor('K3', 'L2', 'L3', 0.999)
# 6. Rectifier Diodes and Load Resistor
circuit.D(1, "sec_top", "out", model="1N4007")
circuit.D(2, "sec_bot", "out", model="1N4007")
circuit.R("load", "center_tap", "out", 1@u_kΩ)
circuit.R("load_ground", "center_tap", circuit.gnd, 1@u_mΩ)  # Load resistor to ground
# 7. Run Transient Simulation
simulator = circuit.simulator(temperature=25, nominal_temperature=25)
analysis = simulator.transient(step_time=100@u_us, end_time=100@u_ms)

# 8. Plot the Results
#plt.figure(figsize=(10, 6))
#plt.plot(analysis.time * 1000, analysis.vinput, label="Input Voltage (Primary)", color="gray", linestyle="--")
#plt.plot(analysis.time * 1000, analysis["sec_top"], label="Secondary Top (Node V_sec_top)", color="blue")
#plt.plot(analysis.time * 1000, analysis["sec_bot"], label="Secondary Bottom (Node V_sec_bot)", color="orange")
#plt.plot(analysis.time * 1000, analysis["center_tap"], label="Rectified Output (V_out)", color="red", linewidth=2)

#plt.title("Center-Tapped Full-Wave Rectifier Simulation")
#plt.xlabel("Time (ms)")
#plt.ylabel("Voltage (V)")
#plt.grid(True)
#plt.legend()
#plt.show()
