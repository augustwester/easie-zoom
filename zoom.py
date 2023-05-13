import cv2
import numpy as np
from effect import Transition, Coord
from tqdm import tqdm

def generate_frames(video_path, effects):
    cap = cv2.VideoCapture(video_path)
    num_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    for effect in effects:
        effect.start_frame = int(effect.start*fps)
        effect.end_frame = int((effect.start+effect.duration)*fps)
    
    effect_index = 0
    frames = np.empty((num_frames, height, width, 3)) # assuming rgb
    progress = tqdm(range(num_frames))
    
    print("Processing video...")
    for i in progress:
        progress.set_description(f"Frame {i+1}/{num_frames}")
        ret, frame = cap.read()
        if not ret: break
        if effect_index+1 < len(effects): # avoid out-of-bounds
            if i >= effects[effect_index+1].start_frame:
                effect_index += 1
        _from = None if effect_index == 0 else effects[effect_index-1]
        to = effects[effect_index]
        t = Transition(to, _from)
        scale, coord = t.state(to.progress(i))
        zoom_frame = zoom(frame, scale, coord=coord)
        frames[i] = zoom_frame
    cap.release()
    
    return frames, fps

def zoom(img, scale, angle=0, coord=Coord(0.5,0.5)):
    assert min(coord) >= 0 and max(coord) <= 1, "Coordinate should be in the range [0,1]"
    h, w = img.shape[:2]
    cy, cx = h*coord.y, w*coord.x
    rot = cv2.getRotationMatrix2D((cx,cy), angle, scale)
    return cv2.warpAffine(img, rot, img.shape[1::-1], flags=cv2.INTER_LINEAR)

def frames_to_video(frames, fps, output_path):
    print("Saving video...")
    frames = np.uint8(frames)
    num_frames, height, width = frames.shape[:3]
    writer = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(output_path, writer, fps, (width, height))
    for i in tqdm(range(num_frames)):
        data = frames[i]
        out.write(data)
    out.release()