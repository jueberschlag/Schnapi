'''
Created on 7 mars 2012

@author: INSA Fuzzing
'''
import sys, subprocess, time
from controller import Controller
from options import *

'''Taille maximum pour une ligne de code de param_generato.py
   Permet de tester si le fichier a été généré ou non'''
MAX_SIZE = 100

def main(args):
    print("SCHNAPI V 1.3.8 : "+str(args[0])+", "+str(args[1]))
    #Création du controller
    c = Controller(args[0], int(args[1]), args[2], args[5], int(args[3]), int(args[4]))
    #Lancement du controller
    c.start()
            
if __name__ == "__main__":
    #Gestion des options
    '''
    args[0] : server,
    args[1] : port,
    args[2] : name, 
    args[3] : request_number, 
    args[4] : number of cores
    args[5] : workspace
    '''
    try :
        args = do_options_schnapi()
    except ValueError :
      print("Erreur : Valeur d'option erronée")
      exit(2)
    
    main(args)
    
