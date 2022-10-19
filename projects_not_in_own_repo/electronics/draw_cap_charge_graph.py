import matplotlib.pyplot as pl
import numpy as np

C = 0.25
R = 10.0
RC = R * C
E = 5
I0 = E / R

t = np.arange(0, 15, 0.1)
ones = np.ones(t.shape)

v = (ones - np.exp(-t / RC)) * E
i = np.exp(-t / RC) * I0

fig, (ax1, ax2) = pl.subplots(nrows=2, sharex=True)
ax1.plot(t,v)
ax1.grid()
ax1.set_title("Voltage across a capacitor charging through a resistor")
ax1.set_xlabel("Time (s)")
ax1.set_ylabel("Voltage (v)")


ax2.set_title("Current for capacitor charging through a resistor")
ax2.set_xlabel("Time (s)")
ax2.set_ylabel("Current (amps)")
ax2.plot(t,i)
ax2.grid()

fig.tight_layout()


fig.show()
pl.show()