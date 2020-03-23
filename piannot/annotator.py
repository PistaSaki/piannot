import numpy as np

from typing import List, Set
from functools import partialmethod

from piannot.annotation import Annotation
from piannot.image_database import ImageDatabase
from piannot.annotation_database import AnnotationDatabase

import logging
logger = logging.getLogger()
            

class Annotator:
    _image_db: ImageDatabase
    _annotation_db: AnnotationDatabase
    
    _image_key: str
    _annotation: Annotation
    _image: np.ndarray
    
    cats: List[str]
    active_cat: str
    
    
    def __init__(self, image_db: ImageDatabase, annotation_db: AnnotationDatabase , cats:List[str]):
        self._image_db = image_db
        self._annotation_db = annotation_db
        
        self.cats = cats
        self.active_cat = cats[0]
        
        self.image_key = self._image_db.key_list[0]
        
            
    def _save_annotation(self):
        self._annotation_db.save_annotation(annotation=self.annotation, key=self.image_key)
        
    @property
    def image_key(self) -> str:
        return self._image_key
        
    @image_key.setter
    def image_key(self, val: str):
        self._image_key = val
        self._image = self._image_db.get_image(self._image_key)
        self._annotation = self._annotation_db.load_annotation(self._image_key)
        
        logger.debug( 
            f"Changed image to {self.image_key} "
            f"and annotation to {self.annotation}."
        )
    
        
    @property
    def annotation(self) -> Annotation:
        return self._annotation
    
    @property
    def image(self) -> np.ndarray:
        return self._image
    
    def get_image_keys(self) -> List[str]:
        return self._image_db.key_list
    
    def _move(self, step = 1):
        images = self._image_db.key_list
        try:
            i = images.index(self.image_key)
            i += step
            i = max(0, min(i, len(images) - 1))
        except ValueError:
            i = 0
            
        self.image_key = images[i]
        
    next_image = partialmethod(_move, 1)
    prev_image = partialmethod(_move, -1)
     
    def add_object(self, x: int, y: int):
        self.annotation.add_object(self.active_cat, x, y) 
        self._save_annotation()
        
    
    def add_missing(self):
        logger.debug("Entered `Annotator.add_missing`.")
        self.annotation.add_missing(self.active_cat)
        self._save_annotation()
        logger.debug("Finished `Annotator.add_missing`.")
        
        
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
        return self.annotation.get_cat_state_description(cat)
        
    
        

if __name__ == "__main__":
    import sys
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    
    annotator = Annotator(
        image_db = ImageDatabase(r"..\data"), 
        annotation_db = AnnotationDatabase(r"..\data"),
        cats = ["ball", "head1", "head2"]
    )