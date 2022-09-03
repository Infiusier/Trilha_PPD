# coding: utf-8
import time,threading,os,json
from datetime import datetime
from intelhex import IntelHex
from queue import Queue
from enum import Enum,auto

from PySide2.QtCore import QThread
from PySide2 import QtCore

from communication import Communication

DEBUG = 1

class States():
    JOIN_GAME = auto()
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
        
        self.state_functions = {States.JOIN_GAME : self.join_game,
                                States.PREPARE_PIECES : self.prepare_pieces}
        
        '''self.state_functions = {States.FLASH_FIRMWARE : self.flash_firmware_stage,
                                States.EXECUTE_SCRIPT : self.execute_script_stage,
                                States.VALIDATE : self.validate_factory_stage,
                                States.FLASH_PROD_FIRMWARE : self.flash_prod_firmware_stage,
                                States.MEMORY_LOCK : self.memory_lock_stage,
                                States.FINAL : self.final_function}'''

    def parse_output_payload(self,message):
        json_payload = {'msg_type' : 'chat msg',
                        'payload' : message}
        
        return json.dumps(json_payload)
        
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
        self.state = States.PREPARE_PIECES
        
    def prepare_pieces(self):
        
        self.mouse_position = None
        self.piece_selected = None
        
        if self.my_turn == False:
            return
        
        if self.pieces_placed >= 9:
            self.mouse_position = None
            self.piece_selected = None
            return
        
        while self.mouse_position == None:
            pass
        
        self.gui_controller.move_piece(self.piece_selected, self.mouse_position)
        self.pieces_placed += 1
    
    def send_chat_message(self,message):
        self.comm_driver.send_message(self.parse_output_payload(message))
        
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
        
        if payload_json['msg_type'] == Protocol.CHAT_MSG:
            self.get_chat_message(payload_json['payload'])
        
        
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
        
    def switch_piece_colors(self):
        command = [GUI_CMD.SWITCH_COLOR]
        self.widget_signal.emit(command)
        
    def show_pieces(self):
        command = [GUI_CMD.SHOW_PIECES]
        self.widget_signal.emit(command)
        
    def move_piece(self,piece,position):
        command = [GUI_CMD.MOVE_PIECE,piece,position]
        self.widget_signal.emit(command)
        
    '''def set_gui_frame_off(self):
        command = [GUI_CMD.SET_GUI_FRAME_OFF]
        self.widget_signal.emit(command)
    
    def set_gui_frame_on(self):
        command = [GUI_CMD.SET_GUI_FRAME_ON]
        self.widget_signal.emit(command)
        
    def append_error_to_log(self,message):
        command=[GUI_CMD.APPEND_TO_LOG,message,"red"]
        self.widget_signal.emit(command)
        
    def append_success_to_log(self,message):
        command=[GUI_CMD.APPEND_TO_LOG,message,"green"]
        self.widget_signal.emit(command)
        
    def append_to_log(self,message):
        command=[GUI_CMD.APPEND_TO_LOG,message,"white"]
        self.widget_signal.emit(command)
        
    def set_frame_red(self):
        command=[GUI_CMD.SET_FRAME_COLOR,Macros.WIDGET_RED_COLOR]
        self.widget_signal.emit(command)
        
    def set_frame_green(self):
        command=[GUI_CMD.SET_FRAME_COLOR,Macros.WIDGET_GREEN_COLOR]
        self.widget_signal.emit(command)
        
    def set_frame_running_stage(self):
        command=[GUI_CMD.SET_FRAME_COLOR,Macros.WIDGET_CURRENT_COLOR]
        self.widget_signal.emit(command)
        
    def set_gui_status_label(self,message,screen_page):
        command=[GUI_CMD.SET_GUI_STATUS_LABEL,message,screen_page]
        self.widget_signal.emit(command)
        
    def set_widget_current_stage(self,stage,screen_page):
        command=[GUI_CMD.SET_WIDGET_COLOR,Macros.WIDGET_CURRENT_COLOR,screen_page,stage]
        self.widget_signal.emit(command)
        
    def set_widget_status(self,stage,screen_page, status: bool):
        if status == True:
            self.set_widget_green(stage,screen_page)
        
        else:
            self.set_widget_red(stage,screen_page)
        
    def set_widget_red(self,stage,screen_page):
        command=[GUI_CMD.SET_WIDGET_COLOR,Macros.WIDGET_RED_COLOR,screen_page,stage]
        self.widget_signal.emit(command)
        
    def set_widget_green(self,stage,screen_page):
        command=[GUI_CMD.SET_WIDGET_COLOR,Macros.WIDGET_GREEN_COLOR,screen_page,stage]
        self.widget_signal.emit(command)
        
    def set_deveui_label(self,deveui):
        command=[GUI_CMD.SET_DEVEUI_LABEL,deveui]
        self.widget_signal.emit(command)
        
    def clear_qr_code_label(self):
        command=[GUI_CMD.CLEAR_QR_CODE_LABEL]
        self.widget_signal.emit(command)
        
    def set_script_running_blink(self,state):
        
        if state == True:
            command = [GUI_CMD.SCRIPT_LABEL_BLINK_ON]
            
        else:
            command = [GUI_CMD.SCRIPT_LABEL_BLINK_OFF]
        
        self.widget_signal.emit(command)
        
    def launch_qr_code_popup(self):
        command=[GUI_CMD.LAUNCH_QRCODE_POPUP]
        self.widget_signal.emit(command)
        
    def set_rssi_value(self, rssi_value: str):
        command=[GUI_CMD.SET_RSSI_VALUE,rssi_value]
        self.widget_signal.emit(command)'''
    
        