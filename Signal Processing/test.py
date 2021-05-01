#import sys
#from PySide2 import QtWidgets # import PySide2 before matplotlib

#import matplotlib
#from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
#from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
#from matplotlib.figure import Figure
#matplotlib.use("Qt5Agg")

#class MplCanvas(FigureCanvasQTAgg):
#  def __init__(self, parent=None, width=5, height=4, dpi=100):
#      fig = Figure(figsize=(width, height), dpi=dpi)
#      self.axes = fig.add_subplot(111)
#      super().__init__(fig)


#class MainWindow(QtWidgets.QMainWindow):
#  def __init__(self):
#      super().__init__()
#      sc = MplCanvas(self, width=5, height=4, dpi=100)
#      sc.axes.plot([0, 1, 2, 3, 4], [10, 1, 20, 3, 40])
#      # Create toolbar, passing canvas as first parament, parent(self, the MainWindow) as second.
#      toolbar = NavigationToolbar(sc, self)
#      layout = QtWidgets.QVBoxLayout()
#      layout.addWidget(toolbar)
#      layout.addWidget(sc)
#      # Create a placeholder widget to hold our toolbar and canvas.
#      widget = QtWidgets.QWidget()
#      widget.setLayout(layout)
#      self.setCentralWidget(widget)
#      self.show()

#app = QtWidgets.QApplication(sys.argv)
#w = MainWindow()
#app.exec_()

###################################################################################"

import sys
import os

from PySide2.QtWidgets import *
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as Navi
from matplotlib.figure import Figure
from scipy import signal
import matplotlib.pyplot as plot

import  numpy  as  np 
import  random
from PySide2.QtWidgets import QApplication


# ------------------ MplWidget ------------------ 
class MatplotlibCanvas(FigureCanvasQTAgg):
	def __init__(self,parent=None, dpi = 120):
		fig = Figure(dpi = dpi)
		self.axes = fig.add_subplot(111)
		super(MatplotlibCanvas,self).__init__(fig)
		fig.tight_layout()


class MainWidget(QWidget):
    
    def __init__(self):
        
        QWidget.__init__(self)

        full_path = os.path.realpath(__file__)
        path, filename = os.path.split(full_path)
        designer_file = QFile(path + "\\form.ui")
        designer_file.open(QFile.ReadOnly)

        loader = QUiLoader()
        self.ui = loader.load(designer_file, self)
        #hLayout = QHBoxLayout()
        #hLayout = self.ui.horizontalLayout
        centralwidget = QtWidgets.QWidget(self)
        canv = MatplotlibCanvas(self)
        df = []
        toolbar = Navi(canv,centralwidget)
        #hLayout.addWidget(toolbar)
        self.ui.horizontalLayout.addWidget(toolbar)
        #loader.registerCustomWidget(MplWidget)
        
        canv.axes.cla()
        ax = canv.axes
        #df.plot(ax = canv.axes)
        ax.set_xlabel('X axis')
        ax.set_ylabel('Y axis')
        xaxis = np.array([2, 8])
        yaxis = np.array([4, 9])
        canv.axes.plot(xaxis, yaxis)
        canv.draw()

        self.ui.verticalLayout.addWidget(canv)

        designer_file.close()

        #self.ui.pushButton.clicked.connect(self.update_graph)

        #self.setWindowTitle("PySide2 & Matplotlib Example GUI")

        grid_layout = QGridLayout() 
        grid_layout.addWidget(self.ui) 
        self.setLayout(grid_layout)


app = QApplication([]) 
window = MainWidget() 
window.show() 
app.exec_()

##############################################################################
