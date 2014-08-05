# -*- coding: utf-8 -*-
import argparse
from utils import *
from numpy import arange
from lxml import etree
from render import render_flame_file


parser = argparse.ArgumentParser(description='Create a flame file with a name')
parser.add_argument('name', help=u'Nombre para el archivo de flames')

args = parser.parse_args()
print('Nombre = ' + args.name)

# Data values, ranges and variation definition
npartes = 2.0

alcoholMin = 0.26
alcoholMax = 1.09
alcoholPaso = (alcoholMax - alcoholMin) / npartes
alcoholVar = 'swirl'

acidezMin = 0.3
acidezMax = 1.8
acidezPaso = (acidezMax - acidezMin) / npartes
acidezVar = 'julia'

sulfMin = 3.4
sulfMax = 6.6
sulfPaso = (sulfMax - sulfMin) / npartes
sulfVar = 'sinusoidal'

rng_alcohol = arange(alcoholMin, alcoholMax + alcoholPaso, alcoholPaso)
rng_acidez = arange(acidezMin, acidezMax + acidezPaso, acidezPaso)
rng_sulf = arange(sulfMin, sulfMax + sulfPaso, sulfPaso)

print('rango alcohol = ' + str(rng_alcohol))
print('rango acidez = ' + str(rng_acidez))
print('rango sulfuroso = ' + str(rng_sulf))
print('')

# Create the xml for the flame file
Flames = etree.Element('Flames', name=args.name)
i = 0

for sulfuroso in rng_sulf:
    for acidez in rng_acidez:
        for alcohol in rng_alcohol:
            flame = etree.SubElement(Flames, 'flame', flame_properties(str(i)))
            xform = etree.SubElement(flame, 'xform', xform_properties(alcoholVar, alcohol, 0))
            xform = etree.SubElement(flame, 'xform', xform_properties(acidezVar, acidez, 8))
            xform = etree.SubElement(flame, 'xform', xform_properties(sulfVar, sulfuroso, 4))
            gradient = etree.SubElement(flame, 'palette', gradient_properties())
            gradient.text = gradient_content()
            i += 1
print(etree.tostring(Flames, pretty_print=True))

f = open('testing.flame', 'w')
f.write(etree.tostring(Flames, pretty_print=True))
f.close()

print('Renderizando...')
render_flame_file('testing.flame', args.name)