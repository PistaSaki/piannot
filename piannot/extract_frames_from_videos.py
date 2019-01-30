import os
import PIL
import moviepy.editor
from typing import Tuple

def extract_frames_from_one_video(video_path: str, out_folder: str, condition = lambda i: True):
    print(f"Extracting frames from {video_path} to {out_folder}.")
    if not os.path.exists(out_folder):
        os.makedirs(out_folder)
    
    clip = moviepy.editor.VideoFileClip(video_path)
    try:
        for i, frame in enumerate(clip.iter_frames()):
            if condition(i):
                out_path = os.path.join(out_folder, "frame_{:0>5d}.jpg".format(i))
                img = PIL.Image.fromarray(frame)
                img.save(out_path)
    finally:    
        ## https://stackoverflow.com/questions/43966523/getting-oserror-winerror-6-the-handle-is-invalid-in-videofileclip-function
        clip.reader.close()
        clip.audio.reader.close_proc()
        

def extract_frames_from_video_folder(video_folder, parent_frame_folder, condition = lambda i: True):
    video_files = [f for f in os.listdir(video_folder) 
                    if os.path.splitext(f)[1] == ".mp4"]
    
    print(f"Found {len(video_files)} mp4 videos.")
    
    for video_name in video_files:
        extract_frames_from_one_video(
            video_path= os.path.join(video_folder, video_name),
            out_folder = os.path.join(
                parent_frame_folder, os.path.splitext(video_name)[0]
            ),
            condition= condition
        )

if __name__ == "__main__": 
    def _retrieve_cmd_line_args() -> Tuple[str, str, int]:
        import argparse
        parser = argparse.ArgumentParser()
        parser.add_argument("video_folder", help = "folder containig input videos")
        parser.add_argument("parent_frame_folder", 
            nargs = "?",
            help = "Folder where to write frames. If not present, use video_folder."
        )
        parser.add_argument("-s", "--step", 
            type = int,
            help = "We save frame with index i iff i is divisible by step. Defaults to 1.",
            default = 1
        )
        args = parser.parse_args()
        
        video_folder = args.video_folder
        parent_frame_folder = args.parent_frame_folder 
        if parent_frame_folder is None:
            parent_frame_folder = video_folder
        step = args.step
        
        return video_folder, parent_frame_folder, step

    video_folder, parent_frame_folder, step = _retrieve_cmd_line_args()
    
    extract_frames_from_video_folder(
        video_folder = video_folder,
        parent_frame_folder = parent_frame_folder,
        condition = lambda i: i % step == 0
    )

    