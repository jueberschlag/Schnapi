#!/bin/sh

rm -f image.ps sortie*

cp description/http_description.xml description/http_description.xml.backup
cp description/http_description_simplify.xml description/http_description.xml

make

mkdir tmp
cp in.grammar_* tmp/.
cp in.grammar/* .

python3.0 description_generation.py -d ./description/http_description_simplify.xml
python3.0 schnapi.py -s localhost -p 8181 -r 100 -j 4

cp tmp/* .

cat log_file_SchnapOperation | grep --color=auto "text/txt"
