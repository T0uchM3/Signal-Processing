import sys
import os
from PySide2.QtWidgets import *
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader

from matplotlib.backends.backend_qt5agg import FigureCanvas ,  NavigationToolbar2QT  as  NavigationToolbar
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as Navi
from matplotlib.figure import Figure
from matplotlib.ticker import FuncFormatter, MultipleLocator
from scipy import signal
import matplotlib.pyplot as plot

import  numpy  as  np 
import  random
from PySide2.QtWidgets import QApplication




# ------------------ MplWidget ------------------ 
class MatplotlibCanvas(FigureCanvasQTAgg):
    def __init__(self,parent=None, dpi = 100):
        fig = Figure(dpi = dpi)
        self.axes =fig.add_subplot(111)
        super(MatplotlibCanvas,self).__init__(fig)

        fig.tight_layout()

class MplWidget(QWidget):
    
    def __init__(self, parent = None):
        
        QWidget.__init__(self, parent)
        
        #self.canvas = FigureCanvas(Figure())
        self.canvas = MatplotlibCanvas(self)
        
        vertical_layout = QVBoxLayout() 
        vertical_layout.addWidget(self.canvas)
        #vertical_layout.addWidget(NavigationToolbar(self.canvas, self))
        
        #self.canvas.axes = self.canvas.figure.add_subplot(111)
        self.setLayout(vertical_layout)




        #self.canvas.figure.tight_layout()
        #t = np.linspace(0, 1, 1000, endpoint=True)
        #plot.plot(t, signal.square(2 * np.pi * 5 * t))
        #plot.title('Sqaure wave - 5 Hz sampled at 1000 Hz /second')
        #plot.xlabel('Time')
        #plot.show()
# ------------------ MainWidget ------------------
class MainWidget(QWidget):
    coef = 0
    def __init__(self):
        
        QWidget.__init__(self)

        full_path = os.path.realpath(__file__)
        path, filename = os.path.split(full_path)
        designer_file = QFile(path + "\\form2.ui")
        designer_file.open(QFile.ReadOnly)

        loader = QUiLoader()
        loader.registerCustomWidget(MplWidget)
        self.ui = loader.load(designer_file, self)

        global coef
        self.coef = 1
        print("MainWidget")
        self.update_graph()

        designer_file.close()

        #self.ui.pushButton.clicked.connect(self.update_graph)

        self.ui.updateBtn.clicked.connect(self.preUpdate)

        self.setWindowTitle("PySide2 & Matplotlib Example GUI")

        grid_layout = QGridLayout() 
        grid_layout.addWidget(self.ui) 
        self.setLayout(grid_layout)

        #xaxis = np.array([2, 8])
        #yaxis = np.array([4, 9])
        #self.ui.MplWidget.canvas.axes.plot(xaxis, yaxis)
        
    def preUpdate(self):
       
        self.coef = self.ui.periodSpin.value()
       
        print("preUpdate "+str(self.coef))
        self.update_graph()

    def generate_sine_wave(self, freq, sample_rate, duration):
        x = np.linspace(0, duration, sample_rate * duration, endpoint=False)
        frequencies = x * freq
        # 2pi because np.sin takes radians
        y = np.sin((2 * np.pi) * frequencies)
        return x, y
    def update_graph(self):
            print("update_graph "+str(self.coef))
            fs = 500
            f = random.randint(1, 100) 
            ts = 1/fs 
            length_of_signal = 100 
            t = np.linspace(0, 1, length_of_signal)
            #t = np.linspace(0, 1, 1000, endpoint=True)
            
            #cosinus_signal  =  np.cos ( 2 * np.pi * f * t ) 
            #sinus_signal  =  np.sin ( 2 * np.pi * f * t )

            xaxis = np.array([2, 8])
            yaxis = np.array([4, 9])
            T=1
            sinSig = np.sin(2 *np.pi*t/T)
            rang = np.arange(0.0, 1.0, 0.01)
            #plt.plot(xaxis, yaxis)
            #plt.show()
            centralwidget = QtWidgets.QWidget(self)
            canv = MatplotlibCanvas(self)
            canv = self.ui.MplWidget.canvas
            toolbar = Navi(canv,centralwidget)
            #toolbar.resize(200,100)
            toolbar.setFixedHeight(25)
            #self.ui.horizontalLayout = None
            if self.ui.horizontalLayout.count()>0:#preventing multiple toolbars
                self.ui.horizontalLayout.itemAt(0).widget().deleteLater()
            self.ui.horizontalLayout.addWidget(toolbar)
            canv.axes.clear() 
            #self.ui.MplWidget.canvas.axes.plot( t ,  cosinus_signal )   #plot takes 2 parameters, 1 for x axis, 2 for y axis 
            #self.ui.MplWidget.canvas.axes.plot( t ,  sinus_signal ) 
            tt = np.arange(0.0,2.0,0.01)
            ss = 1 + np.sin(2* np.pi * tt)
            #x = np.linspace(-np.pi, np.pi, 100)
            #y = 2*np.sin(x)
            
            #x = np.linspace(-5*np.pi,5*np.pi,100)
            #y = np.sin(x)/x
            print(str(self.coef)+' COEF')

            x = np.linspace(-np.pi*self.coef, np.pi*self.coef, 100)
            y = 2*np.cos(x)#↑
            xx, yy = self.generate_sine_wave(2, 44100, 5)
            canv.axes.plot(xx,yy)
            #self.ui.MplWidget.canvas.axes.plot(t, signal.square(2 * np.pi * 5 * t))
            #canv.axes.legend(('cosinus', 'sinus'), loc = 'upper right')
            canv.axes.set_title(' Cosinus - Sinus Signals')
            #self.ui.MplWidget.canvas.axes.plot.axhline(y=0, color='k')
            #canv.axes.set_xlabel('X axis')
            #canv.axes.set_ylabel('Y axis')
            
            canv.axes.spines['left'].set_position('center')
            canv.axes.spines['bottom'].set_position('center')

            # Eliminate upper and right axes
            canv.axes.spines['right'].set_color('none')
            canv.axes.spines['top'].set_color('none')

            # Show ticks in the left and lower axes only
            canv.axes.xaxis.set_ticks_position('bottom')
            canv.axes.yaxis.set_ticks_position('left')

            #canv.axes.set_xlim(-np.pi, np.pi)

            #canv.axes.set_ylim(bottom=0)
            #canv.axes.set_xlim(xmin=0)

            #canv.axes.axhline(color='red', lw=0.5)
            #canv.axes.axvline(color='green', lw=0.5)

            if self.ui.piCheck.isChecked():
                canv.axes.xaxis.set_major_formatter(FuncFormatter(
                 lambda val,pos: '{:.0g}$\pi$'.format(val/np.pi) if val !=0 else '0'))
                canv.axes.xaxis.set_major_locator(MultipleLocator(base=np.pi))
            canv.axes.grid(True)
            canv.draw()
            canv.figure.tight_layout()
            


app = QApplication([]) 
window = MainWidget() 
window.show() 
app.exec_()







