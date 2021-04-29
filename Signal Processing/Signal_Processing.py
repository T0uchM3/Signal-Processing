import sys
import os

from PySide2.QtWidgets import *
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader

from matplotlib.backends.backend_qt5agg import FigureCanvas ,  NavigationToolbar2QT  as  NavigationToolbar
from matplotlib.figure import Figure
import  numpy  as  np 
import  random

#loader = QUiLoader()
#app = QtWidgets.QApplication(sys.argv)
#window = loader.load("form.ui", None)
#window.show()
#app.exec_()

###############################################
###############################################

#class MplCanvas(FigureCanvasQTAgg):

#    def __init__(self, parent=None, width=5, height=4, dpi=100):
#        fig = Figure(figsize=(width, height), dpi=dpi)
#        self.axes = fig.add_subplot(111)
#        super(MplCanvas, self).__init__(fig)


#class MainWindow(QtWidgets.QMainWindow):

#    def __init__(self, *args, **kwargs):
#        super(MainWindow, self).__init__(*args, **kwargs)

#        # Create the maptlotlib FigureCanvas object,
#        # which defines a single set of axes as self.axes.
#        sc = MplCanvas(self, width=5, height=4, dpi=100)
#        sc.axes.plot([0,1,2,3,4], [10,1,20,3,40])
#        self.setCentralWidget(sc)

#        self.show()


#app = QtWidgets.QApplication(sys.argv)
#w = MainWindow()
#app.exec_()

# ------------------ MplWidget ------------------ 
class  MplWidget ( QWidget ):
    
    def  __init__ ( self ,  parent  =  None ):
        
        QWidget . __init__ ( self ,  parent )
        
        self . canvas  =  FigureCanvas ( Figure ())
        
        vertical_layout  =  QVBoxLayout () 
        vertical_layout . addWidget ( self . canvas ) 
        vertical_layout . addWidget ( NavigationToolbar ( self . canvas ,  self ))
        
        self . canvas . axes  =  self . canvas . figure . add_subplot ( 111 ) 
        self . setLayout ( vertical_layout )



# ------------------ MainWidget ------------------ 
class  MainWidget ( QWidget ):
    
    def  __init__ ( self ):
        
        QWidget . __init__ ( self )

        designer_file  =  QFile ( "form.ui" ) 
        designer_file . open ( QFile . ReadOnly )

        loader  =  QUiLoader () 
        loader . registerCustomWidget ( MplWidget ) 
        self . ui  =  loader . load ( designer_file ,  self )

        designer_file . close ()

        self . ui . pushButton . clicked . connect ( self . update_graph )

        self . setWindowTitle ( "PySide2 & Matplotlib Example GUI" )

        grid_layout  =  QGridLayout () 
        grid_layout . addWidget ( self . ui ) 
        self . setLayout ( grid_layout )

    def  update_graph ( self ):
        
            fs  =  500 
            f  =  random . randint ( 1 ,  100 ) 
            ts  =  1 / fs 
            length_of_signal  =  100 
            t  =  np . linspace ( 0 , 1 , length_of_signal )
        
            cosinus_signal  =  np . cos ( 2 * np . pi * f * t ) 
            sinus_signal  =  np . sin ( 2 * np . pi * f * t )

            self . ui . MplWidget . canvas . axes . clear () 
            self . ui . MplWidget . canvas . axes . plot ( t ,  cosinus_signal ) 
            self . ui . MplWidget . canvas . axes . plot ( t ,  sinus_signal ) 
            self . ui . MplWidget . canvas . axes. legend (( 'cosinus' ,  'sinus' ), loc = 'upper right' ) 
            self . ui . MplWidget . canvas . axes . set_title ( ' Cosinus - Sinus Signals' ) 
            self . ui . MplWidget . canvas . draw ()


app  =  QApplication ([]) 
window  =  MainWidget () 
window . show () 
app . exec_ ()









