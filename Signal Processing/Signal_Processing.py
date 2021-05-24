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
from numpy import fft as fft
import  numpy  as  np 
import  random
import wave
from PySide2.QtWidgets import QApplication
import scipy.fftpack
import scipy.io.wavfile
import scipy.integrate as integrate
from scipy.integrate import quad
import scipy.special as special
from sympy import *
from sympy import inverse_fourier_transform, exp, sqrt, pi

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
        
        self.canvas = MatplotlibCanvas(self)
        
        vertical_layout = QVBoxLayout() 
        vertical_layout.addWidget(self.canvas)
        
        self.setLayout(vertical_layout)


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
        self.dropped = False
        self.diracN = 0
        self.selectedFunc = ""
        self.update_graph()

        designer_file.close()

        self.ui.updateBtn.clicked.connect(self.preUpdate)
        self.ui.custFunc.stateChanged.connect(self.customFunction)
        self.ui.diracModifier.valueChanged.connect(self.diracChange)
        self.ui.calFunc.currentTextChanged.connect(self.calculFunction)

        self.setWindowTitle("PySide2 & Matplotlib Example GUI")

        grid_layout = QGridLayout() 
        grid_layout.addWidget(self.ui) 
        self.setLayout(grid_layout)
        self.setAcceptDrops(True)
       
    def calculFunction(self):
        self.selectedFunc= self.ui.calFunc.currentText()
        self.update_graph()
    def diracChange(self):
        self.diracN = int(self.ui.diracModifier.value())
        self.update_graph()

    def customFunction(self):
        if self.ui.custFunc.isChecked():
            self.ui.funcText.setEnabled(True)
            #self.ui.funcStyle.setEnabled(True)
            self.ui.funcType.setEnabled(False)
        else:
            self.ui.funcText.setEnabled(False)
            #self.ui.funcStyle.setEnabled(False)
            self.ui.funcType.setEnabled(True)

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
    def dragEnterEvent(self, e):
        """
        This function will detect the drag enter event from the mouse on the main window
        Like it open the window to accept file dropping
        """
        if e.mimeData().hasUrls:
            e.accept()
        else:
            e.ignore()
    def dropEvent(self,e):
        """
        This function will enable the drop file(s) directly on to the
        main window. The file location will be stored in the self.filename
        """
        for url in e.mimeData().urls():
            fname = str(url.toLocalFile())
        self.filename = fname
        print("PATH: ", self.filename)
        self.dropped = True
        self.update_graph()

    def update_graph(self):
            fs = 500
            f = random.randint(1, 100) 
            ts = 1/fs 
            length_of_signal = 100 
            #t = np.linspace(0, 1, length_of_signal)
            
            #cosinus_signal  =  np.cos ( 2 * np.pi * f * t ) 

            xaxis = np.array([2, 8])
            yaxis = np.array([4, 9])
            #T=1
            #sinSig = np.sin(2 *np.pi*t/T)
            rang = np.arange(0.0, 1.0, 0.01)
            centralwidget = QtWidgets.QWidget(self)
            canv = MatplotlibCanvas(self)
            canv = self.ui.MplWidget.canvas
            toolbar = Navi(canv,centralwidget)
            toolbar.setFixedHeight(25)
            if self.ui.horizontalLayout.count()==0:
                self.ui.horizontalLayout.addWidget(toolbar)
            canv.axes.clear() 

######test


            if self.dropped:

                with wave.open('choral2.wav','r') as wav_file:
                    #Extract Raw Audio from Wav File
                    signal = wav_file.readframes(-1)
                    signal = np.frombuffer(signal, dtype=np.int16)

                    # If Stereo
                    if signal_wave.getnchannels() == 2:
                        #Split the data into channels 
                        channels = [[] for channel in range(wav_file.getnchannels())]
                        for index, datum in enumerate(signal):
                            channels[index%len(channels)].append(datum)

                        #Get time from indices
                        fs = wav_file.getframerate()
                        Time=np.linspace(0, len(signal)//len(channels)//fs, num=len(signal)//len(channels))

                        for channel in channels:
                            canv.axes.plot(Time,channel)
                    else:
                        canv.axes.plot(signal)
                    canv.axes.grid(True)
                    canv.draw()
                    canv.figure.tight_layout()
            else:
                tt = np.arange(0.0,2.0,0.01)
                ss = 1 + np.sin(2* np.pi * tt)
            
                print(str(self.coef)+' COEF')

                xx, yy = self.generate_sine_wave(2, 44100, 5)


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

                SampleRate = float(tString.split(',')[2])
                x = np.linspace(SampleStart*self.coef, SampleEnd*self.coef, 1000)

                #Known functions
                if(self.ui.funcType.currentText()=="Sin"):
                    y = 1*np.sin(x)
                elif(self.ui.funcType.currentText()=="Cos"):
                    y = 1*np.cos(x)#↑(*amplitude)
                else:
                    y = np.sinc(x)
                if not self.ui.custFunc.isChecked() and not self.ui.diracComb.isChecked():
                    canv.axes.plot(x,y)
                    
                #custom functions
                if self.ui.custFunc.isChecked():# and not self.ui.diracComb.isChecked()
                    funcString = self.ui.funcText.text()#A Cos ( B Pi C t/D )
                    piPos = funcString.find("pi")
                    cosPos = funcString.find("cos")
                    sinPos = funcString.find("sin")
                    starPos = funcString.find("*")
                    sincPos = funcString.find("sinc")
                    plusPos = funcString.find("+")
                    if cosPos>0:
                        csPos = cosPos
                    if sinPos>0:
                        csPos = sinPos
                    if sincPos>0:
                        scPos = sincPos
                    if piPos>0:
                        if plusPos > 0:
                            func0=int(funcString[0:plusPos])
                        else:
                            func0=0
                        print("func0 ",func0)
                        funcA=int(funcString[plusPos+1:csPos])
                        print("funcA ",funcA)
                        if sincPos>0:
                            funcB=int(funcString[csPos+5:piPos])
                        else:
                            funcB=int(funcString[csPos+4:piPos])
                            
                        if self.ui.diracComb.isChecked():
                            if starPos < 0:
                                funcD = 2
                            else: 
                                funcD=int(funcString[starPos+1:len(funcString)-1])
                            funcC=int(funcString[piPos+2:starPos])
                            
                        else:
                            funcC=int(funcString[piPos+2:len(funcString)-1])
                            funcD=2
                        
                        
                        print(funcA," ",funcB, " ",funcC)
                        #print(afterPi)
                        if not self.ui.diracComb.isChecked():
                            T=Symbol('T')
                            t=Symbol('t')
                            f0 = 1/T
                            if cosPos>0:
                                canv.axes.clear()#obviously the .clear() above is just chilling 
                                canv.axes.plot(x,func0+funcA*np.cos(funcB*np.pi*funcC*x))
                                if self.selectedFunc=="Moyenne":
                                    func=(func0+funcA*cos(funcB*pi*f0*t))
                                    #func=(b0+b2*sin(9*pi*f0*t))**2
                                    result=simplify(1/T*(integrate(func, (t,0,T))))
                                    self.ui.calResult.setText(str(result))
                            if sinPos>0:
                                canv.axes.clear()
                                canv.axes.plot(x,func0+funcA*np.sin(funcB*np.pi*funcC*x))
                            if sincPos>0:
                                canv.axes.clear()
                                canv.axes.plot(x,func0+funcA*np.sinc(funcB*np.pi*funcC*x))

                        if self.ui.diracComb.isChecked():
                            """          DIRAC            """
                            N=self.diracN
                            T = funcD  # time-distance between diracs
                            Fs = 10000 # sampling frequency
                            t = np.arange(-1*self.coef, 1*self.coef, SampleRate)
                            sigSum = np.ones_like(t)
                            for n in range(1,N+1):
                                if cosPos > 0:
                                    part = funcA*np.cos(funcB*np.pi*funcC*n*t/T)
                                if sinPos > 0:
                                    part = funcA*np.sin(funcB*np.pi*funcC*n*t/T)
                                if sincPos > 0:
                                    part = funcA*np.sinc(funcB*np.pi*funcC*n*t/T)
                                sigSum = sigSum + part
                                if n < 50:
                                    canv.axes.plot(t, part, 'b-')
                            canv.axes.clear()
                            canv.axes.plot(t, sigSum, 'r-', lw=2, zorder=-1)
                            """          DIRAC END           """
                        if self.ui.FFTBox.isChecked():
                            """          FT            """
                            if cosPos>0:
                                y=funcA*np.cos(funcB*np.pi*funcC*x)
                            if sinPos>0:
                                y=funcA*np.sin(funcB*np.pi*funcC*x)
                            if sincPos>0:
                                y=funcA*np.sinc(funcB*np.pi*funcC*x)
                            # fourier transform
                            f = np.fft.fft(y)
                            # sample frequencies
                            freq = np.fft.fftfreq(len(y), d=x[1]-x[0])
                            canv.axes.clear()
                            canv.axes.plot(freq, abs(f)**2)

                        """          FT END           """


                #n = np.arange(50)
                #canv.axes.stem(np.cos(2*np.pi*1/2*n))

                if not self.ui.diracComb.isChecked():
                    canv.axes.set_title(' Cosinus - Sinus Signals')
            
                    canv.axes.spines['left'].set_position('center')
                    canv.axes.spines['bottom'].set_position('center')

                    # Eliminate upper and right axes
                    canv.axes.spines['right'].set_color('none')
                    canv.axes.spines['top'].set_color('none')

                    # Show ticks in the left and lower axes only
                    canv.axes.xaxis.set_ticks_position('bottom')
                    canv.axes.yaxis.set_ticks_position('left')
            
                #startView = self.ui.startSpin.value()
                #endView = self.ui.endSpin.value()
                #startViewY = self.ui.yStartSpin.value()
                #endViewY = self.ui.yEndSpin.value()
                #canv.axes.set_ylim(startViewY,endViewY)
                #canv.axes.set_xlim(startView, endView)

                if self.ui.piCheck.isChecked():
                    canv.axes.xaxis.set_major_formatter(FuncFormatter(
                     lambda val,pos: '{:.0g}$\pi$'.format(val/np.pi) if val !=0 else '0'))
                    canv.axes.xaxis.set_major_locator(MultipleLocator(base=np.pi))

            if self.ui.zMid.isChecked():
                canv.axes.set_xlim(-np.pi, np.pi)
            canv.axes.grid(True)
            print("reached")
            canv.draw()
            canv.figure.tight_layout()


app = QApplication([]) 
window = MainWidget() 
window.show() 
app.exec_()







