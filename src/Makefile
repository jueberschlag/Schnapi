all : param_generator

param_generator  : 
	make -C description all

test: description/param_generator.py
	python3.0 description/param_generator.py
	python3.0 description/param_generator.py 10 20
	python3.0 description/param_generator.py 20 40
	python3.0 description/param_generator.py 30

clean: 
	make -C description clean
