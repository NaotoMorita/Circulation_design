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
        self.setTitle("設計変数 　※各翼終端位置は計算精度確保のため10mm単位で入力のこと")

        #フォント設定
        font = QtGui.QFont()
        font.setPointSize(12)


        self.lift_maxbending_input = QtGui.QWidget(parent = self)
        self.lift_maxbending_input.liftlabel = QtGui.QLabel("揚力(kgf) : ", parent = self.lift_maxbending_input)
        self.lift_maxbending_input.bendinglabel = QtGui.QLabel("  最大たわみ(mm) : ", parent = self.lift_maxbending_input)
        self.lift_maxbending_input.wireposlabel = QtGui.QLabel("  ワイヤー取付位置(mm) : ", parent = self.lift_maxbending_input)
        self.lift_maxbending_input.forcewirelabel = QtGui.QLabel("  ワイヤー下向引張(N) : ", parent = self.lift_maxbending_input)
        self.lift_maxbending_input.velocitylabel = QtGui.QLabel("  速度(m/s) : ", parent = self.lift_maxbending_input)

        self.lift_maxbending_input.liftinput = QtGui.QLineEdit(parent = self.lift_maxbending_input)
        self.lift_maxbending_input.liftinput.setFixedWidth(25)
        self.lift_maxbending_input.liftinput.setText("95")
        self.lift_maxbending_input.velocityinput = QtGui.QLineEdit(parent = self.lift_maxbending_input)
        self.lift_maxbending_input.velocityinput.setFixedWidth(33)
        self.lift_maxbending_input.velocityinput.setText("7.5")
        self.lift_maxbending_input.bendinginput = QtGui.QLineEdit(parent = self.lift_maxbending_input)
        self.lift_maxbending_input.bendinginput.setFixedWidth(33)
        self.lift_maxbending_input.bendinginput.setText("2000")
        self.lift_maxbending_input.wireposinput = QtGui.QLineEdit(parent = self.lift_maxbending_input)
        self.lift_maxbending_input.wireposinput.setFixedWidth(33)
        self.lift_maxbending_input.wireposinput.setText("7000")
        self.lift_maxbending_input.forcewireinput = QtGui.QLineEdit(parent = self.lift_maxbending_input)
        self.lift_maxbending_input.forcewireinput.setFixedWidth(25)
        self.lift_maxbending_input.forcewireinput.setText("400")
        self.lift_maxbending_input.layout = QtGui.QHBoxLayout()
        self.lift_maxbending_input.layout.addStretch(1)
        self.lift_maxbending_input.layout.addWidget(self.lift_maxbending_input.liftlabel)
        self.lift_maxbending_input.layout.addWidget(self.lift_maxbending_input.liftinput)
        self.lift_maxbending_input.layout.addWidget(self.lift_maxbending_input.velocitylabel)
        self.lift_maxbending_input.layout.addWidget(self.lift_maxbending_input.velocityinput)
        self.lift_maxbending_input.layout.addWidget(self.lift_maxbending_input.bendinglabel)
        self.lift_maxbending_input.layout.addWidget(self.lift_maxbending_input.bendinginput)
        self.lift_maxbending_input.layout.addWidget(self.lift_maxbending_input.wireposlabel)
        self.lift_maxbending_input.layout.addWidget(self.lift_maxbending_input.wireposinput)
        self.lift_maxbending_input.layout.addWidget(self.lift_maxbending_input.forcewirelabel)
        self.lift_maxbending_input.layout.addWidget(self.lift_maxbending_input.forcewireinput)

        self.lift_maxbending_input.setLayout(self.lift_maxbending_input.layout)

        #桁剛性をインプットするウィジットを開くボタン
        self.EIinput = QtGui.QFrame(parent = self)
        self.EIinput.EIinputbutton = QtGui.QPushButton("EI setting",parent = self.EIinput)
        self.EIinput.EIinputbutton.setFixedWidth(100)
        self.EIinput.layout = QtGui.QHBoxLayout()
        self.EIinput.layout.addStretch(1)
        self.EIinput.layout.addWidget(self.EIinput.EIinputbutton)
        self.EIinput.setLayout(self.EIinput.layout)

        #スパン設定及び分割数設定のためのテーブルウィジット
        self.tablewidget = QtGui.QTableWidget(parent = self)
        #sizeの設定
        self.tablewidget.setMaximumSize(1000,60)
        self.tablewidget.setMinimumSize(600,60)
        #行数、列数の設定
        self.tablewidget.setColumnCount(6)
        self.tablewidget.setRowCount(1)
        #タイトル付け
        self.tablewidget.setHorizontalHeaderItem(0, QtGui.QTableWidgetItem(""))
        self.tablewidget.setHorizontalHeaderItem(1, QtGui.QTableWidgetItem("第1翼"))
        self.tablewidget.setHorizontalHeaderItem(2, QtGui.QTableWidgetItem("第2翼"))
        self.tablewidget.setHorizontalHeaderItem(3, QtGui.QTableWidgetItem("第3翼"))
        self.tablewidget.setHorizontalHeaderItem(4, QtGui.QTableWidgetItem("第4翼"))
        self.tablewidget.setHorizontalHeaderItem(5, QtGui.QTableWidgetItem("第5翼"))
        self.tablewidget.setItem(0,0,QtGui.QTableWidgetItem("各翼終端位置(mm)"))
        self.tablewidget.item(0,0).setFlags(QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled)


        #初期値を設定
        for i in range(5):
            if i != 0:
                self.tablewidget.setItem(0,i + 1,QtGui.QTableWidgetItem("{default_span}".format(default_span = 3400 * (i) + 1700)))
            else:
                self.tablewidget.setItem(0,i + 1,QtGui.QTableWidgetItem("{default_span}".format(default_span = 1700)))



        #表示に追従してセルの大きさが変化するよう設定
        hheader = self.tablewidget.horizontalHeader();
        hheader.setResizeMode(QtGui.QHeaderView.Stretch);
        vheader = self.tablewidget.verticalHeader();
        vheader.setResizeMode(QtGui.QHeaderView.Stretch);

        self.tablewidget.buttons = QtGui.QWidget(parent = self)
        self.tablewidget.insertcolumn = QtGui.QPushButton("列追加",parent = self.tablewidget.buttons)
        self.tablewidget.deletecolumn = QtGui.QPushButton("列削除",parent = self.tablewidget.buttons)
        self.tablewidget.buttons.layout = QtGui.QHBoxLayout()
        self.tablewidget.buttons.layout.addStretch(1)
        self.tablewidget.buttons.layout.addWidget(self.tablewidget.insertcolumn)
        self.tablewidget.buttons.layout.addWidget(self.tablewidget.deletecolumn)
        self.tablewidget.buttons.setLayout(self.tablewidget.buttons.layout)

        #Widgetのレイアウトを設定
        self.layout = QtGui.QVBoxLayout()
        self.layout.addWidget(self.lift_maxbending_input)
        self.layout.addWidget(self.tablewidget.buttons)
        self.layout.addWidget(self.tablewidget)
        self.layout.addWidget(self.EIinput)
        self.setLayout(self.layout)

class ResultValWidget(QtGui.QGroupBox):
    def __init__(self, parent = None):
        QtGui.QGroupBox.__init__(self, parent = parent)
        self.setTitle("計算結果")


class EIsettingWidget(QtGui.QDialog):
    def __init__(self, tablewidget, parent = None):
        QtGui.QDialog.__init__(self, parent = parent)
        self.setFixedSize(600,170)
        self.setModal(1)
        self.tabwidget = QtGui.QTabWidget(parent = self)



    def EIsetting(self,tablewidget):
        section_num = tablewidget.columnCount()-1
        self.tabwidget.clear()

        self.EIinputWidget = [QtGui.QGroupBox(parent = self) for i in range(section_num)]
        for i in range(section_num):
            self.EIinputWidget[i].setTitle("第{num}翼の剛性と線密度を入力してください".format(num = i+1))
            self.EIinputWidget[i].EIinputtable = QtGui.QTableWidget(parent = self.EIinputWidget[i])
            self.EIinputWidget[i].EIinputtable.setColumnCount(5)
            self.EIinputWidget[i].EIinputtable.setRowCount(3)
            self.EIinputWidget[i].EIinputtable.setFixedSize(570,100)
            hheader = self.EIinputWidget[i].EIinputtable.horizontalHeader();
            hheader.setResizeMode(QtGui.QHeaderView.Stretch)
            vheader = self.EIinputWidget[i].EIinputtable.verticalHeader();
            vheader.setResizeMode(QtGui.QHeaderView.Stretch)

            self.EIinputWidget[i].EIinputtable.setItem(0,0,QtGui.QTableWidgetItem("翼区切終端[mm]"))
            self.EIinputWidget[i].EIinputtable.setItem(1,0,QtGui.QTableWidgetItem("EI"))
            self.EIinputWidget[i].EIinputtable.setItem(2,0,QtGui.QTableWidgetItem("線密度[kg/m]"))
            self.EIinputWidget[i].EIinputtable.item(0,0).setFlags(QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled)
            self.EIinputWidget[i].EIinputtable.item(1,0).setFlags(QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled)
            self.EIinputWidget[i].EIinputtable.item(2,0).setFlags(QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled)

            self.EIinputWidget[i].layout = QtGui.QVBoxLayout()
            self.EIinputWidget[i].layout.addWidget(self.EIinputWidget[i].EIinputtable)
            self.EIinputWidget[i].setLayout(self.EIinputWidget[i].layout)
            self.tabwidget.addTab(self.EIinputWidget[i],"第{num}翼".format(num = i + 1))


class TR797_modified():
    def __init__(self):
        #リスト変数の定義
        self.dy = 0.01

        self.y_div = []
        self.z_div = []
        self.y_section = []
        self.Ndiv_sec = []
        self.y = []
        self.z = []
        self.phi = []

        self.dS = []

        self.sigma = []
        self.spar_weight = []
        #sigma_wireは線密度＋ワイヤー引っ張りを考慮した下向きの[N/m]
        self.sigma_wire = []

        #多角形化行列
        self.polize_mat = [[]]

        #誘導速度行列
        self.Q_ij = [[]]

        #せん断力を積分によって求める行列
        self.sh_mat = [[]]

        #モーメントを積分によって求める行列
        self.mo_mat = [[]]

        #たわみ角を積分によって求める行列
        #剛性値ベクトル
        self.EI = []
        self.vd_mat = []

        #たわみを求める行列
        self.v_mat = []

        #構造制約行列B
        self.B = [[]]

        #揚力制約行列C
        self.C = [[]]

        #最適化行列A
        self.A = [[]]

        #最適循環値
        self.gamma = []
        #誘導速度見積もり
        self.ind_vel = []

    def prepare(self,settingwidget):
        self.b = float(settingwidget.tablewidget.item(0,settingwidget.tablewidget.columnCount() - 1).text()) * 2 / 1000
        self.n_section = int(settingwidget.tablewidget.columnCount()) - 1
        self.max_tawami = float(settingwidget.lift_maxbending_input.bendinginput.text()) / 1000
        self.y_wire = float(settingwidget.lift_maxbending_input.wireposinput.text()) / 1000
        #セクションの区切りの位置
        for n in range(self.n_section):
            self.y_section.append(float(settingwidget.tablewidget.item(0,n + 1).text()) / 1000)

        i = 0
        j = 0
        self.y_div.append(round(self.dy * (1),4))
        while self.y_div[i] < self.b / 2:
            self.y_div.append(round(self.dy * (i + 2),4))
            if round(self.y_div[i],4) >= round(self.y_section[j],4) - self.dy / 2 and round(self.y_div[i],4) <= round(self.y_section[j],4) + self.dy / 2:
                self.Ndiv_sec.append(i)
                j = j + 1
            if self.y_div[i] == self.y_wire:
                self.Ndiv_wire = i
            i = i + 1
        print(self.y_div)
        #パネル幅dSの作成
        coe_tawami = self.max_tawami / (self.b / 2) ** 2
        for n in range(len(self.y_div)):
            self.z_div.append(coe_tawami * self.y_div[n] ** 2)
            if n != 0:
                self.dS.append(numpy.sqrt((self.y_div[n]-self.y_div[n-1])**2+(self.z_div[n]-self.z_div[n-1])**2))
            else:
                self.dS.append(numpy.sqrt(self.y_div[n]**2+self.z_div[n]**2))



    def matrix(self):
        pass
    def optimize(self):
        pass


def main():

    def insertcolumn():
        insertnum = settingwidget.tablewidget.columnCount()
        settingwidget.tablewidget.setColumnCount(insertnum + 1)
        settingwidget.tablewidget.setHorizontalHeaderItem(insertnum, QtGui.QTableWidgetItem("第{num}翼".format(num = insertnum)))

        i = insertnum-1
        print(i)
        eisettingwidget.EIinputWidget.append(QtGui.QGroupBox(parent = eisettingwidget))
        print(eisettingwidget.EIinputWidget)
        eisettingwidget.EIinputWidget[i].setTitle("第{num}翼の剛性と線密度を入力してください".format(num = i + 1))
        eisettingwidget.EIinputWidget[i].EIinputtable = QtGui.QTableWidget(parent = eisettingwidget.EIinputWidget[i])
        eisettingwidget.EIinputWidget[i].EIinputtable.setColumnCount(5)
        eisettingwidget.EIinputWidget[i].EIinputtable.setRowCount(3)
        eisettingwidget.EIinputWidget[i].EIinputtable.setFixedSize(570,100)
        hheader = eisettingwidget.EIinputWidget[i].EIinputtable.horizontalHeader();
        hheader.setResizeMode(QtGui.QHeaderView.Stretch)
        vheader = eisettingwidget.EIinputWidget[i].EIinputtable.verticalHeader();
        vheader.setResizeMode(QtGui.QHeaderView.Stretch)

        eisettingwidget.EIinputWidget[i].EIinputtable.setItem(0,0,QtGui.QTableWidgetItem("翼区切終端[mm]"))
        eisettingwidget.EIinputWidget[i].EIinputtable.setItem(1,0,QtGui.QTableWidgetItem("EI"))
        eisettingwidget.EIinputWidget[i].EIinputtable.setItem(2,0,QtGui.QTableWidgetItem("線密度[kg/m]"))
        eisettingwidget.EIinputWidget[i].EIinputtable.item(0,0).setFlags(QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled)
        eisettingwidget.EIinputWidget[i].EIinputtable.item(1,0).setFlags(QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled)
        eisettingwidget.EIinputWidget[i].EIinputtable.item(2,0).setFlags(QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled)

        eisettingwidget.EIinputWidget[i].layout = QtGui.QVBoxLayout()
        eisettingwidget.EIinputWidget[i].layout.addWidget(eisettingwidget.EIinputWidget[i].EIinputtable)
        eisettingwidget.EIinputWidget[i].setLayout(eisettingwidget.EIinputWidget[i].layout)
        eisettingwidget.tabwidget.addTab(eisettingwidget.EIinputWidget[i],"第{num}翼".format(num = i + 1))

    def deletecolumn():
        deletenum = settingwidget.tablewidget.columnCount()
        if deletenum != 2:
            settingwidget.tablewidget.setColumnCount(deletenum-1)
            hheader = settingwidget.tablewidget.horizontalHeader();
            hheader.setResizeMode(QtGui.QHeaderView.Stretch);
        eisettingwidget.tabwidget.removeTab(deletenum-2)
        eisettingwidget.EIinputWidget.pop(deletenum-2)

    def EIsettingshow():
        def readcelltext(table, row, column):
            if isinstance(table,QtGui.QTableWidget):
                cell = table.item(row, column)
                celltext = cell.text()
                return celltext

        y_div = []
        spar_default_divpos = []
        for i_wing in range(settingwidget.tablewidget.columnCount() - 1):
            y_div.append([])
            spar_default_divpos.append([])
            y_div[i_wing] = float(readcelltext(settingwidget.tablewidget,0,i_wing + 1))
            print(eisettingwidget.EIinputWidget)
            if isinstance(eisettingwidget.EIinputWidget[i_wing].EIinputtable.item(0,2),type(None)):
                #サンプル桁剛性値
                EIsample_list = [34375000000,36671000000,16774000000,8305800000,1864800000]
                if i_wing >= 5:
                    EIsample_list.append(100000000)
                #サンプル線密度
                sigmasample_list = [0.377,0.357,0.284,0.245,0.0929]
                if i_wing >= 5:
                    sigmasample_list.append(0.0800)
                #剛性設定ウィジットに表示する初期値のリスト
                if i_wing != 0:
                    spar_default_divpos[i_wing] = [(y_div[i_wing] - y_div[i_wing-1]) / 4,(y_div[i_wing] - y_div[i_wing-1]) / 2, (y_div[i_wing] - y_div[i_wing-1]) * 3 / 4, y_div[i_wing] - y_div[i_wing-1]]
                else:
                    spar_default_divpos[i_wing] = [(y_div[i_wing]) / 4,(y_div[i_wing]) / 2, (y_div[i_wing]) * 3 / 4,y_div[i_wing]]
                for i_spardiv in range(4):
                    eisettingwidget.EIinputWidget[i_wing].EIinputtable.setItem(0,i_spardiv + 1,QtGui.QTableWidgetItem("{spar_div}".format(spar_div = spar_default_divpos[i_wing][i_spardiv])))
                    #noneditableに
                    eisettingwidget.EIinputWidget[i_wing].EIinputtable.item(0,i_spardiv + 1).setFlags(QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled)
                    #桁剛性値サンプルのセット
                    eisettingwidget.EIinputWidget[i_wing].EIinputtable.setItem(1,i_spardiv + 1,QtGui.QTableWidgetItem("{EI_sample}".format(EI_sample = EIsample_list[i_wing])))
                    #桁線密度サンプルのセット
                    eisettingwidget.EIinputWidget[i_wing].EIinputtable.setItem(2,i_spardiv + 1,QtGui.QTableWidgetItem("{sigma_sample}".format(sigma_sample = sigmasample_list[i_wing])))
        eisettingwidget.show()

    def resultshow():
        pass
    def calculation():
        TR797_opt.prepare(settingwidget)


    qApp = QtGui.QApplication(sys.argv)

    mainwindow = QtGui.QMainWindow()
    mainpanel = QtGui.QWidget()

    resulttabwidget = ResultTabWidget()
    exeexportbutton = ExeExportButton()
    settingwidget = SettingWidget()
    resultvalwidget = ResultValWidget(settingwidget.tablewidget)
    eisettingwidget = EIsettingWidget(settingwidget.tablewidget)
    eisettingwidget.EIsetting(settingwidget.tablewidget)
    TR797_opt = TR797_modified()

    mainpanel_layout = QtGui.QVBoxLayout()
    mainpanel_layout.addWidget(resulttabwidget)
    mainpanel_layout.addWidget(resultvalwidget)
    mainpanel_layout.addWidget(exeexportbutton)
    mainpanel_layout.addWidget(settingwidget)
    mainpanel.setLayout(mainpanel_layout)
    mainwindow.setCentralWidget(mainpanel)

    mainwindow.show()

    settingwidget.connect(settingwidget.tablewidget.insertcolumn,QtCore.SIGNAL('clicked()'),insertcolumn)
    settingwidget.connect(settingwidget.tablewidget.deletecolumn,QtCore.SIGNAL('clicked()'),deletecolumn)
    settingwidget.connect(settingwidget.EIinput.EIinputbutton,QtCore.SIGNAL('clicked()'),EIsettingshow)
    exeexportbutton.connect(exeexportbutton.exebutton,QtCore.SIGNAL('clicked()'),calculation)

    sys.exit(qApp.exec_())

if __name__ == '__main__':
    main()
