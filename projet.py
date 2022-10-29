from time import sleep
from turtle import done
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
from PyQt5 import QtWidgets, uic, QtGui, QtCore
from PyQt5.QtWidgets import QFileDialog
from PandasModel import PandasModel
import sys
import ctypes
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi,tight_layout=True)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)

class Second(QtWidgets.QDialog):
        def __init__(self,df,columns,value,dis_type):
                super(Second, self).__init__()
                uic.loadUi('discret_menu.ui', self)
                self.columns=columns
                self.value=value
                self.type=dis_type
                self.methods=[]
                self.df=df
                self.col_combo=self.findChild(QtWidgets.QComboBox,'discret_combo')
                self.col_combo.addItems(self.columns)
                self.method_combo=self.findChild(QtWidgets.QComboBox,'discret_method')
                self.next_button=self.findChild(QtWidgets.QPushButton,'next_button')
                self.next_button.clicked.connect(self.Next)
                self.ok_button=self.findChild(QtWidgets.QPushButton,'ok')
                self.ok_button.clicked.connect(self.Okay)
                self.cancel_button=self.findChild(QtWidgets.QPushButton,'cancel_button')
                self.cancel_button.clicked.connect(self.Cancel)

        def Next(self):
                if(len(self.columns)!=0):
                        print (self.col_combo.currentText())
                        self.methods.append((self.col_combo.currentText(),self.method_combo.currentText()))
                        self.columns.remove(self.col_combo.currentText())
                        self.col_combo.clear()
                        self.col_combo.addItems(self.columns)
                else:
                        print("liste vide, appuyez sur ok")
        def Okay(self):
                global table_discret
                if(self.type=='K'):
                        valeurs_discret=[]
                        col=[]
                        for each in self.methods:
                                col.append(each[0])
                                valeurs_discret.append(discretisation_amplitude(self.df[each[0]],self.value,each[1]))
                        table_discret=pd.DataFrame(valeurs_discret,col)                                  
                elif(self.type=='Q'):
                        valeurs_discret=[]
                        col=[]
                        for each in self.methods:
                                col.append(each[0])
                                valeurs_discret.append(discretisation_effectifs(self.df[each[0]],self.value,each[1]))
                        table_discret=pd.DataFrame(valeurs_discret,col)
                self.close()        


        def Cancel(self):
                self.close()
		

class Ui(QtWidgets.QMainWindow):
        def __init__(self):
                super(Ui, self).__init__()
                self.setWindowIcon(QtGui.QIcon('pick_logo.png'))
                self.setIconSize(QtCore.QSize(200,180))
                self.setWindowTitle("MineData")
                uic.loadUi('PROJET_DM.ui', self)
                ######################################### items declaration #######################################################
                self.upload_button= self.findChild(QtWidgets.QPushButton,'upload_button')
                self.upload_button.clicked.connect(self.UploadClickListener)

                # self.choose_column= self.findChild(QtWidgets.QPushButton,'choose_column')
                # self.choose_column.clicked.connect(self.ColumnButtonClickListener)

                self.draw_button= self.findChild(QtWidgets.QPushButton,'draw')
                self.draw_button.clicked.connect(self.DrawColumnClickListener)

                self.save_button= self.findChild(QtWidgets.QPushButton,'save_button')
                self.save_button.clicked.connect(self.SaveClickListener)

                self.del_row_button= self.findChild(QtWidgets.QPushButton,'del_row')
                self.del_row_button.clicked.connect(self.Delete_Row_man)
                self.del_col_button= self.findChild(QtWidgets.QPushButton,'del_col')
                self.del_col_button.clicked.connect(self.Delete_Col_man)

                self.auto_row_button= self.findChild(QtWidgets.QPushButton,'eliminate_row')
                self.auto_row_button.clicked.connect(self.auto_row)
                self.auto_col_button= self.findChild(QtWidgets.QPushButton,'eliminate_col')
                self.auto_col_button.clicked.connect(self.auto_col)

                self.minmax_button= self.findChild(QtWidgets.QPushButton,'normal_minmax')
                self.minmax_button.clicked.connect(self.Normal_minmax)

                self.zscore_button= self.findChild(QtWidgets.QPushButton,'normal_zscore')
                self.zscore_button.clicked.connect(self.Normal_zscore)

                self.replace_null_button= self.findChild(QtWidgets.QPushButton,'replace_null')
                self.replace_null_button.clicked.connect(self.ReplaceNull)

                self.replace_outlier_button= self.findChild(QtWidgets.QPushButton,'replace_outlier')
                self.replace_outlier_button.clicked.connect(self.ReplaceOutlier)

                self.boxplot_button= self.findChild(QtWidgets.QRadioButton,'boxplot_radio')
                self.boxplot_button.toggled.connect(self.BoxPlotListener)
                self.boxplot_button.setChecked(True)

                self.histoplot_button= self.findChild(QtWidgets.QRadioButton,'histogramme_radio')
                self.histoplot_button.toggled.connect(self.HistoPlotListener)

                self.scatter_button = self.findChild(QtWidgets.QRadioButton,'scatter_radio')
                self.scatter_button.toggled.connect(self.ScatterPlotListener)

                self.min_spin=self.findChild(QtWidgets.QSpinBox,'min_value')
                self.max_spin=self.findChild(QtWidgets.QSpinBox,'max_value')

                self.Q_spin=self.findChild(QtWidgets.QSpinBox,'Q_value')
                self.K_spin=self.findChild(QtWidgets.QSpinBox,'K_value')
                self.discretize_Q= self.findChild(QtWidgets.QPushButton,'discretize_frequency')
                self.discretize_Q.clicked.connect(self.discretizeQ)
                self.discretize_K= self.findChild(QtWidgets.QPushButton,'discretize_width')
                self.discretize_K.clicked.connect(self.discretizeK)

                self.column1_combo = self.findChild(QtWidgets.QComboBox, 'scatter_column1')
                self.column2_combo = self.findChild(QtWidgets.QComboBox, 'scatter_column2')
                self.column1_combo.activated.connect(self.PlotScatterAuto)
                self.column2_combo.activated.connect(self.PlotScatterAuto)

                self.replace_null_combo=self.findChild(QtWidgets.QComboBox, 'combo_null')
                self.replace_null_column=self.findChild(QtWidgets.QComboBox, 'column_null')
                self.replace_outlier_combo=self.findChild(QtWidgets.QComboBox, 'combo_outlier')
                self.replace_outlier_column=self.findChild(QtWidgets.QComboBox, 'column_outlier')

                self.frame=self.findChild(QtWidgets.QWidget,'widget')

                self.dataset_info= self.findChild(QtWidgets.QLabel,'dataset_info')
                self.column_info= self.findChild(QtWidgets.QPlainTextEdit,'column_info')
                self.correlation= self.findChild(QtWidgets.QLabel,'correlation_label')

                self.tabs=self.findChild(QtWidgets.QTabWidget,"tabwidget")

                self.pandasTv=self.findChild(QtWidgets.QTableView,'pandasTv')
                self.pandasTv.setStyleSheet("QTableView {background-color:rgb(16, 5, 44);}")
                self.pandasTv.setSortingEnabled(True)
                self.show()


        def UploadClickListener(self):
                self.path = QFileDialog.getOpenFileName(self, "Import CSV", "", "CSV data files (*.csv);;Excel (*.xlsx)")
                # path = QFileDialog.getOpenFileName(self, 'Open a file', '','All Files (*.*)') # if we want all files
                self.df = pd.read_csv(self.path[0])
                info="Nombre de lignes: "+str(self.df.shape[0])+"\nNombre de colonnes: "+str(self.df.shape[1])+"\nNombre de valeurs nulles: "+str(self.df.isnull().sum().sum())
                print(info)
                #self.dataset_info.setText(info)
                self.pandasTv_model = PandasModel(self.df)
                self.dataset_info.setText(info)
                self.pandasTv.setModel(self.pandasTv_model)
                self.pandasTv.setStyleSheet("QTableView {background-color:rgb(99,78,163); color:white; gridline-color: black; border-color: rgb(242, 128, 133); font:350 11px 'Bahnschrift SemiLight';} QHeaderView::section {background-color: rgb(63, 50, 105);color: white;height: 35px;width: 45px; font:350 11px 'Bahnschrift SemiLight';} QTableCornerButton::section {background-color: rgb(63, 50, 105); color: rgb(200, 200, 200);}")
                self.pandasTv.clicked[QtCore.QModelIndex].connect(self.ColumnClickListener)
                columns = list(self.df.columns)
                self.replace_null_column.clear()
                self.replace_null_column.addItems(columns)
                self.replace_outlier_column.clear()
                self.replace_outlier_column.addItems(columns)
                if self.path != ('',''):
                        print(self.path[0])
                        return self.path[0]

        def SaveClickListener(self):
                try:
                        dialog = QtWidgets.QFileDialog()
                        self.path = dialog.getSaveFileName(self,"Save File","","CSV data files (*.csv);;Excel (*.xlsx)")
                        self.df.to_csv(self.path[0], index=False)
                        self.df = pd.read_csv(self.path[0])
                        info="Nombre de lignes: "+str(self.df.shape[0])+"\nNombre de colonnes: "+str(self.df.shape[1])+"\nNombre de valeurs nulles: "+str(self.df.isnull().sum().sum())
                        self.dataset_info.setText(info)
                        self.pandasTv_model = PandasModel(self.df)
                        self.pandasTv.setModel(self.pandasTv_model)
                        self.pandasTv.clicked[QtCore.QModelIndex].connect(self.ColumnClickListener)
                        if (self.df.dtypes[self.df.columns[self.item.column()]] != 'object'):
                                td=tendanceCentrale(self.df[self.df.columns[self.item.column()]])
                                dis=dispersion(self.df[self.df.columns[self.item.column()]])
                                q=dis[0][4]
                                if len(dis[1])!=0:
                                        outliers=str(dis[1])
                                else:
                                        outliers="no outliers"
                                info="Column name: "+str(self.df.columns[self.item.column()])+"\nColumn type: "+str(self.df.dtypes[self.df.columns[self.item.column()]])+"\nMean: "+str(td['mean'])+"\nMedian: "+str(td['median'])+"\nMode: "+str(td['mode'])+"\nSymmetry: "+td['symetrie']+"\nEcart type: "+str(dis[0][0])+"\nVariance: "+str(dis[0][1])+"\nMin: "+str(dis[0][3])+"\nQ1: "+str(q[0])+"\nQ3: "+str(q[1])+"\nMax: "+str(dis[0][5])+"\nIQR: "+str(dis[0][2])+"\nOutliers: "+outliers
                                        #print(info)
                                self.column_info.clear()
                                self.column_info.insertPlainText(info)
                        else:
                                info="Column name: "+str(self.df.columns[self.item.column()])+"\nColumn type: "+str(self.df.dtypes[self.df.columns[self.item.column()]])
                                print(info)
                                self.column_info.clear()
                                self.column_info.insertPlainText(info)

                except:
                        ctypes.windll.user32.MessageBoxW(0, "No dataset loaded.", "Error!", 0)


        def discretizeK(self):
                data_num=[]
                for col in self.df.columns:
                        if self.df[col].dtype != 'object':
                                data_num.append(col)
                self.second=Second(self.df,data_num,self.K_spin.value(),"K")
                self.second.setModal(True)
                self.second.setAttribute(QtCore.Qt.WA_DeleteOnClose)                
                self.second.exec()

                self.df=table_discret
                self.pandasTv_model = PandasModel(self.df)
                info="Nombre de lignes: "+str(self.df.shape[0])+"\nNombre de colonnes: "+str(self.df.shape[1])+"\nNombre de valeurs nulles: "+str(self.df.isnull().sum().sum())
                self.dataset_info.setText(info)
                self.pandasTv.setModel(self.pandasTv_model)
                self.pandasTv.clicked[QtCore.QModelIndex].connect(self.ColumnClickListener)


        def discretizeQ(self):
                data_num=[]
                for col in self.df.columns:
                        if self.df[col].dtype != 'object':
                                data_num.append(col)
                self.second=Second(self.df,data_num,self.Q_spin.value(),"Q")
                self.second.setModal(True)
                self.second.setAttribute(QtCore.Qt.WA_DeleteOnClose)                
                self.second.exec()

                self.df=table_discret
                self.pandasTv_model = PandasModel(self.df)
                info="Nombre de lignes: "+str(self.df.shape[0])+"\nNombre de colonnes: "+str(self.df.shape[1])+"\nNombre de valeurs nulles: "+str(self.df.isnull().sum().sum())
                self.dataset_info.setText(info)
                self.pandasTv.setModel(self.pandasTv_model)
                self.pandasTv.clicked[QtCore.QModelIndex].connect(self.ColumnClickListener)



        def ColumnClickListener(self,item):
                print("with item")
                self.item=item
                print(item.column())
                print(self.df.columns[self.item.column()])
                print(self.df.dtypes[self.df.columns[item.column()]])
                info="Nombre de lignes: "+str(self.df.shape[0])+"\nNombre de colonnes: "+str(self.df.shape[1])+"\nNombre de valeurs nulles: "+str(self.df.isnull().sum().sum())
                print(info)
                #self.dataset_info.setText(info)
                self.pandasTv_model = PandasModel(self.df)
                self.dataset_info.setText(info)
                if (self.df.dtypes[self.df.columns[item.column()]] != 'object'):
                        td=tendanceCentrale(self.df[self.df.columns[item.column()]])
                        dis=dispersion(self.df[self.df.columns[item.column()]])
                        q=dis[0][4]
                        if len(dis[1])!=0:
                                outliers=str(dis[1])
                        else:
                                outliers="no outliers"
                        info="Column name: "+str(self.df.columns[item.column()])+"\nColumn type: "+str(self.df.dtypes[self.df.columns[item.column()]])+"\nMean: "+str(td['mean'])+"\nMedian: "+str(td['median'])+"\nMode: "+str(td['mode'])+"\nSymmetry: "+td['symetrie']+"\nEcart type: "+str(dis[0][0])+"\nVariance: "+str(dis[0][1])+"\nMin: "+str(dis[0][3])+"\nQ1: "+str(q[0])+"\nQ3: "+str(q[1])+"\nMax: "+str(dis[0][5])+"\nIQR: "+str(dis[0][2])+"\nOutliers: "+outliers+"\nNumber of missing values: "+str(self.df[[self.df.columns[item.column()]]].isnull().sum().values[0])
                        #print(info)
                        self.column_info.clear()
                        self.column_info.insertPlainText(info)
                else:
                        info="Column name: "+str(self.df.columns[item.column()])+"\nColumn type: "+str(self.df.dtypes[self.df.columns[item.column()]])+"\nUnique Values : "+str(set(uniqueValues(self.df,self.df.columns[self.item.column()])))+"\nNumber of missing values: "+str(self.df[[self.df.columns[item.column()]]].isnull().sum().values[0])
                        print(info)
                        #print("unique"+str(self.df[[self.df.columns[item.column()]]].unique()))
                        self.column_info.clear()
                        self.column_info.insertPlainText(info)

        def BoxPlotListener(self):
                try:    
                        if self.scatter_button.isChecked() == False:
                                self.column1_combo.clear()
                                self.column2_combo.clear()
                                self.column1_combo.setEnabled(False)
                                self.column2_combo.setEnabled(False)
                                self.correlation_label.setText("")
                        if self.boxplot_button.isChecked():
                                sc = MplCanvas(self.frame, width=4, height=4, dpi=100)
                                sc.axes.boxplot(self.df[self.df.columns[self.item.column()]])

                                # Create toolbar, passing canvas as first parament, parent (self, the MainWindow) as second.
                                layout = QtWidgets.QVBoxLayout()
                                layout.addWidget(sc)                

                                # Create a placeholder widget to hold our toolbar and canvas.
                                self.frame.setLayout(layout)
                                layout.deleteLater()
                except: print("")

        def HistoPlotListener(self):
                try:    
                        if self.scatter_button.isChecked() == False:
                                self.column1_combo.clear()
                                self.column2_combo.clear()
                                self.column1_combo.setEnabled(False)
                                self.column2_combo.setEnabled(False)
                                self.correlation_label.setText("")
                        if self.histoplot_button.isChecked():
                                sc = MplCanvas(self.frame, width=4, height=4, dpi=100)
                                if(self.df.dtypes[self.df.columns[self.item.column()]]!='object'):
                                        sns.distplot(self.df[self.df.columns[self.item.column()]],ax=sc.axes,kde=True)
                                else:
                                        b=sns.countplot(x=self.df[self.df.columns[self.item.column()]],ax=sc.axes)
                                        b.tick_params(labelsize=6)
                                        b.set_xticklabels(b.get_xticklabels(), rotation=30, horizontalalignment='right')

                                # Create toolbar, passing canvas as first parament, parent (self, the MainWindow) as second.
                                layout = QtWidgets.QVBoxLayout()
                                layout.addWidget(sc)                

                                # Create a placeholder widget to hold our toolbar and canvas.
                                self.frame.setLayout(layout)
                                layout.deleteLater()
                except: print("")

        def ScatterPlotListener(self):
                try:    
                        if self.scatter_button.isChecked():
                                self.column1_combo.setEnabled(True)
                                self.column2_combo.setEnabled(True)
                                columns = list(self.df.columns)
                                self.column1_combo.clear()
                                self.column1_combo.addItems(columns)
                                self.column2_combo.clear()
                                self.column2_combo.addItems(columns)
                                sc = MplCanvas(self.frame, width=4, height=4, dpi=100)
                                sc.axes.scatter(self.df[[self.column1_combo.currentText()]],self.df[[self.column2_combo.currentText()]], alpha = 0.7)

                                # Create toolbar, passing canvas as first parament, parent (self, the MainWindow) as second.
                                layout = QtWidgets.QVBoxLayout()
                                layout.addWidget(sc)                

                                # Create a placeholder widget to hold our toolbar and canvas.
                                self.frame.setLayout(layout)
                                layout.deleteLater()
                                
                                self.correlation_label.setText(str(correlation(self.df[[self.column1_combo.currentText()]],self.df[[self.column2_combo.currentText()]])))
                except: print("")
        
        def PlotScatterAuto(self):
                try:    
                        if self.scatter_button.isChecked():
                                sc = MplCanvas(self.frame, width=4, height=4, dpi=100)
                                sc.axes.scatter(self.df[[self.column1_combo.currentText()]],self.df[[self.column2_combo.currentText()]], alpha = 0.7)

                                # Create toolbar, passing canvas as first parament, parent (self, the MainWindow) as second.
                                layout = QtWidgets.QVBoxLayout()
                                layout.addWidget(sc)        

                                # Create a placeholder widget to hold our toolbar and canvas.
                                self.frame.setLayout(layout)
                                layout.deleteLater()
                                self.correlation_label.setText(str(correlation(self.df[[self.column1_combo.currentText()]],self.df[[self.column2_combo.currentText()]])))

                except: print("")

        def DrawColumnClickListener(self):
                if (self.boxplot_button.isChecked()):
                        try:
                                print("box plot")
                                sc = MplCanvas(self.frame, width=4, height=4, dpi=100)
                                sc.axes.boxplot(self.df[self.df.columns[self.item.column()]])

                                # Create toolbar, passing canvas as first parament, parent (self, the MainWindow) as second.
                                layout = QtWidgets.QVBoxLayout()
                                layout.addWidget(sc)
                                self.frame.setLayout(layout)
                                layout.deleteLater()
                        except: print("can't plot")
                elif (self.histoplot_button.isChecked()): 
                        try:    
                                if self.histoplot_button.isChecked():
                                        sc = MplCanvas(self.frame, width=4, height=4, dpi=100)
                                        if(self.df.dtypes[self.df.columns[self.item.column()]]!='object'):
                                                sns.distplot(self.df[self.df.columns[self.item.column()]],ax=sc.axes)
                                        else:
                                                b=sns.countplot(x=self.df[self.df.columns[self.item.column()]],ax=sc.axes)
                                                b.tick_params(labelsize=6)
                                                b.set_xticklabels(b.get_xticklabels(), rotation=45, horizontalalignment='right')

                                        # Create toolbar, passing canvas as first parament, parent (self, the MainWindow) as second.
                                        layout = QtWidgets.QVBoxLayout()
                                        layout.addWidget(sc)                

                                        # Create a placeholder widget to hold our toolbar and canvas.
                                        self.frame.setLayout(layout)
                                        layout.deleteLater()
                        except: print("can't plot")
                elif (self.scatter_button.isChecked()): 
                        try:    
                                if self.scatter_button.isChecked():
                                        sc = MplCanvas(self.frame, width=4, height=4, dpi=100)
                                        sc.axes.scatter(self.df[[self.column1_combo.currentText()]],self.df[[self.column2_combo.currentText()]], alpha = 0.7)

                                        # Create toolbar, passing canvas as first parament, parent (self, the MainWindow) as second.
                                        layout = QtWidgets.QVBoxLayout()
                                        layout.addWidget(sc)                

                                        # Create a placeholder widget to hold our toolbar and canvas.
                                        self.frame.setLayout(layout)
                                        layout.deleteLater()
                                        self.correlation_label.setText(str(correlation(self.df[[self.column1_combo.currentText()]],self.df[[self.column2_combo.currentText()]])))

                        except: print("")
        
        def ReplaceNull(self):
                self.df[self.replace_null_column.currentText()]=replace_missing(self.df[self.replace_null_column.currentText()],self.replace_null_combo.currentText())
                self.pandasTv_model = PandasModel(self.df)
                info="Nombre de lignes: "+str(self.df.shape[0])+"\nNombre de colonnes: "+str(self.df.shape[1])+"\nNombre de valeurs nulles: "+str(self.df.isnull().sum().sum())
                self.dataset_info.setText(info)
                if  self.df[self.replace_null_column.currentText()].dtype=='object':
                        info="Column name: "+str(self.replace_null_column.currentText())+"\nColumn type: "+str(self.df[self.replace_null_column.currentText()].dtype)+"\nUnique Values : "+str(set(uniqueValues(self.df,self.df.columns[self.replace_null_column.currentText()])))+"\nNumber of missing values: "+str(self.df[self.replace_null_column].isnull().sum().values[0])
                        print(info)
                        #print("unique"+str(self.df[[self.df.columns[item.column()]]].unique()))
                        self.column_info.clear()
                        self.column_info.insertPlainText(info)
                else:
                        td=tendanceCentrale(self.df[self.replace_null_column.currentText()])
                        dis=dispersion(self.df[self.replace_null_column.currentText()])
                        q=dis[0][4]
                        if len(dis[1])!=0:
                                outliers=str(dis[1])
                        else:
                                outliers="no outliers"
                        info="Column name: "+str(self.replace_null_column.currentText())+"\nColumn type: "+str(self.df[self.replace_null_column.currentText()].dtype)+"\nMean: "+str(td['mean'])+"\nMedian: "+str(td['median'])+"\nMode: "+str(td['mode'])+"\nSymmetry: "+td['symetrie']+"\nEcart type: "+str(dis[0][0])+"\nVariance: "+str(dis[0][1])+"\nMin: "+str(dis[0][3])+"\nQ1: "+str(q[0])+"\nQ3: "+str(q[1])+"\nMax: "+str(dis[0][5])+"\nIQR: "+str(dis[0][2])+"\nOutliers: "+outliers+"\nNumber of missing values: "+str(self.df[self.replace_null_column.currentText()].isnull().sum())
                        #print(info)
                        self.column_info.clear()
                        self.column_info.insertPlainText(info)
                self.pandasTv.setModel(self.pandasTv_model)
                self.pandasTv.clicked[QtCore.QModelIndex].connect(self.ColumnClickListener)
                columns = list(self.df.columns)
                self.replace_null_column.clear()
                self.replace_null_column.addItems(columns)
                self.replace_outlier_column.clear()
                self.replace_outlier_column.addItems(columns)


        def ReplaceOutlier(self):
                self.df=treat_outliers(self.df,self.df[self.replace_outlier_column.currentText()],self.replace_outlier_combo.currentText())
                self.pandasTv_model = PandasModel(self.df)
                info="Nombre de lignes: "+str(self.df.shape[0])+"\nNombre de colonnes: "+str(self.df.shape[1])+"\nNombre de valeurs nulles: "+str(self.df.isnull().sum().sum())
                self.dataset_info.setText(info)
                if  self.df[self.replace_outlier_column.currentText()].dtype=='object':
                        info="Column name: "+str(self.replace_outlier_column.currentText())+"\nColumn type: "+str(self.df[self.replace_outlier_column.currentText()].dtype)+"\nUnique Values : "+str(set(uniqueValues(self.df,self.df.columns[self.replace_outlier_column.currentText()])))+"\nNumber of missing values: "+str(self.df[self.replace_outlier_column].isnull().sum().values[0])
                        print(info)
                        #print("unique"+str(self.df[[self.df.columns[item.column()]]].unique()))
                        self.column_info.clear()
                        self.column_info.insertPlainText(info)
                else:
                        td=tendanceCentrale(self.df[self.replace_outlier_column.currentText()])
                        dis=dispersion(self.df[self.replace_outlier_column.currentText()])
                        q=dis[0][4]
                        if len(dis[1])!=0:
                                outliers=str(dis[1])
                        else:
                                outliers="no outliers"
                        info="Column name: "+str(self.replace_outlier_column.currentText())+"\nColumn type: "+str(self.df[self.replace_outlier_column.currentText()].dtype)+"\nMean: "+str(td['mean'])+"\nMedian: "+str(td['median'])+"\nMode: "+str(td['mode'])+"\nSymmetry: "+td['symetrie']+"\nEcart type: "+str(dis[0][0])+"\nVariance: "+str(dis[0][1])+"\nMin: "+str(dis[0][3])+"\nQ1: "+str(q[0])+"\nQ3: "+str(q[1])+"\nMax: "+str(dis[0][5])+"\nIQR: "+str(dis[0][2])+"\nOutliers: "+outliers+"\nNumber of missing values: "+str(self.df[self.replace_outlier_column.currentText()].isnull().sum())
                        #print(info)
                        self.column_info.clear()
                        self.column_info.insertPlainText(info)
                self.pandasTv.setModel(self.pandasTv_model)
                self.pandasTv.clicked[QtCore.QModelIndex].connect(self.ColumnClickListener)
                columns = list(self.df.columns)
                self.replace_null_column.clear()
                self.replace_null_column.addItems(columns)
                self.replace_outlier_column.clear()
                self.replace_outlier_column.addItems(columns)

        def Normal_minmax(self):
                self.df=min_max_normalisation(self.df,self.min_spin.value(),self.max_spin.value())
                self.pandasTv_model = PandasModel(self.df)
                info="Nombre de lignes: "+str(self.df.shape[0])+"\nNombre de colonnes: "+str(self.df.shape[1])+"\nNombre de valeurs nulles: "+str(self.df.isnull().sum().sum())
                self.dataset_info.setText(info)
                self.column_info.clear()
                self.pandasTv.setModel(self.pandasTv_model)
                self.pandasTv.clicked[QtCore.QModelIndex].connect(self.ColumnClickListener)
                columns = list(self.df.columns)
                self.replace_null_column.clear()
                self.replace_null_column.addItems(columns)
                self.replace_outlier_column.clear()
                self.replace_outlier_column.addItems(columns)

        def Normal_zscore(self):
                self.df=z_score_normalisation(self.df)
                self.pandasTv_model = PandasModel(self.df)
                info="Nombre de lignes: "+str(self.df.shape[0])+"\nNombre de colonnes: "+str(self.df.shape[1])+"\nNombre de valeurs nulles: "+str(self.df.isnull().sum().sum())
                self.dataset_info.setText(info)
                self.column_info.clear()
                self.pandasTv.setModel(self.pandasTv_model)
                self.pandasTv.clicked[QtCore.QModelIndex].connect(self.ColumnClickListener)
                columns = list(self.df.columns)
                self.replace_null_column.clear()
                self.replace_null_column.addItems(columns)
                self.replace_outlier_column.clear()
                self.replace_outlier_column.addItems(columns)

        def Delete_Row_man(self):
                print(self.item)
                print(self.item.row())
                print(self.item.column())
                print(self.df.columns[self.item.column()])
                print(self.df.dtypes[self.df.columns[self.item.column()]])
                self.df=self.df.drop([self.item.row()], axis = 0)
                self.df=self.df.reset_index(drop=True)
                self.pandasTv_model = PandasModel(self.df)                
                info="Nombre de lignes: "+str(self.df.shape[0])+"\nNombre de colonnes: "+str(self.df.shape[1])+"\nNombre de valeurs nulles: "+str(self.df.isnull().sum().sum())
                self.dataset_info.setText(info)
                self.column_info.clear()
                self.pandasTv.setModel(self.pandasTv_model)
                self.pandasTv.clicked[QtCore.QModelIndex].connect(self.ColumnClickListener)
                columns = list(self.df.columns)
                self.replace_null_column.clear()
                self.replace_null_column.addItems(columns)
                self.replace_outlier_column.clear()
                self.replace_outlier_column.addItems(columns)

        def Delete_Col_man(self):
                print(self.item)
                print(self.item.row())
                print(self.item.column())
                print(self.df.columns[self.item.column()])
                print(self.df.dtypes[self.df.columns[self.item.column()]])
                self.df=self.df.drop(self.df.columns[self.item.column()], axis = 1)
                self.df=self.df.reset_index(drop=True)
                self.pandasTv_model = PandasModel(self.df)                
                info="Nombre de lignes: "+str(self.df.shape[0])+"\nNombre de colonnes: "+str(self.df.shape[1])+"\nNombre de valeurs nulles: "+str(self.df.isnull().sum().sum())
                self.dataset_info.setText(info)
                self.column_info.clear()
                self.pandasTv.setModel(self.pandasTv_model)
                self.pandasTv.clicked[QtCore.QModelIndex].connect(self.ColumnClickListener)
                columns = list(self.df.columns)
                self.replace_null_column.clear()
                self.replace_null_column.addItems(columns)
                self.replace_outlier_column.clear()
                self.replace_outlier_column.addItems(columns)

        def auto_row(self):
                red=detect_redundant(self.df)
                for index,row in red[0].iterrows():
                        self.df=Del_Row(self.df,index)
                        self.df=self.df.reset_index(drop=True)
                self.pandasTv_model = PandasModel(self.df)                
                info="Nombre de lignes: "+str(self.df.shape[0])+"\nNombre de colonnes: "+str(self.df.shape[1])+"\nNombre de valeurs nulles: "+str(self.df.isnull().sum().sum())
                self.dataset_info.setText(info)
                self.column_info.clear()
                self.pandasTv.setModel(self.pandasTv_model)
                self.pandasTv.clicked[QtCore.QModelIndex].connect(self.ColumnClickListener)
                columns = list(self.df.columns)
                self.replace_null_column.clear()
                self.replace_null_column.addItems(columns)
                self.replace_outlier_column.clear()
                self.replace_outlier_column.addItems(columns)


        def auto_col(self):
                red=detect_redundant(self.df)
                for index in red[1]:
                        self.df=Del_Column(self.df,index)
                        self.df=self.df.reset_index(drop=True)
                self.pandasTv_model = PandasModel(self.df)                
                info="Nombre de lignes: "+str(self.df.shape[0])+"\nNombre de colonnes: "+str(self.df.shape[1])+"\nNombre de valeurs nulles: "+str(self.df.isnull().sum().sum())
                self.dataset_info.setText(info)
                self.column_info.clear()
                self.pandasTv.setModel(self.pandasTv_model)
                self.pandasTv.clicked[QtCore.QModelIndex].connect(self.ColumnClickListener)
                columns = list(self.df.columns)
                self.replace_null_column.clear()
                self.replace_null_column.addItems(columns)
                self.replace_outlier_column.clear()
                self.replace_outlier_column.addItems(columns)

def discretisation_effectifs(df_column, Q, method):
        step = (len(df_column)//Q)+1
        column = df_column.sort_values(ascending=True).reset_index(drop=True)
        quantiles = []
        for i in range(0,len(df_column),step):
                quantiles.append(column.iloc[i:i+step])
        for i in range(len(quantiles)): 
                if method == "Mean":
                        if df_column.dtype == "int64":
                                quantiles[i] = round(mean(quantiles[i]))
                        else:
                                quantiles[i] = mean(quantiles[i])
                elif method == "Mode":
                        quantiles[i] = mode(quantiles[i])
                elif method == "Median":
                        quantiles[i] = median(pd.Series(quantiles[i]))
                else: print("la methode choisie est invalide")

        # we return the reduced column and then we just make another function to loop over the df?
        # but in this case we need to ask the chosen method for each column so idk about that lol 
        # they must also have the same number of quantiles too so
        return quantiles

import math
def discretisation_amplitude(df_column, K, method):
        if K==0:
                K = 1+3*math.log10(len(df_column))
        ## column = df_column.sort_values(ascending=True).reset_index(drop=True)
        interval_size = (max(df_column)- min(df_column))/K
        
        if df_column.dtype == "int64":
                interval_size = math.ceil(interval_size)
        intervals = []
        i = min(df_column)
        while i < max(df_column):
                intervals.append((i, i+interval_size))
                i+=interval_size
        intervals_values = {}
        for each in df_column:
                for interval in intervals:
                        if each >= interval[0] and each < interval[1]:
                                if interval in intervals_values.keys():
                                        intervals_values[interval].append(each)
                                else: 
                                        intervals_values[interval] = [each]
        discretised = []
        for interval in intervals_values.keys():
                if method == "Mean":
                        if df_column.dtype == "int64":
                                discretised.append(round(mean(intervals_values[interval])))
                        else: discretised.append(mean(intervals_values[interval]))
                elif method == "Median":
                        discretised.append(median(pd.Series(intervals_values[interval])))
                elif method == "Mode":
                        discretised.append(mode(intervals_values[interval]))
                else: print("methode choisie invalide")
        discretised.sort()
        return discretised

def z_score_normalisation(dataframe):
        df = pd.DataFrame(dataframe)
        #dataframe = dataframe.select_dtypes(exclude=['object'])
        z_scores = []
        means = []
        std_devs = []
        for j in df.columns:
                if df[j].dtype !='object':
                        means.append(mean(df[[j]]).values[0])
                        std_devs.append(ecartType(df[[j]]).values[0])
        for i in range(0, dataframe.shape[0]):
                row = []
                c = 0
                for j in df.columns:
                        if df[j].dtype == 'object':
                                row.append(df[j].iloc[i])
                        else:
                                row.append(round(((df[[j]].iloc[i]-means[c])/std_devs[c]).values[0],9))
                                c+=1
                z_scores.append(row)
        normalized = pd.DataFrame(z_scores, columns = df.columns)
        return normalized


def min_max_normalisation(df, min_, max_):
        if max_ < min_ : 
                print("min superior to max, please change values")
                return df
        else:
                normalized_df = []
                #df = df.select_dtypes(exclude=['object'])
                min_old = []
                max_old = []
                for column in df.columns:
                        min_old.append(min(df[column]))
                        max_old.append(max(df[column]))
                for i in range(df.shape[0]):
                        row = []
                        c = 0
                        for column in df.columns:
                                if df[column].dtype == 'object':
                                        row.append(df[column].iloc[i])
                                else:
                                        if max_old[c] != min_old[c]:
                                                row.append(round((((df[column].iloc[i]-min_old[c])/(max_old[c]- min_old[c]))*(max_- min_))+min_,9))
                                        else:
                                                row.append(min_)
                                c+=1
                        normalized_df.append(row)
                normalized = pd.DataFrame(normalized_df, columns = df.columns)
        return normalized

def detect_redundant(df):
        redundances = df.duplicated()
        redundant_columns = []
        for each in df.columns:
                if len(df[each].unique()) == 1 or len(df[each].unique()) == df.shape[0]:
                        redundant_columns.append(each)
        return df[redundances], redundant_columns

def Del_Row(df, index):
        return df.drop([index], axis = 0)

def Del_Column(df, index):
        if type(index) is str:
                if index in df.columns:
                        df = df.drop([index], axis = 1)
        elif type(int(index)) is int:
                df = df.drop(df.columns[index], axis = 1)
        return df

def mean(df_column):
    return(np.sum(df_column)/len(df_column))
            
def median(df_column):
        df_column = df_column.sort_values(ascending=True).reset_index(drop=True)
        if len(df_column) % 2 == 0:
                return ((df_column[len(df_column)//2]+df_column[len(df_column)//2 - 1])/2)
        else: return df_column[len(df_column)//2]

def mode(df_column):
        freq = {}
        for elem in df_column:
                if elem in freq.keys():
                        freq[elem] += 1
                else : freq[elem] = 1
        return max(freq, key=freq.get)

def tendanceCentrale(df_column): #retourne la moyenne, mode et mediane ainsi que la symétrie
        tendances = []
        mean_ = mean(df_column)
        mode_ = mode(df_column)
        median_ = median(df_column)
        tendances.append(mean_)
        tendances.append(mode_)
        tendances.append(median_)
        if round(mean_,1) == round(mode_,1) and round(mean_,1) == round(median_,1) and round(median_,1) == round(mode_,1):
                tendances.append("Symétrique")
        elif round(mean_,1) > round(median_,1) and round(median_,1) > round(mode_,1):
                tendances.append("Positivement")
        elif round(mean_,1) < round(median_,1) and round(median_,1) < round(mode_,1):
                tendances.append("Négativement")
        else: tendances.append("Inindentifiée")
        return pd.Series(np.array(tendances), index=['mean', 'mode', 'median', 'symetrie'])

def ecartType(df_column):
    return(np.sqrt((np.sum(np.power(df_column-mean(df_column),2)))/len(df_column)))

def variance(df_column):
        return(np.power(ecartType(df_column),2))

def getQuartiles(df_column):
        df_column = df_column.sort_values(ascending=True).reset_index(drop=True)
        return (df_column[len(df_column)//4], df_column[(len(df_column)//4)*3])
        
def ecartInterquartile(df_column):
        Q1, Q3 = getQuartiles(df_column)
        return Q3-Q1
        
def dispersion(df_column): #get outlier data and make it into a pandas series
        mesures = []
        standard_deviation = ecartType(df_column)
        variance_ = variance(df_column)
        inter_q = ecartInterquartile(df_column)
        quart = getQuartiles(df_column)
        mesures.append(standard_deviation)
        mesures.append(variance_)
        mesures.append(inter_q)
        mesures.append(min(df_column))
        mesures.append(quart)
        mesures.append(max(df_column))
        outliers = []
        for each in df_column:
                if each > quart[1]+1.5*inter_q or each < quart[0]-1.5*inter_q:
                        outliers.append(each)
        return (pd.Series(np.array(mesures), index=['ecart_type', 'variance', 'IQR', 'min','quartiles', 'max']), set(outliers))
    
def correlation(df_column1, df_column2):
        df_column1 = pd.Series(df_column1.iloc[:,0])
        df_column2 = pd.Series(df_column2.iloc[:,0])
        try:
                N = np.float64(len(df_column1))
                xy_sum = np.float64(np.sum(df_column1*df_column2))
                top_sum = np.float64(N*xy_sum)
                sum_x = np.float64(np.sum(df_column1))
                sum_y = np.float64(np.sum(df_column2))
                bottom_x = np.float64(np.float64(len(df_column1))*np.float64(np.sum(df_column1*df_column1)))
                bottom_y = np.float64(np.float64(len(df_column2))*np.float64(np.sum(df_column2*df_column2)))
                return ((top_sum - (sum_x*sum_y))/np.sqrt(np.float64((bottom_x - np.power(sum_x,2))*(bottom_y - np.power(sum_y,2)))))
        except: print("impossible to calculate")

def replace_missing(df_column, method):
        if df_column.dtype == 'object':
                if method != 'mode': print('this method cannot be used on non-numerical attributes')
                else: 
                        for row in df_column.items():
                                if pd.isnull(row[1]) : 
                                        if method == 'Mode':
                                                df_column[row[0]] = mode(df_column)
        else:
                for row in df_column.items():
                        #print(df_column[0])
                        if pd.isnull(row[1]) : 
                                if method == 'Mode':
                                        df_column[row[0]] = mode(df_column)
                                elif method == 'Median':
                                        df_column[row[0]] = median(df_column)
                                elif method == 'Mean':
                                        df_column[row[0]] = mean(df_column)
                                else: print("an error has occured")
        return df_column

def treat_outliers(dataframe, df_column, method):
        outliers = dispersion(df_column)[1]
        df = dataframe.copy()
        #iterate through all rows
        for i in range(len(df_column)):
                if df_column.iloc[i] in outliers : 
                        if method == "Delete":
                                df=df.drop([i])
                        elif method == "Null":
                                df_column.iloc[i] = np.nan
                        elif method == "Mode":
                                df_column.iloc[i] = mode(df_column)
                        elif method == "Mean":
                                if df_column.dtype == "int64":
                                        df_column.iloc[i] = round(mean(df_column))
                                else: df_column.iloc[i] = mean(df_column)
                        elif method == "Median":
                                df_column.iloc[i] = median(df_column)
                                
                        else: print("la methode choisie est invalide")
        df[df_column.name] = df_column

        return df

import math
def getNull(dataframe):
        sums = {}
        for column in dataframe.columns:
                for i in range(len(dataframe[[column]])):
                        if math.isnan(dataframe[[column]].iloc[i].values[0]):
                                if column not in sums.keys():
                                        sums[column] = 1
                                else:sums[column] += 1
        return sums

def uniqueValues(df,dfColumn):
        return df[dfColumn].unique()
        
app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()
