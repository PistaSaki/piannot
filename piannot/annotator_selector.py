from pathlib import Path
from typing import List

from piannot import data_dir
from piannot.annotation_database import AnnotationDatabase
from piannot.annotator import Annotator
from piannot.image_database import ImageDatabase


class AnnotatorSelector:
    def __init__(self, cats: List[str], parent_frame_dir: Path = None, parent_annot_dir: Path = None):
        self.cats = cats
        self.parent_frame_dir = parent_frame_dir or data_dir / "frames"
        self.parent_annot_dir = parent_annot_dir or data_dir / "annotations"

        for frame in self.parent_frame_dir.glob("**/*.jpg"):
            break
        self.frame_dir = frame.parent

    @property
    def annot_dir(self) -> Path:
        return self.parent_annot_dir / self.frame_dir.relative_to(self.parent_frame_dir)

    def get_annotator(self):
        return Annotator(
            image_db=ImageDatabase(self.frame_dir),
            annotation_db=AnnotationDatabase(self.annot_dir),
            cats=self.cats
        )

