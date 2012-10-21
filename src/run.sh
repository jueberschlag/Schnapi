#!/bin/sh

rm -f image.ps sortie*


python3.0 description_generation.py -d ./description/http_description.xml
python3.0 schnapi.py -s localhost -p 8181 -r 50 -j 4

echo "Début execution R"
bash R --no-save < entreeR
