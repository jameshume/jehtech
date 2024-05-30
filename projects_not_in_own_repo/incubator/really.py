import matplotlib.pyplot as pl
import matplotlib.patches as mpatches

from plotasc import Component, matplotlib_plot_component
from shapes import LTPoint, LTLine

fig, ax = pl.subplots()
ax.invert_yaxis()

state = "normal"

flag_x, flag_y, flag_type = None, None, None

prev_line_cache = None

def parse_flag_line(line, draw=True):
    print(f"DRAW FLAG {line}")
    flag_x, flag_y, flag_type = line.strip().split(" ")[1:]
    flag_x, flag_y = (float(flag_x), float(flag_y))
    
    if flag_type == "0":
        if draw:
            circle1 = mpatches.Circle((flag_x, flag_y), 1, color='r')
            ax.add_patch(circle1)
            hw = 20
            h = 20
            ax.plot([flag_x - hw, flag_x + hw], [flag_y, flag_y], c='b')
            ax.plot([flag_x - hw, flag_x], [flag_y, flag_y + h], c='b')
            ax.plot([flag_x, flag_x + hw], [flag_y + h, flag_y], c='b')
    else:
        print(f"##### Flag type {flag_type} not supported")

    return flag_x, flag_y, flag_type

first_line = True

wires = []

#for line in open("/home/james/Draft4.asc"): #../../src/images/jeh-tech/electronics_lc_tank.asc"):
#for line in open("/home/james/Repos/jehtech/projects_not_in_own_repo/incubator/inductors.asc"):
#for line in open("/home/james/Repos/jehtech/projects_not_in_own_repo/incubator/one_rotated_inductor.asc"):
#for line in open("/home/james/Repos/jehtech/projects_not_in_own_repo/incubator/ne555s.asc"):
#for line in open("../../src/images/jeh-tech/electronics_nmos_depletion.asc"):
for line in open("../../src/images/jeh-tech/electronics_common_emitter_amplifier.asc"):
#for line in open("/home/james/Repos/jehtech/projects_not_in_own_repo/incubator/ground.asc"):
#for line in open("/home/james/Repos/jehtech/projects_not_in_own_repo/incubator/iopin.asc"):
    print(line.strip())
    
    if (prev_line_cache is not None):
        if line.startswith("IOPIN "):
            print("DRAW IOPIN")
            x, y, inout = line.strip().split(" ")[1:]
            x, y = float(x), float(y)
            h = 20
            warrow = 20
            wbody = 20
            if inout == "Out":
                ax.plot([x, x - warrow], [y, y - h], c='b')
                ax.plot([x, x - warrow], [y, y + h], c='b')
            elif inout == "In":
                ax.plot([x, x + warrow], [y, y - h], c='b')
                ax.plot([x, x + warrow], [y, y + h], c='b')
            else:
                print(f"##### IO pin type {inout} not supported")

            flag_x, flag_y, flag_text = parse_flag_line(prev_line_cache, draw=False)
            ax.annotate(flag_text, xy=(x,y))
        else:
            parse_flag_line(prev_line_cache)
        
        prev_line_cache = None

    first_line = False

    
    if line.startswith("WIRE "):
        x1, y1, x2, y2 = [float(x) for x in line.strip().split(" ")[1:]]
        wires.append(LTLine(LTPoint(x1, y1), LTPoint(x2, y2)))
        print(x1, y1, x2, y2)
        ax.plot([x1, x2], [y1, y2], color='blue')

        # The next thing to do is to figure out where lines are joined and plot some little squares
        # or circles to indicate this.

    # Seems like an IOPIN is always
    #   FLAG x y some-string
    #   IOPIN
    #
    # But ground is just
    #   FLAG x y 0
    # Followed by anything other than IOPIN
    elif line.startswith("FLAG "):
        prev_line_cache = line

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

if prev_line_cache is not None:
    prev_line_cache = None
    parse_flag_line(line)

print("LJLKJLKJLKJLKJLKJLKJLKJLKJLKJLKJ")
print(wires)


ax.set_xlim(-500, 500)
ax.set_ylim(-500, 500)
ax.spines[['left', 'bottom', 'right', 'top']].set_visible(False)
ax.set_xticks([]) 
ax.set_yticks([]) 
ax.invert_yaxis()
fig.show()
pl.show()