import socket
import threading
import sys
from random import randint
import time


import grpc
from concurrent import futures
import game_service_pb2_grpc as pb2_grpc
import game_service_pb2 as pb2
    
class Server_provider(pb2_grpc.Game_serviceServicer):
    def __init__(self,port):
        print("Server running")
        self.chats = []
        
    def send_chat_message(self, request: pb2.Message(),conext):
        
        #Server.input_payload.append(request.message)
        self.chats.append(request)
        return pb2.Empty()
        
    def get_chat_message(self, request_iterator, context):
        lastindex = 0
        
        while True:
            # Check if there are any new messages
            while len(self.chats) > lastindex:
                n = self.chats[lastindex]
                lastindex += 1
                yield n
        
class Server():
    
    input_payload = []
    
    def __init__(self,port):
        self.port = port
        self.id = 'server'
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        pb2_grpc.add_Game_serviceServicer_to_server(Server_provider(port), self.server)
        self.server.add_insecure_port('[::]:' + str(port))
        self.server.start()
        #self.server.wait_for_termination()
        
    def run(self):
        self.channel = grpc.insecure_channel('{}:{}'.format('localhost', self.port))

        # bind the client and the server
        self.stub = pb2_grpc.Game_serviceStub(self.channel)
        
        while True:
            for data in self.stub.get_chat_message(pb2.Empty()):
                if data.id != self.id:
                    Server.input_payload.append(str(data.message))
                
    def send_message(self,data):
        try:
            message = pb2.Message(message=data,id = self.id)
            self.stub.send_chat_message(message)
            
        except KeyboardInterrupt:
            sys.exit(0)
        except Exception as e:
            print("Failed to send message: %s" % str(e))
            
            
class Client:
    
    input_payload = []
            
    def __init__(self, address,port):
        self.id = 'client'
        self.channel = grpc.insecure_channel('{}:{}'.format(address, port))

        # bind the client and the server
        self.stub = pb2_grpc.Game_serviceStub(self.channel)
      
    def run(self):
        print("Client running")
        while True:
            for data in self.stub.get_chat_message(pb2.Empty()):
                if data.id != self.id:
                    Client.input_payload.append(str(data.message))

        
    def send_message(self,data):
        try:
            message = pb2.Message(message=data,id = self.id)
            self.stub.send_chat_message(message)
            
        except KeyboardInterrupt:
            sys.exit(0)
        except Exception as e:
            print("Failed to send message: %s" % str(e))
        
class Communication:
    
    def __init__(self):
        self.is_host = None
        self.is_connected = False
        self.handler = None
        self.ip = None
        self.port = None
        
    def send_message(self,data):
        iThread = threading.Thread(target=self.handler.send_message,args=(data,))
        iThread.daemon = True
        iThread.start()
        
    def get_message(self):
        return self.handler.input_payload.pop(0)
    
    def has_message(self):
        return True if len(self.handler.input_payload) > 0 else False
    
    def start(self):
        iThread = threading.Thread(target=self.run)
        iThread.daemon = True
        iThread.start()
                
    def run(self):
        while True:
            try:
                print("Trying to connect...")
                time.sleep(randint(1,5))
                
                try:
                    self.handler = Client(self.ip,self.port)
                    self.is_host = False
                    self.is_connected = True
                    self.handler.run()
                    
                except KeyboardInterrupt:
                    self.is_connected = False
                    sys.exit(0)
                except Exception as e:
                    self.is_connected = False
                    print("Client: " + str(e))
                
                try:
                    self.handler = Server(self.port)
                    self.is_host = True
                    self.is_connected = True
                    self.handler.run()
                except KeyboardInterrupt:
                    sys.exit(0)
                except Exception as e:
                    print("Couldn't start the server: %s" % str(e))
                        
            except KeyboardInterrupt:
                sys.exit(0)
                
            break
                
if __name__ == "__main__":
    comm = Communication()
    comm.ip = 'localhost'
    comm.port = 50051
    comm.start()
    
    while 1:
        time.sleep(1)
        if comm.is_connected == False:
            continue
        
        if comm.has_message() == True:
            print(comm.get_message())
        
        if comm.is_host == False:
            comm.send_message("OI")
            
        else:
            comm.send_message("OLA")
        