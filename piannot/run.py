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


def _run(cats: List[str], parent_frame_dir: Path = None, parent_annot_dir: Path = None):
    annotator_selector = AnnotatorSelector(cats=cats, parent_frame_dir=parent_frame_dir,
                                           parent_annot_dir=parent_annot_dir)

    app = qtw.QApplication(sys.argv)
    ex = MainWindow(annotator_selector)
    sys.exit(app.exec_())


def _parse_args() -> Tuple[Path, Path, List[str]]:
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--image_dir", default=None, help="path to folder with jpg images")
    parser.add_argument("--annot_dir", default=None, help="path to folder with annotation json files.")
    args = parser.parse_args()

    image_dir = Path(args.image_dir or data_dir / "frames")
    annot_dir = Path(args.annot_dir or data_dir / "annotations")
    cats = ["ball", "head1", "head2", "bat1", "bat2", "player1", "player2"]

    return image_dir, annot_dir, cats


def _main():
    parent_frame_dir, parent_annot_dir, cats = _parse_args()
    logger.debug(f"cats={cats}, parent_frame_dir={parent_frame_dir}, parent_annot_dir={parent_annot_dir}")
    _run(cats=cats, parent_frame_dir=parent_frame_dir, parent_annot_dir=parent_annot_dir)


if __name__ == "__main__":
    _main()
