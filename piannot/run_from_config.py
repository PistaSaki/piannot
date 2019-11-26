import sys
import PyQt5.QtWidgets as qtw

from annotator import Annotator
from image_database import ImageDatabase
from annotation_database import AnnotationDatabase
from gui import MainWindow

import yaml

import argparse
import logging


def _get_config() -> dict:
    parser = argparse.ArgumentParser()
    parser.add_argument("config_path", help = "path to configuration yaml file")
    
    args = parser.parse_args()
    with open(args.config_path, "rt") as config_file:
        config = yaml.load(config_file)
        
    return config

def _get_logger() -> logging.Logger:
    logger = logging.getLogger()    
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG,
        format='%(asctime)s %(message)s')
    return logger

config = _get_config()
image_dir = config["image_dir"]
annot_dir = config.get("annot_dir", image_dir)
cats = config["cats"]

logger = _get_logger()
logger.info(f"Annotating images from {image_dir} to {annot_dir}.")

annotator = Annotator(
    image_db = ImageDatabase(image_dir), 
    annotation_db = AnnotationDatabase(annot_dir),
    cats = cats
)

app = qtw.QApplication(sys.argv)
ex = MainWindow(annotator)
sys.exit(app.exec_())
