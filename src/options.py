import subprocess, sys, getopt

'''Valeurs par défaut concernant le serveur distant'''
SERVER_ADDR = "localhost"
PORT = 8181
NAME = "SchnapOperation"
NUMBER = 10
INPUT_FILE = "description/description.xml"
NB_CORES = 2

def do_options_description() :
  try:
    opts, args = getopt.getopt(sys.argv[1:], "d:", ["description="])
  except getopt.GetoptError as err :
    print(str(err))
    sys.exit(2)

  input_file = None
		      
  for opt, arg in opts:
    if opt in ("-d", "--description"): input_file = arg
  
  return (input_file)


def do_options_schnapi() :
  try:
    opts, args = getopt.getopt(sys.argv[1:], "n:s:p:r:j:w", ["name=", "server=", "port=", "request_number=","nb_cores=","workspace="])
  except getopt.GetoptError as err :
    sys.exit(2)
  
  server = None
  port = None
  name = None
  request_number = None
  workspace = None
  nb_cores = None
          
  for opt, arg in opts:
    if opt in ("-s", "--server"): 
      server = arg
    elif opt in ("-p", "--port"):
      if not(isinstance(int(arg),int)):
        raise ValueError
        exit(2)
      port = arg
    # Nom de l'opération de fuzzing
    elif opt in ("-n", "--name"): name = arg
    elif opt in ("-r", "--request_number"):
      if not(isinstance(int(arg),int)):
        raise ValueError
        exit(2)
      request_number = arg
    elif opt in ("-w", "--workspace"): workspace = arg
    elif opt in ("-j", "--nb_cores"):
      if not(isinstance(int(arg),int)):
        raise ValueError
        exit(2)
      nb_cores = arg
    
  if server == None:
    server = SERVER_ADDR
  if  port == None:
    port = PORT
  if  name == None:
    name = NAME
  if  request_number == None:
    request_number = NUMBER
  if  nb_cores == None:
    nb_cores = NB_CORES
  if  workspace == None:
    stdout_file = open('/tmp/stdout.pwd', 'w+')
    pwd = subprocess.Popen('pwd',shell=True, stdout = stdout_file)
    pwd.communicate()
    stdout_file.seek(0)
    stdout = stdout_file.read()
    workspace = stdout.partition("\n")[0]

  return (server, port, name, request_number, nb_cores, workspace)
