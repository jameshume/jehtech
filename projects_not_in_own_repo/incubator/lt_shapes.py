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
    def __init__(self, bbox1 : LTPoint, bbox2 : LTPoint, arc1 : LTPoint, arc2 : LTPoint):
        self._bbox = LTRectangle(bbox1, bbox2)
        self._arc1  = arc1
        self._arc2  = arc2


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

    @property
    def p1(self):
        return self._arc1

    @property
    def p2(self):
        return self._arc2

    @property
    def bbox(self):
        return self._bbox



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
    def __init__(self, p : LTPoint, name : str, component: "LTComponent"):
        self._p = p
        self._name = name
        self._component = component

    def rotate(self, degrees):
        return LTPin(self._p.rotate(degrees), self._name, self._component)

    def translate(self, xy):
        return LTPin(self.p.translate(xy), self._name, self._component)

    @property 
    def name(self):
        return self._name

    @property
    def p(self):
        return self._p

    @property
    def component(self):
        return self._component