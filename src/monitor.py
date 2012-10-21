'''
Created on 7 mars 2012

@author: INSA Fuzzing
'''


from datetime import datetime
from difflib import SequenceMatcher
import os
from image import *


class Monitor(object):
    '''
    Moniteur des campagnes de fuzzing servant a gerer les fichiers de sortie
    '''


    '''
    Constructor
    '''
    def __init__(self, name, workspace, nb_cores, request_file, error_file, log_file):
        #Nom
        self.name = name
        #Nombre de coeur
        self.nb_cores = nb_cores
        #Image
        self.img = image(workspace, self.name, self.nb_cores)
        #Enregistrement des noms de fichiers
        self.error_file_name = error_file
        self.valid_request_file_name = request_file
        self.log_file_name = log_file
        self.campaign_info_file_name = "README"
        
        #Deplacement dans le dossier de travail dans un dossier du nom de l'operation
        try:
            os.chdir(workspace)
        except:
            print("Probleme de workspace dans le moniteur")
            
        #Vidage fichiers valid_request et error
        request_file = open("./"+self.valid_request_file_name+"_"+str(self.name),"w")
        request_file.write("")
        request_file.close()
        request_file = open("./"+self.error_file_name+"_"+str(self.name),"w")
        request_file.write("")
        request_file.close()
        
        

    '''
    Ecrit des donnees dans le fichier de log 
    '''
    def writeLog(self,content):
        log_file = open("./"+self.log_file_name+"_"+str(self.name),"a") #ouverture en append
        log_file.write(str(datetime.now())+": "+content+"\n")
        log_file.close()

    '''
    Ecrit des donnees dans le fichier readme 
    '''
    def writeReadme(self,content):
        log_file = open("./"+self.campaign_info_file_name+"_"+str(self.name),"a") #ouverture en append
        log_file.write(content)
        log_file.close()
    
    '''
    Ecrit des donnees dans le fichier d'erreur   
    '''
    def writeError(self,content):
        error_file = open("./"+self.error_file_name+"_"+str(self.name),"a") #ouverture en append
        error_file.write(str(datetime.now())+": "+content+"\n")
        error_file.close()
    
    '''
    Ecrit des donnees dans le fichier des requetes valides 
    ''' 
    def writeRequest(self,content):
        request_file = open("./"+self.valid_request_file_name+"_"+str(self.name),"a") #ouverture en append
        request_file.write(content+"\n")
        request_file.close()
        
    '''
    Sauvegarde la derniere requete envoyee jusqu'a ce qu'une réponse soit reçue
    '''
    def addRequest(self,request_type,request):
        #2 valeurs possibles pour request_type:  "valid" ou "fuzz"
        self.tempType = request_type
        self.tempRequest = request
    
    '''
    Traitement de la reponse associe a la derniere requete envoyee (qui est stockee dans tempRequest
    '''
    def addResponse(self,response):
        #Si le moniteur n'est pas dans un etat de fuzzing (la derniere requete envoyee est consideree valide)
        if (self.tempType == "valid"):
            #Ajout de la requete associee dans le ficher des requetes valides
            self.writeRequest(self.tempRequest+" -> "+response)
            self.img.addResp(response)
        #Dans le cas d'un état fuzzing
        else:
            #Traitement de la réponse afin d'évaluer sa distance par rapport au centre du cercle des reponses
            self.handleResponse(self.tempRequest,response)
        
            
    '''
    Calcule le perimetre des réponses
    '''
    def computePerimeter(self):
        print("Calcul du périmètre des réponses")
        #Ouverture en lecture du fichier des requetes valides
        with open("./"+self.valid_request_file_name+"_"+str(self.name),'r') as tmp_request_file :
            #Liste temporaire des reponses valides
            responseList = []
            #Lecture de tout le fichier de requetes afin de remplir la liste
            for line in tmp_request_file :
                if (line[0:3] == " ->"):
                    #Ajout d'une réponse dans la liste (la partie de la ligne se trouvant après les caractères "->")
                    #Il faut aussi penser a enlver le retour charriot d'où le "[:-1]"
                    responseList.append(Response(line.partition("-> ")[2][:-1]))
        
        #Pour chaque requete, calcul des ratios de similitudes
        #Boucle optimisee pour ne pas faire plusieurs fois le meme calcul
        for element in responseList:
            #Stockage de l'index de l'element suivant
            nextIndex = responseList.index(element)+1
            #Pour tous les elements suivants dans la liste
            for i in range(nextIndex,len(responseList)) :
                #Calcul de la similitude entre l'element courant et responseList[i] et stockage de celui-ci
                target = responseList[i]
                self.computeDistance(element,target)               
        
        if len(responseList) != 0 :        
            #Calcul et recherche de la distance moyenne minimale i.e recherche du centre
            index_minimum = 0 #Index du minimum (par défaut a 0)
            minimum_value = 2 #Valeur du ratio minimum (initialise a une valeur superieure a la borne sup des ratios, ici 2)
            iter_value = -1 #Variable d'itération
            while iter_value < len(responseList)-1:
                iter_value += 1
                response = responseList[iter_value]
                middle = response.computeMiddle();
                if middle < minimum_value:
                    minimum_value = middle
                    index_minimum = iter_value
            #Recherche et affectation du perimetre et de la réponse centrale
            self.center = responseList[index_minimum].getResponse()
            self.perimeter = responseList[index_minimum].getMinRatio()
            #Creation des requetes valides dans l'image
            content = "* Reponse centrale de la campagne "+str(self.name)+" : "+self.center+"\n\n* Perimetre : "+str(self.perimeter)
            self.writeReadme(content)
            print("------------------")
            print(content)
            print("------------------\n")
                
    
    '''
    Calcule la distance entre une réponse et le centre du 'cercle' des reponses
    '''
    def handleResponse(self,request,response):
        #Calcul de la distance entre la reponse et le centre
        #Les caracteres " " sont ignores
        
        #print("comparaison de :\n"+str(response)+"\n"+self.center+"\n")
        s = SequenceMatcher(lambda x: x == " ",self.center,response)
        ratio = s.ratio()
        #print("comparaison de "+str(ratio)+" et de "+str(self.perimeter)+"\n")
        #Ajout de la difference pour l'image
        self.img.addResp(response)
        #Si le ratio est inférieur au périmètre i.e la reponse est en dehors du cercle de tolérance
        if ratio < self.perimeter:
            #Une erreur s'est produite
            print("/!\/!\/!\ ")
            print("Erreur serveur détéctée causée par la requête: \n"+request)
            print("/!\/!\/!\ ")
            #Copie de la reponse dans le fichier d'erreurs
            self.writeError(request+" -> "+response)
        
        #Actualisation du fichier de log
        self.writeLog(request+" -> "+response)
        
        
    
    '''
    Calcule et enregistre la distance entre 2 réponses a et b
    '''
    def computeDistance(self,a,b):
        #Les caractères " " sont ignorés (i.e junk)'''
        s = SequenceMatcher(lambda x: x == " ",a.getResponse(),b.getResponse())
        #Stockage de la mesure de similarité des 2 séquences entre 0 et 1 (1 si les séquences sont identiques)
        ratio = s.ratio()
        a.addSimilarityRatio(ratio)
        b.addSimilarityRatio(ratio)
       
     
   
class Response(object):
    '''
    Classe correspondant a l'objet resultat d'une requete
    On y stock la reponse associee a une requete ainsi que les les ratios de difference 
    entre celle-ci et toutes les autres réponses associees au meme type de requete
    ''' 
    
    '''Constructeur'''
    def __init__(self,response):
        self.response = response
        self.listRatio = []
    
    '''
    Actualisation du ratio de similitude de cet objet Reponse avec un autre dont l'index est aussi conserve.
    La fonction computePerimeter() gere le remplissage de cette liste.
    '''
    def addSimilarityRatio(self,ratio):
        self.listRatio.append(ratio)
        
    def getRatio(self):
        return self.listRatio
    #Getter sur la réponse
    def getResponse(self):
        return self.response
    
    #Calcul de la moyenne des ratios de similarite
    def computeMiddle(self):
        r = 0
        if len(self.listRatio) !=0 :
            #Variable temporaire utile au calcul de la moyenne
            tmp = 0
            for ratio in self.listRatio:
                tmp += ratio
            r = tmp/(len(self.listRatio))
        else :
            raise ZeroDivisionError
        return r
    
    
    '''Le ratio de difference entre 2 sequences est de 0 dans le cas ou elles n'ont rien en commun
     et vaut 1 si celles-ci sont identiques.'''
    
    '''Cette fonction retourne le minimum des ratios 
    i.e le ratio associé a la reponse la plus différente de celle-ci.
       Le minimum des ratio est le perimetre des réponses.
    '''
    def getMinRatio(self):
        return min(self.listRatio, key=float)
    
    def getMaxRatio(self) :   
        return max(self.listRatio, key=float)
        
            
        
         
