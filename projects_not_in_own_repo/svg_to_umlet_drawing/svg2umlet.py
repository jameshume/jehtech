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
import re
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

def process_polyline_element(el, svg_height, svg_width):
    points_split = re.split(",|\s", el['points'])
    points = []
    
    i = 0
    while i < len(points_split):
        x = points_split[i]
        i += 1
        y = points_split[i]
        i += 1
        points.append((x, y))

    p1 = points[0]
    for point in points[1:]:
        x1, y1 = p1
        x2, y2 = point
        x1_scaled = f"{x1} * (width / {svg_width})"
        y1_scaled = f"{y1} * (height / {svg_height})"
        x2_scaled = f"{x2} * (width / {svg_width})"
        y2_scaled = f"{y2} * (height / {svg_height})"
        print(f"drawLine({x1_scaled},{y1_scaled},{x2_scaled},{y2_scaled})")    
        p1 = point




class CommandTokenizer:
    def __init__(self, path_str):
        self._path_str = path_str
        self._path_str_len = len(path_str)
        self._cursor = 0


    def __eat_whitespace(self, check=False):
        while (self._cursor < self._path_str_len) and (self._path_str[self._cursor] == ' '):
            self._cursor += 1

        if check and (self._cursor >= self._path_str_len):
            raise Exception(f"Command {self._current_cmd} ended prematurely")

    def __eat_comma(self, check=False):
        if self._path_str[self._cursor] == ',':
            self._cursor +=1
        
        if check and (self._cursor >= self._path_str_len):
            raise Exception(f"Command {self._current_cmd} ended prematurely")

    def __get_params(self):
        params = []

        num_dots = 0
        next_minus = False

        while (self._cursor < self._path_str_len):
            self.__eat_whitespace(check=True)
            
            start = self._cursor            
            while (self._cursor < self._path_str_len) and (self._path_str[self._cursor] in '-0123456789.'):
                if self._path_str[self._cursor] == '.':
                    num_dots += 1
                if self._path_str[self._cursor] == '-' and self._cursor != start:
                    next_minus = True
                if num_dots > 1 or next_minus:
                    break
                self._cursor += 1
            end = self._cursor
            
            if (self._cursor >= self._path_str_len):
                raise Exception(f"Command {self._current_cmd} ended prematurely -- {params}")
            elif start == end:
                break
            elif num_dots > 1 or next_minus:
                # next param! see https://stackoverflow.com/q/51607857
                params.append(self._path_str[start:end])
                num_dots = 0
                next_minus = False
            elif self._path_str[self._cursor] == ',' or self._path_str[self._cursor] == ' ':
                params.append(self._path_str[start:end])
                num_dots = 0
                self._cursor += 1
            else:
                params.append(self._path_str[start:end])
                num_dots = 0
                break


        if len(params) == 0:
            raise Exception(f"Command {self._current_cmd} had no parameters!")

        return params

    def __iter__(self):
        self._cursor = 0
        return self


    def __next__(self):

        # Skip over any whitespaces
        self.__eat_whitespace(check=False)

        # If we've reached the end of the string stop the iterator
        if (self._cursor >= self._path_str_len):
            raise StopIteration
        
        # Cursor should now be on the next command character
        self._current_cmd = None
        if self._path_str[self._cursor] in "MmLlHhVvZzCcSsQqTtAa":
            self._current_cmd = self._path_str[self._cursor]
            self._cursor += 1
        else:
            raise Exception(f"Unsupported path command '{self._path_str[self._cursor]}' -- |{self._path_str[:self._cursor+1]} <<<<<|>>>>> {self._path_str[self._cursor+1:]}")

        # Now get all of the parameters for the command. Parameters can be split, it would seem,
        # by either or both of ' ' and ','. Only the "Z" parameter has no commands I think.
        if self._current_cmd == 'z' or self._current_cmd == 'Z':
            return (self._current_cmd, [])
        else:
            return (self._current_cmd, self.__get_params())



        

        





    

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

    Hmm.... looks like SVG path does not need to have spaces between all the characters which will make parsing harder. thankkfully
    the ones I've used so far use this syntax exactly.

    For example a valid path is 
        "M17.94,56.64a3.43,3.43,0,0,1,.82,2.43,3.49,3.49,0,0,1-1.12,2.37l-.1.08"

    """
    home_set = False
    home_x = 0
    home_y = 0
    curr_x = 0
    curr_y = 0
    # Worlds worst copy past code below.... yes, it is shit!
    for cmd, params in CommandTokenizer(el['d']):
        if cmd == "M": # Move to the absolute coordinates x,y
            curr_x = float(params[0])
            curr_y = float(params[1])
            if not home_set:
                home_set = True
                home_x = curr_x
                home_y = curr_y
        elif cmd == "L": # Draw a straight line to the absolute coordinates x,y
            if not home_set:
                home_set = True
                home_x = curr_x
                home_y = curr_y
            x1 = curr_x
            y1 = curr_y
            x2 = float(params[0])
            y2 = float(params[1])
            curr_x = x2
            curr_y = y2            
            x1_scaled = f"{x1} * (width / {svg_width})"
            y1_scaled = f"{y1} * (height / {svg_height})"
            x2_scaled = f"{x2} * (width / {svg_width})"
            y2_scaled = f"{y2} * (height / {svg_height})"
            print(f"drawLine({x1_scaled},{y1_scaled},{x2_scaled},{y2_scaled})")            
        elif cmd == "l": # Draw a straight line to a point that is relatively right x and down y (or left and up if negative values)
            if not home_set:
                home_set = True
                home_x = curr_x
                home_y = curr_y
            x1 = curr_x
            y1 = curr_y
            x2 = x1 + float(params[0])
            y2 = y1 + float(params[1])
            curr_x = x2
            curr_y = y2            
            x1_scaled = f"{x1} * (width / {svg_width})"
            y1_scaled = f"{y1} * (height / {svg_height})"
            x2_scaled = f"{x2} * (width / {svg_width})"
            y2_scaled = f"{y2} * (height / {svg_height})"
            print(f"drawLine({x1_scaled},{y1_scaled},{x2_scaled},{y2_scaled})")    
            
        elif cmd == "Z" or cmd =="z":
            x1 = curr_x
            y1 = curr_y
            x2 = home_x
            y2 = home_y
            x1_scaled = f"{x1} * (width / {svg_width})"
            y1_scaled = f"{y1} * (height / {svg_height})"
            x2_scaled = f"{x2} * (width / {svg_width})"
            y2_scaled = f"{y2} * (height / {svg_height})"
            print(f"drawLine({x1_scaled},{y1_scaled},{x2_scaled},{y2_scaled})")   
        else:
            print(f"// Ignoring unsupported path command '{cmd}'")

        ## TODO
        ## Not sure how to do arcs - SVG arcs have a rotation parameter that Umlet does not have.
        ## 
            




    


node_handlers = {
    "rect" : process_rect_element,
    "ellipse": process_ellipse_element,
    "path": process_path_element,
    "polyline": process_polyline_element,
}

def process_group(group, svg_height, svg_width):
    for child in group.children:
        if child.name is None:
            continue

        if child.name in node_handlers:
            node_handlers[child.name](child, svg_height, svg_width)
        elif child.name == "g":
            process_group(child, svg_height, svg_width)



soup = None
with open(sys.argv[1], "r") as svgFile:
    soup = BeautifulSoup(svgFile, "xml")

print("customelement=")
svg, = soup.find_all("svg")
process_group(svg, float(svg["height"][:-2]), float(svg["width"][:-2]))


