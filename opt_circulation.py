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

class ExeExportButton(QtGui.QWidget):
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent = parent)

        self.exebutton = QtGui.QPushButton("exe",parent = self)
        self.exportbutton = QtGui.QPushButton("export",parent = self)
        self.do_stracutual = QtGui.QCheckBox("構造考慮",parent = self)

        layout = QtGui.QHBoxLayout()
        layout.addStretch(1)
        layout.addWidget(self.do_stracutual)
        layout.addWidget(self.exebutton)
        layout.addWidget(self.exportbutton)

        self.setLayout(layout)

class SettingWidget(QtGui.QGroupBox):
    def __init__(self, parent = None):
        QtGui.QGroupBox.__init__(self, parent = parent)
        self.setTitle("設計変数")

        #フォント設定
        font = QtGui.QFont()
        font.setPointSize(12)


        self.lift_maxbending_input = QtGui.QWidget(parent = self)
        self.lift_maxbending_input.liftlabel = QtGui.QLabel("揚力(kgf) : ", parent = self.lift_maxbending_input)
        self.lift_maxbending_input.bendinglabel = QtGui.QLabel("  最大たわみ(mm) : ", parent = self.lift_maxbending_input)
        self.lift_maxbending_input.liftinput = QtGui.QLineEdit(parent = self.lift_maxbending_input)
        self.lift_maxbending_input.liftinput.setFixedWidth(25)
        self.lift_maxbending_input.liftinput.setText("95")

        self.lift_maxbending_input.bendinginput = QtGui.QLineEdit(parent = self.lift_maxbending_input)
        self.lift_maxbending_input.bendinginput.setFixedWidth(33)
        self.lift_maxbending_input.bendinginput.setText("2000")
        self.lift_maxbending_input.layout = QtGui.QHBoxLayout()
        self.lift_maxbending_input.layout.addStretch(1)
        self.lift_maxbending_input.layout.addWidget(self.lift_maxbending_input.liftlabel)
        self.lift_maxbending_input.layout.addWidget(self.lift_maxbending_input.liftinput)
        self.lift_maxbending_input.layout.addWidget(self.lift_maxbending_input.bendinglabel)
        self.lift_maxbending_input.layout.addWidget(self.lift_maxbending_input.bendinginput)
        self.lift_maxbending_input.setLayout(self.lift_maxbending_input.layout)

        #桁剛性をインプットするウィジットを開くボタン
        self.EIinputbutton = QtGui.QPushButton("EI setting",parent = self)


        #スパン設定及び分割数設定のためのテーブルウィジット
        self.tablewidget = QtGui.QTableWidget(parent = self)
        #sizeの設定
        self.tablewidget.setMaximumSize(1000,100)
        self.tablewidget.setMinimumSize(500,100)
        #行数、列数の設定
        self.tablewidget.setColumnCount(5)
        self.tablewidget.setRowCount(2)
        #タイトル付け
        self.tablewidget.setHorizontalHeaderItem(0, QtGui.QTableWidgetItem(""))
        self.tablewidget.setHorizontalHeaderItem(1, QtGui.QTableWidgetItem("第1翼"))
        self.tablewidget.setHorizontalHeaderItem(2, QtGui.QTableWidgetItem("第2翼"))
        self.tablewidget.setHorizontalHeaderItem(3, QtGui.QTableWidgetItem("第3翼"))
        self.tablewidget.setHorizontalHeaderItem(4, QtGui.QTableWidgetItem("第4翼"))
        self.tablewidget.setItem(0,0,QtGui.QTableWidgetItem("各翼終端位置(mm)"))
        self.tablewidget.setItem(1,0,QtGui.QTableWidgetItem("翼素分割数"))
        #表示に追従してセルの大きさが変化するよう設定
        hheader = self.tablewidget.horizontalHeader();
        hheader.setResizeMode(QtGui.QHeaderView.Stretch);
        vheader = self.tablewidget.verticalHeader();
        vheader.setResizeMode(QtGui.QHeaderView.Stretch);

        #Widgetのレイアウトを設定
        self.layout = QtGui.QVBoxLayout()
        self.layout.addWidget(self.lift_maxbending_input)
        self.layout.addWidget(self.tablewidget)
        self.layout.addWidget(self.EIinputbutton)
        self.setLayout(self.layout)




def main():
    qApp = QtGui.QApplication(sys.argv)

    mainwindow = QtGui.QMainWindow()
    mainpanel = QtGui.QWidget()

    resulttabwidget = ResultTabWidget()
    exeexportutton = ExeExportButton()
    settingwidget = SettingWidget()

    mainpanel_layout = QtGui.QVBoxLayout()
    mainpanel_layout.addWidget(resulttabwidget)
    mainpanel_layout.addWidget(exeexportutton)
    mainpanel_layout.addWidget(settingwidget)
    mainpanel.setLayout(mainpanel_layout)
    mainwindow.setCentralWidget(mainpanel)

    mainwindow.show()
    sys.exit(qApp.exec_())

if __name__ == '__main__':
    main()
