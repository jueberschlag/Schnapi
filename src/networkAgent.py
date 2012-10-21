'''
Created on 12 avr. 2012

@author: INSA Fuzzing
'''
import socket
import sys


class networkAgent(object):
    #Initialization
    def __init__(self,host,port):
        self.HOST = host
        self.PORT = port
        self.connected = 0
        self.response = None

    #Connection to the host
    def connect(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect_ex((self.HOST, self.PORT))
            self.connected = 1
        except Exception as msg:
            print("Probleme de connexion : arrêt de Schnapi")
            sys.exit(0)
    
    #Disconnection from the host
    def disconnect(self):
        if (self.connected == 1):
            self.sock.close()
            
    #Send a request to the host
    def sendRequest(self,request):
        #Connection before sending
        self.connect()
        #Encoding of the request: from string to bytes
        req = request.encode()
        #while there is something to send
        totalsent = 0
        while totalsent < len(req):
            try:
                #Send a part of the request
                sent = self.sock.send(req[totalsent:])
                totalsent = totalsent + sent
            except socket.error as e:
                self.response = ""
                self.disconnect()
                return -1
        #Structure to receive the response
        #print("Lecture de la reponse")
        try:
            data = self.sock.recv(1024)
            string = ""
            #While there is something to receive
            while len(data):
                string = string + str(data)
                data = self.sock.recv(1024)
            #Save the response for later
            self.response = string
        except Exception as e:
            self.response = ""
            self.disconnect()
            return -1
        #Disconnection
        self.disconnect()
    
    #Return the saved response    
    def getResponse(self):
        return self.response
