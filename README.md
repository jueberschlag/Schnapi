Schnapi
=======

Fuzzer developped for a school project.
Take a protocol description (http in our example) to fuzz it.

To generate the parameter-generation class you have to use the following command
  python description_generation.py

Option :
-d : link to the protocol description

Once the parameter-generation class is generated you can launch schnappy like that
	python schnapi.py

Options :
-n : name of the fuzzing campaign
-s : server address
-p : port number to use
-r : number of fuzzing request send to the server
-j : number of core to use

Note : For the first use of Schanpi the class generation with -d option is required. This will generate the module param_generator.py which depends on the xml description of the protocol.