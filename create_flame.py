# -*- coding: utf-8 -*-
import argparse
from utils import *
from numpy import arange
from lxml import etree
from render import render_flame_file
from itertools import product

parser = argparse.ArgumentParser(description='Create a flame file with a name')
parser.add_argument('name', help=u'Nombre para el archivo de flames')

args = parser.parse_args()
print('Nombre = ' + args.name)

# Data values, ranges and variation definition
npartes = 2.0
variation_names = []

alcoholMin = 0.26
alcoholMax = 1.09
alcoholPaso = (alcoholMax - alcoholMin) / npartes
variation_names.append('swirl')

acidezMin = 0.3
acidezMax = 1.8
acidezPaso = (acidezMax - acidezMin) / npartes
variation_names.append('julia')

sulfMin = 3.4
sulfMax = 6.6
sulfPaso = (sulfMax - sulfMin) / npartes
variation_names.append('sinusoidal')

# Get all the ranges and convert them to a list to avoid precision errors
rng_alcohol = arange(alcoholMin, alcoholMax + alcoholPaso, alcoholPaso).tolist()
rng_acidez = arange(acidezMin, acidezMax + acidezPaso, acidezPaso).tolist()
rng_sulf = arange(sulfMin, sulfMax + sulfPaso, sulfPaso).tolist()

print('rango alcohol = ' + str(rng_alcohol))
print('rango acidez = ' + str(rng_acidez))
print('rango sulfuroso = ' + str(rng_sulf))
print('')

# Create the xml for the flame file:
# Get all the combinations for the ranges
data = list(product(rng_alcohol, rng_acidez, rng_sulf))
print('data = ' + str(data))

# Create the XML tree for the .flame file
# root
Flames = etree.Element('Flames', name=args.name)
i = 0
for flame_tuple in data:
    # flame child
    flame = etree.SubElement(Flames, 'flame', flame_properties(str(i)))
    i += 1

    for i, value in enumerate(flame_tuple):
        # transform child (triangles in apophysis)
        xform = etree.SubElement(flame, 'xform', xform_properties(variation_names[i], value, 0))

    # And add a default gradient
    gradient = etree.SubElement(flame, 'palette', gradient_properties())
    gradient.text = gradient_content()

# Print it to screen!
print(etree.tostring(Flames, pretty_print=True))

# Save the XML .flame to a file
f = open('testing.flame', 'w')
f.write(etree.tostring(Flames, pretty_print=True))
f.close()

# Call the render function to render and process all the flames
render_flame_file('testing.flame', args.name)
