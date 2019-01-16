import PyQt5.QtWidgets as qtw
from PyQt5.QtCore import pyqtSignal, Qt


from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
import matplotlib.pyplot as plt

from annotator import Annotator

import logging
logger = logging.getLogger()


class MainWindow(qtw.QMainWindow):
    def __init__(self, annotator):
        super().__init__()
        self.annotator = annotator
        self._initUI()
        
    def _initUI(self):    
        self.main_widget = MainWidget(annotator = self.annotator)
        self.setCentralWidget(self.main_widget)
        
        self.setWindowTitle('Piannot')
        
        self.statusBar().showMessage('Ready')
        
        next_image_action = qtw.QAction("Next_img", self)
        next_image_action.triggered.connect(self.main_widget.next_image)
        next_image_action.setShortcut("right")
        
        prev_image_action = qtw.QAction("Prev_img", self)
        prev_image_action.triggered.connect(self.main_widget.prev_image)
        prev_image_action.setShortcut("left")
        
        missing_action = qtw.QAction("Missing", self)
        missing_action.triggered.connect(self.main_widget.missing_invoked)
        missing_action.setShortcut("m")
        
        auto_next_image_checker = qtw.QAction("Auto_Next", self, checkable = True)
        auto_next_image_checker.setChecked(self.main_widget.auto_next_image)
        auto_next_image_checker.triggered.connect(
                self.main_widget.set_auto_next_image)        
        
        
        menubar = self.menuBar()
        navigationMenu = menubar.addMenu('Navigation')
        annotationMenu = menubar.addMenu('Annotation')
        
        navigationMenu.addAction(prev_image_action)
        navigationMenu.addAction(next_image_action)
        navigationMenu.addAction(auto_next_image_checker)
        
        annotationMenu.addAction(missing_action)
        
        
        self.setGeometry(300, 300, 350, 200)
        self.show()
        
        


class MainWidget(qtw.QWidget):
    annotator: Annotator
    auto_next_image: bool = False
    
    def __init__(self, annotator):
        super().__init__()
        
        self.annotator = annotator
        
        self._initUI()
        
        
    def _initUI(self):               
        layout = qtw.QHBoxLayout()
        self.setLayout(layout)
        
        splitter = qtw.QSplitter(Qt.Horizontal)
        layout.addWidget(splitter)
        
        cat_select = qtw.QListWidget()
        splitter.addWidget(cat_select)
        for cat in self.annotator.cats:
            cat_select.addItem(cat)
            
        cat_select.setCurrentItem(
            cat_select.findItems(
                self.annotator.active_cat, Qt.MatchExactly
            )[0]
        )
        cat_select.currentItemChanged.connect(self.cat_item_changed)
        
        
        self.canvas = ImgCanvas(parent = self)
        splitter.addWidget(self.canvas)
        self.canvas.mouse_pressed_signal.connect(self.mouse_pressed_on_canvas)
        
        
        self.show()
        self.update()
        
                
    def update(self):
        ax = self.canvas.ax
        
        for to_remove in ax.images + ax.collections:
            to_remove.remove()
            
        
        ax.imshow(self.annotator.image)
        ax.set_title(
            f"{self.annotator.active_cat}: "
            f"{self.annotator.get_cat_state_description()}"
        )
        
        objects = [ob for ob in self.annotator.objects 
                   if ob["cat"] == self.annotator.active_cat]        
        ax.scatter(
            x = [ob["x"] for ob in objects], 
            y = [ob["y"] for ob in objects], 
            c = "white"
        )
        
        self.canvas.draw()
        
    def next_image(self):
        self.annotator.next_image()
        self.update()
        
    def prev_image(self):
        self.annotator.prev_image()
        self.update()
    
    def cat_item_changed(self, item):
        logger.debug(f"cat_item_changed: {item.text()}")
        self.annotator.active_cat = item.text()
        self.update()
        
    def mouse_pressed_on_canvas(self, x, y):
        self.annotator.add_object(x, y)
        self.update()
        if self.auto_next_image:
            self.next_image()
        
    def missing_invoked(self):
        logger.debug("missing_invoked")
        self.annotator.add_missing()
        self.update()
        if self.auto_next_image:
            self.next_image()
        
    def set_auto_next_image(self, state):
        self.auto_next_image = state
        
        
        
        
    
        
class ImgCanvas(FigureCanvasQTAgg):
    mouse_pressed_signal = pyqtSignal([float, float])
 
    def __init__(self, parent=None, width=5, height=4):
        fig, self.ax = plt.subplots(figsize=(width, height))
        self._setup_FigureCanvas(parent, fig)
            
        self.setMouseTracking(True)
        
        fig.canvas.mpl_connect("button_press_event", self.onclick)
        
    def _setup_FigureCanvas(self, parent, fig):
        """Set-up the parent class `FigureCanvas`."""
        super().__init__(fig)
        self.setParent(parent)
 
        self.setSizePolicy(
                qtw.QSizePolicy.Expanding,
                qtw.QSizePolicy.Expanding)
        self.updateGeometry()
            
        
    def onclick(self, event):
        print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
              ('double' if event.dblclick else 'single', event.button,
               event.x, event.y, event.xdata, event.ydata)) 
        self.mouse_pressed_signal.emit(event.xdata, event.ydata)
    
        
 
