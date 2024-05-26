import matplotlib.pyplot as pl
import matplotlib.patches as mpatches

from plotasc import Component, matplotlib_plot_component

fig, ax = pl.subplots()
ax.invert_yaxis()

#for line in open("/home/james/Draft4.asc"): #../../src/images/jeh-tech/electronics_lc_tank.asc"):
#for line in open("/home/james/Repos/jehtech/projects_not_in_own_repo/incubator/inductors.asc"):
#for line in open("/home/james/Repos/jehtech/projects_not_in_own_repo/incubator/one_rotated_inductor.asc"):
#for line in open("/home/james/Repos/jehtech/projects_not_in_own_repo/incubator/ne555s.asc"):
#for line in open("../../src/images/jeh-tech/electronics_nmos_depletion.asc"):
#for line in open("../../src/images/jeh-tech/electronics_common_emitter_amplifier.asc"):
for line in open("/home/james/Repos/jehtech/projects_not_in_own_repo/incubator/ground.asc"):
    print(line.strip())
    if line.startswith("WIRE "):
        x1, y1, x2, y2 = [float(x) for x in line.strip().split(" ")[1:]]
        print(x1, y1, x2, y2)
        ax.plot([x1, x2], [y1, y2], color='blue')

    elif line.startswith("FLAG "):
        flag_x, flag_y, flag_type = [x for x in line.strip().split(" ")[1:]]
        flag_x, flag_y = (float(flag_x), float(flag_y))

        if flag_type == "0":
            circle1 = mpatches.Circle((flag_x, flag_y), 1, color='r')
            ax.add_patch(circle1)
            hw = 20
            h = 20
            ax.plot([flag_x - hw, flag_x + hw], [flag_y, flag_y], c='b')
            ax.plot([flag_x - hw, flag_x], [flag_y, flag_y + h], c='b')
            ax.plot([flag_x, flag_x + hw], [flag_y + h, flag_y], c='b')
        else:
            print(f"##### Flag type {flag_type} not supported")

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