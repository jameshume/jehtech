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
