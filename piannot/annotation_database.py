import os
from annotation import Annotation

class AnnotationDatabase:
    _annotation_dir: str
        
    def __init__(self, annotation_dir: str):
        self._annotation_dir = annotation_dir
        
    def _get_annotation_path(self, key: str) -> str:
        return os.path.join(
            self._annotation_dir, 
            os.path.splitext(key)[0] + ".json"
        )
    
    def load_annotation(self, key: str) -> Annotation:
        return Annotation.load(self._get_annotation_path(key))
    
    def save_annotation(self, annotation: Annotation, key: str):
        annotation.to_json(path = self._get_annotation_path(key))
    