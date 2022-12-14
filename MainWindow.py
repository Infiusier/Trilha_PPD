# coding: utf-8
from functools import partial
from queue import Queue
import math

from PySide2.QtCore import (QPropertyAnimation, QCoreApplication, QDate, QDateTime, QMetaObject,QObject, QPoint, QRect, QSize, QTime, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter,QPixmap, QRadialGradient)
from PySide2.QtWidgets import *
from PySide2 import QtWidgets, QtCore    
from PySide2.QtCore import *
from screen import Ui_MainWindow
import time
from subprocess import *
import threading
from Application import *
    
class MainWindow(QtWidgets.QMainWindow,Ui_MainWindow,QtCore.QObject):

    def __init__(self):
        super(MainWindow,self).__init__()
        self.setupUi(self)
        
        self.application = Application()
        self.application.gui_controller.widget_signal.connect(self.handle_communication)
        
        self.begin_button.clicked.connect(self.begin_game)
        self.send_text_button.clicked.connect(self.send_chat_msg)
        self.giveup_button.clicked.connect(self.give_up)
        
        self.board_frame.installEventFilter(self)
        
        pos_1 = (55,130)
        pos_2 = (260,130)
        pos_3 = (473,130)
        pos_4 = (111,185)
        pos_5 = (260,185)
        pos_6 = (415,185)
        pos_7 = (160,250)
        pos_8 = (260,250)
        pos_9 = (360,250)
        pos_10 = (55,341)
        pos_11 = (111,341)
        pos_12 = (160,341)
        pos_13 = (360,341)
        pos_14 = (415,341)
        pos_15 = (473,341)
        pos_16 = (160,432)
        pos_17 = (260,432)
        pos_18 = (360,432)
        pos_19 = (111,493)
        pos_20 = (260,493)
        pos_21 = (415,493)
        pos_22 = (55,541)
        pos_23 = (260,541)
        pos_24 = (473,541)
        
        self.pos_removed = (750,590)
        
        self.piece_positions = [pos_1,pos_2,pos_3,pos_4,pos_5,pos_6,pos_7,pos_8,pos_9,pos_10,pos_11,pos_12,pos_13,pos_14,pos_15,pos_16,pos_17,pos_18,pos_19,pos_20,pos_21,pos_22,pos_23,pos_24,self.pos_removed]
        
        self.opponent_pieces = [self.opponent_1,self.opponent_2,self.opponent_3,self.opponent_4,self.opponent_5,self.opponent_6,self.opponent_7,self.opponent_8,self.opponent_9]
        self.your_pieces = [self.your_pieces_1,self.your_pieces_2,self.your_pieces_3,self.your_pieces_4,self.your_pieces_5,self.your_pieces_6,self.your_pieces_7,self.your_pieces_8,self.your_pieces_9]
        
        for piece in self.your_pieces:
            piece.clicked.connect(partial(self.select_piece,self.your_pieces.index(piece)))
            
        for piece in self.opponent_pieces:
            piece.clicked.connect(partial(self.remove_opponent_piece,self.opponent_pieces.index(piece)))
        
        self.init_screen()
        
# Handle widget signals
    def handle_communication(self,parameters):
        
        if parameters[0]==GUI_CMD.SET_BOARD_OFF:
            self.set_board_frame_off()
            
        if parameters[0]==GUI_CMD.SET_BOARD_ON:
            self.set_board_frame_on()
            
        if parameters[0]==GUI_CMD.CHAT_MSG:
            self.append_chat_msg(parameters[1])
            
        if parameters[0]==GUI_CMD.STATUS_MSG:
            self.host_label.setText(parameters[1])
            
        if parameters[0]==GUI_CMD.SWITCH_COLOR:
            self.switch_pieces_color()
            
        if parameters[0]==GUI_CMD.SHOW_PIECES:
            self.show_pieces()
            
        if parameters[0]==GUI_CMD.MOVE_PIECE:
            self.move_your_piece(parameters[1],parameters[2])
            
        if parameters[0]==GUI_CMD.EN_DIS_PIECE:
            self.set_piece_clickable(parameters[1],parameters[2])
            
        if parameters[0]==GUI_CMD.AID_LABEL:
            self.status_label.setText(parameters[1])
            
        if parameters[0]==GUI_CMD.MOVE_OPPONENT_PIECE:
            self.move_opponent_piece(parameters[1],parameters[2])
            
        if parameters[0]==GUI_CMD.ENABLE_ALL_PIECES:
            for piece in self.your_pieces:
                piece.setEnabled(True)
            
# Game logics
    def give_up(self):
        self.application.give_up = True
        self.host_label.setText("Voc?? desistiu")
        self.status_label.setText("Voc?? desistiu")

    def move_piece(self,piece,position):
        piece.move(position[0],position[1])

    def remove_opponent_piece(self,piece_index):
        self.application.opponent_piece_removed = piece_index

    def set_piece_clickable(self,piece_index,clickable):
        self.your_pieces[piece_index].setEnabled(clickable)

    def select_piece(self, piece_index):
        self.application.piece_selected = piece_index
        
    def move_opponent_piece(self,piece_index, position_index):
        position = self.piece_positions[position_index]
        #self.opponent_pieces[piece_index].move(position[0],position[1])
        self.move_piece(self.opponent_pieces[piece_index], position)
        self.opponent_pieces[piece_index].show()
        
    def move_your_piece(self,piece_index,position):
        #self.your_pieces[piece_index].move(self.piece_positions[position][0],self.piece_positions[position][1])
        self.move_piece(self.your_pieces[piece_index], self.piece_positions[position])
        if position != -1:
            self.application.is_moving_piece = False
    
    def positioning_piece(self, position):
        if self.application.piece_selected == None:
            return
        
        max_distance = 15
        
        new_position = min(self.piece_positions, key=lambda point: math.hypot(position[1]-point[1], position[0]-point[0]))
        
        distance_between_points = math.dist(position, new_position)
        
        if distance_between_points <= max_distance:
            self.application.piece_position = self.piece_positions.index(new_position)

    def append_chat_msg(self,message):
        self.chat_output.append(message)

    def send_chat_msg(self):
        message = self.chat_input.toPlainText()
        self.chat_input.clear()
        
        self.append_chat_msg(("Eu: %s" % message))
        
        self.application.send_chat_message(message)

    def begin_game(self):
        self.host_label.setText("Iniciando jogo...")
        self.application.ip = self.ip_input.text()
        self.application.port = int(self.port_input.value())
        
        self.ip_input.setEnabled(False)
        self.port_input.setEnabled(False)
        
        if len(self.ip_input.text()) == 0:
            self.ip_input.setText("127.0.0.1")
        
        self.application.start()
        
    def handle_mouse_event(self,e):
        #if self.application.state == States.PREPARE_PIECES:
        self.positioning_piece((e.x()-10,e.y()+65))
            
    def eventFilter(self, source, event):
        
        if event.type() == QtCore.QEvent.MouseButtonPress:
            if event.button() == QtCore.Qt.LeftButton:
                self.handle_mouse_event(event)
            
        return QtWidgets.QMainWindow.eventFilter(self, source, event)
    
    def closeEvent(self, event):
        self.application.state = States.FINALIZED
        event.accept()
        
            
# Prepare screen
    def init_screen(self):
        self.color_label.hide()
        self.set_board_frame_off()
        self.host_label.setText("Aperte em Come??ar para iniciar.\n Deixe o IP vazio caso seja o Host")
        self.status_label.setText('')
        self.chat_output.setReadOnly(True)
        
        for piece in self.opponent_pieces:
            piece.hide()
            
        for piece in self.your_pieces:
            piece.hide()
            
# GUI functions

    def show_pieces(self):
        self.color_label.show()
        
        for piece in self.your_pieces:
            piece.show()

    def switch_pieces_color(self):
    
        if self.your_pieces[0].palette().button().color() == 'rgb(170, 0, 0)':
            new_color = 'rgb(61, 61, 61)'
            old_color = 'rgb(170, 0, 0)'
            
        else:
            old_color = 'rgb(61, 61, 61)'
            new_color = 'rgb(170, 0, 0)'
    
        for piece in self.opponent_pieces:
            piece.setStyleSheet("background-color:%s;border-radius:30px;" % new_color)
            
        for piece in self.your_pieces:
            piece.setStyleSheet("background-color:%s;border-radius:30px;" % old_color)
            
        self.color_label.setStyleSheet("color:%s" % old_color)
        

    def set_board_frame_off(self):
        self.board_frame.setEnabled(False)
        self.chat_frame.setEnabled(False)
        
        self.begin_button.setEnabled(True)
        self.giveup_button.setEnabled(False)
        
    def set_board_frame_on(self):
        self.board_frame.setEnabled(True)
        self.chat_frame.setEnabled(True)
        
        self.begin_button.setEnabled(False)
        self.giveup_button.setEnabled(True)