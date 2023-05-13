from timing_functions import ease_in_out

class ZoomEffect:
    def __init__(self,
                 scale,
                 start,
                 duration,
                 coord=(0.5, 0.5),
                 timing_fn=ease_in_out(alpha=1)):
        self.scale = scale
        self.start = start
        self.duration = duration
        self.coord = Coord(*coord)
        self.start_frame = None,
        self.end_frame = None
        self.timing_fn = timing_fn
    
    def progress(self, i):
        if i <= self.start_frame: return 0
        if i >= self.end_frame: return 1
        return (i - self.start_frame) / (self.end_frame - self.start_frame)

class Transition:
    def __init__(self, to: ZoomEffect, _from: ZoomEffect = None):
        self.to = to
        self._from = _from
    
    def state(self, progress):
        p = self.to.timing_fn(progress)
        
        if self._from is None:
            scale = 1 + (self.to.scale - 1) * p
            coord = self.to.coord
            return scale, coord
        
        scale = self._from.scale * (1 - p) + self.to.scale * p
        coord = self._from.coord * (1 - p) + self.to.coord * p
        return scale, coord
    
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