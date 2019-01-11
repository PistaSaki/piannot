import sys
import PyQt5.QtWidgets as qtw
from PyQt5.QtCore import pyqtSignal


from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
import matplotlib.pyplot as plt

import numpy as np

from annotator import Annotator

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
        
        next_image_action = qtw.QAction("Next", self)
        next_image_action.triggered.connect(self._next_image)
        next_image_action.setShortcut("right")
        
        prev_image_action = qtw.QAction("Prev", self)
        prev_image_action.triggered.connect(self._prev_image)
        prev_image_action.setShortcut("left")
        
        menubar = self.menuBar()
        menubar.addAction(prev_image_action)
        menubar.addAction(next_image_action)
        
        
        self.setGeometry(300, 300, 350, 200)
        self.show()
        
    def _next_image(self):
        self.annotator.move()
        self.main_widget.update()
        
    def _prev_image(self):
        self.annotator.move(-1)
        self.main_widget.update()


class MainWidget(qtw.QWidget):
    
    def __init__(self, annotator):
        super().__init__()
        
        self.annotator = annotator
        
        self._initUI()
        
        
    def _initUI(self):               
        layout = qtw.QVBoxLayout()
        self.setLayout(layout)
        
        
        self.canvas = ImgCanvas(
                parent = self, 
                image = self.annotator.image
            )
        layout.addWidget(self.canvas)
        self.canvas.mouse_pressed_signal.connect(self.mouse_pressed_on_canvas)
        
        self.show()
        
        
    def mouse_pressed_on_canvas(self, x, y):
        print(f"mose pressed: x: {x:.2f},  y: {y:.2f}")
        self.canvas.ax.scatter(x, y)
        self.canvas.draw()
        
    def update(self):
        self.canvas.image = self.annotator.image
    
        
class ImgCanvas(FigureCanvasQTAgg):
    mouse_pressed_signal = pyqtSignal([float, float])
 
    def __init__(self, parent=None, width=5, height=4, image = None):
        fig, self.ax = plt.subplots(figsize=(width, height))
        self._setup_FigureCanvas(parent, fig)
        
        self.image = image if image is not None else np.random.rand(13, 10, 3)
        
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
        
    @property
    def image(self):
        return self._image
    @image.setter
    def image(self, val):
        self._image = val
        self._plot()
        
 
    def _plot(self):
        ax = self.ax
        ax.imshow(self.image)
        self.draw()
        
        
    def onclick(self, event):
        print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
              ('double' if event.dblclick else 'single', event.button,
               event.x, event.y, event.xdata, event.ydata)) 
        self.mouse_pressed_signal.emit(event.xdata, event.ydata)
    
        
 

        
if __name__ == '__main__':
    annotator = Annotator(r"D:\python_source\piannot\data", r"D:\python_source\piannot\data")
    app = qtw.QApplication(sys.argv)
    ex = MainWindow(annotator)
    sys.exit(app.exec_())
