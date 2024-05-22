"""
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
            print("TYPE 1")
            self._topleft     = p1
            self._bottomright = p2
        elif p1.x >= p2.x and p2.y >= p1.y:
            print("TYPE 2")
            self._topleft     = LTPoint(p2.x, p1.y)
            self._bottomright = LTPoint(p1.x, p2.y)
        elif p1.x >= p2.x and p1.y >= p2.y:
            print("TYPE 3")
            self._topleft     = p2
            self._bottomright = p1
        elif p2.x >= p1.x and p1.y >= p2.y:
            print("TYPE 4")
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

