"""
A very simple script to convert basic SVG files to Umlet custom drawings.

I use umlet for almost all of my diagrams, but sometimes I want a graphic of sorts in there. For
example, a basic image of a mobile phone. What I wanted to be able to do was use something like
draw.io, export to SVG and convert the SVG, automatically into an Umlet custom drawing.

It turns out this is pretty easy to do, except for Umlet not, at the time of writing at least,
supporting Bezier curves. If one is careful, one can avoid to use of these and get draw.io to use
basic shapes and paths.

For example, here is a very basic mobile phone SVG fragment:
    <svg width="201px" height="386px" viewBox="-0.5 -0.5 201 386" #snipped content# >
        #snipped content#
        <g>
            <rect x="0" y="0" width="200" height="385" rx="30" ry="30" fill="rgb(255, 255, 255)" stroke="rgb(0, 0, 0)" pointer-events="all"/>
            <rect x="80" y="368" width="40" height="10" rx="1.5" ry="1.5" fill="rgb(255, 255, 255)" stroke="rgb(0, 0, 0)" pointer-events="all"/>
            <rect x="14" y="40" width="176" height="320" fill="rgb(255, 255, 255)" stroke="rgb(0, 0, 0)" pointer-events="all"/>
            <ellipse cx="170" cy="20" rx="10" ry="10" fill="rgb(255, 255, 255)" stroke="rgb(0, 0, 0)" pointer-events="all"/>
            <rect x="80" y="10" width="40" height="10" rx="1.5" ry="1.5" fill="rgb(255, 255, 255)" stroke="rgb(0, 0, 0)" pointer-events="all"/>
            <ellipse cx="128" cy="12" rx="5" ry="5" fill="rgb(255, 255, 255)" stroke="rgb(0, 0, 0)" pointer-events="all"/>
            <ellipse cx="141" cy="12" rx="5" ry="5" fill="rgb(255, 255, 255)" stroke="rgb(0, 0, 0)" pointer-events="all"/>
            <ellipse cx="69" cy="10" rx="5" ry="5" fill="rgb(255, 255, 255)" stroke="rgb(0, 0, 0)" pointer-events="all"/>
        </g>
    </svg>

The Umlet script commands are almost exactly the same as these XML "commands".

drawLine(x1,y1,x2,y2)
drawRectangle(x,y,width,height)
drawRectangleRound(x,y,width,height,radius)
drawCircle(x,y,radius)
drawEllipse(x,y,width,height)
drawArc(x,y,width,height,start,extent,open)
drawText(Text,x,y,horizontal alignment)

Would be nice if everything resized too.

Also process very simple paths like
    <path d="
    M 140 200
    L 140 140
    L 120 120
    M 140 140
    L 240 140"
"""


import sys
from bs4 import BeautifulSoup


def process_rect_element(el, svg_height, svg_width):
    if el.has_attr("rx") or el.has_attr("ry"):
        width_as_perc = f"width * {float(el['width']) / svg_width:.2f}"
        height_as_perc = f"height * {float(el['height']) / svg_height:.2f}"
        x_scaled = f"{el['x']} * (width / {svg_width})"
        y_scaled = f"{el['y']} * (height / {svg_height})"
        max_round = max(float(el['rx']), float(el['ry']))
        # cant get max of umlet height and width so just choose height :(
        round_scaled = f"{max_round} * (height / {svg_height})"
        print(f"drawRectangleRound({x_scaled},{y_scaled},{width_as_perc},{height_as_perc},{round_scaled})")
    else:
        width_as_perc = f"width * {float(el['width']) / svg_width:.2f}"
        height_as_perc = f"height * {float(el['height']) / svg_height:.2f}"
        x_scaled = f"{el['x']} * (width / {svg_width})"
        y_scaled = f"{el['y']} * (height / {svg_height})"
        print(f"drawRectangle({x_scaled},{y_scaled},{width_as_perc},{height_as_perc})")

def process_ellipse_element(el, svg_height, svg_width):
    x = float(el['cx']) - float(el['rx'])
    wx = float(el['rx']) * 2
    y = float(el['cy']) - float(el['ry'])
    wy = float(el['ry']) * 2

    x_scaled = f"{x} * (width / {svg_width})"
    y_scaled = f"{y} * (height / {svg_height})"
    width_as_perc = f"width * {wx / svg_width:.2f}"
    height_as_perc = f"height * {wy / svg_height:.2f}"

    print(f"drawEllipse({x_scaled},{y_scaled},{width_as_perc},{height_as_perc})")

def process_path_element(el, svg_height, svg_width):    
    """
        <path d="
    M 140 200
    L 140 140
    L 120 120
    M 140 140
    L 240 140"

    Good ref: https://css-tricks.com/svg-path-syntax-illustrated-guide/

    TODO might be able to approximate bezier curves using arcs: https://pomax.github.io/bezierinfo/#arcapproximation | https://github.com/domoszlai/bezier2biarc/blob/master/Algorithm.cs
    """
    path_tokens = el['d'].split(" ")

    home_set = False
    home_x = 0
    home_y = 0
    curr_x = 0
    curr_y = 0
    cursor = 0
    while cursor < len(path_tokens):
        if path_tokens[cursor] == "M":
            curr_x = float(path_tokens[cursor + 1])
            curr_y = float(path_tokens[cursor + 2])
            if not home_set:
                home_set = True
                home_x = curr_x
                home_y = curr_y
            cursor += 3
        elif path_tokens[cursor] == "L":
            if not home_set:
                home_set = True
                home_x = curr_x
                home_y = curr_y
            x1 = curr_x
            y1 = curr_y
            x2 = float(path_tokens[cursor + 1])
            y2 = float(path_tokens[cursor + 2])
            curr_x = x2
            curr_y = y2            
            cursor += 3
            x1_scaled = f"{x1} * (width / {svg_width})"
            y1_scaled = f"{y1} * (height / {svg_height})"
            x2_scaled = f"{x2} * (width / {svg_width})"
            y2_scaled = f"{y2} * (height / {svg_height})"
            print(f"drawLine({x1_scaled},{y1_scaled},{x2_scaled},{y2_scaled})")            
        elif path_tokens[cursor] == "Z":
            x1 = curr_x
            y1 = curr_y
            x2 = home_x
            y2 = home_y
            cursor += 1
            x1_scaled = f"{x1} * (width / {svg_width})"
            y1_scaled = f"{y1} * (height / {svg_height})"
            x2_scaled = f"{x2} * (width / {svg_width})"
            y2_scaled = f"{y2} * (height / {svg_height})"
            print(f"drawLine({x1_scaled},{y1_scaled},{x2_scaled},{y2_scaled})")            

        else:
            raise Exception(f"Unsupported path command '{path_tokens[cursor]}'")




    


node_handlers = {
    "rect" : process_rect_element,
    "ellipse": process_ellipse_element,
    "path": process_path_element,
}

def process_group(group, svg_height, svg_width):
    for child in group.children:
        if child.name is None:
            continue

        if child.name in node_handlers:
            node_handlers[child.name](child, svg_height, svg_width)
        else:
            raise Exception(f"Unhandled SVG child '{child.name}'")


soup = None
with open(sys.argv[1], "r") as svgFile:
    soup = BeautifulSoup(svgFile, "xml")

print("customelement=")
svg, = soup.find_all("svg")
for group in svg.find_all("g"):
    process_group(group, float(svg["height"][:-2]), float(svg["width"][:-2]))


