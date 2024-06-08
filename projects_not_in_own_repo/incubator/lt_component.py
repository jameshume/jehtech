from lt_shapes import LTPoint, LTRectangle, LTArc, LTLine, LTEllipse, LTPin

class LTComponent:
    def __init__(self, filename):
        self._lines = []
        self._pins  = []
        self._rectangles = []
        self._arcs = []
        self._ellipses = []
        self._windows = []
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
                                self._pins.append(LTPin(LTPoint(x1, y1), line[1]))
                                state = "idle"
                        else:
                            state = "idle"
                            continue


                    break # Always break by default.

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
