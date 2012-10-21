# -*- coding: utf-8 -*-

"""
Created on 13 fevr. 2012

@author:    Florian Fougeanet
            Carla Sauvanaud
            Jereme Ueberschlag
"""
import sys
sys.path.append('./../description/')
import urllib
import random
from http_EnumType import *


'''Set de caractères unicode'''
MIN = set('abcdefghijklmnopqrstuvwxyz')
MAJ = set('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
NUM = set('0123456789')
'''W3school : URLs can only be sent over the Internet using the ASCII character-set.'''
SPEC = set(' .,-_;?!:(){}[]<>\'\`"/\\&$%#*+=@')


def nameGenerator(length):
    """
    Generateur d'un string d'une longueur passee en parametre
    """
    '''Union des set contenant les caracteres autorises pour les noms de fichiers.
    En théorie tous les caractères peuvent être utilisés mais certains sont à éviter
    Il est possible de fuzzer avec des noms de fichiers douteux dans la suite du projet'''
    charset = MAJ | MIN | NUM | set('_')
    res = ''
    for i in range(length) :
        #cast du set en list pour la fonction choice()
        res += random.choice(list(charset))
    return res
    
    
def fuzzHTMLpathGenerator():
    '''Générateur d'un chemin (1 directory) vers un fichier HTML'''
    res = ''
    n = random.randint(1,3)
    for i in range(n) :
        res += '/'+nameGenerator(random.randint(5,10))
    return res+'.html'


def validHTMLpathGenerator():
    '''Pour l'instant 1 path valide sur le serveur'''
    return 'index.html'


def protocolVersionGenerator(n):
    return random.randint(0,n)+'.'+random.randint(0,n)


def protocolGenerator(n,m):
    return nameGenerator(n)+'/'+protocolVersionGenerator(m)


def portGenerator(length):
    return random.randint(0,length)


def requestGenerator(n):
    '''Generateur d une requete HTTP en faisant du fuzzing sur le n-eme champ.
    Pour l'instant il n'y a que 3 cas : 1->1er champ, 2->2eme champ, 3->les 2 premiers champs.'''
    
    requete =''
    #Cas du fuzz de la Methode
    if n == 1 : 
        requete += nameGenerator(6)+"/ "
        requete += validHTMLpathGenerator()
    
    #Fuzz du chemin vers un fichier html
    elif n == 2 :
        #Ajout d'un champ de methode valide
        requete += random.choice(httpEnumType.METHODlist)+"/ "
        requete += fuzzHTMLpathGenerator()
     
    #Fuzz sur les champs Methode et Path   
    elif n == 3 :
        requete += nameGenerator(6)+"/ "
        requete += fuzzHTMLpathGenerator()
    
    else :
        raise NotImplementedError

    return requete

def parseURI(uri): 
    """Parse URI, return (host, porimport sys
sys.path.append('./../fuzzerlib/')t, selector)."""
    
    scheme, netlocation, selector, query, fragmentid = urllib.parse.urlsplit(uri)

    if ':' in netlocation: 
        host, port = netlocation.split(':', 2)
        port = int(port)
    else: host, port = netlocation, 80
    if query: selector += '?' + query
    return host, port, selector

"""
'''Test des fonctions précédentes'''
j = 0
while j < 4 :
    print(fuzzHTMLpathGenerator())
    print(requeteGenerator(1))
    print(requeteGenerator(2))
    print(requeteGenerator(3))
    j += 1
"""

if __name__ == "__main__":
    print(requestGenerator(3))
    
