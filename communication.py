import socket
import threading
import sys
from random import randint
import time

class p2p:
    peers = ['127.0.0.1']

class Server:
    
    connections = []
    peers = []
    
    def __init__(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('127.0.0.1',10000))
        sock.listen(1)
        
        iThread = threading.Thread(target=self.sendMsg)
        iThread.daemon = True
        iThread.start()
        
        print("Server running")
        
        while True:
            c, a = sock.accept()
            cThread = threading.Thread(target = self.handler, args = (c, a))
            cThread.daemon = True
            cThread.start()
            self.connections.append(c)
            self.peers.append(a[0])
            print(str(a[0]) + ':' + str(a[1]),"Connected")
            self.sendPeers()
        
    def handler(self, c, a):
        while True:
            try:
                data = c.recv(1024)
            except:
                data = None
            
            if not data:
                print(str(a[0]) + ':' + str(a[1]),"Disconected")
                self.connections.remove(c)
                self.peers.remove(a[0])
                c.close()
                self.sendPeers()
                break
            
            print(str(data,'utf-8'))
            
            for connection in self.connections:
                if connection.getpeername()[1] != a[1]:
                    connection.send(data)
                
    def sendPeers(self):
        p = ""
        
        for peer in self.peers:
            p = p + peer + ","
            
        for connection in self.connections:
            connection.send(b'\x11' + bytes(p,"utf-8"))
            
    def sendMsg(self):
        while True:
            data = bytes(input(""), 'utf-8')
            try:
                for connection in self.connections:
                    connection.send(data)
                    sock.send(bytes(input(""), 'utf-8'))
            except KeyboardInterrupt:
                sys.exit(0)
            except:
                pass
            
class Client:
    
    def sendMsg(self, sock):
        while True:
            try:
                sock.send(bytes(input(""), 'utf-8'))
            except KeyboardInterrupt:
                sys.exit(0)
            except:
                pass
            
    def __init__(self, address):
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.connect((address,10000))
        
        iThread = threading.Thread(target=self.sendMsg, args=(sock,))
        iThread.daemon = True
        iThread.start()
        
        while True:
            data = sock.recv(1024)
            
            if not data:
                break
            
            if data[0:1] == b'\x11':
                print("Got peers")
                self.updatePeers(data[1:])
                
            else:
                print(str(data,'utf-8'))
        
    def updatePeers(self,peerData):
        p2p.peers = str(peerData,"utf-8").split(",")[:-1]
        
class Communication:
    
    def __init__(self):
        pass
                
    def run(self):
        while True:
            try:
                print("Trying to connect...")
                time.sleep(randint(1,5))
                
                for peer in p2p.peers:
                    try:
                        cliente = Client(peer)
                    except KeyboardInterrupt:
                        sys.exit(0)
                    except Exception as e:
                        print("Client: " + str(e))
                    
                    try:
                        server = Server()
                    except KeyboardInterrupt:
                        sys.exit(0)
                    except:
                        print("Couldn't start the server...")
                        
            except KeyboardInterrupt:
                sys.exit(0)
                
if __name__ == "__main__":
    comm = Communication()
    comm.run()