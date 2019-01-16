import os
import numpy as np

from typing import List, Set
from functools import partialmethod

from annotation import Annotation
from image_database import ImageDatabase

import logging
logger = logging.getLogger()
            

class Annotator:
    def __init__(self, image_db: ImageDatabase, annotation_dir:str , cats:List[str]):
        self._image_db = image_db
        self._annotation_dir = annotation_dir
        self.cats = cats
        self.active_cat = cats[0]
        
        self.image_file = self._image_db.key_list[0]
        
    @property
    def annotation_path(self) -> str:
        return os.path.join(
            self._annotation_dir, 
            os.path.splitext(self.image_file)[0] + ".json"
        )
            
    def _save_annotation(self):
        self._annotation.to_json(path = self.annotation_path)
    
    @property
    def image_file(self) -> str:
        return self._image_file
        
    @image_file.setter
    def image_file(self, val: str):
        self._image_file = val
        self._image = self._image_db.get_image(self._image_file)
        self._annotation = Annotation.load(self.annotation_path)
        
        logger.debug( 
            f"Changed image to {self.image_file} "
            f"and annotation to {self.annotation}."
        )
    
        
    @property
    def annotation(self) -> Annotation:
        return self._annotation
    
    @property
    def image(self) -> np.ndarray:
        return self._image
    
    def _move(self, step = 1):
        images = self._image_db.key_list
        try:
            i = images.index(self.image_file)
            i += step
            i = max(0, min(i, len(images) - 1))
        except ValueError:
            i = 0
            
        self.image_file = images[i]
        
    next_image = partialmethod(_move, 1)
    prev_image = partialmethod(_move, -1)
     
    def add_object(self, x: int, y: int):
        self.annotation.add_object(self.active_cat, x, y) 
        self._save_annotation()
        
    
    def add_missing(self):
        self.annotation.add_missing(self.active_cat)
        self._save_annotation()
        
    @property
    def objects(self) -> List[dict]:
        """Objects of current annotation."""
        return self.annotation.objects
    
    @property
    def missing(self) -> Set[str]:
        """Missing categories in current annotation."""
        return self.annotation.missing
    
    def get_cat_state_description(self, cat:str = None):
        cat = cat or self.active_cat
        
        if cat in self.annotation.missing:
            return "MISSING"
        
        obs = [ob for ob in self.annotation.objects if ob["cat"] == cat]
        if len(obs) == 0:
            return "UNSPECIFIED"
        
        return [(int(round(ob["x"])), int(round(ob["y"]))) for ob in obs]
        
    
        

if __name__ == "__main__":
    import sys
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    
    annotator = Annotator(
        image_db = ImageDatabase(r"D:\python_source\piannot\data"), 
        annotation_dir = r"D:\python_source\piannot\data",
        cats = ["ball", "head1", "head2"]
    )