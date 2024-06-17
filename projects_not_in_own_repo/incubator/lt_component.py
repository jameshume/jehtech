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
            tight_bbox = draw_ltspice_arc(ax, arc, arc_index, draw=False, debug=False)
            self._minmax.add(tight_bbox.topleft)
            self._minmax.add(tight_bbox.bottomright)

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
        
        rect_minmax = LTRectangle(self._minmax.min, self._minmax.max).rotate(rotation_degrees)
        self._minmax = MinMax()
        self._minmax.add(rect_minmax.topleft)
        self._minmax.add(rect_minmax.bottomright)
    
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

        rect_minmax = LTRectangle(self._minmax.min, self._minmax.max).translate(point)
        self._minmax = MinMax()
        self._minmax.add(rect_minmax.topleft)
        self._minmax.add(rect_minmax.bottomright)
    
    @staticmethod
    def radians_to_degrees(radians):
        return radians * 180 / math.pi

    @staticmethod
    def get_quadrant_1_to_4(degrees):
        if degrees >= 0:
            if degrees <= 90:
                return 1
            elif degrees <= 180:
                return 2
            elif degrees <= 270:
                return 3
            elif degrees <= 360:
                return 4
        else:
            if degrees <= -270:
                return 1
            elif degrees <= -180:
                return 2
            elif degrees <= -90:
                return 3
            else:
                return 4
            
        raise RuntimeError(f"get_quadrant_1_to_4({degrees}) not supported")

    @staticmethod
    def rotate_quadrants(quad):
        # LTSpice coordinates are like a screen, but atan2 expects them to be like a graph. This means when looking at
        # an LTSpice arc, what I think of as the 1st quadrant is really the 4th, what I think of as the 2nd is the
        # 3rd, what I think of as the 3rd is the 2nd and what I think of a the 4th is the 1st. 
        if quad == 1:
            return 4
        if quad == 2:
            return 3
        if quad == 3:
            return 2
        
        return 1
        

    def draw_ltspice_arc(arc : LTArc, idx, debug=True):
        if debug:
            print("\n\n\n\n\nPlotting ARC IDX", idx)
        
        arc_centered_at_origin = self.translate(-arc.bbox.center)

        # LTSpice coordinates are like a screen, but atan2 expects them to be like a graph. This means when looking at
        # an LTSpice arc, what I think of as the 1st quadrant is really the 4th, what I think of as the 2nd is the
        # 3rd, what I think of as the 3rd is the 2nd and what I think of a the 4th is the 1st. Which is just the mirror
        # in the y-axis because LTSpice coordinates are screen coordinates and atan is graph coordinates.
        #
        # If I give atan the screen coordinates they are the wrong way around because everything is flipped about the
        # yaxis so swap em! 
        t1_rads = math.atan2(arc_centered_at_origin.p2.y, arc_centered_at_origin.p2.x)
        t2_rads = math.atan2(arc_centered_at_origin.p1.y, arc_centered_at_origin.p1.x)

        t1_degs = radians_to_degrees(t1_rads)
        t2_degs = radians_to_degrees(t2_rads)

        if t1_degs < 0 : t1_degs += 360.0
        if t2_degs < 0 : t2_degs += 360.0

        arc_radii = arc.bbox.dimensions / 2
        
        # Another interesting facet is that the points p1, p2 need not be at the exact point of the arc start or finish,
        # but can be anywhere on the line from the center to the point. Thus, calculate the "real" points...
        # Because t1 and t2 are swapped above, swap them back for get the right point index
        arc_real_p2 = LTPoint(arc_radii.x * math.cos(t1_rads), arc_radii.y * math.sin(t1_rads)).translate(arc.bbox.center)
        arc_real_p1 = LTPoint(arc_radii.x * math.cos(t2_rads), arc_radii.y * math.sin(t2_rads)).translate(arc.bbox.center)

        t2_quad = rotate_quadrants(get_quadrant_1_to_4(t1_degs))
        t1_quad = rotate_quadrants(get_quadrant_1_to_4(t2_degs))
        if debug:
            print("QUAD1", t1_quad, "from", t1_degs)
            print("QUAD2", t2_quad, "from", t2_degs)

        if t1_degs < t2_degs:
            # The arc is going AC and is the short arc between the two points
            if debug:
                print("The arc is going AC and is the short arc between the two points")
            quads = sorted(list(range(t1_quad, t2_quad + 1)))

        else:
            # The arc is going AC and is the long arc between the two points
            if debug: 
                print("The arc is going AC and is the long arc between the two points")
            tmp = list(range(t1_quad, 5))
            tmp.extend(list(range(1, t2_quad + 1)))
            quads = sorted(tmp)

        if debug:
            print("QUADS", quads)

        tight_bbox = arc.bbox.clone()
    
        if 1 in quads and 2 in quads:
            tight_bbox.topleft.y = arc.bbox.topleft.y
        else:
            tight_bbox.topleft.y = min(arc_real_p1.y, arc_real_p2.y)
        
        if 2 in quads and 3 in quads:
            tight_bbox.topleft.x = arc.bbox.topleft.x
        else:
            tight_bbox.topleft.x = min(arc_real_p1.x, arc_real_p2.x)
        
        if 3 in quads and 4 in quads:
            tight_bbox.bottomright.y = arc.bbox.bottomright.y
        else:
            tight_bbox.bottomright.y = max(arc_real_p1.y, arc_real_p2.y)
        
        if 4 in quads and 1 in quads:        
            tight_bbox.bottomright.x = arc.bbox.bottomright.x
        else:
            tight_bbox.bottomright.x = max(arc_real_p1.x, arc_real_p2.x)

        if len(quads) == 4 and t1_quad != t2_quad:
            # The edge between the two points might be shrinkable
            quads = [t1_quad, t2_quad]
            if 1 in quads and 2 in quads:
                tight_bbox.topleft.y = min(arc_real_p1.y, arc_real_p2.y)
            if 2 in quads and 3 in quads:
                tight_bbox.topleft.x = min(arc_real_p1.x, arc_real_p2.x)
            if 3 in quads and 4 in quads:
                tight_bbox.bottomright.y = max(arc_real_p1.y, arc_real_p2.y)
            if 4 in quads and 1 in quads:
                tight_bbox.bottomright.x = max(arc_real_p1.x, arc_real_p2.x)

        if debug:
            print(f"tight_bbox={tight_bbox}")
        
        return tight_bbox


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
