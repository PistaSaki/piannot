import sys
import PyQt5.QtWidgets as qtw

from annotator import Annotator
from image_database import ImageDatabase
from annotation_database import AnnotationDatabase
from gui import MainWindow


import argparse
parser = argparse.ArgumentParser()
parser.add_argument("image_dir", help = "path to folder with jpg images")
parser.add_argument("annot_dir", 
    nargs = "?",
    help = "path to folder with annotation json files. If not present use image_dir."
)
args = parser.parse_args()
image_dir = args.image_dir
annot_dir = args.annot_dir or image_dir


import logging
logger = logging.getLogger()
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

logger.info(f"Annotating images from {image_dir} to {annot_dir}.")

annotator = Annotator(
    image_db = ImageDatabase(image_dir), 
    annotation_db = AnnotationDatabase(annot_dir),
    cats = ["ball", "head1", "head2"]
)

app = qtw.QApplication(sys.argv)
ex = MainWindow(annotator)
sys.exit(app.exec_())
