import cv2
import numpy as np

def zoom_at(img, scale, angle=0, coord=(0.5,0.5)):
    assert min(coord) >= 0 and max(coord) <= 1, "Coordinate should be in the range [0,1]"
    h, w = img.shape[:2]
    cy, cx = h*coord[0], w*coord[1]
    if coord[0] >= 0.5:
        cy = -3*h*coord[0]+2*h
    rot_mat = cv2.getRotationMatrix2D((cx,cy), angle, scale)
    result = cv2.warpAffine(img, rot_mat, img.shape[1::-1], flags=cv2.INTER_LINEAR)
    return result

def ease_in_out(x, alpha=4):
    return (x**alpha) / (x**alpha + (1 - x)**alpha)

def progress(frame_start, frame_end):
    def _progress(i):
        if i <= frame_start: return 0
        if i >= frame_end: return 1
        return (i - frame_start) / (frame_end - frame_start)
    return _progress

cap = cv2.VideoCapture("long-demo.mov")
num_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
fps = 42.59

# should be user-specified
"""
secs = [(1, 1.45), (9, 9.45)]
scales = [0.5, 0.5]
coords = [(0.593, 0.5), (0.5, 0.5)]
frames = [(int(s[0]*fps), int(s[1]*fps)) for s in secs]
progress_fns = [progress(*f) for f in frames]
"""

secs = [(3, 3.45), (12.10, 12.55), (16.50, 16.95), (38.50, 38.95)]
scales = [0.5, 0.5, 0.5, 0.5]
coords = [(0.593, 0.5), (0.5, 0.5), (0.593, 0.5), (0.5, 0.5)]
frames = [(int(s[0]*fps), int(s[1]*fps)) for s in secs]
progress_fns = [progress(*f) for f in frames]

i = 0
cur_anim = 0
cur_scale = 1
cur_coord = (0.5, 0.5)

while cap.isOpened():
    ret, frame = cap.read()
    if ret:
        """
        if i < frames[cur_anim+1][0]:
            progress_fn = progress_fns[0]
            end_scale = scales[0]
            coord = coords[0]
        else:
            progress_fn = progress_fns[1]
            end_scale = scales[1]
            coord = coords[0]
        """
        
        if cur_anim+1 < len(frames): # avoid out-of-bounds
            if i >= frames[cur_anim+1][0]:
                cur_anim += 1
                
        progress_fn = progress_fns[cur_anim]
        end_scale = scales[cur_anim]
        coord = coords[0]
        
        """
        if i < frames[1][0]:
            scale = 1 + ease_in_out(progress_fn(i)) * end_scale
        else:
            scale = 1.5 - ease_in_out(progress_fn(i)) * end_scale
        """
        
        if cur_anim % 2 == 0:
            scale = 1 + ease_in_out(progress_fn(i)) * end_scale
        else:
            scale = 1.5 - ease_in_out(progress_fn(i)) * end_scale
        
        #frame = zoom_at(frame, scale, coord=coord)
        cv2.imshow("Frame", zoom_at(frame, scale, coord=coord))
        #cv2.imwrite(f"long-frames/{i}.jpg", frame)
        if cv2.waitKey(25) & 0xFF == ord("q"):
            break
    else:
        break
    i += 1

cap.release()
cv2.destroyAllWindows()