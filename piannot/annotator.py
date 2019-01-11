import os
import PIL
import numpy as np
import json

from collections import namedtuple
Obj = namedtuple("Obj", ['cat', 'x', 'y'])

class CustomEncoder(json.JSONEncoder):
    def default(self, o):
        print("aaa")
            
        if isinstance(o, Obj):
            return "aaa"
        
        return json.JSONEncoder.default(self, o)
        

class Annotation:
    def __init__(self):
        self.objects = []
        self.missing = []
        
    def add_object(self, cat: str, x: int, y: int):
        self.objects.append(Obj(cat, x, y))
    
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
            
a = Annotation()
print(a.to_json())
            
            
            

class Annotator:
    def __init__(self, image_dir, annotation_dir):
        self._image_dir = image_dir
        self._annotation_dir = annotation_dir
        
        self.image_file = os.listdir(self._image_dir)[0]
        
    
    @property
    def annotation_path(self):
        return os.path.join(
            self._annotation_dir, 
            os.path.splitext(self.image_file)[0] + ".json"
        )
        
    @property
    def image_path(self):
        return os.path.join(self._image_dir, self.image_file)
        
    @property
    def image_file(self):
        return self._image_file
    
    @image_file.setter
    def image_file(self, val):
        self._image_file = val
        self._image = np.array(PIL.Image.open(self.image_path))
        self._annotation = Annotation.load(self.annotation_path)
    
        
    @property
    def annotation(self):
        return self._annotation
    
    @property
    def image(self):
        return self._image
    
    def move(self, step = 1):
        images = os.listdir(self._image_dir)
        try:
            i = images.index(self.image_file)
            i += step
            i = max(0, min(i, len(images) - 1))
        except ValueError:
            i = 0
            
        self.image_file = images[i]
        

