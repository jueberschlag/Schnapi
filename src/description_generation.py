'''
Created on 7 mars 2012

@author: INSA Fuzzing
'''
import sys, subprocess, time
from options import *

'''Taille maximum pour une ligne de code de param_generato.py
   Permet de tester si le fichier a été généré ou non'''
MAX_SIZE = 100

def main(args):
    
    #Actualisation de la description du protocole
    if args != None :
        try:
            #Test si la description renseignée existe
            f = open(args, 'r')
            f.close()
        except IOError:
            print("Error : failed to load external entity : "+args)
            exit(1)
        
        #Application de la transformation xslt
        print("Transformation de la description xml du protocole cible")
        
        try :
          err = open('/tmp/schnapi.err.rm', 'w')
          #Suppression de l'ancien param_generator.py
          rm = subprocess.Popen("rm ./description/param_generator*",shell=True, stdout = sys.stdout, stderr = err)
          rm.communicate()
          err.close()
          err = open('/tmp/schnapi.err.xsltproc', 'w')
          #Création du nouveau fichier
          stdout_file = open("./description/param_generator.py", 'w')
          xsltproc = subprocess.Popen("xsltproc ./description/description_to_python.xsl "+args,shell=True, stdout = stdout_file, stderr = err)
          xsltproc.communicate()
          stdout_file.close()
          err.close()
          #time.sleep(1)
          err = open('/tmp/schnapi.err.xsltproc', 'r')
          #Lecture du fichier d'erreurs
          l = err.read(MAX_SIZE)
          
          err.close()
          if "command not found" in l :
            raise EnvironmentError

        except EnvironmentError :  
          print("Erreur : xsltproc n'est pas installé sur la machine (voir prérequis schnapi)")
          exit(2)

    #Si aucune option précisant l'emplacement de la description xml n'a été précisée
    #on suppose que le xslt a déjà été appliqué dans une campagne précédente.
    
    try:
      with open("description/param_generator.py", 'r') as f:
        l = f.read(MAX_SIZE)
        if not l : raise IOError
        f.close()

    except IOError:
        print("Erreur : param_generator.py n'a jamais été généré")
        print("Veuillez préciser le chemin d'une description xml valide afin de générer param_generator.py (voir options).")
        f.close()
        exit(1)
            
if __name__ == "__main__":
    #Gestion des options
    '''     
    args : input_file 
    '''
    try :
        args = do_options_description()
    except ValueError :
      print("Erreur : Valeur d'option erronée")
      exit(2)

    main(args)
    

