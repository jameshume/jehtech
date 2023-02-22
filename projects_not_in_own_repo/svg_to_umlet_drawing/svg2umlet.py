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

TODO: Deal with the likes of `transform="rotate(-180,50,30)"` attributes for <path> elements would be handy. Could do
      the same for rectangles (would have to convert to paths)

      Todo this - can't do it with ellipses - Umlet doesn't support this
                - rectangles must become paths
                - paths will need two iterations - one the find the center and then one to draw rotated
                - lines easy enough
                - everything else not gonna be doing!
"""
import sys
import re
from bs4 import BeautifulSoup


class IUmletCodeEmitter:
    def output(self, line):
        pass


class UmletCodeStdoutEmitter(IUmletCodeEmitter):
    def output(self, line):
        print(line)


class NullCodeEmitter(IUmletCodeEmitter):
    def output(self, line):
        pass


class IScaleAsUmletString:
    def scale_width_to_umlet_string(self, width):
        pass

    def scale_height_to_umlet_string(self, height):
        pass

    def scale_point_to_umlet_string(self, x, y):
        pass


class ScaleAsUmletString(IScaleAsUmletString):
    def __init__(self, svg_shift_x, svg_shift_y, svg_height, svg_width):
        self._svg_shift_x = svg_shift_x
        self._svg_shift_y = svg_shift_y
        self._svg_height = svg_height
        self._svg_width = svg_width

    def scale_width_to_umlet_string(self, width):
        return f"width * {(float(width) / float(self._svg_width)):.3f}"

    def scale_height_to_umlet_string(self, height):
        return f"height * {(float(height) / float(self._svg_height)):.3f}"

    def scale_point_to_umlet_string(self, x, y):
        x1scaled = self.scale_width_to_umlet_string(float(x) + self._svg_shift_x)
        y1scaled = self.scale_height_to_umlet_string(float(y) + self._svg_shift_y)
        return (x1scaled, y1scaled)


class GetSvgBounds(IScaleAsUmletString):
    def __init__(self):
        self._minX = float(sys.maxsize)
        self._maxX = float(-sys.maxsize)
        self._minY = float(sys.maxsize)
        self._maxY = float(-sys.maxsize)

    def scale_width_to_umlet_string(self, width):
        return ""

    def scale_height_to_umlet_string(self, height):
        return ""

    def scale_point_to_umlet_string(self, x, y):
        x = float(x)
        y = float(y)
        if x < self._minX: self._minX = x
        if x > self._maxX: self._maxX = x
        if y < self._minY: self._minY = y
        if y > self._maxY: self._maxY = y
        return ("", "")

    def get_svg_width(self):
        return self._maxX - self._minX

    def get_svg_height(self):
        return self._maxY - self._minY

    def get_shift_x(self):
        return -self._minX

    def get_shift_y(self):
        return -self._minY

class ElementProcessor:
    def __init__(self, scaler=None, code_emitter=None):
        self._scaler = scaler
        self._code_emitter = code_emitter

    def set_scaler_strategy(self, scaler):
        self._scaler = scaler

    def set_code_emitter_strategy(self, code_emitter):
        self._code_emitter = code_emitter

    def process(self, el):
        pass

class ElementProcessors:
    def __init__(self, scaler=None, code_emitter=None):
        self._scaler = scaler
        self._code_emitter = code_emitter
        self._processor_map = {}

    def add_element_processor_class(self, element_name, processor_class):
        self._processor_map[element_name] = processor_class(self._scaler, self._code_emitter)

    def set_scaler_strategy(self, scaler):
        self._scaler = scaler
        for proc in self._processor_map.values():
            proc.set_scaler_strategy(scaler)

    def set_code_emitter_strategy(self, code_emitter):
        self._code_emitter = code_emitter
        for proc in self._processor_map.values():
            proc.set_code_emitter_strategy(code_emitter)

    def process(self, el):
        if el.name is not None:
            if el.name in self._processor_map:
                self._processor_map[el.name].process(el)
            else:
                self._code_emitter.output(f"// Ignoring unsupported node type '{el.name}'")


class RectangleElementProcessor(ElementProcessor):
    def __init__(self, *args):
        super().__init__(*args)

    def process(self, el):
        width_as_perc      = self._scaler.scale_width_to_umlet_string(el["width"])
        height_as_perc     = self._scaler.scale_height_to_umlet_string(el["height"])
        x_scaled, y_scaled = self._scaler.scale_point_to_umlet_string(el["x"], el["y"])

        ## KLUDGE - so that the ability to get image width/height works
        self._scaler.scale_point_to_umlet_string(float(el["x"]) + float(el["width"]), float(el["y"]) + float(el['height']))

        if el.has_attr("rx") or el.has_attr("ry"):
            # Deal with rounded rectangles. Unfortunately Umlet used the same dimension for the round's
            # width and height and SVG does not so just pick height as we cannot do, in Umlet script,
            # "max(width, height)".
            max_round      = max(float(el['rx']), float(el['ry']))
            round_scaled   = self._scaler.scale_height_to_umlet_string(max_round)
            self._code_emitter.output(
                "drawRectangleRound("
                   f"{x_scaled}, {y_scaled}, {width_as_perc}, {height_as_perc}, {round_scaled})"
            )
        else:
            self._code_emitter.output(
                f"drawRectangle({x_scaled}, {y_scaled}, {width_as_perc}, {height_as_perc})")        

class EllipseElementProcessor(ElementProcessor):
    def __init__(self, *args):
        super().__init__(*args)

    def process(self, el):
        # Convert from the SVG way of specifying an ellipse to the umlet way...
        width_as_perc      = self._scaler.scale_width_to_umlet_string(float(el['rx']) * 2.0)
        height_as_perc     = self._scaler.scale_height_to_umlet_string(float(el['ry']) * 2.0)
        x_scaled, y_scaled = self._scaler.scale_point_to_umlet_string(
            (float(el['cx']) - float(el['rx'])), (float(el['cy']) - float(el['ry']))
        )
        
        ## KLUDGE - so that the ability to get image width/height works
        self._scaler.scale_point_to_umlet_string((float(el['cx']) + float(el['rx'])), (float(el['cy']) + float(el['ry'])))

        self._code_emitter.output(
            f"drawEllipse({x_scaled}, {y_scaled}, {width_as_perc}, {height_as_perc})")


class PolylineElementProcessor(ElementProcessor):
    def __init__(self, *args):
        super().__init__(*args)

    def process(self, el):
        points_split = re.split(",|\s", el['points'])
        points = [tup_xy for tup_xy in zip(points_split[::2], points_split[1::2])]
        
        p1 = points[0]
        for point in points[1:]:
            x1, y1 = p1
            x2, y2 = point
            x1_scaled, y1_scaled = self._scaler.scale_point_to_umlet_string(x1, y1)
            x2_scaled, y2_scaled = self._scaler.scale_point_to_umlet_string(x2, y2)
            p1 = point
            self._code_emitter.output(
                f"drawLine({x1_scaled}, {y1_scaled}, {x2_scaled}, {y2_scaled})")    


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
                raise Exception(f"Command {self._current_cmd} ended prematurely -- {params} -- {self._cursor} -- {self._path_str}")
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


class PathElementProcessor(ElementProcessor):
    def __init__(self, *args):
        super().__init__(*args)
        self._home_set = False
        self._home_x, self._home_y = 0.0, 0.0
        self._curr_x, self._curr_y = 0.0, 0.0

    def __update_home(self):
        if not self._home_set:
            self._home_set = True
            self._home_x, self._home_y = self._curr_x, self._curr_y

    def process(self, el):
        ## TODO
        ## Not sure how to do arcs - SVG arcs have a rotation parameter that Umlet does not have.

        self._home_set = False
        self._home_x, self._home_y = 0.0, 0.0
        self._curr_x, self._curr_y = 0.0, 0.0

        for cmd, params in SVGPathCommandTokenizer(el['d']):
            if cmd == "M":
                # Move to the absolute coordinates x,y
                self._curr_x, self._curr_y = params
                self._code_emitter.output(f"// Path M: {params}")

            elif cmd == "L" or cmd == "l":
                # L => Draw a straight line to the absolute coordinates x,y
                # l => Draw a straight line to a point that is relatively right x and down y (or left and up
                #      if negative values)
                x1, y1 = self._curr_x, self._curr_y
                x2, y2 = params if cmd == "L" else [x1 + float(params[0]), y1 + float(params[1])]
                self._curr_x, self._curr_y = x2, y2
                x1_scaled, y1_scaled = self._scaler.scale_point_to_umlet_string(x1, y1)                
                x2_scaled, y2_scaled = self._scaler.scale_point_to_umlet_string(x2, y2)
                self._code_emitter.output(
                    f"drawLine({x1_scaled}, {y1_scaled}, {x2_scaled}, {y2_scaled}) "
                    f"// Path {cmd}: {[x1, y1]}->{params}"
                )

            elif cmd == "Z" or cmd == "z":
                # Draw a line back to the home coordinate
                x1_scaled, y1_scaled = self._scaler.scale_point_to_umlet_string(self._curr_x, self._curr_y)                
                x2_scaled, y2_scaled = self._scaler.scale_point_to_umlet_string(self._home_x, self._home_y)
                self._code_emitter.output(
                    f"drawLine({x1_scaled}, {y1_scaled}, {x2_scaled}, {y2_scaled}) "
                    f"// Path {cmd}: {[self._curr_x, self._curr_y]}->{[self._home_x, self._home_y]}"
                )
                self._curr_x, self._curr_y = self._home_x, self._home_y

            else:
                self._code_emitter.output(f"// Path Ignoring unsupported path command '{cmd}'")

            self.__update_home()
        



def process_group(group, element_processors):
    for child in group.children:
        if child.name == "g":
            process_group(child, element_processors)
        else:
            element_processors.process(child)


if __name__ == "__main__":
    element_processors = ElementProcessors()
    element_processors.add_element_processor_class("rect", RectangleElementProcessor)
    element_processors.add_element_processor_class("ellipse", EllipseElementProcessor)
    element_processors.add_element_processor_class("polyline", PolylineElementProcessor)
    element_processors.add_element_processor_class("path", PathElementProcessor)

    soup = None
    with open(sys.argv[1], "r") as svgFile:
        soup = BeautifulSoup(svgFile, "xml")

    # Rather than rely on the SVG width and height attributes, go through all the coordinates and
    # get the min and max.
    # Setup the function "pointers" to functions that will keep track of the min/max coords
    # (Note the slight kludge that I mix widths and heights with x and y's...)
    svg_bounds_scaler = GetSvgBounds()
    element_processors.set_scaler_strategy(svg_bounds_scaler)
    element_processors.set_code_emitter_strategy(NullCodeEmitter())
       
    # Iterate through all the elements
    svg, = soup.find_all("svg")
    process_group(svg, element_processors)

    # Now output the actual Umlet code based on the min/max measurements found above.
    element_processors.set_scaler_strategy(
        ScaleAsUmletString(
            svg_bounds_scaler.get_shift_x(),    svg_bounds_scaler.get_shift_y(),
            svg_bounds_scaler.get_svg_height(), svg_bounds_scaler.get_svg_width()
        )
    )
    emitter = UmletCodeStdoutEmitter()
    element_processors.set_code_emitter_strategy(emitter)
    
    emitter.output("customelement=")
    emitter.output(f"// Generated from {sys.argv[1]}")
    emitter.output(f"// Calculated {svg_bounds_scaler.get_svg_width()} x {svg_bounds_scaler.get_svg_height()}")
    emitter.output(f"// With shift ({svg_bounds_scaler.get_shift_x()}, {svg_bounds_scaler.get_shift_y()})")
    svg, = soup.find_all("svg")
    process_group(svg, element_processors)
