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

-----------------------------------------------------------------------------------------------------------------------

The LTSpice canvas axis are like this:
  (0,0)
    ┌───► x
    │
    ▼  
    y  

Ie., y-axis is like a screen not a graph
"""

import math

#######################################################################################################################
class LTPoint:
    def __init__(self, x, y):
        self._x = float(x)
        self._y = float(y)

    def __add__(self, point):
        return LTPoint(self._x + point._x, self._y + point._y)

    def __sub__(self, point):
        return LTPoint(self._x - point._x, self._y - point._y)

    def __truediv__(self, scale):
        return  LTPoint(self._x / float(scale), self._y / float(scale))

    def __mul__(self, scale):
        return  LTPoint(self._x * float(scale), self._y * float(scale))

    def __neg__(self):
        return LTPoint(-self._x, -self._y)

    def __str__(self):
        return f"LTPoint({self._x}, {self._y})"
    
    def __repr__(self):
        return self.__str__()
    
    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False
        return self._x == other._x and self._y == other._y
    
    def __hash__(self):
        # If hash(a) == hash(b), then a might equal b
        # If a == b then hash(a) == hash(b)
        # If hash(a) != hash(b), then a != b
        # Urg this is a bit poo!
        return hash(self._x  + self._y)

    def clone(self):
        return LTPoint(self._x, self._y)

    def abs(self):
        return LTPoint(math.fabs(self._x), math.fabs(self._y))

    def translate(self, xy):
        return self + xy

    def rotate(self, degrees):
        rads = (math.pi / 180.0) * float(degrees)
        return LTPoint(
            (self._x * math.cos(rads)) - (self._y * math.sin(rads)),
            (self._y * math.cos(rads)) + (self._x * math.sin(rads))
        )

    def as_tuple(self):
        return (self._x, self._y)

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = float(value)
    
    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = float(value)



#######################################################################################################################
class LTLine:
    def __init__(self, p1 : LTPoint, p2: LTPoint):
        self._p1 = p1
        self._p2 = p2

    def __str__(self):
        return f"LTLine({self._p1}, {self._p2})"
    
    def __repr__(self):
        return self.__str__()

    def translate(self, xy):
        return LTLine(self._p1.translate(xy), self._p2.translate(xy))

    def rotate(self, degrees):
        rads = (math.pi / 180.0) * float(degrees)
        return LTLine(self._p1.rotate(degrees), self._p2.rotate(degrees))

    @property
    def p1(self):
        return self._p1

    @property
    def p2(self):
        return self._p2



#######################################################################################################################
class LTRectangle:
    """
    ┌───► x
    │
    ▼    Type 1         Type 2         Type 3         Type 4
    y   1┌───┐          ┌───┐1        2┌───┐          ┌───┐2
         |   |          |   |          |   |          |   | 
         └───┘2        2└───┘          └───┘1        1└───┘

         x2 >= x1       x1 >= x2       x1 >= x2       x2 >= x1
         y2 >= y1       y2 >= y1       y1 >= y2       y1 >= y2
         w = x2-x1      w = x1-x2      w = x1-x2      w = x2-x1
         h = y2-y1      h = y2-y1      h = y1-y2      h = y1-y2 
    
    LTSpice will let the first and second point of the rectange vary depending on
    how it was drawn, as shown above.

    This Rectangle object will convert the LTSpice representation into:
        1┌───┐    
         |   |    
         └───┘2   
         
         x2 > x1  
         y2 > x2  
         w = x2-x1
         h = y2-y1
    """
    def __init__(self : "LTRectangle", p1 : LTPoint, p2 : LTPoint):
        if p2.x >= p1.x and p2.y >= p1.y:
            self._topleft     = p1
            self._bottomright = p2
        elif p1.x >= p2.x and p2.y >= p1.y:
            self._topleft     = LTPoint(p2.x, p1.y)
            self._bottomright = LTPoint(p1.x, p2.y)
        elif p1.x >= p2.x and p1.y >= p2.y:
            self._topleft     = p2
            self._bottomright = p1
        elif p2.x >= p1.x and p1.y >= p2.y:
            self._topleft     = LTPoint(p1.x, p2.y)
            self._bottomright = LTPoint(p2.x, p1.y)
        else:
            raise RuntimeError("Logic error.")

    def clone(self):
        return LTRectangle(self._topleft.clone(), self._bottomright.clone())

    def __str__(self):
        return f"LTRectangle({self._topleft}, {self._bottomright}) [w={self.dimensions._x}, h={self.dimensions._y}]"
    
    def rotate(self, degrees):
        return LTRectangle(self._topleft.rotate(degrees), self._bottomright.rotate(degrees))

    def translate(self, xy):
        return LTRectangle(self._topleft.translate(xy), self._bottomright.translate(xy))

    @property
    def topleft(self):
        return self._topleft


    @property
    def bottomright(self):
        return self._bottomright

    @property
    def dimensions(self):
        return self._bottomright - self._topleft
    
    @property
    def center(self):
        return self._topleft + self.dimensions / 2
    

#######################################################################################################################
class LTArc:
    """
    From the designer.
    When bbox is 
        ┌───► x    
        │
        ▼   1┌───┐  
        y    |   |  
             └───┘2 
    Arc draws in an anti clockwise direction. So a long arc has p1 at a larger rotation than p2. Opposite for a short arc.

    Arc in first quadrant (o = line drawn, . = no line):
        
            o  1                                              .  2
         o        .                                        .        o
        o          2                                      .          1
        o          o                                      .          .
         o        o                                        .        .
            o  o                                              .  .
        
        Theta(p1) > Theta(p2). Arc is always              Theta(p1) < Theta(p2). Arc is always
        drawn anti-clockwise, so a long arc               drawn anti-clockwise, so a short arc
        is drawn.                                         is drawn.

        
    Arc in second quadrant (o = line drawn, . = no line):
                                                            
            2  o                                              2  .
         .        o                                        o        .
        1          o                                      1          .
        o          o                                      .          .
         o        o                                        .        .
            o  o                                              .  .
        Theta(p1) > Theta(p2). Arc is always              Theta(p1) < Theta(p2). Arc is always
        drawn anti-clockwise, so a long arc               drawn anti-clockwise, so a short arc
        is drawn.                                         is drawn.

    And so on for all other quadrants...

    Another interesting facet is that the points p1, p2 need not be at the exact point of the
    arc start or finish, but can be anywhere on the line from the center to the point. This
    becomes important when trying to figure out the the bounding box of the arc *segment*
    (not the bounding box of the ellipse that defined the arc, just the visible part of the
    ellipse that is the arc).
    """
    def __init__(self, bbox1 : LTPoint, bbox2 : LTPoint, arc1 : LTPoint, arc2 : LTPoint, _calculate_tight_bbox=True):
        self._bbox = LTRectangle(bbox1, bbox2)
        self._arc1  = arc1
        self._arc2  = arc2
        # This is necessary to allow us to avoid infinite recursion in the calculate tight bbox method!
        if _calculate_tight_bbox:
            self._calculate_tight_arc_bounding_box()
        else:
            self._t1_degs = None
            self._t2_degs = None
            self._tight_bbox = None

    def __str__(self):
        return f"LTArc(bb={self._bbox}, p1={self._arc1}, p2={self._arc2})"

    def translate(self, xy):
        translated_bbox = self._bbox.translate(xy)
        return LTArc(translated_bbox._topleft, translated_bbox._bottomright, self._arc1.translate(xy), self._arc2.translate(xy))
    
    def rotate(self, degrees):
        rot_bbox = self._bbox.rotate(degrees)
        return LTArc(rot_bbox.topleft, rot_bbox.bottomright, self._arc1.rotate(degrees), self._arc2.rotate(degrees))
    
    def clone(self):
        return LTArc(self.bbox.topleft.clone(), self.bbox.bottomright.clone(), self._arc1.clone(), self._arc2.clone())

    @staticmethod
    def _radians_to_degrees(radians):
        return radians * 180 / math.pi

    @staticmethod
    def _get_quadrant_1_to_4(degrees):
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
    def _rotate_quadrants(quad):
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
        

    def _calculate_tight_arc_bounding_box(self, debug=False):
        # Cannot call translate() direcly as will result in infinite recursion - hence use of _calculate_tight_bbox param
        arc_centered_at_origin = LTArc(self.bbox.topleft.clone(), self.bbox.bottomright.clone(), self._arc1.clone(), self._arc2.clone(), _calculate_tight_bbox=False) 
        arc_centered_at_origin._bbox = arc_centered_at_origin._bbox.translate(-self._bbox.center)
        arc_centered_at_origin._arc1 = self._arc1.translate(-self._bbox.center)
        arc_centered_at_origin._arc2 = self._arc2.translate(-self._bbox.center)

        # LTSpice coordinates are like a screen, but atan2 expects them to be like a graph. This means when looking at
        # an LTSpice arc, what I think of as the 1st quadrant is really the 4th, what I think of as the 2nd is the
        # 3rd, what I think of as the 3rd is the 2nd and what I think of a the 4th is the 1st. Which is just the mirror
        # in the y-axis because LTSpice coordinates are screen coordinates and atan is graph coordinates.
        #
        # If I give atan the screen coordinates they are the wrong way around because everything is flipped about the
        # yaxis so swap em! 
        t1_rads = math.atan2(arc_centered_at_origin.p2.y, arc_centered_at_origin.p2.x)
        t2_rads = math.atan2(arc_centered_at_origin.p1.y, arc_centered_at_origin.p1.x)

        t1_degs = self._radians_to_degrees(t1_rads)
        t2_degs = self._radians_to_degrees(t2_rads)

        if t1_degs < 0 : t1_degs += 360.0
        if t2_degs < 0 : t2_degs += 360.0

        arc_radii = self._bbox.dimensions / 2
        
        # Another interesting facet is that the points p1, p2 need not be at the exact point of the arc start or finish,
        # but can be anywhere on the line from the center to the point. Thus, calculate the "real" points...
        # Because t1 and t2 are swapped above, swap them back for get the right point index
        arc_real_p2 = LTPoint(arc_radii.x * math.cos(t1_rads), arc_radii.y * math.sin(t1_rads)).translate(self._bbox.center)
        arc_real_p1 = LTPoint(arc_radii.x * math.cos(t2_rads), arc_radii.y * math.sin(t2_rads)).translate(self._bbox.center)

        t2_quad = self._rotate_quadrants(self._get_quadrant_1_to_4(t1_degs))
        t1_quad = self._rotate_quadrants(self._get_quadrant_1_to_4(t2_degs))
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

        tight_bbox = self._bbox.clone()
    
        if 1 in quads and 2 in quads:
            tight_bbox.topleft.y = self._bbox.topleft.y
        else:
            tight_bbox.topleft.y = min(arc_real_p1.y, arc_real_p2.y)
        
        if 2 in quads and 3 in quads:
            tight_bbox.topleft.x = self._bbox.topleft.x
        else:
            tight_bbox.topleft.x = min(arc_real_p1.x, arc_real_p2.x)
        
        if 3 in quads and 4 in quads:
            tight_bbox.bottomright.y = self._bbox.bottomright.y
        else:
            tight_bbox.bottomright.y = max(arc_real_p1.y, arc_real_p2.y)
        
        if 4 in quads and 1 in quads:        
            tight_bbox.bottomright.x = self._bbox.bottomright.x
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
        
        self._t1_degs = t1_degs
        self._t2_degs = t2_degs
        self._tight_bbox = tight_bbox

    @property
    def p1(self):
        return self._arc1

    @property
    def p2(self):
        return self._arc2

    @property
    def bbox(self):
        return self._bbox

    @property
    def tight_bbox(self):
        return self._tight_bbox 

    @property
    def t1_degs(self):
        self._t1_degs

    @property
    def t2_degs(self):
        self._t2_degs



#######################################################################################################################
class LTEllipse:
    def __init__(self, xy_center : LTPoint, w, h):
        self._xy_center = xy_center
        self._h = h
        self._w = w
    
    def translate(self, xy):
        return LTEllipse(self._xy_center.translate(xy), self._w, self._h)
    
    def rotate(self, degrees):
        # Aaar this doesn't work for anything other than 90,180 turns, which luckily is all LTSpice does....
        if degrees in [0, 180, 360]:
            w = self._w
            h = self._h
        elif degrees in [90, 270]:
            w = self._h
            h = self._w
        else:
            print("*" * 80)
            print(degrees)
            assert(False)

        return LTEllipse(self._xy_center.rotate(degrees), w, h)

    @property 
    def xy(self):
        return self._xy_center
    
    @property 
    def h(self):
        return self._h

    @property 
    def w(self):
        return self._w
    

#######################################################################################################################
class LTPin:
    def __init__(self, p : LTPoint, name : str, spice_order : int, component: "LTComponent"):
        self._p = p
        self._name = name
        self._spice_order = spice_order
        self._component = component

    def __str__(self):
        return f"LTPin({self._p}, {self._name}, {self._spice_order}, {hex(id(self._component))})"
    
    def __repr(self):
        return self.__str__()

    def rotate(self, degrees):
        return LTPin(self._p.rotate(degrees), self._name, self._spice_order, self._component)

    def translate(self, xy):
        return LTPin(self.p.translate(xy), self._name, self._spice_order, self._component)

    @property 
    def name(self):
        return self._name

    @property
    def p(self):
        return self._p

    @property
    def spice_order(self):
        return self._spice_order

    @property
    def component(self):
        return self._component