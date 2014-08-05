# -*- coding: utf-8 -*-
from utils import *

print('Testing position(pos) function...')
print(position(0) == '1 0 0 1 -1 1' and position(4) == '1 0 0 1 0 0')
print
print('Testing flame_properties("a-random-flame")...')
defs = {'name': "a-random-flame",
        # A bunch of nice defaults
        'version': 'Apophisis 2.09',
        'size': '640 480',
        'center': '0 0',
        'scale': '25',
        'filter': '0.5',
        'quality': '50',
        'background': '0 0 0',
        'brightness': '4',
        'gamma': '4',
        'gamma_threshold': '0.04'}
print(flame_properties("a-random-flame") == defs)
print
print('Testing xform_properties("pinneaple", 54, 6)...')
defs = {'weight': '0.5', 'color': '0', 'coefs': position(6), "pinneaple": str(54)}
print(xform_properties("pinneaple", 54, 6) == defs)