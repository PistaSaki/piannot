import json
import os

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
