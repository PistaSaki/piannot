import sys
from pathlib import Path
from typing import Tuple, List

import PyQt5.QtWidgets as qtw

from piannot import data_dir
from piannot.annotator_selector import AnnotatorSelector
from piannot.gui import MainWindow

import logging
logger = logging.getLogger()
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


annotator_selector = AnnotatorSelector(cats=["ball", "head1", "head2"])

app = qtw.QApplication(sys.argv)
ex = MainWindow(annotator_selector)
sys.exit(app.exec_())

