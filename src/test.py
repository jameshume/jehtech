import matplotlib.pyplot as pl
import numpy as np

pi2 = 2 * np.pi
sigFreqHz = 2
sampFreqHz = 2 * sigFreqHz

fig = pl.figure()
ax = fig.add_subplot(1,1,1)
ax.grid(True)

x = np.linspace(0, pi2, 1000)
y = np.sin(sigFreqHz * x)
ax.plot(x,y)

xticks = np.linspace(0., 10., 9) / 10.
ax.set_xticks( xticks * pi2)
pl.xticks(rotation=45)
ax.set_xticklabels([str(x) for x in xticks])

x2 = np.linspace(0, 2*np.pi, 8)
y2 = np.sin(sigFreqHz * x2)
for x,y in zip(x2,y2):
    ax.plot(x,y, marker='o', color='k')

print(0.5 * (x2[1] - x2[0]))


pl.show()