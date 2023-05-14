from effect import ZoomEffect
from timing_functions import ease_in_out
from zoom import generate_frames, frames_to_video

timing_fn = ease_in_out(alpha=4)
effects = [ZoomEffect(scale=2.4,
                      start=1,
                      duration=0.5,
                      coord=(0.5, 0.55),
                      timing_fn=timing_fn),
           ZoomEffect(scale=2.4,
                      start=6.2,
                      duration=0.5,
                      coord=(0.5, 0.18),
                      timing_fn=timing_fn),
           ZoomEffect(scale=1,
                      start=8,
                      duration=0.5,
                      coord=(0.5, 0.5),
                      timing_fn=timing_fn)]

frames, fps = generate_frames("sidekick-demo.mov", effects)
frames_to_video(frames, fps, "output.mp4")