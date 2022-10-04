# coding: utf-8
import time,threading,os,json
from enum import Enum,auto

from PySide2.QtCore import QThread
from PySide2 import QtCore

from communication import Communication

class States():
    JOIN_GAME = auto()
    WAITING_OPPONENT = auto()
    PREPARE_PIECES_GUI = auto()
    PREPARE_PIECES =auto()
    MOVING_PIECES_GUI = auto()
    MOVING_PIECES =auto()
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
        self.opponent_piece_removed = None
        self.ip = None
        self.port = None
        self.give_up = False
        self.opponent_has_connected = False
        
        self.state_functions = {States.JOIN_GAME : self.join_game,
                                States.WAITING_OPPONENT : self.waiting_opponent,
                                States.PREPARE_PIECES_GUI : self.prepare_pieces_gui,
                                States.PREPARE_PIECES : self.prepare_pieces,
                                States.MOVING_PIECES_GUI : self.moving_pieces_gui,
                                States.MOVING_PIECES : self.moving_pieces,
                                States.FINALIZED : self.finalized}

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
    
    def parse_remove_piece_command(self,piece):
        json_payload = {'msg_type' : 'remove piece',
                        'payload' : piece}
        
        return json.dumps(json_payload)
    
    def parse_give_up_command(self):
        json_payload = {'msg_type' : 'give up',
                        'payload' : ''}
        
        return json.dumps(json_payload)
    
    def change_turn(self):
        self.comm_driver.send_message(self.parse_your_turn())
        
    def move_piece_command(self,piece,position):
        self.comm_driver.send_message(self.parse_move_piece_command(piece, position))
        
    def give_up_command(self):
        self.comm_driver.send_message(self.parse_give_up_command())
        
    def has_connected_command(self):
        json_payload = {'msg_type' : 'has connected',
                        'payload' : ''}
        self.comm_driver.send_message(json.dumps(json_payload))
        
    def remove_piece_command(self,piece):
        self.comm_driver.send_message(self.parse_remove_piece_command(piece))
        
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
        
        self.has_connected_command()
        
        if self.opponent_has_connected == False:
            time.sleep(1)
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
        
    def prepare_pieces(self):
        
        if self.my_turn == False:
            self.piece_position = None
            self.piece_selected = None
            return
        
        if self.pieces_placed >= 9:
            self.piece_position = None
            #self.piece_selected = None
            self.state = States.MOVING_PIECES_GUI
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
        
    def moving_pieces_gui(self):
        self.gui_controller.set_status_message("Fase de movimentação de Peças")
        self.gui_controller.enable_all_pieces()
        
        if self.my_turn == True:
            self.gui_controller.set_aid_label_message("Seu Turno")
            
        else:
            self.gui_controller.set_aid_label_message("Turno do Oponente")
            
        self.is_moving_piece = True
        self.piece_position = None
        self.piece_selected = None
        
        self.state = States.MOVING_PIECES
        
    def moving_pieces(self):
        
        if self.my_turn == False:
            self.piece_position = None
            self.piece_selected = None
            return
        
        if self.is_moving_piece == True:
            if self.piece_position != None:
                self.gui_controller.move_piece(self.piece_selected, self.piece_position)
                self.move_piece_command(self.piece_selected, self.piece_position)
                self.piece_position = None
            
            return
                
        self.my_turn = False
        self.is_moving_piece = True
        self.gui_controller.set_aid_label_message("Turno do Oponente")
        self.change_turn()
        
    def finalized(self):
        pass
        
    def handle_opponent_pieces_removed(self):
        if self.opponent_piece_removed == None:
            return
        
        self.gui_controller.move_opponent_piece(self.opponent_piece_removed, -1)
        self.remove_piece_command(self.opponent_piece_removed)
        
        self.opponent_piece_removed = None
        
    def send_chat_message(self,message):
        self.comm_driver.send_message(self.parse_send_chat_msg(message))
        
    def get_chat_message(self,message):
        msg = "Oponente: %s" % message
        self.gui_controller.append_chat_message(msg)
        
    def give_up_func(self):
        if self.give_up == False:
            return
        
        self.give_up_command()
        self.state = States.FINALIZED
    
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
            self.gui_controller.move_opponent_piece(payload_json['payload']['piece'],payload_json['payload']['position'])
            
        elif payload_json['msg_type'] == 'remove piece':
            self.gui_controller.move_piece(payload_json['payload'], -1)
            
        elif payload_json['msg_type'] == 'has connected':
            self.opponent_has_connected = True
            
        elif payload_json['msg_type'] == 'give up':
            self.gui_controller.set_aid_label_message("Oponente Desistiu")
            self.gui_controller.set_status_message("Oponente Desistiu")
            self.state = States.FINALIZED
            
        
    def start(self):
        thread = threading.Thread(target=self.run,args=())
        thread.start()
        
    def run_game(self):
        
        while self.state != States.FINALIZED:
            self.give_up_func()
            self.parse_input_payload()
            self.handle_opponent_pieces_removed()
            self.state_functions[self.state]()
    
    def run(self):
        self.state = States.JOIN_GAME
        
        self.gui_controller.set_board_gui_on()
        
        self.comm_driver.ip = self.ip
        self.comm_driver.port = self.port
        self.comm_driver.start()
        
        time.sleep(10)
        
        self.run_game()
        
        self.gui_controller.set_board_gui_off()
        
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
    ENABLE_ALL_PIECES = auto()

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
        
    def enable_all_pieces(self):
        command = [GUI_CMD.ENABLE_ALL_PIECES]
        self.widget_signal.emit(command)
        