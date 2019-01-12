import sys
import PyQt5.QtWidgets as qtw
from PyQt5.QtCore import pyqtSignal


from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
import matplotlib.pyplot as plt

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
        
        
        self.canvas = ImgCanvas(parent = self)
        layout.addWidget(self.canvas)
        self.canvas.mouse_pressed_signal.connect(self.mouse_pressed_on_canvas)
        
        self.show()
        self.update()
        
        
    def mouse_pressed_on_canvas(self, x, y):
        self.annotator.add_object(x, y)
        self.update()
        
    def update(self):
        ax = self.canvas.ax
        
        for to_remove in ax.images + ax.collections:
            to_remove.remove()
            
        
        ax.imshow(self.annotator.image)
        ax.scatter(
            x = [ob.x for ob in self.annotator.objects], 
            y = [ob.y for ob in self.annotator.objects], 
            c = "white"
        )
        
        self.canvas.draw()
        
        
        
    
        
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
    
        
 

        
if __name__ == '__main__':
    annotator = Annotator(
        image_dir = r"D:\python_source\piannot\data", 
        annotation_dir = r"D:\python_source\piannot\data",
        cats = ["ball", "head1", "heads2"]
    )
    app = qtw.QApplication(sys.argv)
    ex = MainWindow(annotator)
    sys.exit(app.exec_())
