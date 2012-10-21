'''
Created on 7 mars 2012

@author: INSA Fuzzing
'''
import sys
from monitor import Monitor
from campaign import Campaign
from networkAgent import networkAgent

class Controller(object):
    '''
    Controlleur principal du fuzzer Schnapi
    '''
    
    #Constructor
    def __init__(self,host,port,name,workspace,nb_request,nb_cores):
        #Attributes initialization
        self.host = host
        self.port = port
        self.name = name
        self.nb_request = nb_request
        self.workspace = workspace
        self.nb_cores = nb_cores
        #Monitor initialization
        self.monitor = Monitor(name,workspace,nb_cores,"valid_request_file","error_file","log_file")
        #networkAgent initialization
        self.networkAgent = networkAgent(host,port)
        
    #Add a valid request to the monitor
    def addValidRequestToMoniteur(self,request):
        self.monitor.addRequest("valid",request)
    
    #Add a fuzzing request to the monitor
    def addFuzzingRequestToMoniteur(self,request):
        self.monitor.addRequest("fuzz",request)
            
    #Add a response to the monitor
    def addResponseToMoniteur(self,response):
        self.monitor.addResponse(response)
        
    #Notifiy that the valid request are done so we can compute the central response
    def endOfValidRequest(self):
        self.monitor.computePerimeter()
        
    #Send a valid request to the http agent
    def sendValidRequest(self,request):
        #Send the request to the http socket
        if (self.networkAgent.sendRequest(request) == -1):
            print("Probleme d'envoi des requetes pendant la phase de requêtes valides")
            sys.exit(1)
        #Add the request to the log
        self.addValidRequestToMoniteur(request)
        
    #Send a fuzzing request to the http agent
    def sendFuzzingRequest(self,request):
        #Send the request to the http socket
        if (self.networkAgent.sendRequest(request) == -1):
            print("Probleme d'envoi des requetes pendant la phase de fuzzing")
            #Add to error file
            self.addFuzzingRequestToMoniteur(request)
            self.addResponseToMoniteur(self.networkAgent.getResponse())
            self.monitor.img.fin()
            sys.exit(1)
        else:
            #Add the request to the log
            self.addFuzzingRequestToMoniteur(request)
   
    #Get the response to a request
    def receiveResponse(self):
        #Get the response
        response = self.networkAgent.getResponse()
        #Add the response to the log and check if there is an error
        self.monitor.addResponse(str(response))
        
    #Launch a campaign
    def start(self):
        print("Lancement du Controlleur principal")
        #Create the campaign
        print("Création de la campagne de fuzzing")
        camp = Campaign(self.name, self, self.nb_request)
        #Start the campaign
        print("Lancement de la campagne de fuzzing")
        camp.startCampaign()
        #End of campaign: image
        print("Création image Latex et R")
        self.monitor.img.fin()

        
    
