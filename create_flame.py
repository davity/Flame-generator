# -*- coding: utf-8 -*-
import argparse
from lxml import etree
from render import render_flame_file
from xml_generator import generate_xml_flame


parser = argparse.ArgumentParser(description='Create a flame file with a name')
parser.add_argument('name', help=u'Nombre para el archivo de flames')

args = parser.parse_args()
print('Nombre = ' + args.name)

# Data ranges, samples and variation definition
data = [
    [1, 7, 1, 'swirl'], # N - 9 + 1
    [0.1, 1.3, 8, 'julia'], # N + 0.1
    [5, 12, 1, 'sinusoidal'] # N/10
]
name = 'prueba-con-funcion'

# Pass the data to the XML-Flame generator
flames = generate_xml_flame(data, name)

# Print it to screen!
print(etree.tostring(flames, pretty_print=True))

# Save the XML .flame to a file
f = open(name + '.flame', 'w')
f.write(etree.tostring(flames, pretty_print=True))
f.close()

# Call the render function to render and process all the flames
render_flame_file(name + '.flame', name)
