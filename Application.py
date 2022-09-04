# coding: utf-8
import time,threading,os,json
from enum import Enum,auto

from PySide2.QtCore import QThread
from PySide2 import QtCore

from communication import Communication

DEBUG = 1

class States():
    JOIN_GAME = auto()
    WAITING_OPPONENT = auto()
    PREPARE_PIECES_GUI = auto()
    PREPARE_PIECES =auto()
    FINALIZED = auto()
    
class Protocol():
    CHAT_MSG = 'chat msg'

class Application():
    
    def __init__(self):
        super(Application,self).__init__()
        
        self.comm_driver = Communication()
        self.gui_controller=GUI_Controller()
        
        self.state = States.JOIN_GAME
        self.pieces_placed = 0
        self.positioning_piece = False
        self.my_turn = None
        self.opponent_has_moved = False
        
        self.state_functions = {States.JOIN_GAME : self.join_game,
                                States.WAITING_OPPONENT : self.waiting_opponent,
                                States.PREPARE_PIECES_GUI : self.prepare_pieces_gui,
                                States.PREPARE_PIECES : self.prepare_pieces}

    def parse_send_chat_msg(self,message):
        json_payload = {'msg_type' : 'chat msg',
                        'payload' : message}
        
        return json.dumps(json_payload)
    
    def parse_your_turn(self):
        json_payload = {'msg_type' : 'your turn',
                        'payload' : ''}
        
        return json.dumps(json_payload)
    
    def parse_move_piece_command(self,piece, position):
        json_payload = {'msg_type' : 'move piece',
                        'payload' : {'piece' : piece, 'position' : position}}
        
        return json.dumps(json_payload)
    
    def change_turn(self):
        self.comm_driver.send_message(self.parse_your_turn())
        
    def join_game(self):
        if self.comm_driver.is_connected == False:
            return
        
        if self.comm_driver.is_host == True:
            self.gui_controller.set_status_message("Você é o Host da Partida.")
            self.gui_controller.switch_piece_colors()
            self.my_turn = True
        else:
            self.gui_controller.set_status_message("Conectado ao Host.")
            self.my_turn = False
            
        self.gui_controller.show_pieces()
        self.gui_controller.set_status_message("Aguardando Oponente")
        self.state = States.WAITING_OPPONENT
        
    def waiting_opponent(self):
        
        if self.comm_driver.opponent_has_connected() == False:
            return
        
        self.state = States.PREPARE_PIECES_GUI
        
    def prepare_pieces_gui(self):
        self.gui_controller.set_status_message("Fase de alocação de Peças")
        
        if self.my_turn == True:
            self.gui_controller.set_aid_label_message("Seu Turno")
            
        else:
            self.gui_controller.set_aid_label_message("Turno do Oponente")
        
        self.is_moving_piece = True
        self.piece_position = None
        self.piece_selected = None
        self.state = States.PREPARE_PIECES
        
    def move_piece_command(self,piece,position):
        self.comm_driver.send_message(self.parse_move_piece_command(piece, position))
        
    def prepare_pieces(self):
        
        if self.my_turn == False:
            self.piece_position = None
            self.piece_selected = None
            return
        
        if self.pieces_placed >= 9:
            self.piece_position = None
            self.piece_selected = None
            return
        
        if self.is_moving_piece == True:
            if self.piece_position != None:
                self.gui_controller.move_piece(self.piece_selected, self.piece_position)
                self.move_piece_command(self.piece_selected, self.piece_position)
                self.piece_position = None
            
            return
                
        self.gui_controller.set_piece_clickable(self.piece_selected, False)
        self.my_turn = False
        self.is_moving_piece = True
        self.gui_controller.set_aid_label_message("Turno do Oponente")
        self.change_turn()
        
        self.pieces_placed += 1
        
    def send_chat_message(self,message):
        self.comm_driver.send_message(self.parse_send_chat_msg(message))
        
    def get_chat_message(self,message):
        msg = "Oponente: %s" % message
        self.gui_controller.append_chat_message(msg)
    
    def parse_input_payload(self):
        if self.comm_driver.is_connected == True:
            if self.comm_driver.has_message():
                payload = self.comm_driver.get_message()
                
            else:
                return
            
        else:
            return
        
        payload_json = json.loads(payload)
        
        if payload_json['msg_type'] == 'chat msg':
            self.get_chat_message(payload_json['payload'])
        
        elif payload_json['msg_type'] == 'your turn':
            self.gui_controller.set_aid_label_message("Seu Turno")
            self.my_turn = True
            
        elif payload_json['msg_type'] == 'move piece':
            self.opponent_has_moved = True
            self.gui_controller.move_opponent_piece(payload_json['payload']['piece'],payload_json['payload']['position'])
            
        
    def start(self):
        thread = threading.Thread(target=self.run,args=())
        thread.start()
        
    def run_game(self):
        
        while self.state != States.FINALIZED:
            self.parse_input_payload()
            self.state_functions[self.state]()
    
    def run(self):
        self.state = States.JOIN_GAME
        
        self.gui_controller.set_board_gui_on()
        
        self.comm_driver.start()
        self.run_game()
        
        self.gui_controller.set_board_gui_off()
        
    def print_debug(self,message):
        if DEBUG == 1:
            print(message)
        
class GUI_CMD():
    SET_BOARD_OFF = auto()
    SET_BOARD_ON = auto()
    CHAT_MSG = auto()
    STATUS_MSG = auto()
    SWITCH_COLOR = auto()
    SHOW_PIECES = auto()
    MOVE_PIECE = auto()
    EN_DIS_PIECE = auto()
    AID_LABEL = auto()
    MOVE_OPPONENT_PIECE = auto()

class GUI_Controller(QtCore.QObject):
    '''Sinais que comunicam com a thread da GUI'''
    widget_signal=QtCore.Signal(object)
    
    def __init__(self):
        super(GUI_Controller,self).__init__()
        
    def set_board_gui_off(self):
        command = [GUI_CMD.SET_BOARD_OFF]
        self.widget_signal.emit(command)
        
    def set_board_gui_on(self):
        command = [GUI_CMD.SET_BOARD_ON]
        self.widget_signal.emit(command)
        
    def append_chat_message(self,message):
        command = [GUI_CMD.CHAT_MSG,message]
        self.widget_signal.emit(command)
        
    def set_status_message(self,message):
        command = [GUI_CMD.STATUS_MSG,message]
        self.widget_signal.emit(command)
        
    def set_aid_label_message(self,message):
        command = [GUI_CMD.AID_LABEL,message]
        self.widget_signal.emit(command)
        
    def switch_piece_colors(self):
        command = [GUI_CMD.SWITCH_COLOR]
        self.widget_signal.emit(command)
        
    def show_pieces(self):
        command = [GUI_CMD.SHOW_PIECES]
        self.widget_signal.emit(command)
        
    def move_piece(self,piece,position):
        command = [GUI_CMD.MOVE_PIECE,piece,position]
        self.widget_signal.emit(command)
        
    def set_piece_clickable(self,piece,clickable):
        command = [GUI_CMD.EN_DIS_PIECE,piece,clickable]
        self.widget_signal.emit(command)
        
    def move_opponent_piece(self,piece,position):
        command = [GUI_CMD.MOVE_OPPONENT_PIECE,piece,position]
        self.widget_signal.emit(command)
        