# -*- coding: utf-8 -*-
'''
Created on 22 fevr. 2012

@author:    Florian Fougeanet
            Carla Sauvanaud
            Jereme Ueberschlag
'''

import random
import os.path

#Classe testée

class ByteSwap(object):
    '''
    Classe inversant les octects d'un fichier.
    '''

    def __init__(self, nb, file, new_name):
        self.nb_of_bytes = nb
        self.main_file = file
        self.new_name = new_name


    def byteSwap(self):
        """Swap n times nb bytes of the file
            n = the size of the file
        """
        
        with open(self.main_file,'r') as f :
            byte =[]
            size = os.path.getsize(self.main_file)
            for i in range(size) :
                byte.append(f.read(self.nb_of_bytes))
            
            for i in range(size) :
                r1 = random.randint(0,size-1)
                r2 = random.randint(0,size-1)
                byte[r1],byte[r2] = byte[r2], byte[r1]
        
        if not self.exists('./'+self.new_name) :
            with open(self.new_name,'w') as new_file :
                for item in byte :
                    new_file.write(item)
        else :
            raise NameError('File name : %s already exists.' % self.new_name)
       
    
    def exists(self,path):
        return os.path.isfile(path)
    
    
"""   
'''Test de la fonction byteSwap'''
if __name__ == "__main__":
    b = ByteSwap(1,'parse.py','parseSwaped.py')
    b.byteSwap()
"""
