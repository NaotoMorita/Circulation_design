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

import numpy, csv,copy

import sys, os, random, copy
from PyQt4 import QtGui, QtCore

import matplotlib.backends.backend_qt4agg
import matplotlib.backends.backend_agg
import matplotlib.pyplot as plt

class Dataplot(matplotlib.backends.backend_qt4agg.FigureCanvasQTAgg):
    def __init__(self, parent=None, width=6, height=3, dpi=50):
        fig = matplotlib.figure.Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        self.axes.tick_params(axis='both', which='major', labelsize=20)
        self.axes.hold(True)

        matplotlib.backends.backend_qt4agg.FigureCanvasQTAgg.__init__(self, fig)
        self.setParent(parent)

        matplotlib.backends.backend_qt4agg.FigureCanvasQTAgg.setSizePolicy(self,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding)
        matplotlib.backends.backend_qt4agg.FigureCanvasQTAgg.updateGeometry(self)

    def drawplot(self,x,y,x2 = "None",y2 = "None",xlabel = "None",ylabel = "None",legend = "None", aspect = "equal"):

            self.axes.plot(x,y)
            if x2 != "None":
                self.axes.plot(x2,y2,'--')
            if xlabel != "None":
                self.axes.set_xlabel(xlabel,fontsize = 20)
            if ylabel != "None":
                self.axes.set_ylabel(ylabel,fontsize = 20)

            if legend != "None":
                self.axes.legend(legend,fontsize = 15)
            if aspect =="equal":
                self.axes.set_aspect("equal")

            self.draw()

class ResultTabWidget(QtGui.QTabWidget):
    def __init__(self, parent = None):
        QtGui.QTabWidget.__init__(self, parent = parent)

        self.circulation_graph = Dataplot()
        self.bending_graph     = Dataplot()
        self.bendingangle_graph= Dataplot()
        self.moment_graph      = Dataplot()
        self.shforce_graph     = Dataplot()
        self.ind_graph         = Dataplot()

        self.addTab(self.circulation_graph,"循環分布")
        self.addTab(self.ind_graph,"誘導角度[deg]")
        self.addTab(self.bending_graph,"たわみ(軸:等倍)")
        self.addTab(self.bendingangle_graph,"たわみ角[deg]")
        self.addTab(self.moment_graph,"曲げモーメント[N/m]")
        self.addTab(self.shforce_graph,"せん断力[N]")


class ExeExportButton(QtGui.QWidget):
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent = parent)

        self.exebutton = QtGui.QPushButton("計算",parent = self)
        self.exportbutton = QtGui.QPushButton("CSV出力",parent = self)
        self.do_stracutual = QtGui.QCheckBox("構造考慮",parent = self)
        self.do_stracutual.toggle()
        self.progressbar = QtGui.QProgressBar(None)
        DEFAULT_STYLE = """
        QProgressBar{
        border: 2px solid grey;
        border-radius: 5px;
        text-align: center
        }

        QProgressBar::chunk {
        background-color: lightblue;
        width: 10px;
        margin: 1px;
        }
        """
        self.progressbar.setStyleSheet(DEFAULT_STYLE)

        layout = QtGui.QHBoxLayout()
        layout.addStretch(1)
        layout.addWidget(self.progressbar)
        layout.addWidget(self.do_stracutual)
        layout.addWidget(self.exebutton)
        layout.addWidget(self.exportbutton)

        self.setLayout(layout)

class SettingWidget(QtGui.QGroupBox):
    def __init__(self, parent = None):
        QtGui.QGroupBox.__init__(self, parent = parent)
        self.setTitle("設計変数 　※各翼終端位置は計算精度確保のため50mm単位で入力すること")

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
        self.lift_maxbending_input.liftinput.setText("97")
        self.lift_maxbending_input.velocityinput = QtGui.QLineEdit(parent = self.lift_maxbending_input)
        self.lift_maxbending_input.velocityinput.setFixedWidth(33)
        self.lift_maxbending_input.velocityinput.setText("7.5")
        self.lift_maxbending_input.bendinginput = QtGui.QLineEdit(parent = self.lift_maxbending_input)
        self.lift_maxbending_input.bendinginput.setFixedWidth(33)
        self.lift_maxbending_input.bendinginput.setText("2500")
        self.lift_maxbending_input.wireposinput = QtGui.QLineEdit(parent = self.lift_maxbending_input)
        self.lift_maxbending_input.wireposinput.setFixedWidth(33)
        self.lift_maxbending_input.wireposinput.setText("6550")
        self.lift_maxbending_input.forcewireinput = QtGui.QLineEdit(parent = self.lift_maxbending_input)
        self.lift_maxbending_input.forcewireinput.setFixedWidth(25)
        self.lift_maxbending_input.forcewireinput.setText("485")
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
        self.strechwid = QtGui.QFrame(parent = self)
        self.tablewidget = QtGui.QTableWidget(parent = self.strechwid)
        #sizeの設定
        self.tablewidget.setMaximumSize(1000,100)
        self.tablewidget.setMinimumSize(600,100)
        #行数、列数の設定
        self.tablewidget.setColumnCount(7)
        self.tablewidget.setRowCount(2)
        #タイトル付け
        self.tablewidget.setHorizontalHeaderItem(0, QtGui.QTableWidgetItem(""))
        self.tablewidget.setHorizontalHeaderItem(1, QtGui.QTableWidgetItem("第1翼"))
        self.tablewidget.setHorizontalHeaderItem(2, QtGui.QTableWidgetItem("第2翼"))
        self.tablewidget.setHorizontalHeaderItem(3, QtGui.QTableWidgetItem("第3翼"))
        self.tablewidget.setHorizontalHeaderItem(4, QtGui.QTableWidgetItem("第4翼"))
        self.tablewidget.setHorizontalHeaderItem(5, QtGui.QTableWidgetItem("第5翼"))
        self.tablewidget.setHorizontalHeaderItem(6, QtGui.QTableWidgetItem("第6翼"))
        self.tablewidget.setItem(0,0,QtGui.QTableWidgetItem("各翼終端位置(mm)"))
        self.tablewidget.setItem(1,0,QtGui.QTableWidgetItem("EI・線密度調整係数"))
        self.tablewidget.item(0,0).setFlags(QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled)
        self.tablewidget.item(1,0).setFlags(QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled)


        #初期値を設定
        span_list = [2300,6900,10400,12400,16500,17000]
        for i in range(6):
                self.tablewidget.setItem(0,i + 1,QtGui.QTableWidgetItem("{default_span}".format(default_span = span_list[i])))
                self.tablewidget.setItem(1,i + 1,QtGui.QTableWidgetItem("1"))




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

        self.strechwid.layout = QtGui.QHBoxLayout()
        self.strechwid.layout.addStretch(1)
        self.strechwid.layout.addWidget(self.tablewidget)
        self.strechwid.setLayout(self.strechwid.layout)
        self.layout = QtGui.QVBoxLayout()
        self.layout.addWidget(self.lift_maxbending_input)
        self.layout.addWidget(self.tablewidget.buttons)
        self.layout.addWidget(self.strechwid)
        self.layout.addWidget(self.EIinput)
        self.setLayout(self.layout)

class ResultValWidget(QtGui.QGroupBox):
    def __init__(self, parent = None):
        font = QtGui.QFont()
        font.setPointSize(12)

        QtGui.QGroupBox.__init__(self, parent = parent)
        self.setTitle("計算結果")
        self.liftresultlabel = QtGui.QLabel("計算揚力[kgf] : {Lift}".format(Lift = "--"),parent = self)
        self.Diresultlabel = QtGui.QLabel("   抗力[N] : {Di}".format(Di = "--"),parent = self)
        self.lambda1label = QtGui.QLabel("   構造制約係数λ1[-] : {lambda1}".format(lambda1 = "--"),parent = self)
        self.lambda2label = QtGui.QLabel("   揚力制約係数λ2[-] : {lambda2}".format(lambda2 = "--"),parent = self)

        self.layout = QtGui.QHBoxLayout()
        self.layout.addStretch(1)
        self.layout.addWidget(self.liftresultlabel)
        self.layout.addWidget(self.Diresultlabel)
        self.layout.addWidget(self.lambda1label)
        self.layout.addWidget(self.lambda2label)
        self.setLayout(self.layout)

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
        self.dy = 0.05

        self.y_div = []
        self.z_div = []
        self.y_section = []
        self.Ndiv_sec = []
        self.y = []
        self.z = []
        self.phi = []

        self.dS = []

        self.sigma = []
        self.spar_weight = 0
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

    def prepare(self,settingwidget,eisettingwidget):
        self.b = round(float(settingwidget.tablewidget.item(0,settingwidget.tablewidget.columnCount() - 1).text()) * 2 / 1000,4)
        self.n_section = int(settingwidget.tablewidget.columnCount()) - 1
        self.max_tawami = float(settingwidget.lift_maxbending_input.bendinginput.text()) / 1000
        self.y_wire = float(settingwidget.lift_maxbending_input.wireposinput.text()) / 1000
        self.rho = 1.184
        self.U = float(settingwidget.lift_maxbending_input.velocityinput.text())
        self.M = float(settingwidget.lift_maxbending_input.liftinput.text())
        #セクションの区切りの位置
        for n in range(self.n_section):
            self.y_section.append(float(settingwidget.tablewidget.item(0,n + 1).text()) / 1000)

        i = 0
        j = 0
        while True:
            self.y_div.append(round(self.dy * (i + 1),4))
            if round(self.y_div[i],4) > round(self.y_section[j]  - self.dy / 2,4) and round(self.y_div[i],4) <= round(self.y_section[j] + self.dy / 2,4):
                self.Ndiv_sec.append(i)
                j = j + 1
            if self.y_div[i] == self.y_wire:
                self.Ndiv_wire = i

            if j == self.n_section:
                break
            i = i + 1

        #パネル幅dSの作成
        coe_tawami = self.max_tawami / (self.b / 2) ** 2
        for n in range(len(self.y_div)):
            self.z_div.append(coe_tawami * self.y_div[n] ** 2)
            if n != 0:
                self.dS.append(numpy.sqrt((self.y_div[n]-self.y_div[n-1])**2+(self.z_div[n]-self.z_div[n-1])**2) / 2)
                self.y.append((self.y_div[n]+self.y_div[n-1]) / 2)
                self.z.append((self.z_div[n]+self.z_div[n-1]) / 2)
                self.phi.append(numpy.arctan((self.z_div[n]-self.z_div[n-1]) / (self.y_div[n]-self.y_div[n-1])))
            else:
                self.dS.append(numpy.sqrt(self.y_div[n]**2+self.z_div[n]**2) / 2)
                self.y.append(self.y_div[n] / 2)
                self.z.append(self.z_div[n] / 2)
                self.phi.append(numpy.arctan(self.z_div[n] / self.y_div[n]))
        #control pointにおける桁剛性、線密度
        n = 0
        for i_wings in range(self.n_section) :
            j = 1
            coe_EI = float(settingwidget.tablewidget.item(1,i_wings + 1).text())
            print(coe_EI)
            while True:
                if i_wings == 0:
                    if round(self.y[n],4) < round(float(eisettingwidget.EIinputWidget[i_wings].EIinputtable.item(0,j).text()) / 1000 ,4):
                        self.EI.append(float(eisettingwidget.EIinputWidget[i_wings].EIinputtable.item(1,j).text()) * coe_EI)
                        self.sigma.append(float(eisettingwidget.EIinputWidget[i_wings].EIinputtable.item(2,j).text()) *coe_EI)
                    else:
                        self.EI.append(float(eisettingwidget.EIinputWidget[i_wings].EIinputtable.item(1,j).text()) *coe_EI)
                        self.sigma.append(float(eisettingwidget.EIinputWidget[i_wings].EIinputtable.item(2,j).text()) *coe_EI)
                        j = j + 1

                elif i_wings != 0:
                    if round(self.y[n],4) < round(float(eisettingwidget.EIinputWidget[i_wings].EIinputtable.item(0,j).text()) / 1000 + self.y_section[i_wings-1],4):
                        self.EI.append(float(eisettingwidget.EIinputWidget[i_wings].EIinputtable.item(1,j).text())* coe_EI)
                        self.sigma.append(float(eisettingwidget.EIinputWidget[i_wings].EIinputtable.item(2,j).text())* coe_EI)
                    else:
                        self.EI.append(float(eisettingwidget.EIinputWidget[i_wings].EIinputtable.item(1,j).text())* coe_EI)
                        self.sigma.append(float(eisettingwidget.EIinputWidget[i_wings].EIinputtable.item(2,j).text())* coe_EI)
                        j = j + 1
                n = n + 1
                if n == len(self.y):
                    break
                if not round(self.y[n],4) < round(self.y_section[i_wings],4):
                    break



        self.spar_weight = numpy.sum(numpy.array(self.sigma) * numpy.array(self.dS) * 2) * 2

        self.sigma_wire = self.sigma
        self.sigma_wire[self.Ndiv_wire] += float(settingwidget.lift_maxbending_input.forcewireinput.text()) / self.dS[self.Ndiv_wire] / 2

    def matrix(self,progressbar):
        def calc_Q(y,z,phi,dS,progressbar):
            Q_ij = numpy.zeros([len(y),len(y)])
            yd_ij = numpy.zeros([len(y),len(y)])
            zd_ij = numpy.zeros([len(y),len(y)])
            ydd_ij = numpy.zeros([len(y),len(y)])
            zdd_ij = numpy.zeros([len(y),len(y)])

            R_2_Pij = numpy.zeros([len(y),len(y)])
            R_2_Mij = numpy.zeros([len(y),len(y)])
            Rd_2_Pij = numpy.zeros([len(y),len(y)])
            Rd_2_Mij = numpy.zeros([len(y),len(y)])

            Q_ij_1 = numpy.zeros([len(y),len(y)])
            Q_ij_2 = numpy.zeros([len(y),len(y)])
            Q_ij_3 = numpy.zeros([len(y),len(y)])
            Q_ij_4 = numpy.zeros([len(y),len(y)])

            for i in range (len(y)):
                for j in range(len(y)):
                    progressbar.setValue((i*len(y)+(j+1))/len(y)**2*100)
                    yd_ij[i,j] =  (y[i] - y[j]) * numpy.cos(phi[j]) + (z[i]-z[j]) * numpy.sin(phi[j])
                    zd_ij[i,j] = -(y[i] - y[j]) * numpy.sin(phi[j]) + (z[i]-z[j]) * numpy.cos(phi[j])
                    ydd_ij[i,j] = (y[i] + y[j]) * numpy.cos(phi[j]) - (z[i]-z[j]) * numpy.sin(phi[j])
                    zdd_ij[i,j] = (y[i] + y[j]) * numpy.sin(phi[j]) + (z[i]-z[j]) * numpy.cos(phi[j])

                    R_2_Pij[i,j] = (yd_ij[i,j] - dS[j]) ** 2 + zd_ij[i,j] ** 2
                    R_2_Mij[i,j] = (yd_ij[i,j] + dS[j]) ** 2 + zd_ij[i,j] ** 2
                    Rd_2_Pij[i,j] = (ydd_ij[i,j] + dS[j]) ** 2 + zdd_ij[i,j] ** 2
                    Rd_2_Mij[i,j] = (ydd_ij[i,j] - dS[j])**2 + zdd_ij[i,j] ** 2

                    Q_ij_1[i,j] = ((yd_ij[i,j] - dS[j]) / R_2_Pij[i,j] - (yd_ij[i,j] + dS[j]) / R_2_Mij[i,j]) * numpy.cos(phi[i]-phi[j])
                    Q_ij_2[i,j] = ((zd_ij[i,j]) / R_2_Pij[i,j] - (zd_ij[i,j]) / R_2_Mij[i,j]) * numpy.sin(phi[i] - phi[j])
                    Q_ij_3[i,j] = ((ydd_ij[i,j] - dS[j]) / Rd_2_Mij[i,j] - (ydd_ij[i,j] + dS[j]) / Rd_2_Pij[i,j]) * numpy.cos(phi[i]+phi[j]);
                    Q_ij_4[i,j] = ((zdd_ij[i,j]) / Rd_2_Mij[i,j] - (zdd_ij[i,j]) / Rd_2_Pij[i,j]) * numpy.sin(phi[i]+phi[j])

                    Q_ij[i,j] = -1 / 2 / numpy.pi * (Q_ij_1[i,j] + Q_ij_2[i,j] + Q_ij_3[i,j] + Q_ij_4[i,j])
            return Q_ij


        self.Q_ij = calc_Q(self.y,self.z,self.phi,self.dS,progressbar)
        #-----多角形化行列
        self.polize_mat = numpy.zeros([len(self.y),self.n_section])
        for i in range(self.Ndiv_sec[1]):
            self.polize_mat[i,0]           = 1
            self.polize_mat[i,self.n_section-1] = 0

        for j in range(1,self.n_section):
            for i in range(self.Ndiv_sec[j-1] + 1, self.Ndiv_sec[j] + 1):
                self.polize_mat[i,j-1]   =  -(self.y[i]-self.y_section[j])   / (self.y_section[j]-self.y_section[j-1])
                self.polize_mat[i,j]     =   (self.y[i]-self.y_section[j-1]) / (self.y_section[j]-self.y_section[j-1])

        #積分によりせん断力Qを求める
        self.sh_mat = numpy.zeros([len(self.y),len(self.y)])
        for j in range(len(self.y)-1,-1,-1):
            for i in range(j,-1,-1):
                if j == i:
                    self.sh_mat[i,j] = self.dS[j]
                else:
                    self.sh_mat[i,j] = self.dS[j] * 2
        self.sh_mat = self.sh_mat * self.U * self.rho
        #積分によりモーメントを求める
        self.mo_mat = numpy.zeros([len(self.y),len(self.y)])
        for j in range(len(self.y)-1,-1,-1):
            for i in range(j,-1,-1):
                if j == i:
                    self.mo_mat[i,j] = self.dS[j]
                else:
                    self.mo_mat[i,j] = self.dS[j] * 2

        #積分によりたわみ角を求める行列
        self.vd_mat = numpy.zeros([len(self.y),len(self.y)])
        for i in range(len(self.y)-1,-1,-1):
            for j in range(i,-1,-1):
                if j == i:
                    self.vd_mat[i,j] = self.dS[j] / self.EI[j]* 10 ** 6
                else:
                    self.vd_mat[i,j] = self.dS[j] / self.EI[j] * 10 ** 6 * 2

        self.v_mat = numpy.zeros([len(self.y),len(self.y)])
        for i in range(len(self.y)-1,-1,-1):
            for j in range(i,-1,-1):
                if j == i:
                    self.v_mat[i,j] = self.dS[j]
                else:
                    self.v_mat[i,j] = self.dS[j] * 2

        #制約となる撓みとなる位置（固定)
        B_want = numpy.zeros([1,len(self.y)])
        B_want[0,len(self.y)-1] = 1

        #構造制約行列
        self.B = numpy.dot(B_want,numpy.dot(self.v_mat,numpy.dot(self.vd_mat,numpy.dot(self.mo_mat,numpy.dot(self.sh_mat,self.polize_mat)))))
        self.B_val = self.max_tawami + numpy.dot(numpy.dot(B_want,numpy.dot(self.v_mat,numpy.dot(self.vd_mat,numpy.dot(self.mo_mat,self.sh_mat)))),numpy.array(self.sigma_wire).T / self.rho / self.U)

        #-----揚力制約条件行列
        self.C = 4 * self.rho * self.U * numpy.dot(self.dS,self.polize_mat)
        #-----揚力制約条件の値
        self.C_val = self.M * 9.8


    def optimize(self,checkbox):
        def calc_ellipticallift(self):
            root_gamma = self.M * 9.8 * 4 / numpy.pi / self.b / self.U / self.rho
            self.gamma_el = numpy.zeros(len(self.y))
            for i in range(len(self.y)):
                self.gamma_el[i] = (numpy.sqrt(root_gamma ** 2 -(self.y[i] * root_gamma / self.b * 2)**2 ))


        if checkbox.checkState() == 2:
            #構造考慮
            A = copy.deepcopy(self.Q_ij)
            for i in range(A.shape[1]):
                for j in range(A.shape[0]):
                    A[j,i] = A[j,i] * self.dS[j] * 2
            Mat_indD = A * self.rho
            A = (A + A.T)
            A = self.rho * numpy.dot(self.polize_mat.T,numpy.dot(A,self.polize_mat))
            A = numpy.vstack((A,-self.B))
            A = numpy.vstack((A,-self.C))
            A = numpy.column_stack((A,numpy.append(-self.B,[0,0]).T))
            A = numpy.column_stack((A,numpy.append(-self.C,[0,0]).T))
            A_val = numpy.zeros([A.shape[0],1])
            A_val[A.shape[0]-2,0] = -self.B_val
            A_val[A.shape[0]-1,0] = -self.C_val

            self.Optim_Answer = numpy.linalg.solve(A,A_val)
            self.lambda1 = self.lambda2 = self.Optim_Answer[self.n_section-1,0]
            self.lambda2 = self.Optim_Answer[self.n_section,0]
            self.gamma_opt = self.Optim_Answer[0:self.n_section,:]

        else:
            #構造無視
            A = copy.deepcopy(self.Q_ij)
            for i in range(A.shape[1]):
                for j in range(A.shape[0]):
                    A[j,i] = A[j,i] * self.dS[j] * 2
            A = (A + A.T)
            A = self.rho * numpy.dot(self.polize_mat.T,numpy.dot(A,self.polize_mat))
            A = numpy.vstack((A,-self.C))
            A = numpy.column_stack((A,numpy.append(-self.C,[0]).T))
            A_val = numpy.zeros([A.shape[0],1])
            A_val[A.shape[0]-1,0] = -self.C_val

            self.Optim_Answer = numpy.linalg.solve(A,A_val)
            self.lambda1 = 0
            self.lambda2 = self.Optim_Answer[self.n_section,0]
            self.gamma_opt = self.Optim_Answer[0:self.n_section,:]

        self.bending_mat = numpy.dot(self.v_mat,numpy.dot(self.vd_mat,numpy.dot(self.mo_mat,self.sh_mat)))
        self.shearForce = numpy.dot(self.sh_mat,(numpy.dot(self.polize_mat,self.gamma_opt) - numpy.array([self.sigma_wire]).T / self.U / self.rho))
        self.moment = numpy.dot(numpy.dot(self.mo_mat,self.sh_mat),(numpy.dot(self.polize_mat,self.gamma_opt) - numpy.array([self.sigma_wire]).T / self.U / self.rho))
        self.bending_angle =numpy.dot(numpy.dot(self.vd_mat,numpy.dot(self.mo_mat,self.sh_mat)),(numpy.dot(self.polize_mat,self.gamma_opt) - numpy.array([self.sigma_wire]).T / self.U / self.rho))
        self.bending = numpy.dot(self.bending_mat,(numpy.dot(self.polize_mat,self.gamma_opt) - numpy.array([self.sigma_wire]).T / self.U / self.rho))

        calc_ellipticallift(self)
        self.gamma = numpy.dot(self.polize_mat,self.gamma_opt)
        self.ind_vel = numpy.dot(self.Q_ij / 2 ,self.gamma)
        self.Di = 0
        self.Lift = numpy.dot(self.C,self.gamma_opt)[0]
        for i in range(len(self.y)):
            self.Di += self.rho * self.ind_vel[i] * self.gamma[i] * self.dy * 2
        self.Di = self.Di[0]



def main():

    def insertcolumn():
        def readcelltext(table, row, column):
            if isinstance(table,QtGui.QTableWidget):
                cell = table.item(row, column)
                celltext = cell.text()
                return celltext

        insertnum = settingwidget.tablewidget.columnCount()
        settingwidget.tablewidget.setColumnCount(insertnum + 1)
        settingwidget.tablewidget.setHorizontalHeaderItem(insertnum, QtGui.QTableWidgetItem("第{num}翼".format(num = insertnum)))
        settingwidget.tablewidget.setItem(0,insertnum,QtGui.QTableWidgetItem("{insertspar}".format(insertspar = float(settingwidget.tablewidget.item(0,insertnum-1).text()) + 2000)))

        i = insertnum-1
        eisettingwidget.EIinputWidget.append(QtGui.QGroupBox(parent = eisettingwidget))
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

        y_div = []
        spar_default_divpos = []
        for i_wing in range(settingwidget.tablewidget.columnCount()-1):
            y_div.append([])
            spar_default_divpos.append([])
            y_div[i_wing] = float(readcelltext(settingwidget.tablewidget,0,i_wing + 1))

        for i_spardiv in range(4):
            spar_default_divpos = [(y_div[i] - y_div[i-1]) / 4,(y_div[i] - y_div[i-1]) / 2, (y_div[i] - y_div[i-1]) * 3 / 4, y_div[i] - y_div[i-1]]
            eisettingwidget.EIinputWidget[i].EIinputtable.setItem(0,i_spardiv + 1,QtGui.QTableWidgetItem("{defaultdivpos}".format(defaultdivpos = spar_default_divpos[i_spardiv])))
            #桁剛性値サンプルのセット
            eisettingwidget.EIinputWidget[i].EIinputtable.setItem(1,i_spardiv + 1,QtGui.QTableWidgetItem("{EI_sample}".format(EI_sample = 1000000000)))
            #桁線密度サンプルのセット
            eisettingwidget.EIinputWidget[i].EIinputtable.setItem(2,i_spardiv + 1,QtGui.QTableWidgetItem("{sigma_sample}".format(sigma_sample = 0.0700)))


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
        EIsetting_init()
        eisettingwidget.show()

    def EIsetting_init():
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
            #剛性設定ウィジットに表示する初期値のリスト
            if i_wing != 0:
                spar_default_divpos[i_wing] = [(y_div[i_wing] - y_div[i_wing-1]) / 4,(y_div[i_wing] - y_div[i_wing-1]) / 2, (y_div[i_wing] - y_div[i_wing-1]) * 3 / 4, y_div[i_wing] - y_div[i_wing-1]]
            else:
                spar_default_divpos[i_wing] = [(y_div[i_wing]) / 4,(y_div[i_wing]) / 2, (y_div[i_wing]) * 3 / 4,y_div[i_wing]]

            for i_spardiv in range(4):
                eisettingwidget.EIinputWidget[i_wing].EIinputtable.setItem(0,i_spardiv + 1,QtGui.QTableWidgetItem("{spar_div}".format(spar_div = spar_default_divpos[i_wing][i_spardiv])))
                #noneditableに
                eisettingwidget.EIinputWidget[i_wing].EIinputtable.item(0,i_spardiv + 1).setFlags(QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled)


    def resultshow():
        resulttabwidget.circulation_graph.axes.clear()
        resulttabwidget.circulation_graph.drawplot(numpy.array(TR797_opt.y).T,numpy.dot(TR797_opt.polize_mat,TR797_opt.gamma_opt),numpy.array(TR797_opt.y),TR797_opt.gamma_el,xlabel = "y[m]",ylabel = "gamma[m^2/s]",legend = ("optimized","elliptical"),aspect = "auto")
        resulttabwidget.bending_graph.axes.clear()
        resulttabwidget.bending_graph.drawplot(numpy.array(TR797_opt.y).T,TR797_opt.bending,xlabel = "y[m]",ylabel = "bending[m]")
        resulttabwidget.ind_graph.axes.clear()
        resulttabwidget.ind_graph.drawplot(numpy.array(TR797_opt.y).T, numpy.arctan(-TR797_opt.ind_vel / TR797_opt.U) * 180 / numpy.pi , xlabel = "y[m]",ylabel = "induced angle[deg]",aspect = "auto")
        resulttabwidget.bendingangle_graph.axes.clear()
        resulttabwidget.bendingangle_graph.drawplot(numpy.array(TR797_opt.y).T,TR797_opt.bending_angle * 180 / numpy.pi,xlabel = "y[m]",ylabel = "bending angle[deg]",aspect = "auto")
        resulttabwidget.moment_graph.axes.clear()
        resulttabwidget.moment_graph.drawplot(numpy.array(TR797_opt.y).T,TR797_opt.moment,xlabel = "y[m]",ylabel = "moment[N/m]",aspect = "auto")
        resulttabwidget.shforce_graph.axes.clear()
        resulttabwidget.shforce_graph.drawplot(numpy.array(TR797_opt.y).T,TR797_opt.shearForce,xlabel = "y[m]",ylabel = "shearforce[N]",aspect = "auto")

        resultvalwidget.liftresultlabel.setText("計算揚力[kgf] : {Lift}".format(Lift = numpy.round(TR797_opt.Lift / 9.8,3)))
        resultvalwidget.Diresultlabel.setText("   抗力[N] : {Di}".format(Di = numpy.round(TR797_opt.Di,3)))
        if exeexportbutton.do_stracutual.checkState() == 2:
            resultvalwidget.lambda1label.setText("   構造制約係数λ1[-] : {lambda1}".format(lambda1 = numpy.round(TR797_opt.lambda1,3)))
        else:
            resultvalwidget.lambda1label.setText("   構造制約係数λ1[-] : {lambda1}".format(lambda1 = "--"))

        resultvalwidget.lambda2label.setText("   揚力制約係数λ2[-] : {lambda2}".format(lambda2 = numpy.round(TR797_opt.lambda2,3)))

    def calculation():
        EIsetting_init()
        TR797_opt.__init__()
        TR797_opt.prepare(settingwidget,eisettingwidget)
        TR797_opt.matrix(exeexportbutton.progressbar)
        TR797_opt.optimize(exeexportbutton.do_stracutual)
        resultshow()

    def exportCSV():
        projectname = QtGui.QFileDialog.getSaveFileName(None, caption = "CSV出力",filter = "CSV(*.csv)")
        fid = open(projectname,"w")
        writecsv = csv.writer(fid,lineterminator = "\n")
        writecsv.writerow(["循環分布最適化結果"])
        writecsv.writerow(["スパン方向位置y[m]","循環[m^2/s]","誘導角度[deg]","たわみ[m]","たわみ角[deg]","曲げモーメント","せん断力","剛性","線密度"])
        for n in range(len(TR797_opt.y)):
            writecsv.writerow([TR797_opt.y[n],TR797_opt.gamma[n,0],numpy.arctan(TR797_opt.ind_vel[n,0] / TR797_opt.U)*180/numpy.pi,TR797_opt.bending[n,0],TR797_opt.bending_angle[n,0]*180/numpy.pi,TR797_opt.moment[n,0],TR797_opt.shearForce[n,0],TR797_opt.EI[n],TR797_opt.sigma[n]])
        writecsv.writerow(["--"])
        writecsv.writerow(["誘導速度行列Q(右から循環の縦ベクトルを掛ければ誘導速度になります"])
        writecsv.writerows(TR797_opt.Q_ij/2)



    qApp = QtGui.QApplication(sys.argv)

    mainwindow = QtGui.QMainWindow()
    mainpanel = QtGui.QWidget()

    resulttabwidget = ResultTabWidget()
    exeexportbutton = ExeExportButton()
    settingwidget = SettingWidget()
    resultvalwidget = ResultValWidget(settingwidget.tablewidget)
    eisettingwidget = EIsettingWidget(settingwidget.tablewidget)
    eisettingwidget.EIsetting(settingwidget.tablewidget)
    EIsetting_init()

    EIsample_list = [34375000000,36671000000,16774000000,8305800000,1864800000,70940000]
    sigmasample_list = [0.377,0.357,0.284,0.245,0.0929,0.0440]
    for i_wing in range(settingwidget.tablewidget.columnCount() - 1):
        for i_spardiv in range(4):
            #桁剛性値サンプルのセット
            eisettingwidget.EIinputWidget[i_wing].EIinputtable.setItem(1,i_spardiv + 1,QtGui.QTableWidgetItem("{EI_sample}".format(EI_sample = EIsample_list[i_wing])))
            #桁線密度サンプルのセット
            eisettingwidget.EIinputWidget[i_wing].EIinputtable.setItem(2,i_spardiv + 1,QtGui.QTableWidgetItem("{sigma_sample}".format(sigma_sample = sigmasample_list[i_wing])))

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
    exeexportbutton.connect(exeexportbutton.exportbutton,QtCore.SIGNAL('clicked()'),exportCSV)

    sys.exit(qApp.exec_())

if __name__ == '__main__':
    main()
