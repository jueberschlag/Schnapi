# -*- coding: utf-8 -*-

'''
Created on 25 fevr. 2012

@author: Florian Fougeanet
        Carla Sauvanaud
        Jerome Ueberschlag
'''
import sys
sys.path.append('./description/')
import random
try :
    from param_generator import *
except ImportError :
     print("Attente de la creation de ./description/param_generator.py")

NB_VALID_REQUEST = 6
'''Valeur par défaut pour le nombre de requete valides à envoyer au serveur distant'''

class Campaign(object):
    '''
    Classe decrivant une operation du moniteur. Celle-ci peut etre une operation valide ou bien de fuzzing.
    Chaque objet Campaign pourra par la suite decrire un certain type de fuzzing recherchant une faille precise.
    '''
    

    def __init__(self, name,controller,nb_request):
        '''Constructeur'''
        self.NB_FUZZING_REQUEST = 1
        self.name = name
        self.controller = controller
        #Nombre de requêtes de fuzzing à envoyer au seveur distant
        self.nb_request = nb_request
    
    '''
    Lance la campagne de requetes
    '''
    def startCampaign(self):
        for i in range(0,self.nb_request):
            self.validExecution()
        #Calcul du perimetre
        self.controller.endOfValidRequest()
        params_allowed = params_availabled()
        
        for i in range(0,self.nb_request):
            elements_done = []
            for i in range(random.randint(1, len(params_allowed)-1)):
                e = random.choice(params_allowed)
                while (e in elements_done):
	                e = random.choice(params_allowed)
                elements_done.append(e)

            self.fuzzExecution(elements_done)
        print("Campagne terminée")
	
    '''
    Envoi sur le reseau d'une requete valide grace a l'agent http
    '''
    def validExecution(self):
        #Generation d'une liste d'arguments pour la requete http
        request_params = request_generator([])
        request = transform_to_request(request_params)

        #Envoi d'une requete valide
        print("Envoi d'une requete valide")
        self.controller.sendValidRequest(request)

        #Lecture de la reponse
        self.controller.receiveResponse()
        

    '''
    Envoi sur le reseau une requete de fuzzing
    
    @param args Liste de nombre correspondant a un champ a fuzzer
          methods : 1 
          urls : 2
          versions : 3
          headers : 4
              headers -> Accept : 4.1
              headers -> Accept-Charset :4.2 [...]
    ''' 
    def fuzzExecution(self, args):        
        #Generation d'une liste d'arguments pour la requete http
        
        request_params = request_generator(args)
        request = transform_to_request(request_params)
        
        #Envoie d'une requete invalide
        print("Envoi requete invalide numéro "+str(self.NB_FUZZING_REQUEST))
        self.controller.sendFuzzingRequest(request);
                   
        #Lecture de la reponse
        print("Lecture de la reponse")
        self.controller.receiveResponse()
        
        self.NB_FUZZING_REQUEST = self.NB_FUZZING_REQUEST + 1
