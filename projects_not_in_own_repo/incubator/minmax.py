from lt_shapes import LTPoint

class MinMax:
    def __init__(self):
        self.min : Optional[LTPoint] = None
        self.max : Optional[LTPoint] = None

    def __str__(self):
        return f"MinMax(min={self.min}, max={self.max})"
    
    def add(self, point : LTPoint):
        if self.min is None:      self.min = point.clone()
        if self.max is None:      self.max = point.clone()
        if self.min.x > point.x:  self.min.x = point.x
        if self.min.y > point.y:  self.min.y = point.y
        if self.max.x < point.x:  self.max.x = point.x
        if self.max.y < point.y:  self.max.y = point.y

    def merge(self, other_minmax):
        self.add(other_minmax.min)
        self.add(other_minmax.max)
