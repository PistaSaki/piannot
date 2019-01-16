import sys
import PyQt5.QtWidgets as qtw

from annotator import Annotator
from image_database import ImageDatabase
from annotation_database import AnnotationDatabase
from gui import MainWindow

import logging
logger = logging.getLogger()
        
if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    
    annotator = Annotator(
        image_db = ImageDatabase(r"..\data"), 
        annotation_db = AnnotationDatabase(r"..\data"),
        cats = ["ball", "head1", "head2"]
    )
    
    app = qtw.QApplication(sys.argv)
    ex = MainWindow(annotator)
    sys.exit(app.exec_())
