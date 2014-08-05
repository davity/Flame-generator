# -*- coding: utf-8 -*-
from lxml import etree
from setuptools.command.easy_install import easy_install
from xlrd import open_workbook


class Flame:
    """" General individual flame class """
    name = None
    # Some good defaults
    version = 'Apophisis 2.09'
    size = '640 480'
    center = '0 0'
    scale = '25'
    oversample = '1'
    filter = '0.5'
    quality = '50'
    background = '0 0 0'
    brightness = '4'
    gamma = '4'
    gamma_threshold = '0.04'

    def __init__(self, name):
        self.name = name

    def getProperties(self):
        return {
                    'name': str(self.name),
                    'version': 'Apophisis 2.09',
                    'size': '640 480',
                    'center': '0 0',
                    'scale': '25',
                    'oversample': '1',
                    'filter': '0.5',
                    'quality': '50',
                    'background': '0 0 0',
                    'brightness': '4',
                    'gamma': '4',
                    'gamma_threshold': '0.04'
                }

    def to_xml(self):
        etree.Element('Flame')

# Open excel file
wb = open_workbook('RecopilacionDatos.xls')
# Open the excel sheet
s = wb.sheet_by_name('Hoja3')
# Create XML root Flame with the name
AFlame = etree.Element('Flame', name='Prueba000')

# Fill the Flame file with various flames
for i, row in enumerate(range(s.nrows)):
    values = []
    for i, col in enumerate(range(s.ncols)):
        values.append(s.cell(row, col).value)
    print(values)
print('Tipo: ', type(values))
print('Cant: ', values.__len__())

f = Flame('mi-flame-molon')
print(f.getProperties())
s = {'oversample': '1', 'background': '0 0 0', 'gamma_threshold': '0.04', 'quality': '50', 'center': '0 0', 'scale': '25', 'name': 'mi-flame-molon', 'brightness': '4', 'filter': '0.5', 'version': 'Apophisis 2.09', 'size': '640 480', 'gamma': '4'}

sub = etree.SubElement(AFlame, 'flame', {'oversample': '1', 'background': '0 0 0', 'gamma_threshold': '0.04', 'quality': '50', 'center': '0 0', 'scale': '25', 'name': 'mi-flame-molon', 'brightness': '4', 'filter': '0.5', 'version': 'Apophisis 2.09', 'size': '640 480', 'gamma': '4'})
etree.SubElement(sub, 'xform')
print(etree.tostring(AFlame, pretty_print=True))