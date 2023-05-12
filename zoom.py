import cv2
import numpy as np
from effect import Transition, Coord

def generate_frames(video_path, effects):
    cap = cv2.VideoCapture(video_path)
    num_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = 42.59
    
    for effect in effects:
        effect.start_frame = int(effect.start*fps)
        effect.end_frame = int((effect.start+effect.duration)*fps)
    
    frame_index, effect_index = 0, 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret: break
        if effect_index+1 < len(effects): # avoid out-of-bounds
            if frame_index >= effects[effect_index+1].start_frame:
                effect_index += 1
        _from = None if effect_index == 0 else effects[effect_index-1]
        to = effects[effect_index]
        t = Transition(to, _from)
        scale, coord = t.state(to.progress(frame_index))
        cv2.imshow("Frame", zoom_at(frame, scale, coord=coord))
        if cv2.waitKey(25) & 0xFF == ord("q"): break
        frame_index += 1
    cap.release()
    cv2.destroyAllWindows()

def zoom_at(img, scale, angle=0, coord=Coord(0.5,0.5)):
    assert min(coord) >= 0 and max(coord) <= 1, "Coordinate should be in the range [0,1]"
    h, w = img.shape[:2]
    cy, cx = h*coord.y, w*coord.x
    #if coord.y >= 0.5:
    #    cy = -3*h*coord.y+2*h
    rot_mat = cv2.getRotationMatrix2D((cx,cy), angle, scale)
    result = cv2.warpAffine(img, rot_mat, img.shape[1::-1], flags=cv2.INTER_LINEAR)
    return result