"""
A very simple script to convert basic SVG files to Umlet custom drawings.

I use Umlet for almost all of my diagrams, but sometimes I want a graphic of sorts in there. For
example, a basic image of a mobile phone. What I wanted to be able to do was use something like
draw.io, export to SVG and convert that SVG, automatically, into an Umlet custom drawing.

It turns out this is pretty easy to do, except for Umlet not, at the time of writing at least,
supporting Bezier curves. If one is careful, one can avoid to use of these and get draw.io to use
basic shapes and paths. Arcs also turned out to be another issue as SVG arcs can be rotated whereas
Umlet arcs do not support this.

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

A summary of the Umlet commands:
    drawLine(x1,y1,x2,y2)
    drawRectangle(x,y,width,height)
    drawRectangleRound(x,y,width,height,radius)
    drawCircle(x,y,radius)
    drawEllipse(x,y,width,height)
    drawArc(x,y,width,height,start,extent,open)
    drawText(Text,x,y,horizontal alignment)

Rather than use absolute SVG coordinates I wanted the images to scale, so everything is expressed
as a percentage of the width and height of the Umlet custom element. This means that the SVG must
include the total width and height as attributes in the <svg> tag. I have not implemented anything
that will parse the file to find the maximum and minimum coordinates and calculate height and width.

TODO: Annoyingly not all SVGs have the "width" and "height" attributes set in the <svg> element and
also coordinates can be negative. Would be good to be able to get the min/max xyu coordindates in
the file and then calculate the width and height from that, and also shift everything so there are
no negative coordinates.

"""
import sys
import re
from bs4 import BeautifulSoup

gblGetBounds = False

def __output_umlet_code(output_str):
    print(output_str)

def __scale_width_as_umlet_string(width, svg_width):
    return f"width * {(float(width) / float(svg_width)):.3f}"

def __scale_height_as_umlet_string(height, svg_height):
    return f"height * {(float(height) / float(svg_height)):.3f}"

output_umlet_code = __output_umlet_code
scale_width_as_umlet_string = __scale_width_as_umlet_string
scale_height_as_umlet_string = __scale_height_as_umlet_string




def scale_point_as_umlet_string(x, y, svg_width, svg_height):
    x1_scaled = scale_width_as_umlet_string(float(x), svg_width)
    y1_scaled = scale_height_as_umlet_string(float(y), svg_height)
    return (x1_scaled, y1_scaled)

def scale_point_pair_as_umlet_string(x1, y1, x2, y2, svg_width, svg_height):
    return (
        *scale_point_as_umlet_string(x1, y2, svg_width, svg_height),
        *scale_point_as_umlet_string(x2, y2, svg_width, svg_height)
    )

def process_rect_element(el, svg_height, svg_width):
    width_as_perc      = scale_width_as_umlet_string(el["width"], svg_width)
    height_as_perc     = scale_height_as_umlet_string(el["height"], svg_height)
    x_scaled, y_scaled = scale_point_as_umlet_string(el["x"], el["y"], svg_width, svg_height)

    if el.has_attr("rx") or el.has_attr("ry"):
        # Deal with rounded rectangles. Unfortunately Umlet used the same dimension for the round's
        # width and height and SVG does not so just pick height as we cannot do, in Umlet script,
        # "max(width, height)".
        max_round      = max(float(el['rx']), float(el['ry']))
        round_scaled   = scale_height_as_umlet_string(max_round, svg_height)
        output_umlet_code(f"drawRectangleRound({x_scaled}, {y_scaled}, {width_as_perc}, {height_as_perc}, {round_scaled})")
    else:
        output_umlet_code(f"drawRectangle({x_scaled}, {y_scaled}, {width_as_perc}, {height_as_perc})")


def process_ellipse_element(el, svg_height, svg_width):
    # Convert from the SVG way of specifying an ellipse to the umlet way...
    width_as_perc  = scale_width_as_umlet_string(float(el['rx']) * 2, svg_width)
    height_as_perc = scale_height_as_umlet_string(float(el['ry']) * 2, svg_height)
    x_scaled       = scale_width_as_umlet_string(float(el['cx']) - float(el['rx']), svg_width)
    y_scaled       = scale_height_as_umlet_string(float(el['cy']) - float(el['ry']), svg_height)
    output_umlet_code(f"drawEllipse({x_scaled}, {y_scaled}, {width_as_perc}, {height_as_perc})")



def process_polyline_element(el, svg_height, svg_width):
    points_split = re.split(",|\s", el['points'])
    points = [tup_xy for tup_xy in zip(points_split[::2], y[points_split::2])]
    
    p1 = points[0]
    for point in points[1:]:
        x1, y1 = p1
        x2, y2 = point
        x1_scaled, y1_scaled, x2_scaled, y2_scaled = (
            scale_point_pair_as_umlet_string(x1, y1, x2, y2, svg_width, svg_height))
        p1 = point
        output_umlet_code(f"drawLine({x1_scaled}, {y1_scaled}, {x2_scaled}, {y2_scaled})")    


class SVGPathCommandTokenizer:
    """
    Iterator which when given an SVG path string returns, per iteration, a command and all
    its parameters as a tuple (character, list-of-params-as-floats).

    Used the following good reference to understand what the commands meant:
        Good ref: https://css-tricks.com/svg-path-syntax-illustrated-guide/

    When I looked at draw.io SVG exports I thought the paths were nice and easy:
        <path d="M 140 200 L 140 140 L 120 120 M 140 140 L 240 140..." ...>

    But, looked at BoxySVG exports and found out a valid path is  also:
        "M17.94,56.64a3.43,3.43,0,0,1,.82,2.43,3.49,3.49,0,0,1-1.12,2.37l-.1.08"
    Which made the parsing much harder... hence this class. Had to look up how strings like
    "1-1" and ".1.08" were valid -- see https://stackoverflow.com/q/51607857.

    TODO might be able to approximate bezier curves using arcs:
        https://pomax.github.io/bezierinfo/#arcapproximation | https://github.com/domoszlai/bezier2biarc/blob/master/Algorithm.cs
    Or not... depends on whether this requires arcs to have a rotation parameter, which Umlet does
    not support.
    """

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
                params.append(float(self._path_str[start:end]))
                num_dots = 0
                next_minus = False
            elif self._path_str[self._cursor] == ',' or self._path_str[self._cursor] == ' ':
                params.append(float(self._path_str[start:end]))
                num_dots = 0
                self._cursor += 1
            else:
                params.append(float(self._path_str[start:end]))
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
    home_set = False
    home_x, home_y = 0.0, 0.0
    curr_x, curr_y = 0.0, 0.0

    def update_home():
        nonlocal home_set, home_x, home_y
        if not home_set:
            home_set = True
            home_x, home_y = curr_x, curr_y

    # Worlds worst copy past code below.... yes, it is shit!
    for cmd, params in SVGPathCommandTokenizer(el['d']):
        if cmd == "M":
            # Move to the absolute coordinates x,y
            curr_x, curr_y = params
            update_home()

        elif cmd == "L":
            # Draw a straight line to the absolute coordinates x,y
            x1, y1 = curr_x, curr_y
            x2, y2 = params
            curr_x, curr_y = x2, y2
            update_home()
            x1_scaled, y1_scaled, x2_scaled, y2_scaled = scale_point_pair_as_umlet_string(
                x1, y1, x2, y2, svg_width, svg_height)
            output_umlet_code(f"drawLine({x1_scaled}, {y1_scaled}, {x2_scaled}, {y2_scaled})")            

        elif cmd == "l":
            # Draw a straight line to a point that is relatively right x and down y (or left and up
            # if negative values)
            x1, y1 = curr_x, curr_y
            x2, y2 = x1 + float(params[0]), y1 + float(params[1])
            curr_x, curr_y = x2, y2            
            update_home()
            x1_scaled, y1_scaled, x2_scaled, y2_scaled = scale_point_pair_as_umlet_string(
                x1, y1, x2, y2, svg_width, svg_height)
            output_umlet_code(f"drawLine({x1_scaled}, {y1_scaled}, {x2_scaled}, {y2_scaled})")    

        elif cmd == "Z" or cmd =="z":
            # Draw a line back to the home coordinate
            x1_scaled, y1_scaled, x2_scaled, y2_scaled = scale_point_pair_as_umlet_string(
                curr_x, curr_y, home_x, home_y, svg_width, svg_height)
            output_umlet_code(f"drawLine({x1_scaled}, {y1_scaled}, {x2_scaled}, {y2_scaled})")   

        else:
            output_umlet_code(f"// Ignoring unsupported path command '{cmd}'")

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


if __name__ == "__main__":
    soup = None
    with open(sys.argv[1], "r") as svgFile:
        soup = BeautifulSoup(svgFile, "xml")

    output_umlet_code("customelement=")
    svg, = soup.find_all("svg")
    process_group(svg, float(svg["height"][:-2]), float(svg["width"][:-2]))
