import matplotlib.pyplot as pl
import matplotlib.patches as mpatches

from plotasc import Component, matplotlib_plot_component

fig, ax = pl.subplots()
ax.invert_yaxis()

for line in open("/home/james/Draft6.asc"): #../../src/images/jeh-tech/electronics_lc_tank.asc"):
    print(line.strip())
    if line.startswith("WIRE "):
        x1, y1, x2, y2 = [float(x) for x in line.strip().split(" ")[1:]]
        print(x1, y1, x2, y2)
        ax.plot([x1, x2], [y1, y2], color='blue')

    elif line.startswith("SYMBOL "):
         tokens = line.strip().split(" ")[1:]
         name = tokens[0]
         x = float(tokens[1])
         y = float(tokens[2])
         rotation = float(tokens[3][1:])

         name = name.replace("\\", "/")

         totalname = f"/home/james/.wine/drive_c/Program Files/LTC/LTspiceXVII/lib/sym/{name}.asy"
         print(totalname, rotation)
         matplotlib_plot_component(Component(totalname), ax, x, y, rotation)


ax.set_xlim(-500, 500)
ax.set_ylim(-500, 500)
#ax.spines[['left', 'bottom', 'right', 'top']].set_visible(False)
#ax.set_xticks([]) 
#ax.set_yticks([]) 
ax.invert_yaxis()
fig.show()
pl.show()