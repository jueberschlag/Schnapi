all : description

description : http_description.xml description_to_python.xsl
	xsltproc description_to_python.xsl http_description.xml > param_generator.py

clean:
	rm -f param_generator.py

