import sys
import time

import numpy as np

from matplotlib.backends.backend_qtagg import FigureCanvas
from matplotlib.backends.backend_qtagg import \
    NavigationToolbar2QT as NavigationToolbar
#from matplotlib.backends.qt_compat import QtWidgets
from matplotlib.figure import Figure
from PyQt5 import QtWidgets, uic


from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg



class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(ApplicationWindow, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('plot.ui', self) # Load the .ui file
        
        #this is a canvas object from MatPlotLib for PyQt
        self.static_canvas = FigureCanvas(Figure(figsize=(5, 3)))
        #add the navigation bar inside the widget
        self.verticalLayout.addWidget(NavigationToolbar(self.static_canvas, self))
        #add the canvas inside the widget
        self.verticalLayout.addWidget(self.static_canvas)

    def draw_plot(self):
        #CHANGE HERE: Change this according to your problem
        self._static_ax = self.static_canvas.figure.subplots()
        t = np.linspace(0, 10, 501)
        m = np.random.rand(128,128)
        #self._static_ax.plot(t, np.tan(t), ".")
        self._static_ax.imshow(m)

if __name__ == "__main__":
    qapp = QtWidgets.QApplication.instance()
    if not qapp:
        qapp = QtWidgets.QApplication(sys.argv)

    app = ApplicationWindow()
    app.show()
    app.draw_plot()
    qapp.exec()