import random
from protolib import *
import urllib.request
import string
import subprocess
import binascii


'''Macros de nom de fichiers'''
PATH_FILE = "in.grammar_path"
METHOD_FILE = "in.grammar_method"
STRING_FILE = "in.grammar_string"
VERSION_FILE = "in.grammar_version"

"""
  Genere un string de taille controlee

  @param minlen Longueur minimale du string resultat
  @param maxlen Longueur maximale du strnig resultat
  @param chars Sequence de caractere que peut contenir le string resultat
  @result string de longueur n comprise entre minlen et maxlen determinee pseudo-aleatoirement
"""

def string_generator(minlen, maxlen, chars):
  n = random.randint(minlen, maxlen)
  return urllib.request.pathname2url(''.join(random.choice(chars) for x in range(n)))

"""
  Genere aleatoirement un path 

  @return Un string de la forme [a-zA-Z](/[a-zA-Z])*
"""
def abnfgen_path():
  stdout_file = open('/tmp/stdout.grammar_path', 'w+')
  abnfgen = subprocess.Popen(['abnfgen '+PATH_FILE],shell=True,stdout=stdout_file)
  abnfgen.communicate()
  stdout_file.seek(0)
  stdout = stdout_file.read()
  return stdout

"""
  Genere aleatoirement un string 

  @return Un string de la forme ALPHA(/ALPHA)*
"""
def abnfgen_string():
  stdout_file = open('/tmp/stdout.grammar_string', 'w+')
  abnfgen = subprocess.Popen(['abnfgen '+STRING_FILE],shell=True,stdout=stdout_file)
  abnfgen.communicate()
  stdout_file.seek(0)
  stdout = stdout_file.read()
  return stdout

"""
  Genere aleatoirement un string 

  @return Un string de la forme donne dans in.grammar_version
"""
def abnfgen_version():
  stdout_file = open('/tmp/stdout.grammar_version', 'w+')
  abnfgen = subprocess.Popen(['abnfgen '+VERSION_FILE],shell=True,stdout=stdout_file)
  abnfgen.communicate()
  stdout_file.seek(0)
  stdout = stdout_file.read()
  return stdout

"""
  Genere aleatoirement une methode 

  @return Un string de la forme correspondant à une regexp
    contenue dans in.grammar_method
"""
def abnfgen_method():
  stdout_file = open('/tmp/stdout.grammar_method', 'w+')
  abnfgen = subprocess.Popen(['abnfgen '+METHOD_FILE],shell=True,stdout=stdout_file)
  abnfgen.communicate()
  stdout_file.seek(0)
  stdout = stdout_file.read()
  return stdout

# def transform_to_final_form(tab):
#   if len(tab[0]) == 1:
#     r = str(tab[0][0])
#   else:
#     r = str()
#     for i in range(len(tab[0])):
#       r += str(tab[0][i]) + "\n"
#   return r

def is_fuzz_requested(tuple_list, id):   
    list_id = []
    
    list_id.append(id)
    
    finish = False;
    while not(finish):
        last_index = id.rfind(".")
        list_id.append(id[:last_index+1] + "*")
        id = id[:last_index]
        if last_index == -1:
            finish = True
                
    for i in list_id:
        if i in tuple_list:
            return True
   
    return False

def transform_to_request(request):
        res = str()

        if isinstance(request, str):
                return request
        else:
                for req in request:
                        res += transform_to_request(req)
        return res

