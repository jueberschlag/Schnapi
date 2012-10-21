'''
Created on 13 avr. 2012

@author: root
'''
from httpSocket import *

if __name__ == '__main__':
    httpSocket = httpSocket("localhost",8181)
    httpSocket.connect()
    
    httpSocket.sendRequest("requete")
    response = httpSocket.getResponse()
    print(response)
    
    httpSocket.disconnect()