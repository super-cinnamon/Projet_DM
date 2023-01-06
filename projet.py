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
import random
import timeit
from collections import Counter
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
                self.setWindowIcon(QtGui.QIcon('pick_logo.png'))
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
                        ctypes.windll.user32.MessageBoxW(0, "List empty, press OK to proceed.", "", 0)
        def Okay(self):
                if len(self.methods)!=0:
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
                else:
                        ctypes.windll.user32.MessageBoxW(0, "No column added, please add at least one column.", "", 0)


        def Cancel(self):
                self.close()
		
class User_Input(QtWidgets.QDialog):
        def __init__(self,dataset,columns,tree,forest):
                super(User_Input, self).__init__()
                uic.loadUi('user_input.ui', self)
                self.setWindowIcon(QtGui.QIcon('pick_logo.png'))
                
                self.columns=columns
                self.nb_cols=len(columns)
                self.original_df=pd.read_csv('dataset1.csv')
                self.processed_df=dataset
                self.column_combo=self.findChild(QtWidgets.QComboBox,'column_combo')
                self.column_combo.addItems(self.columns)
                self.tree=tree
                self.forest=forest
                self.value_edit = self.findChild(QtWidgets.QPlainTextEdit,'value_edit')
                self.category_combo=self.findChild(QtWidgets.QComboBox,'category_combo')
                self.next_button=self.findChild(QtWidgets.QPushButton,'next_button')
                self.next_button.clicked.connect(self.Next)
                self.ok_button=self.findChild(QtWidgets.QPushButton,'ok')
                self.ok_button.clicked.connect(self.Okay)
                self.cancel_button=self.findChild(QtWidgets.QPushButton,'cancel_button')
                self.cancel_button.clicked.connect(self.Cancel)
                self.column_combo.activated.connect(self.column_changed)
                self.method_combo=self.findChild(QtWidgets.QComboBox,'method_combo')
                self.input = []
                self.indexes = []

                if len(self.original_df[self.column_combo.currentText()].unique())<=15 or self.original_df[self.column_combo.currentText()].dtype=='object':                        
                        self.value_edit.setEnabled(False)
                        self.category_combo.setEnabled(True)
                        if self.original_df[self.column_combo.currentText()].unique().dtype==np.int64 or self.original_df[self.column_combo.currentText()].unique().dtype==np.float64:
                                self.category_combo.addItems([str(x) for x in self.original_df[self.column_combo.currentText()].dropna().unique()])
                        else:
                                self.category_combo.addItems(self.original_df[self.column_combo.currentText()].unique())
                else:
                        self.value_edit.setEnabled(True)
                        self.category_combo.setEnabled(False)

                

        def column_changed(self):
                self.value_edit.clear()
                self.category_combo.clear()
                if len(self.original_df[self.column_combo.currentText()].unique())<=15 or self.original_df[self.column_combo.currentText()].dtype=='object':                        
                        self.value_edit.setEnabled(False)
                        self.category_combo.setEnabled(True)
                        if self.original_df[self.column_combo.currentText()].unique().dtype==np.int64 or self.original_df[self.column_combo.currentText()].unique().dtype==np.float64:
                                self.category_combo.addItems([str(x) for x in self.original_df[self.column_combo.currentText()].dropna().unique()])
                        else:
                                self.category_combo.addItems(self.original_df[self.column_combo.currentText()].unique())
                else:
                        self.value_edit.setEnabled(True)
                        self.category_combo.setEnabled(False)

        def Next(self):
                if(len(self.columns)!=0):
                        if len(self.original_df[self.column_combo.currentText()].unique())<=15 or self.original_df[self.column_combo.currentText()].dtype=='object':
                                self.input.append(self.category_combo.currentText())
                                self.indexes.append(self.column_combo.currentText())
                                self.columns.remove(self.column_combo.currentText())
                                self.column_combo.clear()
                                self.value_edit.clear()
                                self.category_combo.clear()
                                self.column_combo.addItems(self.columns)
                        else:
                                if self.original_df[self.column_combo.currentText()].dtype==np.int64 and self.value_edit.toPlainText().isdigit():                                        
                                        self.input.append(int(self.value_edit.toPlainText()))
                                        print(type(self.input[-1]))
                                        self.indexes.append(self.column_combo.currentText())
                                        self.columns.remove(self.column_combo.currentText())
                                        self.column_combo.clear()
                                        self.value_edit.clear()
                                        self.category_combo.clear()
                                        self.column_combo.addItems(self.columns)
                                        if(len(self.columns)!=0):

                                                if len(self.original_df[self.column_combo.currentText()].unique())<=15 or self.original_df[self.column_combo.currentText()].dtype=='object':                        
                                                        self.value_edit.setEnabled(False)
                                                        self.category_combo.setEnabled(True)
                                                        if self.original_df[self.column_combo.currentText()].unique().dtype==np.int64 or self.original_df[self.column_combo.currentText()].unique().dtype==np.float64:
                                                                self.category_combo.addItems([str(x) for x in self.original_df[self.column_combo.currentText()].dropna().unique()])
                                                        else:
                                                                self.category_combo.addItems(self.original_df[self.column_combo.currentText()].unique())
                                                else:
                                                        self.value_edit.setEnabled(True)
                                                        self.category_combo.setEnabled(False)
                                elif self.original_df[self.column_combo.currentText()].dtype==np.float64 and type(float(self.value_edit.toPlainText()))==self.original_df[self.column_combo.currentText()].dtype:
                                        self.input.append(float(self.value_edit.toPlainText()))
                                        print(type(self.input[-1]))
                                        self.indexes.append(self.column_combo.currentText())
                                        self.columns.remove(self.column_combo.currentText())
                                        self.column_combo.clear()
                                        self.value_edit.clear()
                                        self.category_combo.clear()
                                        self.column_combo.addItems(self.columns)
                                        if(len(self.columns)!=0):
                                                if len(self.original_df[self.column_combo.currentText()].unique())<=15 or self.original_df[self.column_combo.currentText()].dtype=='object':                        
                                                        self.value_edit.setEnabled(False)
                                                        self.category_combo.setEnabled(True)
                                                        if self.original_df[self.column_combo.currentText()].unique().dtype==np.int64 or self.original_df[self.column_combo.currentText()].unique().dtype==np.float64:
                                                                self.category_combo.addItems([str(x) for x in self.original_df[self.column_combo.currentText()].dropna().unique()])
                                                        else:
                                                                self.category_combo.addItems(self.original_df[self.column_combo.currentText()].unique())
                                                else:
                                                        self.value_edit.setEnabled(True)
                                                        self.category_combo.setEnabled(False)
                                else : ctypes.windll.user32.MessageBoxW(0, "Input must be integer or float.", "", 0)
                        
                else:
                        ctypes.windll.user32.MessageBoxW(0, "List empty, press OK to proceed.", "", 0)

        def Okay(self):
                if len(self.input)==self.nb_cols:
                        global prediction
                        series_topredict=pd.Series(self.input,index=self.indexes)
                        for column,value in series_topredict.items():
                                print(column,value)
                                if self.original_df[column].dtype !='object':
                                        old_min=float(self.original_df[column].min())
                                        old_max=float(self.original_df[column].max())
                                        new_min=float(self.processed_df[column].min())
                                        new_max=float(self.processed_df[column].max())
                                        series_topredict[column]=(float(value)-old_min)/(old_max-old_min)*(new_max-new_min)+new_min
                                elif column=='Gender':                                        
                                        self.original_df.loc[self.original_df[column]=='Female','Gender']=0
                                        self.original_df.loc[self.original_df[column]=='Male','Gender']=1
                                        if value == 'Female': value=0
                                        else: value=1
                                        if series_topredict[column] ==0:
                                                series_topredict[column]=0
                                                old_min=float(self.original_df[column].min())
                                                old_max=float(self.original_df[column].max())
                                                new_min=float(self.processed_df[column].min())
                                                new_max=float(self.processed_df[column].max())
                                                series_topredict[column]=(float(value)-old_min)/(old_max-old_min)*(new_max-new_min)+new_min
                                        else:
                                                series_topredict[column]=1
                                                old_min=float(self.original_df[column].min())
                                                old_max=float(self.original_df[column].max())
                                                new_min=float(self.processed_df[column].min())
                                                new_max=float(self.processed_df[column].max())
                                                series_topredict[column]=(float(value)-old_min)/(old_max-old_min)*(new_max-new_min)+new_min
                                elif column=='BusinessTravel':
                                        self.original_df.loc[self.original_df[column]=='Non-Travel','BusinessTravel']=0
                                        self.original_df.loc[self.original_df[column]=='Travel_Rarely','BusinessTravel']=1
                                        self.original_df.loc[self.original_df[column]=='Travel_Frequently','BusinessTravel']=2
                                        if value == 'Non-Travel': value=0
                                        elif value == 'Travel_Rarely': value=1
                                        else: value=2
                                        if series_topredict[column] ==0:
                                                series_topredict[column]=0
                                                old_min=float(self.original_df[column].min())
                                                old_max=float(self.original_df[column].max())
                                                new_min=float(self.processed_df[column].min())
                                                new_max=float(self.processed_df[column].max())
                                                series_topredict[column]=(float(value)-old_min)/(old_max-old_min)*(new_max-new_min)+new_min
                                        elif series_topredict[column] ==1:
                                                series_topredict[column]=1
                                                old_min=float(self.original_df[column].min())
                                                old_max=float(self.original_df[column].max())
                                                new_min=float(self.processed_df[column].min())
                                                new_max=float(self.processed_df[column].max())
                                                series_topredict[column]=(float(value)-old_min)/(old_max-old_min)*(new_max-new_min)+new_min
                                        else:
                                                series_topredict[column]=2
                                                old_min=float(self.original_df[column].min())
                                                old_max=float(self.original_df[column].max())
                                                new_min=float(self.processed_df[column].min())
                                                new_max=float(self.processed_df[column].max())
                                                series_topredict[column]=(float(value)-old_min)/(old_max-old_min)*(new_max-new_min)+new_min
                        print(series_topredict)

                        if(self.method_combo.currentText()=="Decision trees" and self.tree is not None) :
                                if self.tree is not None:
                                        prediction=predict_example(series_topredict,self.tree)
                                        print(prediction)
                                        self.close()
                        elif (self.method_combo.currentText()=="Random forest" and self.forest is not None):
                                if (self.forest is not None):   
                                        series_topredict = series_topredict.to_frame().T
                                        prediction = random_forest_predictions(series_topredict, self.forest)
                                        prediction = prediction[0]
                                        self.close()             

                        
                else:
                        ctypes.windll.user32.MessageBoxW(0, "Insert a value for all columns.", "", 0)

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

                self.preprocess= self.findChild(QtWidgets.QPushButton,'preprocess_button')
                self.preprocess.clicked.connect(self.Preprocess)

                self.apriori_exec= self.findChild(QtWidgets.QPushButton,'apriori_button')
                self.apriori_exec.clicked.connect(self.Apriori)

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
                self.Min_supp=self.findChild(QtWidgets.QDoubleSpinBox,'min_supp')
                self.Min_conf=self.findChild(QtWidgets.QDoubleSpinBox,'min_conf')
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

                self.categ_list=self.findChild(QtWidgets.QListView,'categ_list')
                self.categ_list.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
                self.listModel = QtGui.QStandardItemModel()
                self.categ_list.setModel(self.listModel)
                self.categ_combo=self.findChild(QtWidgets.QComboBox,'vids_categories')
                self.add_categ= self.findChild(QtWidgets.QPushButton,'add_categ')
                self.add_categ.clicked.connect(self.Add_Category)
                self.remove_categ= self.findChild(QtWidgets.QPushButton,'remove_categ')
                self.remove_categ.clicked.connect(self.Remove_Category)
                self.Recommend_button= self.findChild(QtWidgets.QPushButton,'recommend_button')
                self.Recommend_button.clicked.connect(self.Recommend)
                self.clear_button= self.findChild(QtWidgets.QPushButton,'clear_button')
                self.clear_button.clicked.connect(self.Clear)

                self.split_spin=self.findChild(QtWidgets.QDoubleSpinBox,'split_spin')
                self.split_button= self.findChild(QtWidgets.QPushButton,'split_btn')
                self.split_button.clicked.connect(self.Split)
                self.max_depth_tree=self.findChild(QtWidgets.QSpinBox,'max_depth_tree')
                self.generate_tree=self.findChild(QtWidgets.QPushButton,'gen_tree')
                self.generate_tree.clicked.connect(self.GenerateTree)
                self.runtimeedit = self.findChild(QtWidgets.QPlainTextEdit,'runtime')
                self.accuracyedit_tree = self.findChild(QtWidgets.QPlainTextEdit,'accuracy_edit')
                self.accracy_tree = self.findChild(QtWidgets.QPushButton,'get_accuracy_tree')
                self.accracy_tree.clicked.connect(self.GetAccuracyTree)
                self.specificityedit = self.findChild(QtWidgets.QPlainTextEdit,'specificity')
                self.sensitivityedit = self.findChild(QtWidgets.QPlainTextEdit,'sensitivity')
                self.precisionedit = self.findChild(QtWidgets.QPlainTextEdit,'precision')
                self.fscoreedit = self.findChild(QtWidgets.QPlainTextEdit,'fscore')
                self.nb_samples_spin = self.findChild(QtWidgets.QSpinBox,'nb_samples_spin')
                self.nb_trees_spin = self.findChild(QtWidgets.QSpinBox,'nb_trees_spin')
                self.max_depth_forest = self.findChild(QtWidgets.QSpinBox,'max_depth_forest')
                self.nb_features_forest = self.findChild(QtWidgets.QSpinBox,'nb_features_forest')
                self.generate_forest = self.findChild(QtWidgets.QPushButton,'gen_forest')
                self.generate_forest.clicked.connect(self.GenerateForest)
                self.get_acc_forest = self.findChild(QtWidgets.QPushButton,'get_acc_forest')
                self.get_acc_forest.clicked.connect(self.GetAccuracyForest)
                self.accuracyedit_forest = self.findChild(QtWidgets.QPlainTextEdit,'acc_forest')
                self.nb_bootstraps = self.findChild(QtWidgets.QSpinBox,'nb_bootstraps')
                self.insertvalues_btn = self.findChild(QtWidgets.QPushButton,'insertvalues_btn')
                self.insertvalues_btn.clicked.connect(self.InsertValues)
                self.tree=None
                self.forest=None
                self.class_predict= self.findChild(QtWidgets.QPlainTextEdit,'class_predict')
                self.matrix = self.findChild(QtWidgets.QTableView,'matrix')
                self.matrix.setStyleSheet("QTableView {background-color:rgb(99,78,163); color:white; gridline-color: black; border-color: rgb(242, 128, 133); font:350 11px 'Bahnschrift SemiLight';} QHeaderView::section {background-color: rgb(63, 50, 105);color: white;height: 20px;width: 20px; font:350 10px 'Bahnschrift SemiLight';} QTableCornerButton::section {background-color: rgb(63, 50, 105); color: rgb(200, 200, 200);}")
                self.matrix.resizeRowsToContents()
                self.matrix.resizeColumnsToContents()

                self.epsilon_spin = self.findChild(QtWidgets.QDoubleSpinBox,'epsilon_spin')
                self.min_samples_spin = self.findChild(QtWidgets.QSpinBox,'min_samples_spin')
                self.number_of_clusters_text = self.findChild(QtWidgets.QPlainTextEdit,'nb_clusters_text')
                self.execute_dbscan = self.findChild(QtWidgets.QPushButton,'execute_dbscan')
                self.execute_dbscan.clicked.connect(self.ExecuteDBSCAN)
                self.runtime_2 = self.findChild(QtWidgets.QPlainTextEdit,'runtime_2')
                self.noise_text = self.findChild(QtWidgets.QPlainTextEdit,'noise_text')
                self.accuracy_dbscan = self.findChild(QtWidgets.QPushButton,'accuracy_dbscan')
                self.accuracy_dbscan.clicked.connect(self.GetAccuracyDBSCAN)
                self.accuracy_edit_3 = self.findChild(QtWidgets.QPlainTextEdit,'accuracy_edit_3')
                self.sensitivity_2 = self.findChild(QtWidgets.QPlainTextEdit,'sensitivity_2')
                self.specificity_2 = self.findChild(QtWidgets.QPlainTextEdit,'specificity_2')
                self.precision_2 = self.findChild(QtWidgets.QPlainTextEdit,'precision_2')
                self.fscore_2 = self.findChild(QtWidgets.QPlainTextEdit,'fscore_2')
                self.matrix_2 = self.findChild(QtWidgets.QTableView,'matrix_2')
                self.matrix_2.setStyleSheet("QTableView {background-color:rgb(99,78,163); color:white; gridline-color: black; border-color: rgb(242, 128, 133); font:350 11px 'Bahnschrift SemiLight';} QHeaderView::section {background-color: rgb(63, 50, 105);color: white;height: 20px;width: 20px; font:350 10px 'Bahnschrift SemiLight';} QTableCornerButton::section {background-color: rgb(63, 50, 105); color: rgb(200, 200, 200);}")
                self.matrix_2.resizeRowsToContents()
                self.matrix_2.resizeColumnsToContents()
                self.linkage_combo = self.findChild(QtWidgets.QComboBox,'linkage_combo')
                self.execute_agnes = self.findChild(QtWidgets.QPushButton,'execute_agnes')
                self.execute_agnes.clicked.connect(self.ExecuteAGNES)
                self.nb_clusters_spin = self.findChild(QtWidgets.QSpinBox,'nb_clusters_spin')
                #self.get_results_agnes = self.findChild(QtWidgets.QPushButton,'get_results_agnes')
                #self.get_results_agnes.clicked.connect(self.GetResultsAGNES)
                self.accuracy_agnes = self.findChild(QtWidgets.QPushButton,'accuracy_agnes')
                self.accuracy_agnes.clicked.connect(self.GetAccuracyAGNES)
                self.inter_btn = self.findChild(QtWidgets.QPushButton,'inter_btn')
                self.inter_btn.clicked.connect(self.InterCluster)
                self.intra_btn = self.findChild(QtWidgets.QPushButton,'intra_btn')
                self.intra_btn.clicked.connect(self.IntraCluster)
                self.distances_list = self.findChild(QtWidgets.QListView,'distances_list')
                self.listModel2 = QtGui.QStandardItemModel()
                self.distances_list.setModel(self.listModel2)


                self.pandasTv=self.findChild(QtWidgets.QTableView,'pandasTv')
                self.pandasTv.setStyleSheet("QTableView {background-color:rgb(16, 5, 44);}")
                self.pandasTv.setSortingEnabled(True)
                self.loaded=False
                self.show()


        def UploadClickListener(self):
                try:

                        self.path = QFileDialog.getOpenFileName(self, "Import CSV", "", "CSV data files (*.csv);")
                        # path = QFileDialog.getOpenFileName(self, 'Open a file', '','All Files (*.*)') # if we want all files
                        self.df = pd.read_csv(self.path[0])
                        self.loaded=True
                        info="Nombre de lignes: "+str(self.df.shape[0])+"\nNombre de colonnes: "+str(self.df.shape[1])+"\nNombre de valeurs nulles: "+str(self.df.isnull().sum().sum())
                        print(info)
                        #self.dataset_info.setText(info)
                        self.pandasTv_model = PandasModel(self.df)
                        self.dataset_info.setText(info)
                        self.pandasTv.setModel(self.pandasTv_model)
                        self.pandasTv.setStyleSheet("QTableView {background-color:rgb(99,78,163); color:white; gridline-color: black; border-color: rgb(242, 128, 133); font:350 11px 'Bahnschrift SemiLight';} QHeaderView::section {background-color: rgb(63, 50, 105);color: white;height: 35px;width: 45px; font:350 11px 'Bahnschrift SemiLight';} QTableCornerButton::section {background-color: rgb(63, 50, 105); color: rgb(200, 200, 200);}")
                        self.pandasTv.clicked[QtCore.QModelIndex].connect(self.ColumnClickListener)
                        self.column_info.clear()
                        columns = list(self.df.columns)
                        self.replace_null_column.clear()
                        self.replace_null_column.addItems(columns)
                        self.replace_outlier_column.clear()
                        self.replace_outlier_column.addItems(columns)
                        self.categ_combo.clear()
                        if self.path != ('',''):
                                print(self.path[0])                                
                                if self.path[0].endswith('dataset2.csv'):
                                        self.all_categs = []
                                        for each in self.df['videoCategoryLabel']:
                                                self.all_categs.append(each)
                                        self.all_categs = list(set( self.all_categs))
                                        self.all_categs = [x.replace('_',' ') for x in  self.all_categs]
                                        self.categ_combo.addItems(self.all_categs)
                                        self.categ_combo.setEnabled(True)
                                return self.path[0]
                except:
                        ctypes.windll.user32.MessageBoxW(0, "Error occured.", "Error!", 0)

        def SaveClickListener(self):
                try:
                        if(self.loaded==True):
                                dialog = QtWidgets.QFileDialog()
                                self.path = dialog.getSaveFileName(self,"Save File","","CSV data files (*.csv);")
                                self.df.to_csv(self.path[0], index=False)
                                self.df = pd.read_csv(self.path[0])
                                info="Nombre de lignes: "+str(self.df.shape[0])+"\nNombre de colonnes: "+str(self.df.shape[1])+"\nNombre de valeurs nulles: "+str(self.df.isnull().sum().sum())
                                self.dataset_info.setText(info)
                                self.pandasTv_model = PandasModel(self.df)
                                self.pandasTv.setModel(self.pandasTv_model)
                                self.pandasTv.clicked[QtCore.QModelIndex].connect(self.ColumnClickListener)
                                self.column_info.clear()
                                # if (self.df.dtypes[self.df.columns[self.item.column()]] != 'object'):
                                #         td=tendanceCentrale(self.df[self.df.columns[self.item.column()]])
                                #         dis=dispersion(self.df[self.df.columns[self.item.column()]])
                                #         q=dis[0][4]
                                #         if len(dis[1])!=0:
                                #                 outliers=str(dis[1])
                                #         else:
                                #                 outliers="no outliers"
                                #         info="Column name: "+str(self.df.columns[self.item.column()])+"\nColumn type: "+str(self.df.dtypes[self.df.columns[self.item.column()]])+"\nMean: "+str(td['mean'])+"\nMedian: "+str(td['median'])+"\nMode: "+str(td['mode'])+"\nSymmetry: "+td['symetrie']+"\nEcart type: "+str(dis[0][0])+"\nVariance: "+str(dis[0][1])+"\nMin: "+str(dis[0][3])+"\nQ1: "+str(q[0])+"\nQ3: "+str(q[1])+"\nMax: "+str(dis[0][5])+"\nIQR: "+str(dis[0][2])+"\nOutliers: "+outliers
                                #                 #print(info)
                                #         self.column_info.clear()
                                #         self.column_info.insertPlainText(info)
                                # else:
                                #         info="Column name: "+str(self.df.columns[self.item.column()])+"\nColumn type: "+str(self.df.dtypes[self.df.columns[self.item.column()]])
                                #         print(info)
                                #         self.column_info.clear()
                                #         self.column_info.insertPlainText(info)
                        else:
                                ctypes.windll.user32.MessageBoxW(0, "No dataset loaded.", "Error!", 0)

                except:
                        ctypes.windll.user32.MessageBoxW(0, "Error occured.", "Error!", 0)


        def discretizeK(self):
                try:
                        data_num=[]
                        for col in self.df.columns:
                                if self.df[col].dtype != 'object':
                                        data_num.append(col)
                        self.second=Second(self.df,data_num,self.K_spin.value(),"K")
                        self.second.setModal(True)
                        self.second.setAttribute(QtCore.Qt.WA_DeleteOnClose)                
                        self.second.exec()
                        try:

                                self.df=table_discret.T
                                self.pandasTv_model = PandasModel(self.df)
                                info="Nombre de lignes: "+str(self.df.shape[0])+"\nNombre de colonnes: "+str(self.df.shape[1])+"\nNombre de valeurs nulles: "+str(self.df.isnull().sum().sum())
                                self.dataset_info.setText(info)
                                self.pandasTv.setModel(self.pandasTv_model)
                                self.pandasTv.clicked[QtCore.QModelIndex].connect(self.ColumnClickListener)
                        except:
                                ctypes.windll.user32.MessageBoxW(0, "Discretization was cancelled.", "Message", 0)
                except:
                        ctypes.windll.user32.MessageBoxW(0, "No dataset loaded.", "Error!", 0)


        def discretizeQ(self):
                try:                                
                        data_num=[]
                        for col in self.df.columns:
                                if self.df[col].dtype != 'object':
                                        data_num.append(col)
                        self.second=Second(self.df,data_num,self.Q_spin.value(),"Q")
                        self.second.setModal(True)
                        self.second.setAttribute(QtCore.Qt.WA_DeleteOnClose)                
                        self.second.exec()
                        try:

                                self.df=table_discret.T
                                self.pandasTv_model = PandasModel(self.df)
                                info="Nombre de lignes: "+str(self.df.shape[0])+"\nNombre de colonnes: "+str(self.df.shape[1])+"\nNombre de valeurs nulles: "+str(self.df.isnull().sum().sum())
                                self.dataset_info.setText(info)
                                self.pandasTv.setModel(self.pandasTv_model)
                                self.pandasTv.clicked[QtCore.QModelIndex].connect(self.ColumnClickListener)
                        except:
                                ctypes.windll.user32.MessageBoxW(0, "Discretization was cancelled.", "Message", 0)
                except:
                        ctypes.windll.user32.MessageBoxW(0, "No dataset loaded.", "Error!", 0)



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
                try:

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
                except:
                        ctypes.windll.user32.MessageBoxW(0, "No dataset loaded.", "Error!", 0)


        def ReplaceOutlier(self):
                try:

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
                except:
                        ctypes.windll.user32.MessageBoxW(0, "No dataset loaded.", "Error!", 0)

        def Normal_minmax(self):
                try:

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
                except:
                        ctypes.windll.user32.MessageBoxW(0, "No dataset loaded.", "Error!", 0)

        def Normal_zscore(self):
                try:
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
                except : 
                        ctypes.windll.user32.MessageBoxW(0, "No dataset loaded.", "Error!", 0)

        def Delete_Row_man(self):
                try:
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
                except:
                        ctypes.windll.user32.MessageBoxW(0, "No dataset loaded or no row selected.", "Error!", 0)

        def Delete_Col_man(self):
                try:
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
                except:
                        ctypes.windll.user32.MessageBoxW(0, "No dataset loaded or no column selected.", "Error!", 0)

        def auto_row(self):
                try:

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
                except:
                        ctypes.windll.user32.MessageBoxW(0, "No dataset loaded.", "Error!", 0)


        def auto_col(self):
                try:
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
                except:
                        ctypes.windll.user32.MessageBoxW(0, "No dataset loaded.", "Error!", 0)

        def organize_df(self,dataframe, new_index, target):
                new_df = dataframe.set_index(new_index)
                user_categs = {}
                for each in new_df.index.unique():
                        if(isinstance(new_df.loc[each][target], str)): 
                                user_categs[each] = [new_df.loc[each][target]]
                        else: 
                                user_categs[each] = list(set(new_df.loc[each][target]))
                return user_categs

        def Preprocess(self):
                try:
                        data=self.organize_df(self.df, "Watcher", "videoCategoryLabel")
                        users=data.keys()
                        rows=[]
                        for user in users:
                                row=[]
                                vids=data[user]
                                for vid in vids:
                                        row.append(vid)
                                rows.append(row)
                        df=pd.DataFrame(rows,users)
                        df.fillna(value=np.nan,inplace=True)
                        info="Nombre de lignes: "+str(df.shape[0])+"\nNombre de colonnes: "+str(df.shape[1])+"\nNombre de valeurs nulles: "+str(df.isnull().sum().sum())
                        print(info)
                        self.pandasTv_model = PandasModel(df)
                        self.pandasTv.setModel(self.pandasTv_model)
                        self.pandasTv.clicked[QtCore.QModelIndex].connect(self.ColumnClickListener)
                        self.dataset_info.setText(info)
                        self.column_info.clear()
                except:
                        ctypes.windll.user32.MessageBoxW(0, "Error occured.", "Error!", 0)
                

        def Apriori(self):
                try:
                        self.data = create_data_table(self.df)        
                        rules = algorithme_apriori(self.data, self.Min_supp.value(), self.Min_conf.value())
                        pd.set_option('display.max_colwidth', None)
                        self.association_rules = pd.DataFrame(rules, columns = ["Rule","Confidence","Lift"])
                        self.df=self.association_rules                
                        info="Nombre de lignes: "+str(self.df.shape[0])+"\nNombre de colonnes: "+str(self.df.shape[1])+"\nNombre de valeurs nulles: "+str(self.df.isnull().sum().sum())
                        print(info)
                        #self.dataset_info.setText(info)
                        self.pandasTv_model = PandasModel(self.df)
                        self.pandasTv.clicked[QtCore.QModelIndex].connect(self.ColumnClickListener)
                        self.pandasTv.setModel(self.pandasTv_model)
                        self.dataset_info.setText(info)
                        self.column_info.clear()
                except:
                        ctypes.windll.user32.MessageBoxW(0, "Error occured.", "Error!", 0)
                
        def Add_Category(self):
                try:
                        self.listModel.appendRow(QtGui.QStandardItem(self.categ_combo.currentText()))
                except:
                        ctypes.windll.user32.MessageBoxW(0, "Error occured.", "Error!", 0)

        def Remove_Category(self):
                try:
                        if self.listModel.rowCount()>0:
                                indexes = self.categ_list.selectedIndexes()
                                if indexes:
                                        index = indexes[0]
                                        self.listModel.removeRow(index.row())
                except:
                        ctypes.windll.user32.MessageBoxW(0, "Error occured.", "Error!", 0)

        def Recommend(self):
                try:
                        categs = []
                        for index in range(self.listModel.rowCount()):
                                item = self.listModel.item(index).text()
                                categs.append(item)
                        self.listModel.removeRows( 0, self.listModel.rowCount())
                        recoms = get_relevent_rules(self.association_rules,list(set(categs)))
                        recoms.extend(categs)
                        categs=list(set(recoms))
                        print (categs)
                        for each in categs:
                                self.listModel.appendRow(QtGui.QStandardItem(each))
                except:
                        ctypes.windll.user32.MessageBoxW(0, "Error occured.", "Error!", 0)

        def Clear(self):
                self.listModel.removeRows( 0, self.listModel.rowCount() )

        def Split(self):
                self.data = self.df
                self.data['label'] = self.data.Attrition
                self.data = self.data.drop("Attrition", axis=1)
                self.train_df, self.test_df = train_test_split(self.data, test_size=self.split_spin.value())
                print(self.train_df)

        def GenerateTree(self):
                try:    
                        print(self.max_depth_tree.value())                
                        start = timeit.default_timer()
                        self.tree = decision_tree_algorithm(self.train_df,min_samples=self.nb_samples_spin.value(), max_depth=self.max_depth_tree.value())
                        stop = timeit.default_timer()
                        print(stop-start)
                        self.runtimeedit.clear()
                        self.runtimeedit.insertPlainText(str(round(stop-start,3)))
                        
                except:
                        ctypes.windll.user32.MessageBoxW(0, "Error occured.", "Error!", 0)

        def GetAccuracyTree(self):
                try:
                        start = timeit.default_timer()
                        self.predictions = decision_tree_predictions(self.test_df, self.tree)
                        self.accuracy = calculate_accuracy(self.predictions, self.test_df.label)
                        self.f_score = f_score(self.test_df.label,self.predictions)
                        self.precision = precision(self.test_df.label,self.predictions)
                        self.sensitivity = sensitivity(self.test_df.label,self.predictions )
                        self.specificity = specificity(self.test_df.label,self.predictions )
                        stop = timeit.default_timer()
                        print(stop-start)
                        self.runtimeedit.clear()
                        self.accuracyedit_tree.clear()
                        self.specificityedit.clear()
                        self.sensitivityedit.clear()
                        self.precisionedit.clear()
                        self.fscoreedit.clear()
                        self.runtimeedit.insertPlainText(str(round(stop-start,3)))
                        self.accuracyedit_tree.insertPlainText(str(round(self.accuracy,3)))
                        self.specificityedit.insertPlainText(str(round(self.specificity,3)))
                        self.sensitivityedit.insertPlainText(str(round(self.sensitivity,3)))
                        self.precisionedit.insertPlainText(str(round(self.precision,3)))
                        self.fscoreedit.insertPlainText(str(round(self.f_score,3)))
                        self.matrix_model = PandasModel(pd.DataFrame(confusion_matrix(self.predictions,self.test_df.label),index=['1','0'],columns=['1','0']))
                        self.matrix.resizeRowsToContents()
                        self.matrix.resizeColumnsToContents()
                        self.matrix.setModel(self.matrix_model)
                except:
                        ctypes.windll.user32.MessageBoxW(0, "Error occured.", "Error!", 0)

        def GenerateForest(self):
                try:
                        start = timeit.default_timer()
                        self.forest = random_forest_algorithm(train_df = self.train_df,n_trees= self.nb_trees_spin.value(),dt_max_depth=self.max_depth_tree.value(),n_bootstrap=self.nb_bootstraps.value(),n_features=self.nb_features_forest.value())
                        stop = timeit.default_timer()
                        print(stop-start)
                        self.runtimeedit.clear()
                        self.runtimeedit.insertPlainText(str(round(stop-start,3)))
                except:
                        ctypes.windll.user32.MessageBoxW(0, "Error occured.", "Error!", 0)

        def GetAccuracyForest(self):
                try:
                        start = timeit.default_timer()
                        self.predictions = random_forest_predictions(self.test_df, self.forest)
                        self.accuracy = calculate_accuracy(self.predictions, self.test_df.label)
                        self.f_score = f_score(self.test_df.label,self.predictions)
                        self.precision = precision(self.test_df.label,self.predictions)
                        self.sensitivity = sensitivity(self.test_df.label,self.predictions )
                        self.specificity = specificity(self.test_df.label,self.predictions )
                        stop = timeit.default_timer()
                        print(stop-start)
                        self.runtimeedit.clear()
                        self.accuracyedit_forest.clear()
                        self.specificityedit.clear()
                        self.sensitivityedit.clear()
                        self.precisionedit.clear()
                        self.fscoreedit.clear()
                        self.runtimeedit.insertPlainText(str(round(stop-start,3)))
                        self.accuracyedit_forest.insertPlainText(str(round(self.accuracy,3)))
                        self.specificityedit.insertPlainText(str(round(self.specificity,3)))
                        self.sensitivityedit.insertPlainText(str(round(self.sensitivity,3)))
                        self.precisionedit.insertPlainText(str(round(self.precision,3)))
                        self.fscoreedit.insertPlainText(str(round(self.f_score,3)))
                        self.matrix_model = PandasModel(pd.DataFrame(confusion_matrix(self.predictions,self.test_df.label),index=['1','0'],columns=['1','0']))
                        self.matrix.resizeRowsToContents()
                        self.matrix.resizeColumnsToContents()
                        self.matrix.setModel(self.matrix_model)
                except:
                        ctypes.windll.user32.MessageBoxW(0, "Error occured.", "Error!", 0)

        def InsertValues(self):
                data_num=[]
                for col in self.df.columns:
                        if col not in ['Attrition','label'] :
                                data_num.append(col)
                self.user_input= User_Input(self.df,data_num,self.tree,self.forest)
                self.user_input.setModal(True)
                self.user_input.setAttribute(QtCore.Qt.WA_DeleteOnClose)                
                self.user_input.exec()
                try:
                        if prediction == 0:
                                self.class_predict.clear()
                                self.class_predict.insertPlainText("No")
                        else:
                                self.class_predict.clear()
                                self.class_predict.insertPlainText("Yes")
                except:
                        ctypes.windll.user32.MessageBoxW(0, "Error occured.", "Error!", 0)
        
        def ExecuteDBSCAN(self):
                try:
                        old_df = self.df.copy()
                        df = old_df.copy()
                        columns = ['Department', 'EducationField', 'JobRole', 'MaritalStatus', 'OverTime']
                        print('prob 1')
                        #target based encoding, each category of the column will bear the mean
                        for column in columns:
                                if column == 'Department':
                                        df[column] = df.groupby(column)['JobSatisfaction'].transform('mean')
                                elif column == 'EducationField':
                                        df[column] = df.groupby(column)['HourlyRate'].transform('mean')
                                elif column == 'JobRole':
                                        df[column] = df.groupby(column)['HourlyRate'].transform('mean')
                                elif column == 'MaritalStatus':
                                        df[column] = df.groupby(column)['WorkLifeBalance'].transform('mean')
                                elif column == 'OverTime':
                                        df[column] = df.groupby(column)['YearsSinceLastPromotion'].transform('mean')
                        print('prob 2')
                        self.Y = old_df['Attrition'].values
                        df = df.drop(['Attrition'], axis=1)
                        self.X = df.values
                        print('prob 3')
                        start = timeit.default_timer()
                        self.dbscan = DBSCAN(eps=self.epsilon_spin.value(), min_pts=self.min_samples_spin.value(),data=self.X)
                        self.dbscan.fit()                        
                        stop = timeit.default_timer()
                        print(stop-start)
                        self.clusters = self.dbscan.get_clusters()
                        self.noise = self.dbscan.get_noise()
                        self.number_of_clusters_text.clear()
                        self.number_of_clusters_text.insertPlainText(str(len(self.clusters)))
                        self.noise_text.clear()
                        self.noise_text.insertPlainText(str(len(self.noise)))
                        self.runtime_2.clear()
                        self.runtime_2.insertPlainText(str(round(stop-start,3)))
                except Exception as e:
                        print(e)
                        ctypes.windll.user32.MessageBoxW(0, "Error occured.", "Error!", 0)

        def GetAccuracyDBSCAN(self):
                try:
                        self.dbscan_res = {}
                        val = 0
                        for cluster in self.dbscan.get_clusters():
                                for i in cluster:
                                        self.dbscan_res[i] = val
                                val += 1
                        self.dbscan_res = {k: self.dbscan_res[k] for k in sorted(self.dbscan_res)}
                        self.dbscan_res = list(self.dbscan_res.values())
                        noise = self.dbscan.get_noise()
                        R = np.delete(self.Y, noise)
                        self.dbscan_res = np.array(self.dbscan_res)
                        self.accuracy_edit_3.clear()
                        self.accuracy_edit_3.insertPlainText(str(round(accuracy(R, self.dbscan_res),3)))
                        self.sensitivity_2.clear()
                        self.sensitivity_2.insertPlainText(str(round(sensitivity(R, self.dbscan_res),3)))
                        self.specificity_2.clear()
                        self.specificity_2.insertPlainText(str(round(specificity(R, self.dbscan_res),3)))
                        self.precision_2.clear()
                        self.precision_2.insertPlainText(str(round(precision(R, self.dbscan_res),3)))
                        self.fscore_2.clear()
                        self.fscore_2.insertPlainText(str(round(f_score(R, self.dbscan_res),3)))
                        self.matrix_model_2 = PandasModel(pd.DataFrame(confusion_matrix(R, self.dbscan_res),index=['1','0'],columns=['1','0']))
                        self.matrix_2.resizeRowsToContents()
                        self.matrix_2.resizeColumnsToContents()
                        self.matrix_2.setModel(self.matrix_model_2)

                except Exception as e:
                        print(e)
                        ctypes.windll.user32.MessageBoxW(0, "Error occured.", "Error!", 0)

        def ExecuteAGNES(self):
                try:
                        old_df = self.df.copy()
                        df = old_df.copy()
                        columns = ['Department', 'EducationField', 'JobRole', 'MaritalStatus', 'OverTime']
                        print('prob 1')
                        #target based encoding, each category of the column will bear the mean
                        for column in columns:
                                if column == 'Department':
                                        df[column] = df.groupby(column)['JobSatisfaction'].transform('mean')
                                elif column == 'EducationField':
                                        df[column] = df.groupby(column)['HourlyRate'].transform('mean')
                                elif column == 'JobRole':
                                        df[column] = df.groupby(column)['HourlyRate'].transform('mean')
                                elif column == 'MaritalStatus':
                                        df[column] = df.groupby(column)['WorkLifeBalance'].transform('mean')
                                elif column == 'OverTime':
                                        df[column] = df.groupby(column)['YearsSinceLastPromotion'].transform('mean')
                        print('prob 2')
                        self.Y = old_df['Attrition'].values
                        df = df.drop(['Attrition'], axis=1)
                        self.X = df.values
                        print('prob 3')
                        start = timeit.default_timer()
                        self.agnes = AGNES(n_clusters=self.nb_clusters_spin.value(), linkage=self.linkage_combo.currentText())
                        self.agnes.fit_predict(self.X)
                        stop = timeit.default_timer()
                        print(stop-start)
                        self.runtime_2.clear()
                        self.runtime_2.insertPlainText(str(round(stop-start,3)))
                except Exception as e:
                        print(e)
                        ctypes.windll.user32.MessageBoxW(0, "Error occured.", "Error!", 0)

        def GetAccuracyAGNES(self):
                try :
                        results = self.agnes.get_results()
                        self.accuracy_edit_3.clear()
                        self.accuracy_edit_3.insertPlainText(str(round(accuracy(self.Y, results[self.nb_clusters_spin.value()][0]),3)))
                        self.sensitivity_2.clear()
                        self.sensitivity_2.insertPlainText(str(round(sensitivity(self.Y, results[self.nb_clusters_spin.value()][0]),3)))
                        self.specificity_2.clear()
                        self.specificity_2.insertPlainText(str(round(specificity(self.Y, results[self.nb_clusters_spin.value()][0]),3)))
                        self.precision_2.clear()
                        self.precision_2.insertPlainText(str(round(precision(self.Y, results[self.nb_clusters_spin.value()][0]),3)))
                        self.fscore_2.clear()
                        self.fscore_2.insertPlainText(str(round(f_score(self.Y, results[self.nb_clusters_spin.value()][0]),3)))
                        self.matrix_model_2 = PandasModel(pd.DataFrame(confusion_matrix(self.Y, results[self.nb_clusters_spin.value()][0]),index=['1','0'],columns=['1','0']))
                        self.matrix_2.resizeRowsToContents()
                        self.matrix_2.resizeColumnsToContents()
                        self.matrix_2.setModel(self.matrix_model_2)
                except Exception as e:
                        print(e)
                        ctypes.windll.user32.MessageBoxW(0, "Error occured.", "Error!", 0)

        def InterCluster(self):
                try:
                        results = self.agnes.get_results()
                        self.listModel2.removeRows( 0, self.listModel2.rowCount())
                        for item in inter_cluster(self.X,results[self.nb_clusters_spin.value()][0]):
                                self.listModel2.appendRow(QtGui.QStandardItem(str(item)))   
                except Exception as e:
                        print(e)
                        ctypes.windll.user32.MessageBoxW(0, "Error occured.", "Error!", 0)
        
        def IntraCluster(self):
                try:
                        results = self.agnes.get_results()
                        self.listModel2.removeRows( 0, self.listModel2.rowCount())
                        for item in intra_cluster(self.X,results[self.nb_clusters_spin.value()][0]):
                                self.listModel2.appendRow(QtGui.QStandardItem(str(item)))                        
                except Exception as e:
                        print(e)
                        ctypes.windll.user32.MessageBoxW(0, "Error occured.", "Error!", 0)

def get_relevent_rules(association_rules, list_of_interests):
        recommendation = []
        for r in association_rules.Rule:
                rule = r.replace('{', '')
                rule = rule.replace('}', '')
                rule = rule.replace("'", '')
                rule = rule.split(" ---> ")
                X = rule[0].split(", ")
                Y = rule[1].split(", ")
                if any(list_of_interests[idx : idx + len(X)] == X for idx in range(len(list_of_interests) - len(X) + 1)):
                        recommendation.extend(Y)
        return list(set(recommendation))

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
                                df=df.drop([i],axis=0)
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
        df=df.reset_index(drop=True)
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

# fonction qui convertis le dataset au format adapté pour l'execution de l'algo apriori
def create_data_table(df):
    # On enleve les espaces pour eviter des bugs lors de l'execution de l'algo
    for d in df["videoCategoryLabel"].unique():
        dd = d.replace(" ", "_")
        df["videoCategoryLabel"] = df["videoCategoryLabel"].replace(d, dd)

    # Pour chaque transaction (watcher) on lui associes ses items (videoCategoryLabel)
    data = dict()
    for d in df["Watcher"].unique():
        t = df.loc[df["Watcher"] == d]
        data[d] = list(set(t["videoCategoryLabel"]))

    return data

# fonction qui retourne une liste d'item dans le meme format que dans lequel ils se trouvent dans le dictionaire de base
def item_format(item):
    item_list = list(item.split("'"))
    special_characters = "[', ']"
    # les items etant stocker sours le formet ['X'] on le rend sous le format X
    item_list_format = [i for i in item_list if  i not in special_characters]
    return item_list_format

# fonction qui crée les tables C1, C2, C3,...,Ck
def create_ck_table(data, lk, k):
    c = Counter() # structure pythonique pour conter les objets

    if k == 1: # Dans le cas ou on construit C1 on récupére les items de notre dataset
        item_set = list(set(sum(data.values(), [])))
    else: # sinon on pour k >= 2 on les récupère de la table L(k-1)
        item_set = set()
        temp = list(lk)
        # on réalise des k-itemset unique en faisant des unions avec les objets de la table L(k-1)
        for i in range(0,len(temp)):
            for j in range(i+1,len(temp)):
                t = {z for z in item_format(temp[i])}.union({w for w in item_format(temp[j])})
                if(len(t) == k):
                    t = sorted(t)
                    item_set.add(str(t))
        item_set = list(item_set)

    # on compte le support de chaque k-itemset obtenue
    for i in item_set:
        c[i] = 0
        for d in data.values():
            if all(item in d for item in item_format(i)):
                c[i] += 1
    
    return c

# fonction qui crée les tables L1, L2, L3,...,Lk
def create_lk_table(data, ck, k, s):
    l = Counter()
    # On conserve uniquement les k-itemset de la table Ck qui vérifie le min support
    for i in ck:
        if(ck[i] >= s):
            l[str(i)] += ck[i]
    return l

# fonction qui permet de sauvegarder la table Lk dans l'ensemble L
def save_lk_table(lk, k):
    final = []
    for i in lk:
        i_set = set()
        for it in item_format(i):
            i_set.add(it)
        final.append(i_set)
    return final

# execution de l'algo apriori
def apriori(data,s):
    min_s = len(data) * s # calcule du minimum support
    final = [] # l'ensemble final L
    ck = Counter() # Table Ck
    lk = Counter() # Table Lk

    #On fixe la limite a 1000 pour etre sur de terminer l'execution de l'algorithme
    for k in range(1,1000):
        ck = create_ck_table(data,lk,k)
        if len(ck) == 0: # si la table Ck est vide on termine l'algo
            break

        lk = create_lk_table(data,ck,k,min_s)
        if len(lk) == 0: # si la table Lk est vide on termine l'algo
            break
        
        # On sauvegarde les k-itemset de la table Lk dans l'ensemble L
        l_items = save_lk_table(lk,k)
        for li in l_items:
            final.append(li)
    
    return final

# fonction qui combine tout les items de l'ensemble L entre eux pour obtenir toutes les combinaisons possibles
def pair_up(items):
    pairs = []
    for i in range(len(items)):
        for j in range(len(items)):
            pairs.append((items[i],items[j]))
    return pairs

# fonction qui retournes l'ensembles des régles possibles
# une régle est sous la forme {X --> Y} avec X et Y des itemset
def make_rules(items):
    rules = pair_up(items) # on récupère toutes les combinaisons d'itemset possible
    final_rules = list()

    # on filtres les combinaisons qui sont acceptables comme regles
    for r in rules :
        X = list(r[0])
        Y = list(r[1])
        # Dans le cas ou X intersection Y != {} on retire les items en commun de Y 
        for x in X:
            if x in Y:
                Y.remove(x)
        # Dans le cas ou la régle n'existe pas dèja et que l'itemset Y n'est pas vide après lui avoir
        # retiré les items commun on sauvegarde la régle
        if (X,Y) not in final_rules and len(Y) != 0:
            final_rules.append((X,Y))

    return final_rules

# fonction qui retourne les régles ayant une confiance supperieur a la confiance minimum 
# elle retourne aussi pour chaque regle sa confiance et son lift
def association_correlation_rules(data, items, min_conf):
    table = []
    rules = make_rules(items) # recupere les regles 
    min_c = min_conf * len(data.values()) # on calcule la confiance minimum

    # pour chaque regle on calcule sa confiance et on vérifie si elle est sup a la conf min
    for fr in rules:
        x, y = fr # on recupere les itemsets de la regle par exemple pour la regle {I1, I2} --> {I3, I4}
                # on obtient x = {I1, I2} et y = {I3, I4}

        xy = sum(fr,[]) # transforme la regle de {I1, I2} --> {I3, I4} a {I1, I2, I3, I4}

        count_x, count_y, count_xy = 0, 0, 0 # on initialise un compteur pour chaque itemset

        # on remet les espaces enlever au debut pour l'affichage final
        str_x, str_y = str(set(x)).replace("_", " "), str(set(y)).replace("_", " ")
        rule = str_x +" ---> "+ str_y

        # On calcule la frequence de chaque itemset dans notre dataset
        for d in data.values():
            if x[0] in d:
                count_x += 1
            if y[0] in d:
                count_y += 1
            check =  all(item in d for item in xy)
            if check:
                count_xy += 1
        
        # on calcule leur support 
        support_x = count_x / len(data.values())
        support_y = count_y / len(data.values())
        support_xy = count_xy / len(data.values())

        conf = support_xy / support_x  # On calcule la confiance de la regle 
        lift = support_xy / (support_x * support_y) # On calcule le lift de la regle

        if (conf * len(data.values()) >= min_c): # si la confiance de la regle >= min_c on la sauvegarde avec sa confiance et son lift
            table.append([rule, str(int(conf*100))+"%", "{:.2f}".format(round(support_xy, 2))])
    return table

# Version final de l'algo regroupant toute les fonctions
def algorithme_apriori(data,min_support,min_confidence):
    L = apriori(data,min_support)
    return association_correlation_rules(data, L, min_confidence)

# Retourne les conséquents (Y) de toutes les règles avec un item particulier comme antécédant (X)
def get_recommendation(item, rules):
    recomendations = []
    for r in rules :
        rule = r[0].split(" ---> ")
        X = rule[0]
        Y = rule[1]
        if X == item:
            recomendations.append(Y)
    return recomendations

# 1. Train-Test-Split, 
# test size is the percentage of the dataset that should be in the test set
def train_test_split(df, test_size):
    # make sure it is a float and get the number of instances in the test set
    if isinstance(test_size, float):
        test_size = round(test_size * len(df))
    # get the indices for the test set
    indices = df.index.tolist()
    # choose them randomly
    test_indices = random.sample(population=indices, k=test_size)
    # separate into test and train
    test_df = df.loc[test_indices]
    train_df = df.drop(test_indices)
    
    return train_df, test_df


# 2. Distinguish categorical and continuous features
def determine_type_of_feature(df):
    # in order to properly split the nodes, we need to know if a feature is categorical or continuous
    feature_types = []
    # this threshold is used to determine if a feature is categorical, it can be changed
    n_unique_values_treshold = 15
    for feature in df.columns:
        # get all features except for the label
        if feature != "label":
            unique_values = df[feature].unique()
            example_value = unique_values[0]
            # we use the number of unique values and the type of the first value to determine the type of the feature
            if (isinstance(example_value, str)) or (len(unique_values) <= n_unique_values_treshold):
                feature_types.append("categorical")
            else:
                feature_types.append("continuous")
    
    return feature_types


# 3. Accuracy
def calculate_accuracy(predictions, labels):
    # calculate the accuracy of the predictions
    # we compare the predictions to the labels and count the number of correct predictions
    predictions_correct = predictions == labels
    accuracy = predictions_correct.mean()
    
    return accuracy

# another method to calculate accuracy
def accuracy(y_true, y_pred):
    accuracy = np.sum(y_true == y_pred) / len(y_true)
    return accuracy

def precision(y_true, y_pred):
    tp = np.sum(y_true * y_pred)
    fp = np.sum((1 - y_true) * y_pred)
    return tp / (tp + fp)

def sensitivity(y_true, y_pred):
    tp = np.sum(y_true * y_pred)
    fn = np.sum(y_true * (1 - y_pred))
    return tp / (tp + fn)

def specificity(y_true, y_pred):
    tn = np.sum((1 - y_true) * (1 - y_pred))
    fp = np.sum((1 - y_true) * y_pred)
    return tn / (tn + fp)

def f_score(y_true, y_pred):
    tp = np.sum(y_true * y_pred)
    fn = np.sum(y_true * (1 - y_pred))
    fp = np.sum((1 - y_true) * y_pred)
    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    return 2 * precision * recall / (precision + recall)

# confusion matrix containing true positives, false negatives, false positives and true negatives
def confusion_matrix(y_true, y_pred):
    tp = np.sum(y_true * y_pred)
    fn = np.sum(y_true * (1 - y_pred))
    fp = np.sum((1 - y_true) * y_pred)
    tn = np.sum((1 - y_true) * (1 - y_pred))
    return np.array([[tp, fn], [fp, tn]])

# 1. Decision Tree helper functions 

# 1.1 Data pure
def check_purity(data):
    # check if labels are pure, i.e. all belong to the same class
    label_column = data[:, -1]
    unique_classes = np.unique(label_column)

    if len(unique_classes) == 1:
        return True
    else:
        return False

    
# 1.2 Classify
def classify_data(data):
    # get the labels of the data and return the most common one (majority vote)
    label_column = data[:, -1]
    unique_classes, counts_unique_classes = np.unique(label_column, return_counts=True)

    index = counts_unique_classes.argmax()
    classification = unique_classes[index]
    
    return classification


# 1.3 Potential splits?
def get_potential_splits(data, random_subspace):
    
    potential_splits = {}
    _, n_columns = data.shape
    column_indices = list(range(n_columns - 1))    # excluding the last column which is the label
    
    # if we decide to take a limited amount of features, we randomly choose a subset of them, this is only used for random forests
    if random_subspace and random_subspace <= len(column_indices):
        column_indices = random.sample(population=column_indices, k=random_subspace)
    
    # we iterate over all columns and find the unique values in each column, in order to determine the splits in our decision tree
    for column_index in column_indices:          
        values = data[:, column_index]
        unique_values = np.unique(values)
        
        potential_splits[column_index] = unique_values
    
    return potential_splits


# 1.4 Lowest Overall Entropy?
def calculate_entropy(data):
    # simply calculate the entropy of the data
    label_column = data[:, -1]
    _, counts = np.unique(label_column, return_counts=True)

    probabilities = counts / counts.sum()
    entropy = sum(probabilities * -np.log2(probabilities))
     
    return entropy

# this is done to calculate the entropy of the split leaves
def calculate_overall_entropy(data_below, data_above):
    # data below is the left leaf and data above is the right leaf
    n = len(data_below) + len(data_above)
    p_data_below = len(data_below) / n
    p_data_above = len(data_above) / n
    
    #calculate both their entropy, sum them and return the overall entropy
    overall_entropy =  (p_data_below * calculate_entropy(data_below) 
                      + p_data_above * calculate_entropy(data_above))
    
    return overall_entropy


def determine_best_split(data, potential_splits):
    # we iterate over all potential splits and calculate the overall entropy of the split leaves
    overall_entropy = 9999
    for column_index in potential_splits:
        for value in potential_splits[column_index]:
            data_below, data_above = split_data(data, split_column=column_index, split_value=value)
            # remove empty lines
            if(len(data_below)==0 or len(data_above)==0):
                break
            
            current_overall_entropy = calculate_overall_entropy(data_below, data_above)
            #compare last calculated overall entropy with the current one, if it is lower, we update the best split
            if current_overall_entropy <= overall_entropy:
                overall_entropy = current_overall_entropy
                best_split_column = column_index
                best_split_value = value
    #once we have iterated over all potential splits and compared them, we return the best split
    return best_split_column, best_split_value


# 1.5 Split data
def split_data(data, split_column, split_value):
    
    split_column_values = data[:, split_column]
    #check the type of the feature whether it is continuous or categorical
    type_of_feature = FEATURE_TYPES[split_column]
    if type_of_feature == "continuous":
        #if continuous we compare in values larger or smaller
        data_below = data[split_column_values <= split_value]
        data_above = data[split_column_values >  split_value]
    
    # feature is categorical   
    else:
        #if feature is categorical we compare in values equal or not equal
        data_below = data[split_column_values == split_value]
        data_above = data[split_column_values != split_value]
    # we return the leaves
    return data_below, data_above


# 2. Decision Tree Algorithm
def decision_tree_algorithm(df, counter=0, min_samples=2, max_depth=5, random_subspace=None):
    
    # data preparations
    if counter == 0:
        # we need to store the data globally, so we can use it in the helper functions
        global COLUMN_HEADERS, FEATURE_TYPES
        COLUMN_HEADERS = df.columns
        FEATURE_TYPES = determine_type_of_feature(df)
        data = df.values
    else:
        data = df           
    
    
    # base cases
    # since our loop is recursive, this will be our end case for a leaf node
    # if the node only has data of one class, we return the class and stop splitting, it will then be a terminal leaf node
    if (check_purity(data)) or (len(data) < min_samples) or (counter == max_depth):
        classification = classify_data(data)
        
        return classification

    
    # recursive part
    else:    
        counter += 1

        # helper functions 
        potential_splits = get_potential_splits(data, random_subspace)
        split_column, split_value = determine_best_split(data, potential_splits)
        data_below, data_above = split_data(data, split_column, split_value)
        
        # check for empty data
        if len(data_below) == 0 or len(data_above) == 0:
            classification = classify_data(data)
            # the node cannod be split anymore, so we return the class, it is a terminal node
            return classification
        
        # determine question
        feature_name = COLUMN_HEADERS[split_column]
        type_of_feature = FEATURE_TYPES[split_column]
        # feature is continuous, we use <=
        if type_of_feature == "continuous":
            question = "{}__<=__{}".format(feature_name, split_value)
            
        # feature is categorical, we use =
        else:
            question = "{}__=__{}".format(feature_name, split_value)
        
        # instantiate sub-tree
        sub_tree = {question: []}
        
        # find answers (recursion)
        # yes is the left leaf, no is the right leaf
        yes_answer = decision_tree_algorithm(data_below, counter, min_samples, max_depth, random_subspace)
        no_answer = decision_tree_algorithm(data_above, counter, min_samples, max_depth, random_subspace)
        
        # If the answers are the same, then there is no point in asking the qestion.
        # This could happen when the data is classified even though it is not pure
        # yet (min_samples or max_depth base case).
        if yes_answer == no_answer:
            sub_tree = yes_answer
        else:
            sub_tree[question].append(yes_answer)
            sub_tree[question].append(no_answer)
        # we construct the tree and return it
        return sub_tree


# 3. Make predictions
# 3.1 One example
def predict_example(example, tree):
    # this is to predict only one instance
    # get the node questions in order to classify
    question = list(tree.keys())[0]
    #print(question + '\n')
    
    #print(example)
    feature_name, comparison_operator, value = question.split("__")

    # ask question
    if comparison_operator == "<=":
        if example[feature_name] <= float(value):
            answer = tree[question][0]
        else:
            answer = tree[question][1]
    
    # feature is categorical
    else:
        if str(example[feature_name]) == value:
            # we go to the left leaf
            answer = tree[question][0]
        else:
            # we go to the right leaf
            answer = tree[question][1]

    # base case
    # if the answer is not a sub-tree, that means it's a terminal node, we return the classification
    if not isinstance(answer, dict):
        return answer
    
    # recursive part
    # we go deeper into the tree using the sub-tree returned in the answer
    else:
        residual_tree = answer
        return predict_example(example, residual_tree)

    
# 3.2 All examples of the test data
def decision_tree_predictions(test_df, tree):
    # we predict all the instances in the test data using a loop
    predictions = test_df.apply(predict_example, args=(tree,), axis=1)
    return predictions

# creating the dataset for each decision tree of the forest
def bootstrapping(train_df, n_bootstrap):
    bootstrap_indices = np.random.randint(low=0, high=len(train_df), size=n_bootstrap)
    df_bootstrapped = train_df.iloc[bootstrap_indices]
    
    return df_bootstrapped

# creating the forest
def random_forest_algorithm(train_df, n_trees, n_bootstrap, n_features, dt_max_depth):
    forest = []
    for i in range(n_trees):
        # we generate a sub dataset for each tree
        df_bootstrapped = bootstrapping(train_df, n_bootstrap)
        # we train each tree using the sub dataset
        tree = decision_tree_algorithm(df_bootstrapped, max_depth=dt_max_depth, random_subspace=n_features)
        # we add the tree to the forest
        forest.append(tree)
    
    return forest

def random_forest_predictions(test_df, forest):
    df_predictions = {}
    for i in range(len(forest)):
        # we organize every prediction in a dictionary
        column_name = "tree_{}".format(i)
        predictions = decision_tree_predictions(test_df, tree=forest[i])
        df_predictions[column_name] = predictions
    # we create a dataframe from the dictionary of predictions
    df_predictions = pd.DataFrame(df_predictions)
    # we make the final prediction by taking the mode of the predictions, aka majority vote
    random_forest_predictions = df_predictions.mode(axis=1)[0]
    
    return random_forest_predictions

class DBSCAN: 
    def __init__(self, eps, min_pts, data):
        self.eps = eps
        self.min_pts = min_pts
        self.data = data
        self.clusters = []
        self.noise = []
        self.core_pts = []
        self.visited = []
        self.clustered = []
        self.cluster_num = 0
        self.clustered_pts = []
        
    def _distance(self, p1, p2):
        # result = 0
        # for i in range(len(p1)):
        #     if(type(p1[i]) == str or type(p2[i]) == str):
        #         if(p1[i] != p2[i]):
        #             result += 1
        #     else : result += (p1[i] - p2[i]) ** 2
        # return math.sqrt(result)
        return math.sqrt(sum([(a - b) ** 2 for a, b in zip(p1, p2)]))
    
    def _region_query(self, point):
        neighbors = []
        for i in range(len(self.data)):
            if self._distance(point, self.data[i]) < self.eps:
                neighbors.append(i)
        return neighbors
    
    def _expand_cluster(self, point, neighbors):
        self.clusters[self.cluster_num].append(point)
        self.clustered.append(point)
        self.visited.append(point)
        for i in neighbors:
            if i not in self.visited:
                self.visited.append(i)
                new_neighbors = self._region_query(self.data[i])
                if len(new_neighbors) >= self.min_pts:
                    neighbors += new_neighbors
            if i not in self.clustered:
                self.clusters[self.cluster_num].append(i)
                self.clustered.append(i)
                
    def fit(self):
        for i in range(len(self.data)):
            if i not in self.visited:
                self.visited.append(i)
                neighbors = self._region_query(self.data[i])
                if len(neighbors) < self.min_pts:
                    self.noise.append(i)
                else:
                    self.clusters.append([])
                    self._expand_cluster(i, neighbors)
                    self.cluster_num += 1
                    
    def get_clusters(self):
        return self.clusters
    
    def get_noise(self):
        return self.noise

class AGNES:
    def __init__(self, n_clusters=2, linkage='average'):
        self.n_clusters = n_clusters
        self.linkage = linkage
        self.labels_ = None
        self.cluster_centers_ = None
        self.n_leaves = None
        self.results = {}
        self.linkage_matrix = []
        self.merge_history = []

    def fit(self, X):
        #X = np.array([self.string_to_numerical(x) for x in X])
        
        self.n_leaves = X.shape[0]
        self.labels_ = np.arange(self.n_leaves)
        self.cluster_centers_ = X.copy()
        self.results[self.n_leaves] = [self.labels_.copy(), self.cluster_centers_.copy()]
        self.linkage_matrix = np.empty((0,4), dtype=float)
        self.merge_history = list(range(X.shape[0]))
        #print(self.merge_history)
        # while self.n_leaves >= self.n_clusters:
        #     self.merge()

        while self.n_leaves >= 1:
            self.merge()
            self.results[self.n_leaves] = [self.labels_.copy(), self.cluster_centers_.copy()]
        return self

    def merge(self):
        dist = self.distance(self.cluster_centers_)
        np.fill_diagonal(dist, np.inf)
        i, j = np.unravel_index(dist.argmin(), dist.shape)
        #i, j = np.unravel_index(self.masked_argmin(dist,0), dist.shape)
        self.cluster_centers_[i] = self._linkage(i, j)
        
        self.cluster_centers_ = np.delete(self.cluster_centers_, j, axis=0)
        self.labels_[self.labels_ == j] = i
        self.labels_[self.labels_ > j] -= 1
        self.n_leaves -= 1
        # we need to keep track of the clusters, problem is i and j are being lost
        self.linkage_matrix = np.vstack((self.linkage_matrix, [self.merge_history[i], self.merge_history[j], dist[i, j], self.n_leaves]))
        #print(i,j)
        self.merge_history[i] = max(self.merge_history)+1
        self.merge_history[j] = max(self.merge_history)+1
    
    def get_linkage_matrix(self):
        return self.linkage_matrix
    
    def string_to_numerical(self,arr):
        """Convert a string to a numerical value"""
        # Convert the string to a list of ASCII values
        new_arr = []
        for s in arr:
            #print(type(s))
            if (type(s) == str):
                ascii_values = [ord(c) for c in s]
                # Convert the list of ASCII values to a numpy array
                ascii_array = np.array(ascii_values)
                # Return the sum of the array
                new_arr.append(ascii_array.sum())
            else: new_arr.append(s)
        return np.array(new_arr)

    def distance(self, X):
        return np.sqrt(-2 * np.dot(X, X.T) + np.sum(X ** 2, axis=1) + np.sum(X ** 2, axis=1)[:, np.newaxis])


    def _distance(self, p1, p2):
        result = 0
        for i in range(len(p1)):
            if(type(p1[i]) == str or type(p2[i]) == str):
                if(p1[i] != p2[i]):
                    result += 1
            else : result += (p1[i] - p2[i]) ** 2
        return math.sqrt(result)

    def distance2(self, X):
        distances = []
        for i in range(len(X)):
            for j in range(len(X)):
                distances.append(self._distance(X[i], X[j]))
        return np.array(distances).reshape(len(X), len(X))
                
    

    def _linkage(self, i, j):
        if self.linkage == 'average':
            # linkage = []
            # for i in range (len(self.cluster_centers_[i])):
            #     if type(self.cluster_centers_[i][i]) == str:
            #         if self.cluster_centers_[i][i] != self.cluster_centers_[j][i]:
            #             linkage.append(0)
            #         else: linkage.append(1)
            #     else: linkage.append((self.cluster_centers_[i][i] + self.cluster_centers_[j][i]))
            # linkage = np.array(linkage)
            # return linkage / 2
            return (self.cluster_centers_[i] + self.cluster_centers_[j]) / 2
        elif self.linkage == 'single':
            return np.minimum(self.cluster_centers_[i], self.cluster_centers_[j])
        elif self.linkage == 'complete':
            return np.maximum(self.cluster_centers_[i], self.cluster_centers_[j])
        else:
            raise ValueError('Unknown linkage method: {}'.format(self.linkage))

    def predict(self, X):
        return self.labels_

    def fit_predict(self, X):
        self.fit(X)
        return self.predict(X)

    def get_results(self):
        return self.results

def inter_cluster(X, labels):
    # calculate the mean of each cluster
    cluster_means = []
    for i in range(len(np.unique(labels))):
        cluster_means.append(np.mean(X[labels == i], axis=0))
    cluster_means = np.array(cluster_means)
    # calculate the mean of all data points
    all_mean = np.mean(X, axis=0)
    # calculate the inter cluster distance
    inter_cluster_dist = np.sum(np.square(cluster_means - all_mean), axis=1)
    return inter_cluster_dist

def intra_cluster(X, labels):
    # calculate the mean of each cluster
    cluster_means = []
    for i in range(len(np.unique(labels))):
        cluster_means.append(np.mean(X[labels == i], axis=0))
    cluster_means = np.array(cluster_means)
    # calculate the intra cluster distance
    intra_cluster_dist = []
    for i in range(len(np.unique(labels))):
        intra_cluster_dist.append(np.sum(np.square(X[labels == i] - cluster_means[i])))
    intra_cluster_dist = np.array(intra_cluster_dist)
    return intra_cluster_dist

app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()
