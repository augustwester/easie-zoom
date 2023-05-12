from effect import ZoomEffect, Coord
from zoom import generate_frames

"""
effects = [ZoomEffect(scale=1.5, start=1, duration=0.3, coord=Coord(0.593, 0.5)),
           ZoomEffect(scale=1, start=9, duration=0.3, coord=Coord(0.5, 0.5)),
           ZoomEffect(scale=1.5, start=18, duration=0.3, coord=Coord(1, 1)),
           ZoomEffect(scale=1, start=21, duration=0.3, coord=Coord(0.5, 0.5))]
"""

effects = [ZoomEffect(scale=2.4, start=1, duration=0.3, coord=Coord(0.5, 0.55)),
           ZoomEffect(scale=2, start=6, duration=0.3, coord=Coord(0.5, 0.18)),
           ZoomEffect(scale=1, start=8, duration=0.3, coord=Coord(0.5, 0.5))] 

generate_frames("sidekick-demo.mov", effects)
#frames = generate_frames("sidekick-demo.mov", effects)
#frames_to_video(frames, "zoomed-demo.mov")