import matplotlib.pyplot as pl
import matplotlib.patches as mpatches

from plotasc import Component, matplotlib_plot_component

fig, ax = pl.subplots()

for line in open("../../src/images/jeh-tech/electronics_lc_tank.asc"):
    print(line.strip())
    if line.startswith("WIRE "):
        x1, y1, x2, y2 = [float(x) for x in line.strip().split(" ")[1:]]
        print(x1, y1, x2, y2)
        ax.plot([x1, x2], [y1, y2], color='blue')

        ax.add_patch(mpatches.Circle((x1, y1), 1, color='r'))
        ax.add_patch(mpatches.Circle((x2, y2), 1, color='r'))

    elif line.startswith("SYMBOL "):
         tokens = line.strip().split(" ")[1:]
         name = tokens[0]
         x = float(tokens[1])
         y = float(tokens[2])
         rotation = float(tokens[3][1:])

         totalname = f"/home/james/.wine/drive_c/Program Files/LTC/LTspiceXVII/lib/sym/{name}.asy"
         matplotlib_plot_component(Component(totalname), ax, x, y, rotation)


        
fig.show()
pl.show()