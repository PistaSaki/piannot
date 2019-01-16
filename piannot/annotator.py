import os
import PIL
import numpy as np
import json

from typing import List, Set
from functools import partialmethod

from image_database import ImageDatabase

import logging
logger = logging.getLogger()
        

class Annotation:
    def __init__(self, objects = None, missing = None):
        self.objects = list(objects) or list()
        self.missing = set(missing) or set()
        self._check_consistency()
        
    def add_object(self, cat: str, x: int, y: int, unique: bool=True):
        if unique:
            self.objects = [o for o in self.objects if not o["cat"] == cat ]
        self.objects.append({"cat": cat, "x": x, "y": y})
        self.missing.discard(cat)
    
    def add_missing(self, cat):
        self.objects = [o for o in self.objects if not o["cat"] == cat ]
        self.missing.add(cat)
        
    def _is_empty(self):
        return len(self.objects) == len(self.missing) == 0

    
    def to_json(self, path: str = None):
        self._check_consistency()
        dic = {
            "objects": self.objects,
            "missing": list(self.missing)
        }
        
        if path is None:
            return json.dumps(dic)
        else:
            if not self._is_empty():
                with open(path, "wt") as file:
                    json.dump(dic, file)
                    
    def __repr__(self):
        return self.to_json()
    
    def __str__(self):
        return self.to_json()
    
    def _check_consistency(self):
        object_cats = set(ob["cat"] for ob in self.objects)
        problem_cats = self.missing.intersection(object_cats)
        assert len(problem_cats) == 0, str(problem_cats)
    
    @staticmethod
    def load(path: str):
        if not os.path.exists(path):
            return Annotation()
        else:
            with open(path, "rt") as file:
                dic = json.load(file)
            return Annotation(**dic)
            
            
            

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