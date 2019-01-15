import os
import PIL
import numpy as np
import json

from typing import List
from functools import partialmethod
        

class Annotation:
    def __init__(self):
        self.objects = []
        self.missing = []
        
    def add_object(self, cat: str, x: int, y: int):
        self.objects.append({"cat": cat, "x": x, "y": y})
    
    def add_missing(self, cat):
        self.missing.append(cat)

    
    def to_json(self, path: str = None):
        if path is None:
            return json.dumps(self.__dict__)
        else:
            raise NotImplementedError()
    
    @staticmethod
    def load(path: str):
        if not os.path.exists(path):
            return Annotation()
        else:
            raise NotImplementedError()
            
            
            

class Annotator:
    def __init__(self, image_dir: str, annotation_dir: str , cats: List[str]):
        self._image_dir = image_dir
        self._annotation_dir = annotation_dir
        self.cats = cats
        self.active_cat = cats[0]
        
        self.image_file = os.listdir(self._image_dir)[0]
        
        
    
    @property
    def annotation_path(self) -> str:
        return os.path.join(
            self._annotation_dir, 
            os.path.splitext(self.image_file)[0] + ".json"
        )
        
    @property
    def image_path(self) -> str:
        return os.path.join(self._image_dir, self.image_file)
        
    @property
    def image_file(self) -> str:
        return self._image_file
    
    @image_file.setter
    def image_file(self, val: str):
        self._image_file = val
        self._image = np.array(PIL.Image.open(self.image_path))
        self._annotation = Annotation.load(self.annotation_path)
    
        
    @property
    def annotation(self) -> Annotation:
        return self._annotation
    
    @property
    def image(self) -> np.ndarray:
        return self._image
    
    def _move(self, step = 1):
        images = os.listdir(self._image_dir)
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
        
    
    def add_missing(self):
        self.annotation.add_missing(self.active_cat)
        
    @property
    def objects(self):
        return self.annotation.objects
    
    @property
    def missing(self):
        return self.annotation.missing
    
        
