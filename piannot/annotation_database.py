import os
from os.path import splitext
from annotation import Annotation
from typing import List

class SimpleAnnotationDatabase:
    """This simpler class works but it is slow when reading all annotations."""
    _annotation_dir: str
        
    def __init__(self, annotation_dir: str):
        self._annotation_dir = annotation_dir
        
    def _get_annotation_path(self, key: str) -> str:
        return os.path.join(
            self._annotation_dir, 
            splitext(key)[0] + ".json"
        )
    
    def load_annotation(self, key: str) -> Annotation:
        return Annotation.load(self._get_annotation_path(key))
    
    def save_annotation(self, annotation: Annotation, key: str):
        annotation.to_json(path = self._get_annotation_path(key))

class AnnotationDatabase:
    _annotation_dir: str
    _annotations: List[Annotation]
    
    def __init__(self, annotation_dir: str):
        os.makedirs(annotation_dir, exist_ok=True)
        self._annotation_dir = annotation_dir
        self._preload_annotations()
        
    def _preload_annotations(self):
        annotation_dir = self._annotation_dir
        jsons = [
                f for f in os.listdir(annotation_dir) 
                if splitext(f)[1] == ".json"
        ]
        self._annotations = {
            splitext(f)[0]: Annotation.load(os.path.join(annotation_dir, f)) 
            for f in jsons
        }
        
    def _get_annotation_path(self, key: str) -> str:
        return os.path.join(
            self._annotation_dir, 
            splitext(key)[0] + ".json"
        )
    
####### Public Methods ########
    
    def load_annotation(self, key: str) -> Annotation:
        return self._annotations.get(key, Annotation())
        
    def save_annotation(self, annotation: Annotation, key: str):
        self._annotations[key] = annotation
        annotation.to_json(path = self._get_annotation_path(key))
        