from pathlib import Path
import itertools as itt

import numpy as np
import PIL.Image
from typing import Tuple, Iterator

from moviepy.video.io.VideoFileClip import VideoFileClip


def video_frames(path: Path, t_start=0, t_end=None) -> Iterator[np.ndarray]:
    """Video frames iterator that releases the resources correctly."""
    clip = VideoFileClip(str(path))
    try:
        subclip = clip.subclip(t_start=t_start, t_end=t_end)
        yield from subclip.iter_frames()
    finally:
        ## https://stackoverflow.com/questions/43966523/getting-oserror-winerror-6-the-handle-is-invalid-in-videofileclip-function
        clip.reader.close()
        clip.audio.reader.close_proc()


def _save_frame(i: int, frame: np.array, out_folder: Path) -> None:
    out_folder.mkdir(parents=True, exist_ok=True)
    out_path = out_folder / f"frame_{i:0>5d}.jpg"
    img = PIL.Image.fromarray(frame)
    img.save(out_path)


def extract_frames_from_one_video(video_path: Path, out_folder: Path, step: int = 1, divide: int = None):
    print(f"Extracting frames from {video_path} to {out_folder}.")

    fr = enumerate(video_frames(video_path))
    fr = itt.islice(fr, None, None, step)

    if not divide:
        for i, frame in fr:
            _save_frame(i, frame, out_folder=out_folder)
    else:
        for i, frame in fr:
            start_i = divide * (i // divide)
            end_i = start_i + divide - 1
            sub_folder = f"frames_{start_i:0>5d}-{end_i:0>5d}"
            _save_frame(i, frame, out_folder=out_folder / sub_folder)


def _retrieve_cmd_line_args() -> Tuple[Path, Path, int, int]:
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("video_folder", help="folder containig input videos")
    parser.add_argument("parent_frame_folder", help="Folder where to write frames.")
    parser.add_argument("-s", "--step", type=int,
                        help="We save frame with index i iff i is divisible by step. Defaults to 1.",
                        default=1
                        )
    parser.add_argument("--divide", type=int,
                        help="We divide the frames into folders with specified number of frames.",
                        default=None
                        )
    args = parser.parse_args()

    video_folder = Path(args.video_folder)
    parent_frame_folder = Path(args.parent_frame_folder) if args.parent_frame_folder is not None else video_folder

    return video_folder, parent_frame_folder, args.step, args.divide


def _main():
    video_folder, parent_frame_folder, step, divide = _retrieve_cmd_line_args()

    for video_path in video_folder.glob("**/*.mp4"):
        out_folder = parent_frame_folder / video_path.relative_to(video_folder).with_suffix("")
        extract_frames_from_one_video(video_path, out_folder, step, divide)


if __name__ == "__main__":
    _main()
