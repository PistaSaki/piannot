import os
from annotation import Annotation
from typing import Tuple

def count_annotated_objects_in_folder(folder:str, recursive:bool=True) -> int:
    jsons = [
        os.path.join(folder, f) for f in os.listdir(folder) 
        if os.path.splitext(f)[1] == ".json"
    ]
    count = 0
    for f in jsons:
        ann =  Annotation.load(f)
        count += len(ann.objects) + len(ann.missing)
        
    if recursive:
        subfolders = [
            os.path.join(folder, f)
            for f in os.listdir(folder)
            if os.path.isdir(os.path.join(folder, f))
        ]
        count += sum(
            count_annotated_objects_in_folder(subfolder, True)
            for subfolder in subfolders
        )
        
    return count

def _retrieve_cmd_line_args() -> Tuple[str, str]:
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("folder", help = "folder containig annotations")
    
    parser.add_argument("--out_file", 
        type = str,
        help = "Text file where to write the output.",
        default = None
    )
    args = parser.parse_args()
    
    return args.folder, args.out_file

def _save_to_file(count:int, out_file: str):
    import datetime
    now = datetime.datetime.now()
    
    out_string = f"{now:%D %H:%M} {count}"
    print(f"Saving '{out_string}' to {out_file}")
    
    with open(out_file, "at") as file:
        file.write("\n" + out_string)
    
    
if __name__ == "__main__":
    folder, out_file = _retrieve_cmd_line_args()
    
    count = count_annotated_objects_in_folder(folder = folder)
    print(count)
    
    if out_file:
        _save_to_file(count, out_file)
        
        
        
    
    
    
    