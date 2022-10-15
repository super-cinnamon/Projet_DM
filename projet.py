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

class Ui(QtWidgets.QMainWindow):
        def __init__(self):
                super(Ui, self).__init__()
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

                self.boxplot_button= self.findChild(QtWidgets.QRadioButton,'boxplot_radio')
                self.boxplot_button.toggled.connect(self.BoxPlotListener)
                self.boxplot_button.setChecked(True)

                self.histoplot_button= self.findChild(QtWidgets.QRadioButton,'histogramme_radio')
                self.histoplot_button.toggled.connect(self.HistoPlotListener)

                self.scatter_button = self.findChild(QtWidgets.QRadioButton,'scatter_radio')
                self.scatter_button.toggled.connect(self.ScatterPlotListener)

                self.column1_combo = self.findChild(QtWidgets.QComboBox, 'scatter_column1')
                self.column2_combo = self.findChild(QtWidgets.QComboBox, 'scatter_column2')
                self.column1_combo.activated.connect(self.PlotScatterAuto)
                self.column2_combo.activated.connect(self.PlotScatterAuto)

                self.frame=self.findChild(QtWidgets.QWidget,'widget')

                self.dataset_info= self.findChild(QtWidgets.QLabel,'dataset_info')
                self.column_info= self.findChild(QtWidgets.QLabel,'column_info')
                self.correlation= self.findChild(QtWidgets.QLabel,'correlation_label')

                self.pandasTv=self.findChild(QtWidgets.QTableView,'pandasTv')
                self.pandasTv.setSortingEnabled(True)
                self.show()


        def UploadClickListener(self):
                self.path = QFileDialog.getOpenFileName(self, "Import CSV", "", "CSV data files (*.csv)")
                # path = QFileDialog.getOpenFileName(self, 'Open a file', '','All Files (*.*)') # if we want all files
                self.df = pd.read_csv(self.path[0])
                info="Nombre de lignes: "+str(self.df.shape[0])+"\nNombre de colonnes: "+str(self.df.shape[1])+"\nNombre de valeurs nulles: "+str(self.df.isnull().sum().sum())
                print(info)
                #self.dataset_info.setText(info)
                self.pandasTv_model = PandasModel(self.df)
                self.dataset_info.setText(info)
                self.pandasTv.setModel(self.pandasTv_model)
                self.pandasTv.clicked[QtCore.QModelIndex].connect(self.ColumnClickListener)
                if self.path != ('',''):
                        print(self.path[0])
                        return self.path[0]

        def SaveClickListener(self):
                try:
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
                                self.column_info.setText(info)
                        else:
                                info="Column name: "+str(self.df.columns[self.item.column()])+"\nColumn type: "+str(self.df.dtypes[self.df.columns[self.item.column()]])
                                print(info)
                                self.column_info.setText(info)
                except:
                        ctypes.windll.user32.MessageBoxW(0, "No dataset loaded.", "Error!", 0)


        def ColumnClickListener(self,item):
                print("with item")
                self.item=item
                print(item.column())
                print(self.df.columns[self.item.column()])
                print(self.df.dtypes[self.df.columns[item.column()]])
                self.df = pd.read_csv(self.path[0])
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
                        self.column_info.setText(info)
                else:
                        info="Column name: "+str(self.df.columns[item.column()])+"\nColumn type: "+str(self.df.dtypes[self.df.columns[item.column()]])
                        print(info)
                        #print("unique"+str(self.df[[self.df.columns[item.column()]]].unique()))
                        self.column_info.setText(info)

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
                                sns.distplot(self.df[self.df.columns[self.item.column()]],ax=sc.axes)

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
                                        sns.distplot(self.df[self.df.columns[self.item.column()]],ax=sc.axes)

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



app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()
