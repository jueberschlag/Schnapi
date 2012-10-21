'''
Created on 11 avr. 2012

@author: INSA Fuzzing


classe qui créer un fichier tex_image.tex qu'il faut compiler pour avoir une image


'''
import os
import sys
import threading
import time
from random import random, randint
from math import pow, sqrt, fabs
from difflib import SequenceMatcher
#import multiprocessing as mp
#from multiprocessing import Process, Queue, Lock, Array
import multiprocessing

'''Macros designant differents espaces de travail pour les tests'''

class image(object):
    
    def __init__(self,workspace, name, nb_cores):
        #Repertoire de travail
        self.workspace = workspace
        #Nom de l'opération de fuzzing
        self.name = name
        #Changement de répertoire, ouverture du fichier et ecriture du début du fichier latex
        os.chdir(self.workspace)
        #Liste des difference par rapport au préimetre
        self.listResp = []
        #Nombre de coeurs
        self.nb_cores = nb_cores
        
    def addResp(self,resp):
        self.listResp.append(resp)


    def calcul(self, ligneMatrice, arr):
        while True:
            if ligneMatrice.empty():
                sys.exit(0)
            ligne = ligneMatrice.get()
            d = self.listResp[ligne]
            print("Image R : ligne "+str(ligne)+" sur "+str(len(self.listResp)))
            for n1 in range(0, len(self.listResp)):
                if arr[n1*len(self.listResp)+ligne] == 0:
                    d1 = self.listResp[n1]
                    s = SequenceMatcher(lambda x: x == " ",d,d1)
                    ratio = s.ratio()
                    arr[ligne*len(self.listResp)+n1] = ratio
                    arr[n1*len(self.listResp)+ligne] = ratio 
    
    def drawFigureMulti(self):
        #Variables multi-processing safe
        ligneMatrice = multiprocessing.Queue()

        #Creation liste de listes vide
        arr = multiprocessing.Array('d',len(self.listResp)*len(self.listResp))
        
        for n1 in range(0,len(self.listResp)):
            ligneMatrice.put(n1)
        
        nb_processes = self.nb_cores
        #for all response couple 
        processes = []
        for n in range(1, nb_processes):
            process = multiprocessing.Process(target=image.calcul, args=(self, ligneMatrice, arr))
            processes.append(process)
            process.start()
        
        for n in range(1, nb_processes):
            processes[n-1].join()
        
        f = open("./sortieR_"+str(self.name), "w")
        for n1 in range(0,len(self.listResp)):
            for n2 in range(0,len(self.listResp)):
                f.write(str(arr[n1*len(self.listResp)+n2])+" ")
            f.write("\n")
        f.close()

    
    def drawFigureMono(self):
        print("Monocoeur")
        debutTime = time.time()
        #Creation liste de listes vide
        arr = []
        for n1 in range(0,len(self.listResp)):
            arr.append([])
            for n2 in range(0,len(self.listResp)):
                arr[n1].append([])
    
        #for all response couple
        longueur = len(self.listResp)	
        for n1 in range(0,longueur):
            print("Image R : ligne "+str(n1)+" sur "+str(longueur))
            for n2 in range(n1,longueur):
                #responses of index n1 and n2
                d1 = self.listResp[n1]
                d2 = self.listResp[n2]
                #Ratio
                s = SequenceMatcher(lambda x: x == " ",d1,d2)
                ratio = s.ratio()
                arr[n1][n2] = ratio
                arr[n2][n1] = ratio

        finTime = time.time()
        diffTime = finTime - debutTime
        difftuple = time.gmtime(diffTime)
        print("Executé en "+str(difftuple.tm_min)+" min et "+str(difftuple.tm_sec)+" sec")

        f = open("./sortieR_"+str(self.name), "w")
        for n1 in range(0,len(arr)):
            for n2 in range(0,len(arr)):
                f.write(str(arr[n1][n2])+" ")
            f.write("\n")
        f.close()	  

  
    def fin(self):
        if self.nb_cores > 1:
            self.drawFigureMulti()
        else:
            self.drawFigureMono()

