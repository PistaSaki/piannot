import os
import numpy as np
import PIL

class ImageDatabase:
    def __init__(self, image_dir: str):
        self._image_dir = image_dir
        
    @property
    def key_list(self):
        extensions = {".jpg"}
        all_files =  os.listdir(self._image_dir)
        return [
            name for name, ext in [os.path.splitext(f) for f in all_files] 
            if ext in extensions
        ]
    
    
    def get_image(self, key) -> np.ndarray:
        path = os.path.join(self._image_dir, key + ".jpg")
        return np.array(PIL.Image.open(path))
    