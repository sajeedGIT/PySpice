import matplotlib.pyplot as plt


import PySpice.Logging.Logging as Logging
logger = Logging.setup_logging()


from PySpice.Probe.Plot import plot
from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *


from Transformer import Transformer

circuit = Circuit('Transformer')
circuit.include('1N4007.lib')  # Include the diode model library
ac_line = circuit.AcLine('input', 'input', circuit.gnd, rms_voltage=230@u_V, frequency=50@u_Hz)
circuit.subcircuit(Transformer(turn_ratio=10))
circuit.X('transformer', 'Transformer', 'input', circuit.gnd, 'output', circuit.gnd)
circuit.R('load', 'output', circuit.gnd, 1@u_kΩ)
simulator = circuit.simulator(temperature=25, nominal_temperature=25)
analysis = simulator.transient(step_time=ac_line.period/200, end_time=ac_line.period*3)

figure, ax = plt.subplots(figsize=(20, 10))
ax.plot(analysis.input)
ax.plot(analysis.output)
ax.legend(('Vin [V]', 'Vout [V]'), loc=(.8,.8))
ax.grid()
ax.set_xlabel('t [s]')
ax.set_ylabel('[V]')

plt.tight_layout()
plt.show()