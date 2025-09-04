#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Moto: Induction motor parameter estimation tool

Main window

Author: Julius Susanto
Last edited: August 2014
"""

import os, sys
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtGui import QAction, QFont, Qt
from PySide6.QtWidgets import QLabel, QLineEdit
import numpy as np
import dateutil, pyparsing
import matplotlib
matplotlib.use('QtAgg')
import matplotlib.pyplot as plt
import globals
import saveload
from common_calcs import get_torque, get_torque_sc
from descent import nr_solver, lm_solver, dnr_solver, nr_solver_sc
from genetic import ga_solver
from hybrid import hy_solver

class Window(QtWidgets.QMainWindow):
    
    def __init__(self):
        super(Window, self).__init__()
        
        globals.init()
        self.initUI()       
        
    def initUI(self):
        
        self.resize(800, 600)
        self.centre()
        
        # palette = QtGui.QPalette()
        # palette.setColor(QtGui.QPalette.Window, QtCore.Qt.white)
        # self.setPalette(palette)
        
        self.setWindowTitle('SPE Moto | Induction Motor Parameter Estimation Tool')
        self.setWindowIcon(QtGui.QIcon('icons/motor.png'))    
              
        """
        Actions
        """
        exitAction = QtGui.QAction(QtGui.QIcon('icons/exit.png'), '&Exit', self)        
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(QtWidgets.QApplication.quit)
        
        loadAction = QAction('&Open File...', self)
        loadAction.setStatusTip('Open file and load motor data')
        loadAction.triggered.connect(self.load_action)
        
        saveAction = QAction('&Save As...', self)
        saveAction.setStatusTip('Save motor data')
        saveAction.triggered.connect(self.save_action)
        
        aboutAction = QAction('&About Moto', self)
        aboutAction.setStatusTip('About Moto')
        aboutAction.triggered.connect(self.about_dialog)
        
        helpAction = QAction('&User Manual', self)
        helpAction.setShortcut('F1')
        helpAction.setStatusTip('Moto user documentation')
        helpAction.triggered.connect(self.user_manual)
        
        """
        Menubar
        """
        menu_bar = self.menuBar() 
        fileMenu = menu_bar.addMenu('&File')
        fileMenu.addAction(loadAction)
        fileMenu.addAction(saveAction)
        fileMenu.addAction(exitAction)
        helpMenu = menu_bar.addMenu('&Help')
        helpMenu.addAction(helpAction)
        helpMenu.addSeparator()
        helpMenu.addAction(aboutAction)
        
        """
        Main Screen
        """
        
        heading_font = QFont()
        heading_font.setPointSize(10)
        heading_font.setBold(True)
        
        ################
        # Motor details
        ################
        
        header1 = QtWidgets.QLabel('Motor')
        #header1.setMinimumWidth(50)
        header1.setMinimumHeight(30)
        header1.setFont(heading_font)
        
        label1 = QtWidgets.QLabel('Description')
        #label1.setMinimumWidth(50)
        
        self.le1 = QtWidgets.QLineEdit()
        #self.le1.setMinimumWidth(150)
        self.le1.setText(str(globals.motor_data["description"]))
               
        label2 = QtWidgets.QLabel('Synchronous speed')
        #label2.setMinimumWidth(50)
        
        self.le2 = QtWidgets.QLineEdit()
        #self.le2.setMinimumWidth(50)
        self.le2.setText(str(globals.motor_data["sync_speed"]))
        
        label2a = QtWidgets.QLabel('rpm')
        #label2a.setMinimumWidth(30)
 
        label3 = QtWidgets.QLabel('Rated speed')
        #label3.setMinimumWidth(50)
        
        self.le3 = QtWidgets.QLineEdit()
        #self.le3.setMinimumWidth(50)
        self.le3.setText(str(globals.motor_data["rated_speed"]))
        
        label3a = QtWidgets.QLabel('rpm')
        #label3a.setMinimumWidth(30)
           
        label4 = QtWidgets.QLabel('Rated power factor')
        #label4.setMinimumWidth(50)
        
        self.le4 = QtWidgets.QLineEdit()
        #self.le4.setMinimumWidth(50)
        self.le4.setText(str(globals.motor_data["rated_pf"]))
        
        label4a = QtWidgets.QLabel('pf')
        #label4a.setMinimumWidth(20)
        
        label5 = QtWidgets.QLabel('Rated efficiency')
        #label5.setMinimumWidth(50)
        
        self.le5 = QtWidgets.QLineEdit()
        #self.le5.setMinimumWidth(50)
        self.le5.setText(str(globals.motor_data["rated_eff"]))
        
        label5a = QtWidgets.QLabel('pu')
        #label5a.setMinimumWidth(20)

        label6 = QtWidgets.QLabel('Breakdown torque')
        #label6.setMinimumWidth(50)
        
        self.le6 = QtWidgets.QLineEdit()
        #self.le6.setMinimumWidth(50)
        self.le6.setText(str(globals.motor_data["T_b"]))
        
        label6a = QtWidgets.QLabel('T/Tn')
        #label6a.setMinimumWidth(40)
        
        label7 = QtWidgets.QLabel('Locked rotor torque')
        #label7.setMinimumWidth(50)
        
        self.le7 = QtWidgets.QLineEdit()
        #self.le7.setMinimumWidth(50)
        self.le7.setText(str(globals.motor_data["T_lr"]))
        
        label7a = QtWidgets.QLabel('T/Tn')
        #label7a.setMinimumWidth(40)
        
        label8 = QtWidgets.QLabel('Locked rotor current')
        #label8.setMinimumWidth(50)
        
        self.le8 = QtWidgets.QLineEdit()
        #self.le8.setMinimumWidth(50)
        self.le8.setText(str(globals.motor_data["I_lr"]))
        
        label8a = QtWidgets.QLabel('pu')
        #label8a.setMinimumWidth(40)

        label_rp = QLabel('Rated Power')
        self.lex9 = QLineEdit()
        self.lex9.setText(str(globals.motor_data["rated_power"]))
        labelex9 = QLabel('Kw')

        label_ri = QLabel('Rated Current')
        self.lex10 = QLineEdit()
        self.lex10.setText(str(globals.motor_data["rated_current"]))
        labelex10 = QLabel('I')

        label_rv = QLabel('Rated Voltage')
        self.lex11 = QLineEdit()
        self.lex11.setText(str(globals.motor_data["rated_voltage"]))
        labelex11 = QLabel('V')

        ########
        # Model
        ########
        
        header2 = QtWidgets.QLabel('Model')
        header2.setMinimumHeight(40)
        header2.setFont(heading_font)
        
        label_model = QtWidgets.QLabel('Model')
        #label_model.setMinimumWidth(150)
        
        self.combo_model = QtWidgets.QComboBox()
        self.combo_model.addItem("Single cage")
        # self.combo_model.addItem("Single cage w/o core losses")
        self.combo_model.addItem("Double cage")
        self.combo_model.setCurrentIndex(1)
        
        self.img1 = QtWidgets.QLabel()
        self.img1.setPixmap(QtGui.QPixmap('images/dbl_cage.png'))
        
        #####################
        # Algorithm settings
        #####################
        
        header3 = QtWidgets.QLabel('Settings')
        header3.setMinimumHeight(40)
        header3.setFont(heading_font)
        
        label9 = QtWidgets.QLabel('Maximum # iterations')
        
        self.le9 = QtWidgets.QLineEdit()
        self.le9.setText(str(globals.algo_data["max_iter"]))
        self.le9.setStatusTip('Maximum number of iterations allowed')
        
        label10 = QtWidgets.QLabel('Convergence criterion')
        
        self.le10 = QtWidgets.QLineEdit()
        self.le10.setText(str(globals.algo_data["conv_err"]))
        self.le10.setStatusTip('Squared error required to qualify for convergence')

        self.label11 = QtWidgets.QLabel('Linear constraint k_r')
        
        self.le11 = QtWidgets.QLineEdit()
        self.le11.setText(str(globals.algo_data["k_r"]))
        self.le11.setStatusTip('Linear constraint for Rs')

        self.label12 = QtWidgets.QLabel('Linear constraint k_x')
        
        self.le12 = QtWidgets.QLineEdit()
        self.le12.setText(str(globals.algo_data["k_x"]))
        self.le12.setStatusTip('Linear constraint for Xr2')
        
        # Genetic Algorithm Widgets
        ############################
        
        self.labeln_gen = QtWidgets.QLabel('Maximum # generations')
        self.labeln_gen.setVisible(0)
        self.labelpop = QtWidgets.QLabel('Members in population')
        self.labelpop.setVisible(0)
        self.labeln_r = QtWidgets.QLabel('Members in mating pool')
        self.labeln_r.setVisible(0)
        self.labeln_e = QtWidgets.QLabel('Elite children')
        self.labeln_e.setVisible(0)
        self.labelc_f = QtWidgets.QLabel('Crossover fraction')
        self.labelc_f.setVisible(0)
        
        self.len_gen = QtWidgets.QLineEdit()
        self.len_gen.setText(str(globals.algo_data["n_gen"]))
        self.len_gen.setStatusTip('Maximum number of generations allowed')
        self.len_gen.hide()
        
        self.lepop = QtWidgets.QLineEdit()
        self.lepop.setText(str(globals.algo_data["pop"]))
        self.lepop.setStatusTip('Number of members in each generation')
        self.lepop.hide()
        
        self.len_r = QtWidgets.QLineEdit()
        self.len_r.setText(str(globals.algo_data["n_r"]))
        self.len_r.setStatusTip('Number of members in a mating pool')
        self.len_r.hide()
        
        self.len_e = QtWidgets.QLineEdit()
        self.len_e.setText(str(globals.algo_data["n_e"]))
        self.len_e.setStatusTip('Number of elite children')
        self.len_e.hide()
        
        self.lec_f = QtWidgets.QLineEdit()
        self.lec_f.setText(str(globals.algo_data["c_f"]))
        self.lec_f.setStatusTip('Proportion of children spawned through crossover')
        self.lec_f.hide()
        
        
        label_algo = QtWidgets.QLabel('Algorithm')
        #label_algo.setMinimumWidth(150)
        
        self.combo_algo = QtWidgets.QComboBox()
        self.combo_algo.addItem("Newton-Raphson")
        self.combo_algo.addItem("Levenberg-Marquardt")
        self.combo_algo.addItem("Damped Newton-Raphson")
        self.combo_algo.addItem("Genetic Algorithm")
        self.combo_algo.addItem("Hybrid GA-NR")
        self.combo_algo.addItem("Hybrid GA-LM")
        self.combo_algo.addItem("Hybrid GA-DNR")
        
        calc_button = QtWidgets.QPushButton("Calculate")
        calc_button.setStatusTip('Estimate equivalent circuit parameters')
        
        self.plot_button = QtWidgets.QPushButton("Plot")
        self.plot_button.setDisabled(1)
        self.plot_button.setStatusTip('Plot torque-speed and current-speed curves')
        
        ####################
        # Algorithm results
        ####################
        
        header4 = QtWidgets.QLabel('Results')
        #header4.setMinimumWidth(150)
        header4.setMinimumHeight(40)
        header4.setFont(heading_font)
        
        label13 = QtWidgets.QLabel('R_s')
        #label13.setFixedWidth(50)
        
        self.leRs = QtWidgets.QLineEdit()
        self.leRs.setStatusTip('Stator resistance (pu)')
        
        label14 = QtWidgets.QLabel('X_s')
        #label14.setMinimumWidth(150)
        
        self.leXs = QtWidgets.QLineEdit()
        self.leXs.setStatusTip('Stator reactance (pu)')
        
        label15 = QtWidgets.QLabel('X_m')
        #label15.setMinimumWidth(150)
        
        self.leXm = QtWidgets.QLineEdit()
        self.leXm.setStatusTip('Magnetising resistance (pu)')
        
        label16 = QtWidgets.QLabel('X_r1')
        #label16.setMinimumWidth(150)
        
        self.leXr1 = QtWidgets.QLineEdit()
        self.leXr1.setStatusTip('Inner cage rotor reactance (pu)')
        
        label17 = QtWidgets.QLabel('R_r1')
        #label17.setMinimumWidth(150)
        
        self.leRr1 = QtWidgets.QLineEdit()
        self.leRr1.setStatusTip('Inner cage rotor resistance (pu)')
        
        self.label18 = QtWidgets.QLabel('X_r2')
        #label18.setMinimumWidth(150)
        
        self.leXr2 = QtWidgets.QLineEdit()
        self.leXr2.setStatusTip('Outer cage rotor reactance (pu)')
        
        self.label19 = QtWidgets.QLabel('R_r2')
        #label19.setMinimumWidth(150)
        
        self.leRr2 = QtWidgets.QLineEdit()
        self.leRr2.setStatusTip('Outer cage rotor resistance (pu)')
        
        label20 = QtWidgets.QLabel('R_c')
        #label20.setMinimumWidth(150)
        
        self.leRc = QtWidgets.QLineEdit()
        self.leRc.setStatusTip('Core loss resistance (pu)')
        
        label21 = QtWidgets.QLabel('Converged?')
        #label21.setMinimumWidth(150)
        
        self.leConv = QtWidgets.QLineEdit()
        self.leConv.setStatusTip('Did algorithm converge?')
        
        label22 = QtWidgets.QLabel('Squared Error')
        #label22.setMinimumWidth(150)
        
        self.leErr = QtWidgets.QLineEdit()
        self.leErr.setStatusTip('Squared error of estimate')
        
        label23 = QtWidgets.QLabel('Iterations')
        #label23.setMinimumWidth(150)
        
        self.leIter = QtWidgets.QLineEdit()
        self.leIter.setStatusTip('Number of iterations / generations')
        
        ##############
        # Grid layout
        ##############
        
        grid = QtWidgets.QGridLayout()
        
        # Motor details
        i = 0
        grid.addWidget(header1, i, 0)
        grid.addWidget(label1, i+1, 0)
        grid.addWidget(self.le1, i+1, 1, 1, 5)
        grid.addWidget(label2, i+2, 0)
        grid.addWidget(self.le2, i+2, 1)
        grid.addWidget(label2a, i+2, 2)
        grid.addWidget(label3, i+3, 0)
        grid.addWidget(self.le3, i+3, 1)
        grid.addWidget(label3a, i+3, 2)
        grid.addWidget(label4, i+4, 0)
        grid.addWidget(self.le4, i+4, 1)
        grid.addWidget(label4a, i+4, 2)
        grid.addWidget(label5, i+5, 0)
        grid.addWidget(self.le5, i+5, 1)
        grid.addWidget(label5a, i+5, 2)
        grid.addWidget(label6, i+3, 4)
        grid.addWidget(self.le6, i+3, 5)
        grid.addWidget(label6a, i+3, 6)
        grid.addWidget(label7, i+4, 4)
        grid.addWidget(self.le7, i+4, 5)
        grid.addWidget(label7a, i+4, 6)
        grid.addWidget(label8, i+5, 4)
        grid.addWidget(self.le8, i+5, 5)
        grid.addWidget(label8a, i+5, 6)
        grid.addWidget(label_rp, i+6, 0)
        grid.addWidget(self.lex9, i+6, 1)
        grid.addWidget(labelex9, i+6, 2)

        grid.addWidget(label_ri, i+7, 0)
        grid.addWidget(self.lex10, i+7, 1)
        grid.addWidget(labelex10, i+7, 2)

        grid.addWidget(label_rv, i+8, 0)
        grid.addWidget(self.lex11, i+8, 1)
        grid.addWidget(labelex11, i+8, 2)


        # Model
        i = 9
        #grid.addWidget(header2, i, 0)
        grid.addWidget(label_model, i+1, 0)
        grid.addWidget(self.combo_model, i+1, 1)
        grid.addWidget(self.img1, i+1, 3, i-7, 6)
        
        # Algorithm settings
        i = 12
        grid.addWidget(header3, i, 0)
        grid.addWidget(label_algo, i+1, 0)
        grid.addWidget(self.combo_algo, i+1, 1)
        grid.addWidget(label9, i+2, 0)
        grid.addWidget(self.le9, i+2, 1)
        grid.addWidget(label10, i+3, 0)
        grid.addWidget(self.le10, i+3, 1)
        grid.addWidget(self.label11, i+2, 3)
        grid.addWidget(self.le11, i+2, 4)
        grid.addWidget(self.label12, i+3, 3)
        grid.addWidget(self.le12, i+3, 4)
        
        # Genetic algorithm parameters
        grid.addWidget(self.labeln_gen, i+2, 3)
        grid.addWidget(self.len_gen, i+2, 4)
        grid.addWidget(self.labelpop, i+3, 3)
        grid.addWidget(self.lepop, i+3, 4)
        grid.addWidget(self.labeln_r, i+4, 3)
        grid.addWidget(self.len_r, i+4, 4)
        grid.addWidget(self.labeln_e, i+2, 5)
        grid.addWidget(self.len_e, i+2, 6)
        grid.addWidget(self.labelc_f, i+3, 5)
        grid.addWidget(self.lec_f, i+3, 6)
        
        grid.addWidget(calc_button, i+4, 5)
        grid.addWidget(self.plot_button, i+4, 6)
        
        # Algorithm results
        i = 17
        grid.addWidget(header4, i, 0)
        grid.addWidget(label13, i+1, 0)
        grid.addWidget(self.leRs, i+1, 1)
        grid.addWidget(label14, i+2, 0)
        grid.addWidget(self.leXs, i+2, 1)
        grid.addWidget(label15, i+3, 0)
        grid.addWidget(self.leXm, i+3, 1)
        grid.addWidget(label20, i+4, 0)
        grid.addWidget(self.leRc, i+4, 1)
        grid.addWidget(label16, i+1, 3)
        grid.addWidget(self.leXr1, i+1, 4)
        grid.addWidget(label17, i+2, 3)
        grid.addWidget(self.leRr1, i+2, 4)
        grid.addWidget(self.label18, i+3, 3)
        grid.addWidget(self.leXr2, i+3, 4)
        grid.addWidget(self.label19, i+4, 3)
        grid.addWidget(self.leRr2, i+4, 4)
        grid.addWidget(label21, i+1, 5)
        grid.addWidget(self.leConv, i+1, 6)
        grid.addWidget(label22, i+2, 5)
        grid.addWidget(self.leErr, i+2, 6)
        grid.addWidget(label23, i+3, 5)
        grid.addWidget(self.leIter, i+3, 6)
        
        grid.setAlignment(Qt.AlignTop)      

        main_screen = QtWidgets.QWidget()
        main_screen.setLayout(grid)
        main_screen.setStatusTip('Ready')
        
        self.setCentralWidget(main_screen)
        
        # Event handlers
        calc_button.clicked.connect(self.calculate)
        self.plot_button.clicked.connect(self.plot_curves)
        
        self.le1.editingFinished.connect(self.update_data)
        self.le2.editingFinished.connect(self.update_data)
        self.le3.editingFinished.connect(self.update_data)
        self.le4.editingFinished.connect(self.update_data)
        self.le5.editingFinished.connect(self.update_data)
        self.le6.editingFinished.connect(self.update_data)
        self.le7.editingFinished.connect(self.update_data)
        self.le8.editingFinished.connect(self.update_data)
        self.le9.editingFinished.connect(self.update_data)
        self.le10.editingFinished.connect(self.update_data)
        self.le11.editingFinished.connect(self.update_data)
        self.le12.editingFinished.connect(self.update_data)
        self.len_gen.editingFinished.connect(self.update_data)
        self.lepop.editingFinished.connect(self.update_data)
        self.len_r.editingFinished.connect(self.update_data)
        self.len_e.editingFinished.connect(self.update_data)
        self.lec_f.editingFinished.connect(self.update_data)
        
        ##########################
        #TO DO - connects for combo boxes - combo_model and combo_algo (what signal to use?)
        ##########################
        self.combo_algo.currentIndexChanged.connect(self.update_algo)
        self.combo_model.currentIndexChanged.connect(self.update_model)
        
        self.statusBar().showMessage('Ready')
    
    # Calculate parameter estimates
    def calculate(self):
        self.statusBar().showMessage('Calculating...')
        
        sf = (globals.motor_data["sync_speed"] - globals.motor_data["rated_speed"]) / globals.motor_data["sync_speed"]
        
        if self.combo_model.currentIndex() == 0:
            # Single cage
            p = [sf, globals.motor_data["rated_eff"], globals.motor_data["rated_pf"], globals.motor_data["T_b"]]
            [z, iter, err, conv] = nr_solver_sc(p, 0, globals.algo_data["k_x"], globals.algo_data["k_r"], globals.algo_data["max_iter"], globals.algo_data["conv_err"]) 
            
        else:
            # Double cage
            p = [sf, globals.motor_data["rated_eff"], globals.motor_data["rated_pf"], globals.motor_data["T_b"], globals.motor_data["T_lr"], globals.motor_data["I_lr"] ]            
            
            if self.combo_algo.currentText() == "Newton-Raphson":
                [z, iter, err, conv] = nr_solver(p, 0, globals.algo_data["k_x"], globals.algo_data["k_r"], globals.algo_data["max_iter"], globals.algo_data["conv_err"])           
            
            if self.combo_algo.currentText() == "Levenberg-Marquardt":
                [z, iter, err, conv] = lm_solver(p, 0, globals.algo_data["k_x"], globals.algo_data["k_r"], 1e-7, 5.0, globals.algo_data["max_iter"], globals.algo_data["conv_err"])
                
            if self.combo_algo.currentText() == "Damped Newton-Raphson":
                [z, iter, err, conv] = dnr_solver(p, 0, globals.algo_data["k_x"], globals.algo_data["k_r"], 1e-7, globals.algo_data["max_iter"], globals.algo_data["conv_err"])
                
            if self.combo_algo.currentText() == "Genetic Algorithm":
                [z, iter, err, conv] = ga_solver(self, p, globals.algo_data["pop"], globals.algo_data["n_r"], globals.algo_data["n_e"], globals.algo_data["c_f"], globals.algo_data["n_gen"], globals.algo_data["conv_err"])
                
            if self.combo_algo.currentText() == "Hybrid GA-NR":
                [z, iter, err, conv] = hy_solver(self, "NR", p, globals.algo_data["pop"], globals.algo_data["n_r"], globals.algo_data["n_e"], globals.algo_data["c_f"], globals.algo_data["n_gen"], globals.algo_data["conv_err"])
                
            if self.combo_algo.currentText() == "Hybrid GA-LM":
                [z, iter, err, conv] = hy_solver(self, "LM", p, globals.algo_data["pop"], globals.algo_data["n_r"], globals.algo_data["n_e"], globals.algo_data["c_f"], globals.algo_data["n_gen"], globals.algo_data["conv_err"])
                
            if self.combo_algo.currentText() == "Hybrid GA-DNR":
                [z, iter, err, conv] = hy_solver(self, "DNR", p, globals.algo_data["pop"], globals.algo_data["n_r"], globals.algo_data["n_e"], globals.algo_data["c_f"], globals.algo_data["n_gen"], globals.algo_data["conv_err"])
        
        self.leRs.setText(str(np.round(z[0],5)))
        self.leXs.setText(str(np.round(z[1],5)))
        self.leXm.setText(str(np.round(z[2],5)))
        self.leRr1.setText(str(np.round(z[3],5)))        
         
        if self.combo_model.currentIndex() == 1:
            self.leXr1.setText(str(np.round(z[4],5)))
            self.leRr2.setText(str(np.round(z[5],5)))
            self.leXr2.setText(str(np.round(z[6],5)))
            self.leRc.setText(str(np.round(z[7],5)))
        else:
            self.leRc.setText(str(np.round(z[4],5)))
            self.leXr1.setText(str(np.round(z[5],5)))
        
        if conv == 1:
            self.leConv.setText("Yes")
        else:
            QMessageBox.warning(self, 'Warning', "Algorithm did not converge.", QMessageBox.Ok)
            self.leConv.setText("No")
            
        self.leErr.setText(str(np.round(err,9)))
        self.leIter.setText(str(iter))
        
        # Only enable the plot button if the squared error is within the bounds of reason
        if err < 1:
            self.plot_button.setEnabled(1)
        else:
            self.plot_button.setDisabled(1)
        
        self.statusBar().showMessage('Ready')
        
    # Plot torque-speed and current-speed curves
    def plot_curves(self):
        sf = (globals.motor_data["sync_speed"] - globals.motor_data["rated_speed"]) / globals.motor_data["sync_speed"]
        if self.combo_model.currentIndex() == 0:
            # Single cage
            x = [float(self.leRs.text()), float(self.leXs.text()) , float(self.leXm.text()), float(self.leRr1.text()), float(self.leRc.text()), float(self.leXr1.text())]
        else:
            # Double cage
            x = [float(self.leRs.text()), float(self.leXs.text()) , float(self.leXm.text()), float(self.leRr1.text()), float(self.leXr1.text()), float(self.leRr2.text()), float(self.leXr2.text()), float(self.leRc.text())]
        
        # Rated per-unit torque
        T_rtd = globals.motor_data["rated_eff"] * globals.motor_data["rated_pf"] / (1 - sf)
        
        Tm = np.zeros(1001)
        Im = np.zeros(1001)
        speed = np.zeros(1001)
        speed[1000] = globals.motor_data["sync_speed"]
        for n in range(0,1000):
            speed[n] = float(n) / 1000 * globals.motor_data["sync_speed"]
            i = 1 - float(n) / 1000
            if self.combo_model.currentIndex() == 0:
                # Single cage
                [Ti, Ii] = get_torque_sc(i,x)
            else:
                # Double cage
                [Ti, Ii] = get_torque(i,x)
            
            Tm[n] = Ti / T_rtd      # Convert torque to T/Tn value
            Im[n] = np.abs(Ii)
        
        # Plot torque-speed and current-speed curves
        if plt.fignum_exists(1):
            # Do nothing
            QMessageBox.warning(self, 'Warning', "A plot is already open. Please close to create a new plot.", QMessageBox.Ok)
        else:
            plt.figure(1, facecolor='white')
            plt.subplot(211)
            plt.plot(speed, Tm)
            plt.xlim([0, globals.motor_data["sync_speed"]])
            plt.xlabel("Speed (rpm)")
            plt.ylabel("Torque (T/Tn)")
            plt.grid(color = '0.75', linestyle='--', linewidth=1)
            
            plt.subplot(212)
            plt.plot(speed, Im, 'r')
            plt.xlim([0, globals.motor_data["sync_speed"]])
            plt.xlabel("Speed (rpm)")
            plt.ylabel("Current (pu)")
            plt.grid(color = '0.75', linestyle='--', linewidth=1)
            
            plt.show()
    
    # Update global variables on change in data fields
    def update_data(self):
        try:
            globals.motor_data["description"] = str(self.le1.text())
            globals.motor_data["sync_speed"] = float(self.le2.text())
            globals.motor_data["rated_speed"] = float(self.le3.text())
            globals.motor_data["rated_pf"] = float(self.le4.text())
            globals.motor_data["rated_eff"] = float(self.le5.text())
            globals.motor_data["T_b"] = float(self.le6.text())
            globals.motor_data["T_lr" ] = float(self.le7.text())
            globals.motor_data["I_lr"] = float(self.le8.text())
            globals.algo_data["max_iter"] = int(self.le9.text())
            globals.algo_data["conv_err"] = float(self.le10.text())
            globals.algo_data["k_r"] = float(self.le11.text())
            globals.algo_data["k_x"] = float(self.le12.text())
            globals.algo_data["n_gen"] = int(self.len_gen.text())
            globals.algo_data["pop"] = int(self.lepop.text())
            globals.algo_data["n_r"] = int(self.len_r.text())
            globals.algo_data["n_e"] = int(self.len_e.text())
            globals.algo_data["c_f"] = float(self.lec_f.text())
        except Exception as err:
            print(err)
    
    # Update data in the main window
    def update_window(self):
        self.le1.setText(str(globals.motor_data["description"]))
        self.le2.setText(str(globals.motor_data["sync_speed"]))
        self.le3.setText(str(globals.motor_data["rated_speed"]))
        self.le4.setText(str(globals.motor_data["rated_pf"]))
        self.le5.setText(str(globals.motor_data["rated_eff"]))
        self.le6.setText(str(globals.motor_data["T_b"]))
        self.le7.setText(str(globals.motor_data["T_lr"]))
        self.le8.setText(str(globals.motor_data["I_lr"]))
        
        self.le9.setText(str(globals.algo_data["max_iter"]))
        self.le10.setText(str(globals.algo_data["conv_err"]))
        self.le11.setText(str(globals.algo_data["k_r"]))
        self.le12.setText(str(globals.algo_data["k_x"]))
        self.len_gen.setText(str(globals.algo_data["n_gen"]))
        self.lepop.setText(str(globals.algo_data["pop"]))
        self.len_r.setText(str(globals.algo_data["n_r"]))
        self.len_e.setText(str(globals.algo_data["n_e"]))
        self.lec_f.setText(str(globals.algo_data["c_f"]))
    
    # Update the screen if the algorithm changes
    def update_algo(self):
        if (self.combo_algo.currentText() == "Genetic Algorithm") or (self.combo_algo.currentText() == "Hybrid GA-LM") or (self.combo_algo.currentText() == "Hybrid GA-NR") or (self.combo_algo.currentText() == "Hybrid GA-DNR"):
                self.label11.setVisible(0)
                self.le11.hide()
                self.label12.setVisible(0)
                self.le12.hide()
                
                self.labeln_gen.setVisible(1)
                self.labelpop.setVisible(1)
                self.labeln_r.setVisible(1)
                self.labeln_e.setVisible(1)
                self.labelc_f.setVisible(1)
                self.len_gen.show()
                self.lepop.show()
                self.len_r.show()
                self.len_e.show()
                self.lec_f.show()
        else:
                self.label11.setVisible(1)
                self.le11.show()
                self.label12.setVisible(1)
                self.le12.show()
                
                self.labeln_gen.setVisible(0)
                self.labelpop.setVisible(0)
                self.labeln_r.setVisible(0)
                self.labeln_e.setVisible(0)
                self.labelc_f.setVisible(0)
                self.len_gen.hide()
                self.lepop.hide()
                self.len_r.hide()
                self.len_e.hide()
                self.lec_f.hide()
    
    # Update if model combo box changed
    def update_model(self):
        if self.combo_model.currentIndex() == 0:
            # Single cage
            self.img1.setPixmap(QtGui.QPixmap('images/single_cage.png'))
            self.combo_algo.setCurrentIndex(0)
            self.combo_algo.clear()
            self.combo_algo.addItem("Newton-Raphson")
            self.label18.setVisible(0)
            self.label19.setVisible(0)
            self.leXr2.hide()
            self.leRr2.hide()
        else:
            # Double cage
            self.img1.setPixmap(QtGui.QPixmap('images/dbl_cage.png'))
            self.combo_algo.addItem("Levenberg-Marquardt")
            self.combo_algo.addItem("Damped Newton-Raphson")
            self.combo_algo.addItem("Genetic Algorithm")
            self.combo_algo.addItem("Hybrid GA-NR")
            self.combo_algo.addItem("Hybrid GA-LM")
            self.combo_algo.addItem("Hybrid GA-DNR")
            self.label18.setVisible(1)
            self.label19.setVisible(1)
            self.leXr2.show()
            self.leRr2.show()
    
    # Open file and load motor data
    def load_action(self):
        # Open file dialog box
        filename = QFileDialog.getOpenFileName(self, "Open Moto File", "library/", "Moto files (*.mto)")
        
        if filename[0]:
            saveload.load_file(filename[0])
            self.update_window()
    
    # Save motor data to file
    def save_action(self):
        # Open save file dialog box
        filename = QFileDialog.getSaveFileName(self, "Save Moto File", "library/", "Moto files (*.mto)")
        
        if filename:
            saveload.save_file(filename)
    
    # Launch user manual
    def user_manual(self):
        os.system("start docs/moto_user_manual.pdf")
    
    # About dialog box
    def about_dialog(self):
        QMessageBox.about(self, "About Moto",
                """<b>Moto</b> is a parameter estimation tool that can be used to determine the equivalent circuit parameters of induction machines. The tool is intended for use in dynamic time-domain simulations such as stability and motor starting studies.
                   <p>
                   Version: <b>v0.2<b><P>
                   <p>
                   Website: <a href="http://www.sigmapower.com.au/moto.html">www.sigmapower.com.au/moto.html</a>
                   <p> </p>
                   <p><img src="images/Sigma_Power.png"></p>
                   <p>&copy; 2014 Sigma Power Engineering Pty Ltd</p>
                   <p>All rights reserved.</p>             
                   """)
    
    # Centre application window on screen
    def centre(self):
        qr = self.frameGeometry()
        screen = QtWidgets.QApplication.primaryScreen()
        cp = screen.availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

def main():
    
    app = QtWidgets.QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()