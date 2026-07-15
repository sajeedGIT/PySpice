import numpy as np
import matplotlib.pyplot as plt
import PySpice.Logging.Logging as Logging
logger = Logging.setup_logging()

####################################################################################################

from PySpice.Doc.ExampleTools import find_libraries
from PySpice.Probe.Plot import plot
from PySpice.Spice.Library import SpiceLibrary
from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *

circuit = Circuit('Transistor VI Characteristics')

# Define the BC547A NPN transistor model
circuit.model('BC547A', 'NPN',
              IS=1.8e-14, BF=400, NF=0.9955, ISE=1.03e-14, NE=1.3, IKF=0.05,
              VAF=80, BR=9.5, NR=0.9952, ISC=4.7e-11, NC=2, IKR=0.012,
              VAR=10, RB=280, RE=1, RC=40, CJC=6.0e-12, VJC=0.48, MJC=0.33,
              CJE=1.2e-11, VJE=0.48, MJE=0.5, TF=5.0e-10, TR=5.0E-8)

# Add the transistor to your circuit (Collector, Base, Emitter)
circuit.BJT(1, 'collector_node', 'base_node', 'emitter_node', model='BC547A')

circuit.V('cc', 'collector_node', circuit.gnd, 1@u_V)  # Supply voltage
circuit.R('B1', 'collector_node', 'base_node', 15@u_kΩ)  # Bias resistor  
circuit.R('B2', 'base_node', circuit.gnd, 4.7@u_kΩ)  # Bias resistor
circuit.R('E', 'emitter_node', circuit.gnd, 1@u_kΩ)  # Emitter resistor
circuit.R('C', 'Vcc', 'collector_node', 1@u_kΩ)  # Collector resistor
circuit.V('input', 'base_node', circuit.gnd, 0@u_V)  # Input voltage source

simulator = circuit.simulator(temperature=25, nominal_temperature=25)

# DC Sweep
analysis = simulator.dc(Vinput=slice(0, 1.0, 0.01))  # Sweep Vin from 0V to 1V in steps of 0.01V

# Voltage across transistor
vbe = np.array(analysis.base_node - analysis.emitter_node)  # Base-Emitter voltage
print(vbe)  # Print the base-emitter voltage values
# Current through voltage source
current = np.array(analysis.base_node)  # Current through the input voltage source
print(current)  # Print the current values
# Plot
plt.figure(figsize=(7, 5))  
plt.plot(vbe, current)  # Convert current to mA
plt.grid(True)
plt.xlabel("Base-Emitter Voltage (V)")
plt.ylabel("Base Current (mA)")
plt.title("BC547A Transistor I-V Characteristics")
plt.show()



