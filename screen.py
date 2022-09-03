# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'gui_file.ui'
##
## Created by: Qt User Interface Compiler version 5.15.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

import resource_file_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1280, 720)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.stackedWidget = QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setGeometry(QRect(0, 0, 1280, 720))
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.frame = QFrame(self.page)
        self.frame.setObjectName(u"frame")
        self.frame.setGeometry(QRect(0, 0, 1280, 720))
        self.frame.setStyleSheet(u"background-color: #ECF0F5;")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(80, 10, 291, 61))
        font = QFont()
        font.setFamily(u"Cubic")
        font.setPointSize(20)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setStyleSheet(u"font: 20pt \"Cubic\";")
        self.label.setAlignment(Qt.AlignCenter)
        self.frame_3 = QFrame(self.frame)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setGeometry(QRect(10, 10, 70, 70))
        self.frame_3.setStyleSheet(u"image: url(:/images/imgs/tabuleiro.png);")
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.board_frame = QFrame(self.frame)
        self.board_frame.setObjectName(u"board_frame")
        self.board_frame.setGeometry(QRect(20, 100, 550, 550))
        self.board_frame.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"border-radius: 30px;")
        self.board_frame.setFrameShape(QFrame.StyledPanel)
        self.board_frame.setFrameShadow(QFrame.Raised)
        self.frame_4 = QFrame(self.board_frame)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setGeometry(QRect(25, 25, 500, 500))
        self.frame_4.setStyleSheet(u"image: url(:/images/imgs/tabuleiro.png);")
        self.frame_4.setFrameShape(QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.frame_6 = QFrame(self.frame)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setGeometry(QRect(920, 20, 341, 121))
        self.frame_6.setFrameShape(QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QFrame.Raised)
        self.host_label = QLabel(self.frame_6)
        self.host_label.setObjectName(u"host_label")
        self.host_label.setGeometry(QRect(0, 0, 341, 41))
        font1 = QFont()
        font1.setFamily(u"Cubic")
        font1.setPointSize(10)
        font1.setBold(False)
        font1.setItalic(False)
        font1.setWeight(50)
        self.host_label.setFont(font1)
        self.begin_button = QPushButton(self.frame_6)
        self.begin_button.setObjectName(u"begin_button")
        self.begin_button.setGeometry(QRect(0, 70, 141, 51))
        font2 = QFont()
        font2.setFamily(u"Cubic")
        font2.setPointSize(15)
        self.begin_button.setFont(font2)
        self.begin_button.setStyleSheet(u"QPushButton{\n"
"border-radius:10px;\n"
"background-color: #219653;\n"
"color:white;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"border-radius:4px;\n"
"background-color: #605e5e;\n"
"border: 1px solid black;\n"
"color: white;\n"
"}\n"
"\n"
"QPushButton:pressed{\n"
"border-radius:4px;\n"
"background-color: #605e5e;\n"
"border: 1px solid black;\n"
"color: white;\n"
"}")
        self.giveup_button = QPushButton(self.frame_6)
        self.giveup_button.setObjectName(u"giveup_button")
        self.giveup_button.setGeometry(QRect(200, 70, 141, 51))
        self.giveup_button.setFont(font2)
        self.giveup_button.setStyleSheet(u"QPushButton{\n"
"border-radius:10px;\n"
"background-color: rgb(226, 0, 0);\n"
"color:white;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"border-radius:4px;\n"
"background-color: #605e5e;\n"
"border: 1px solid black;\n"
"color: white;\n"
"}\n"
"\n"
"QPushButton:pressed{\n"
"border-radius:4px;\n"
"background-color: #605e5e;\n"
"border: 1px solid black;\n"
"color: white;\n"
"}")
        self.chat_frame = QFrame(self.frame)
        self.chat_frame.setObjectName(u"chat_frame")
        self.chat_frame.setGeometry(QRect(860, 250, 421, 471))
        self.chat_frame.setFrameShape(QFrame.StyledPanel)
        self.chat_frame.setFrameShadow(QFrame.Raised)
        self.label_3 = QLabel(self.chat_frame)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(30, 20, 371, 41))
        self.label_3.setFont(font2)
        self.label_3.setAlignment(Qt.AlignCenter)
        self.chat_output = QTextEdit(self.chat_frame)
        self.chat_output.setObjectName(u"chat_output")
        self.chat_output.setGeometry(QRect(30, 70, 371, 321))
        self.chat_output.setStyleSheet(u"color:black;\n"
"font: 9pt \"Helvetica\";\n"
"background-color: rgb(255, 255, 255);\n"
"border-radius: 15px;")
        self.chat_input = QTextEdit(self.chat_frame)
        self.chat_input.setObjectName(u"chat_input")
        self.chat_input.setGeometry(QRect(30, 410, 301, 41))
        self.chat_input.setStyleSheet(u"color:black;\n"
"font: 9pt \"Helvetica\";\n"
"background-color: rgb(255, 255, 255);\n"
"border-radius: 15px;")
        self.send_text_button = QPushButton(self.chat_frame)
        self.send_text_button.setObjectName(u"send_text_button")
        self.send_text_button.setGeometry(QRect(340, 410, 61, 41))
        font3 = QFont()
        font3.setFamily(u"Cubic")
        self.send_text_button.setFont(font3)
        self.send_text_button.setStyleSheet(u"QPushButton{\n"
"border-radius:10px;\n"
"background-color: white;\n"
"color:black;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"border-radius:4px;\n"
"background-color: #605e5e;\n"
"border: 1px solid black;\n"
"color: black;\n"
"}\n"
"\n"
"QPushButton:pressed{\n"
"border-radius:4px;\n"
"background-color: #605e5e;\n"
"border: 1px solid black;\n"
"color: black;\n"
"}")
        self.your_pieces_1 = QPushButton(self.frame)
        self.your_pieces_1.setObjectName(u"your_pieces_1")
        self.your_pieces_1.setGeometry(QRect(630, 180, 60, 60))
        self.your_pieces_1.setStyleSheet(u"background-color: rgb(170, 0, 0);\n"
"border-radius: 30px;")
        self.your_pieces_2 = QPushButton(self.frame)
        self.your_pieces_2.setObjectName(u"your_pieces_2")
        self.your_pieces_2.setGeometry(QRect(720, 180, 60, 60))
        self.your_pieces_2.setStyleSheet(u"background-color: rgb(170, 0, 0);\n"
"border-radius: 30px;")
        self.your_pieces_3 = QPushButton(self.frame)
        self.your_pieces_3.setObjectName(u"your_pieces_3")
        self.your_pieces_3.setGeometry(QRect(630, 260, 60, 60))
        self.your_pieces_3.setStyleSheet(u"background-color: rgb(170, 0, 0);\n"
"border-radius: 30px;")
        self.your_pieces_4 = QPushButton(self.frame)
        self.your_pieces_4.setObjectName(u"your_pieces_4")
        self.your_pieces_4.setGeometry(QRect(720, 260, 60, 60))
        self.your_pieces_4.setStyleSheet(u"background-color: rgb(170, 0, 0);\n"
"border-radius: 30px;")
        self.your_pieces_5 = QPushButton(self.frame)
        self.your_pieces_5.setObjectName(u"your_pieces_5")
        self.your_pieces_5.setGeometry(QRect(630, 340, 60, 60))
        self.your_pieces_5.setStyleSheet(u"background-color: rgb(170, 0, 0);\n"
"border-radius: 30px;")
        self.your_pieces_6 = QPushButton(self.frame)
        self.your_pieces_6.setObjectName(u"your_pieces_6")
        self.your_pieces_6.setGeometry(QRect(720, 340, 60, 60))
        self.your_pieces_6.setStyleSheet(u"background-color: rgb(170, 0, 0);\n"
"border-radius: 30px;")
        self.your_pieces_7 = QPushButton(self.frame)
        self.your_pieces_7.setObjectName(u"your_pieces_7")
        self.your_pieces_7.setGeometry(QRect(630, 430, 60, 60))
        self.your_pieces_7.setStyleSheet(u"background-color: rgb(170, 0, 0);\n"
"border-radius: 30px;")
        self.your_pieces_8 = QPushButton(self.frame)
        self.your_pieces_8.setObjectName(u"your_pieces_8")
        self.your_pieces_8.setGeometry(QRect(720, 430, 60, 60))
        self.your_pieces_8.setStyleSheet(u"background-color: rgb(170, 0, 0);\n"
"border-radius: 30px;")
        self.your_pieces_9 = QPushButton(self.frame)
        self.your_pieces_9.setObjectName(u"your_pieces_9")
        self.your_pieces_9.setGeometry(QRect(630, 510, 60, 60))
        self.your_pieces_9.setStyleSheet(u"background-color: rgb(170, 0, 0);\n"
"border-radius: 30px;")
        self.opponent_2 = QLabel(self.frame)
        self.opponent_2.setObjectName(u"opponent_2")
        self.opponent_2.setGeometry(QRect(780, 630, 60, 60))
        self.opponent_2.setStyleSheet(u"background-color: rgb(61, 61, 61);\n"
"border-radius: 30px;")
        self.opponent_3 = QLabel(self.frame)
        self.opponent_3.setObjectName(u"opponent_3")
        self.opponent_3.setGeometry(QRect(780, 630, 60, 60))
        self.opponent_3.setStyleSheet(u"background-color: rgb(61, 61, 61);\n"
"border-radius: 30px;")
        self.opponent_4 = QLabel(self.frame)
        self.opponent_4.setObjectName(u"opponent_4")
        self.opponent_4.setGeometry(QRect(780, 620, 60, 60))
        self.opponent_4.setStyleSheet(u"background-color: rgb(61, 61, 61);\n"
"border-radius: 30px;")
        self.opponent_1 = QLabel(self.frame)
        self.opponent_1.setObjectName(u"opponent_1")
        self.opponent_1.setGeometry(QRect(780, 640, 60, 60))
        self.opponent_1.setStyleSheet(u"background-color: rgb(61, 61, 61);\n"
"border-radius: 30px;")
        self.opponent_5 = QLabel(self.frame)
        self.opponent_5.setObjectName(u"opponent_5")
        self.opponent_5.setGeometry(QRect(780, 620, 60, 60))
        self.opponent_5.setStyleSheet(u"background-color: rgb(61, 61, 61);\n"
"border-radius: 30px;")
        self.opponent_6 = QLabel(self.frame)
        self.opponent_6.setObjectName(u"opponent_6")
        self.opponent_6.setGeometry(QRect(780, 640, 60, 60))
        self.opponent_6.setStyleSheet(u"background-color: rgb(61, 61, 61);\n"
"border-radius: 30px;")
        self.opponent_7 = QLabel(self.frame)
        self.opponent_7.setObjectName(u"opponent_7")
        self.opponent_7.setGeometry(QRect(780, 630, 60, 60))
        self.opponent_7.setStyleSheet(u"background-color: rgb(61, 61, 61);\n"
"border-radius: 30px;")
        self.opponent_8 = QLabel(self.frame)
        self.opponent_8.setObjectName(u"opponent_8")
        self.opponent_8.setGeometry(QRect(770, 630, 60, 60))
        self.opponent_8.setStyleSheet(u"background-color: rgb(61, 61, 61);\n"
"border-radius: 30px;")
        self.opponent_9 = QLabel(self.frame)
        self.opponent_9.setObjectName(u"opponent_9")
        self.opponent_9.setGeometry(QRect(780, 630, 60, 60))
        self.opponent_9.setStyleSheet(u"background-color: rgb(61, 61, 61);\n"
"border-radius: 30px;")
        self.chat_frame.raise_()
        self.label.raise_()
        self.frame_3.raise_()
        self.board_frame.raise_()
        self.frame_6.raise_()
        self.your_pieces_1.raise_()
        self.your_pieces_2.raise_()
        self.your_pieces_3.raise_()
        self.your_pieces_4.raise_()
        self.your_pieces_5.raise_()
        self.your_pieces_6.raise_()
        self.your_pieces_7.raise_()
        self.your_pieces_8.raise_()
        self.your_pieces_9.raise_()
        self.opponent_2.raise_()
        self.opponent_3.raise_()
        self.opponent_4.raise_()
        self.opponent_1.raise_()
        self.opponent_5.raise_()
        self.opponent_6.raise_()
        self.opponent_7.raise_()
        self.opponent_8.raise_()
        self.opponent_9.raise_()
        self.stackedWidget.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.frame_2 = QFrame(self.page_2)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setGeometry(QRect(0, 0, 1280, 720))
        self.frame_2.setStyleSheet(u"background-color: #ECF0F5;")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.stackedWidget.addWidget(self.page_2)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.stackedWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Jogo da Trilha", None))
        self.host_label.setText(QCoreApplication.translate("MainWindow", u"Voc\u00ea \u00e9 o Host da Partida.", None))
        self.begin_button.setText(QCoreApplication.translate("MainWindow", u"Come\u00e7ar", None))
        self.giveup_button.setText(QCoreApplication.translate("MainWindow", u"Desistir", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Chat da Partida", None))
        self.send_text_button.setText(QCoreApplication.translate("MainWindow", u"Enviar", None))
        self.your_pieces_1.setText("")
        self.your_pieces_2.setText("")
        self.your_pieces_3.setText("")
        self.your_pieces_4.setText("")
        self.your_pieces_5.setText("")
        self.your_pieces_6.setText("")
        self.your_pieces_7.setText("")
        self.your_pieces_8.setText("")
        self.your_pieces_9.setText("")
        self.opponent_2.setText("")
        self.opponent_3.setText("")
        self.opponent_4.setText("")
        self.opponent_1.setText("")
        self.opponent_5.setText("")
        self.opponent_6.setText("")
        self.opponent_7.setText("")
        self.opponent_8.setText("")
        self.opponent_9.setText("")
    # retranslateUi

