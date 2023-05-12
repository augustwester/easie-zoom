class Coord:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __mul__(self, other):
        return Coord(self.x*other, self.y*other)
    
    def __add__(self, other):
        return Coord(self.x+other.x, self.y+other.y)
    
    def __sub__(self, other):
        return Coord(self.x-other.x, self.y-other.y)
    
    def __iter__(self):
        for i in (self.x, self.y):
            yield i
            
    def __repr__(self) -> str:
        return f"(x: {self.x}, y: {self.y})"

class ZoomEffect:
    def __init__(self, scale, start, duration, coord=Coord(0.5, 0.5)):
        self.scale = scale
        self.start = start
        self.duration = duration
        self.coord = coord
        self.start_frame = None,
        self.end_frame = None
    
    def progress(self, i):
        if i <= self.start_frame: return 0
        if i >= self.end_frame: return 1
        return (i - self.start_frame) / (self.end_frame - self.start_frame)

class Transition:
    def __init__(self, to: ZoomEffect, _from: ZoomEffect = None):
        self.to = to
        self._from = _from
        
    def ease_in_out(self, x, alpha=4):
        return (x**alpha) / (x**alpha + (1 - x)**alpha)
    
    def state(self, progress):
        p = self.ease_in_out(progress)
        
        if self._from is None:
            scale = 1 + (self.to.scale - 1) * p
            coord = self.to.coord
            return scale, coord
        
        diff_scale = self.to.scale - self._from.scale
        diff_coord = self.to.coord - self._from.coord
        scale = self._from.scale + diff_scale * p
        coord = self._from.coord + diff_coord * p
        #coord = self._from.coord * (1 - p) + self.to.coord * p
        return scale, coord