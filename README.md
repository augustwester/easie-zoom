# easie-zoom

Add some polish to your screen recording's zoom effects using easing functions! To the best of my knowledge, no free video editors support this functionality[^1]. Hence this little script.

* Is this script fast? **No.**
* Does it work? **Maybe.**
* Is it easy to use? **Very, if you know Python.**
* Are you completely insane for being so pedantic about timing functions? **Probably.**

Below is an example of a screen recording I made of my app, [Sidekick](https://sidekiiick.com). Notice the zoom effects? They look nice because of this code.

https://github.com/augustwester/easie-zoom/assets/747600/86db79a0-e4dc-4439-9289-f5daa2c56ee5

The video was made using the code in `demo.py`. More specifically:

```python
from effect import ZoomEffect
from timing_functions import ease_in_out
from zoom import generate_frames, frames_to_video

# we will use this as the timing function for all zoom effects
timing_fn = ease_in_out(alpha=4)

# specify the zooms we want
effects = [ZoomEffect(scale=2.4, start=1, duration=0.5, coord=(0.5, 0.55), timing_fn=timing_fn),
           ZoomEffect(scale=2.4, start=6.2, duration=0.5, coord=(0.5, 0.18), timing_fn=timing_fn),
           ZoomEffect(scale=1, start=8, duration=0.5, coord=(0.5, 0.5), timing_fn=timing_fn)]

# produce the frames of the "fancy" video. this is just a numpy array.
frames, fps = generate_frames("sidekick-demo.mov", effects)

# convert the numpy array to a video file
frames_to_video(frames, fps, "out.mp4")
```

Some transitions can look at bit "off" when there's too much zooming and panning going on at the same time. You can see that in the "zoom out" effect in the video above. Not sure how to solve this, but you're welcome to submit a pull request if you have a fix.

[^1]: Do not get me started about OpenShot...
