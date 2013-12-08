#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      NaotoMORITA
#
# Created:     09/12/2013
# Copyright:   (c) NaotoMORITA 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import numpy, csv

import sys, os, random, copy
from PyQt4 import QtGui, QtCore

import matplotlib.backends.backend_qt4agg
import matplotlib.backends.backend_agg

class Dataplot(matplotlib.backends.backend_qt4agg.FigureCanvasQTAgg):
    def __init__(self, parent=None, width=6, height=3, dpi=50):
        fig = matplotlib.figure.Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        self.axes.tick_params(axis='both', which='major', labelsize=10)
        self.axes.hold(False)

        matplotlib.backends.backend_qt4agg.FigureCanvasQTAgg.__init__(self, fig)
        self.setParent(parent)

        matplotlib.backends.backend_qt4agg.FigureCanvasQTAgg.setSizePolicy(self,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding)
        matplotlib.backends.backend_qt4agg.FigureCanvasQTAgg.updateGeometry(self)

    def drowplot(self,x,y):
        if not isinstance(x,list) or not isinstance(y,list):
            print("not list")
        else:
            self.axes.plot(x,y)
            self.draw()

class ResultTabWidget(QtGui.QTabWidget):
    def __init__(self, parent = None):
        QtGui.QTabWidget.__init__(self, parent = parent)

        self.circulation_graph = Dataplot()
        self.bending_graph     = Dataplot()

        self.addTab(self.circulation_graph,"循環分布")
        self.addTab(self.bending_graph,"たわみ")


def main():
    qApp = QtGui.QApplication(sys.argv)

    resulttabwidget = ResultTabWidget()
    resulttabwidget.show()
    #dataplot.drowplot([[0],[1]],[[1],[2]])
    sys.exit(qApp.exec_())

if __name__ == '__main__':
    main()
