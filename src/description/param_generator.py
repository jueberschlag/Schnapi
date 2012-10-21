import sys
sys.path.append('./fuzzerlib/')
import string
import random
from protolib import *
from fuzzerlib.fuzzerlib import *
def preambule():
	init()
def main(args):
	r = request_generator(args)
	print_request2(*r)
def request_generator(args):
	r = []
	tuple_list = args
	r += [methods(tuple_list, is_fuzz_requested(tuple_list, "1"))]
	r += [' ']
	r += [urls(tuple_list, is_fuzz_requested(tuple_list, "2"))]
	r += [' ']
	r += [versions(tuple_list, is_fuzz_requested(tuple_list, "3"))]
	r += ['\n']
	return r
def methods(tuple_list, fuzz):
	context = []
	r = []
	l = None
	d = None
	i = None
	if fuzz:
		r += [[abnfgen_method()]]
	else : 
		context.append(l)
		l = []
		context.append(r)
		r = []
		r += ['POST']
		r += ['DELETE']
		r += ['GET']
		r += ['HEAD']
		r += ['OPTIONS']
		r += ['PUT']
		r += ['TRACE']
		l = r
		r = context.pop()
		r += [l]
		l = context.pop()
		l = r[len(r)-1]
		r[len(r)-1] = []
		element_done = []
		for i in range(1) :
			e = random.choice(l)
			while (e in element_done): 
				e = random.choice(l)
			r[len(r)-1] += [e]
			element_done.append(e)

	return r
def urls(tuple_list, fuzz):
	context = []
	r = []
	l = None
	d = None
	i = None
	if fuzz:
		r += [[abnfgen_path()]]
	else : 
		context.append(l)
		l = []
		context.append(r)
		r = []
		r += ['/']
		r += ['/index.html']
		l = r
		r = context.pop()
		r += [l]
		l = context.pop()
		l = r[len(r)-1]
		r[len(r)-1] = []
		element_done = []
		for i in range(1) :
			e = random.choice(l)
			while (e in element_done): 
				e = random.choice(l)
			r[len(r)-1] += [e]
			element_done.append(e)

	return r
def versions(tuple_list, fuzz):
	context = []
	r = []
	l = None
	d = None
	i = None
	if fuzz:
		r += [[abnfgen_version()]]
	else : 
		context.append(l)
		l = []
		context.append(r)
		r = []
		r += ['HTTP/1.0']
		r += ['HTTP/1.1']
		r += ['HTTP/0.9']
		l = r
		r = context.pop()
		r += [l]
		l = context.pop()
		l = r[len(r)-1]
		r[len(r)-1] = []
		element_done = []
		for i in range(1) :
			e = random.choice(l)
			while (e in element_done): 
				e = random.choice(l)
			r[len(r)-1] += [e]
			element_done.append(e)

	return r
def postambule():
	pass
	deinit()
def params_availabled():
	r = []
	r.append("1")
	r.append("2")
	r.append("3")
	return r
if __name__ == "__main__":
	main(sys.argv[1:])
