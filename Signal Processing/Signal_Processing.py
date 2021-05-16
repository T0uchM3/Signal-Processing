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
        self.ui.custFunc.stateChanged.connect(self.customFunction)

        self.setWindowTitle("PySide2 & Matplotlib Example GUI")

        grid_layout = QGridLayout() 
        grid_layout.addWidget(self.ui) 
        self.setLayout(grid_layout)

        #xaxis = np.array([2, 8])
        #yaxis = np.array([4, 9])
        #self.ui.MplWidget.canvas.axes.plot(xaxis, yaxis)
        
    def customFunction(self):
        if self.ui.custFunc.isChecked():
            self.ui.funcText.setEnabled(True)
            self.ui.funcStyle.setEnabled(True)
            self.ui.funcType.setEnabled(False)
            #self.ui.periodSpin.setEnabled(False)
        else:
            self.ui.funcText.setEnabled(False)
            self.ui.funcStyle.setEnabled(False)
            self.ui.funcType.setEnabled(True)
            #self.ui.periodSpin.setEnabled(True)

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
            
            cosinus_signal  =  np.cos ( 2 * np.pi * f * t ) 
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

            #x = np.linspace(-np.pi*self.coef, np.pi*self.coef, 1000)
            #x =  np.linspace(np.pi, 3*np.pi, 1000)
            #y = 1*np.cos(x)#↑(*amplitude)  
            xx, yy = self.generate_sine_wave(2, 44100, 5)
            #txx = np.linspace(0, 1, 1000)
            #txx = np.linspace(-np.pi*self.coef, np.pi*self.coef, 1000)
            #txx = np.linspace(-1*self.coef, 1*self.coef, 1000, endpoint=True)


            tString = self.ui.tTextField.text()
            if tString.split(',')[0].find("pi")>=0:
                if tString.split(',')[0][0:1]=="-":
                    SampleStart = -np.pi
                else:
                    SampleStart = np.pi
            else:
                if tString.split(',')[0][0:1]=="-":
                    SampleStart = -(int(tString.split(',')[0][1:len(tString.split(',')[0])]))
                else:
                    SampleStart = int(tString.split(',')[0])

            if tString.split(',')[1].find("pi")>=0:

                if tString.split(',')[1][0:1]=="-":
                    SampleEnd = -np.pi
                else:
                    SampleEnd = np.pi
            else:
                if tString.split(',')[1][0:1]=="-":
                    SampleEnd =  -(int(tString.split(',')[1][1:len(tString.split(',')[1])]))
                else:
                    SampleEnd = int(tString.split(',')[1])

            SampleRate = int(tString.split(',')[2])
            #print("ggggg",tString.split(',')[1].find("pi"))
            x = np.linspace(SampleStart*self.coef, SampleEnd*self.coef, SampleRate)
            #print(SampleStart,",",SampleEnd,",",SampleRate)
            #print(tString.split(',')[1].find("pi"))
            #print(tString.split(',')[2])


            if(self.ui.funcType.currentText()=="Sin"):
                y = 1*np.sin(x)
            elif(self.ui.funcType.currentText()=="Cos"):
                y = 1*np.cos(x)#↑(*amplitude)
            else:
                y = np.sinc(x)
            #canv.axes.plot(xx,yy)
            if not self.ui.custFunc.isChecked():
                canv.axes.plot(x,y)
            else:
                funcString = self.ui.funcText.text()#A Cos ( B Pi C t )
                piPos = funcString.find("pi")
                cosPos = funcString.find("cos") 
                sinPos = funcString.find("sin")
                if cosPos>0:
                    csPos = cosPos
                if sinPos>0:
                    csPos = sinPos
                if piPos>0:
                    funcA=int(funcString[0:csPos])
                    funcB=int(funcString[csPos+4:piPos])
                    funcC=int(funcString[piPos+2:len(funcString)-1])
                    print(funcA," ",funcB, " ",funcC)
                    #print(afterPi)
                    if cosPos>0:
                        canv.axes.plot(x,funcA*np.cos(funcB*np.pi*funcC*x))
                    if sinPos>0:
                        canv.axes.plot(txx,funcA*np.sin(funcB*np.pi*funcC*x))


            #canv.axes.plot(txx,2*np.cos(2*np.pi*5*txx))
            #canv.axes.plot(txx,2*np.cos(2*np.pi*5*txx))

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

            

            
            #canv.axes.set_ylim(bottom=0)
            #canv.axes.set_xlim(xmin=0)
            startView = self.ui.startSpin.value()
            endView = self.ui.endSpin.value()
            startViewY = self.ui.yStartSpin.value()
            endViewY = self.ui.yEndSpin.value()
            canv.axes.set_ylim(startViewY,endViewY)
            canv.axes.set_xlim(startView, endView)

            #canv.axes.axhline(color='red', lw=0.5)
            #canv.axes.axvline(color='green', lw=0.5)


            if self.ui.piCheck.isChecked():
                canv.axes.xaxis.set_major_formatter(FuncFormatter(
                 lambda val,pos: '{:.0g}$\pi$'.format(val/np.pi) if val !=0 else '0'))
                canv.axes.xaxis.set_major_locator(MultipleLocator(base=np.pi))

            if self.ui.zMid.isChecked():
                canv.axes.set_xlim(-np.pi, np.pi)
            canv.axes.grid(True)
            canv.draw()
            canv.figure.tight_layout()
            


app = QApplication([]) 
window = MainWidget() 
window.show() 
app.exec_()







