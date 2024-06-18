"""
Copyright 2024 James E Hume

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the “Software”), to deal in the Software without restriction, including without limitation the
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit
persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
from lt_shapes import LTPoint, LTRectangle, LTArc, LTLine, LTEllipse, LTPin
from minmax import MinMax


class LTComponent:
    def __init__(self, filename : str):
        self._lines = []
        self._pins  = []
        self._rectangles = []
        self._arcs = []
        self._ellipses = []
        self._windows = []
        self._pins_by_spice_order = {}
        self._minmax = MinMax()
        arc_index = 0
        state = "idle"

        with open(filename, "r", encoding="utf-8", errors="ignore") as fh:
            filecontents = fh.readlines()
            for line in filecontents:
                line = line.strip()

                while True:
                    if state == "idle":
                        if line.startswith("LINE "):
                            line = line.split()[1:]
                            if not self._represents_int(line[0]):
                                line = line[1:]
                            x1 = float(line[0])
                            y1 = float(line[1])
                            x2 = float(line[2])
                            y2 = float(line[3])
                            self._lines.append(
                                LTLine(
                                    LTPoint(x1, y1),
                                    LTPoint(x2, y2)
                                )
                            )

                        elif line.startswith("PIN "):
                            line = line.split()[1:]
                            x1 = float(line[0])
                            y1 = float(line[1])
                            state = "pin"

                        elif line.startswith("RECTANGLE "):
                            line = line.split()[1:]
                            if not self._represents_int(line[0]):
                                line = line[1:]
                            x1 = float(line[0])
                            y1 = float(line[1])
                            x2 = float(line[2])
                            y2 = float(line[3])
                            self._rectangles.append(LTRectangle(LTPoint(x1, y1), LTPoint(x2, y2)))

                        elif line.startswith("ARC "):
                            line = line.split()[1:]
                            if not self._represents_int(line[0]):
                                line = line[1:]

                            bbox_x1 = float(line[0])
                            bbox_y1 = float(line[1])
                            bbox_x2 = float(line[2])
                            bbox_y2 = float(line[3])
                            arc1x   = float(line[4])
                            arc1y   = float(line[5])
                            arc2x   = float(line[6])
                            arc2y   = float(line[7])
                            arc_index += 1

                            self._arcs.append((
                                    LTArc(
                                        LTPoint(bbox_x1, bbox_y1),
                                        LTPoint(bbox_x2, bbox_y2),
                                        LTPoint(arc1x, arc1y),
                                        LTPoint(arc2x, arc2y)
                                    ),
                                    arc_index))

                        elif line.startswith("CIRCLE "):
                            line = line.split()[1:]
                            if not self._represents_int(line[0]):
                                line = line[1:]
                            x1 = float(line[0])
                            y1 = float(line[1])
                            x2 = float(line[2])
                            y2 = float(line[3])
                            cx = min(x1, x2) + abs(x1 - x2)/2
                            cy = min(y1, y2) + abs(y1 - y2)/2
                            w = abs(x1 - x2)
                            h = abs(y1 - y2)
                            self._ellipses.append(LTEllipse(LTPoint(cx, cy), w, h))
                        
                        elif line.startswith("WINDOW "):
                            line = line.split()[1:]
                            a = float(line[0])
                            b = float(line[1])
                            c = float(line[2])
                            d = line[3]
                            e = float(line[4])
                            self._windows.append((a,b,c,d,e))
                            
                    elif state == "pin":
                        if line.startswith("PINATTR "):
                            line = line.split()[1:]
                            if line[0] == "PinName":
                                pin_name = line[1]
                            elif line[0] == "SpiceOrder":
                                self._pins.append(LTPin(LTPoint(x1, y1), pin_name, int(line[1]), self))
                                state = "idle"
                        else:
                            # This line is not to do with a pin, so go round the loop again to reparse it
                            # from the idle state
                            state = "idle" 
                            continue


                    break # Always break by default.
        
        for pin in self._pins:
            self._pins_by_spice_order[pin.spice_order] = pin

        for line in self._lines:
            self._minmax.add(line.p1)
            self._minmax.add(line.p2)

        for rect in self._rectangles:
            self._minmax.add(rect.topleft)
            self._minmax.add(rect.bottomright)

        for ellipse in self._ellipses:
            self._minmax.add(LTPoint(ellipse.xy.x - ellipse.w / 2, ellipse.xy.y - ellipse.h / 2))
            self._minmax.add(LTPoint(ellipse.xy.x + ellipse.w / 2, ellipse.xy.y + ellipse.h / 2))

        for arc, arc_index in self._arcs:
            tight_bbox = arc.tight_bbox
            self._minmax.add(tight_bbox.topleft)
            self._minmax.add(tight_bbox.bottomright)

    ## TODO: THIS MODIFIES THE OBJECT BUT ALL OTHER LT SHAPE METHODS LIKE THIS CREATE A NEW OBJECT. THIS SHOULD
    ##       REALLY DO THAT TOO
    def rotate(self, rotation_degrees : float):
        for idx, line in enumerate(self._lines):
            self._lines[idx] = line.rotate(rotation_degrees)

        for idx, rect in enumerate(self._rectangles):
            self._rectangles[idx] = rect.rotate(rotation_degrees)

        for idx, ellipse in enumerate(self._ellipses):
            self._ellipses[idx] = ellipse.rotate(rotation_degrees)

        for idx, pin in enumerate(self._pins):
            self._pins[idx] = pin.rotate(rotation_degrees)
        
        for idx, (arc, arc_index) in enumerate(self._arcs):
            self._arcs[idx] = (arc.rotate(rotation_degrees), arc_index)

        # Update the map as it will be holding the old non-rotated pins
        for pin in self._pins:
            self._pins_by_spice_order[pin.spice_order] = pin
        
        rect_minmax = LTRectangle(self._minmax.min, self._minmax.max).rotate(rotation_degrees)
        self._minmax = MinMax()
        self._minmax.add(rect_minmax.topleft)
        self._minmax.add(rect_minmax.bottomright)
    
    ## TODO: THIS MODIFIES THE OBJECT BUT ALL OTHER LT SHAPE METHODS LIKE THIS CREATE A NEW OBJECT. THIS SHOULD
    ##       REALLY DO THAT TOO
    def translate(self, point : LTPoint):
        for idx, line in enumerate(self._lines):
            self._lines[idx] = line.translate(point)

        for idx, rect in enumerate(self._rectangles):
            self._rectangles[idx] = rect.translate(point)

        for idx, ellipse in enumerate(self._ellipses):
            self._ellipses[idx] = ellipse.translate(point)

        for idx, pin in enumerate(self._pins):
            self._pins[idx] = pin.translate(point)

        for idx, (arc, arc_index) in enumerate(self._arcs):
            self._arcs[idx] = (arc.translate(point), arc_index)

        # Update the map as it will be holding the old non-translated pins
        for pin in self._pins:
            self._pins_by_spice_order[pin.spice_order] = pin

        rect_minmax = LTRectangle(self._minmax.min, self._minmax.max).translate(point)
        self._minmax = MinMax()
        self._minmax.add(rect_minmax.topleft)
        self._minmax.add(rect_minmax.bottomright)

    def get_pin_by_spice_order(self, order):
        return self._pins_by_spice_order[order]

    @staticmethod
    def _represents_int(s):
        try: 
            int(s)
        except ValueError:
            return False
        else:
            return True

    @property
    def lines(self):
          return self._lines

    @property 
    def rectangles(self):
        return self._rectangles    

    @property
    def pins(self):
        return self._pins

    @property
    def arcs(self):
        return self._arcs
    
    @property
    def ellipses(self):
        return self._ellipses
    
    @property
    def flags(self):
        return self._flags

    @property
    def minmax(self):
        return self._minmax
