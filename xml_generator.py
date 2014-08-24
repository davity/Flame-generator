# -*- coding: utf-8 -*-
from utils import *
from numpy import linspace
from lxml import etree
from itertools import product


def generate_xml_flame(variation_values, variation_names, parameter_names, batch_name, output_path='./output/'):
    """
    Recibe varias listas: valores de las variaciones, nombres de las var., nombres de los params, nombre del lote y
    devuelve un objeto etree con el XML generado

    :param data_list: lista de listas
    :param batch_name: nombre del archivo de flames
    :return: etree
    """

    # Crear el árbol XML para el archivo .flame
    # raíz
    flames = etree.Element('Flames', name=batch_name)
    for i, range_tuple in enumerate(variation_values):
        # flame hijo
        flame = etree.SubElement(flames, 'flame', flame_properties(str(i)))

        # Obtener colores de las transformadas
        tcolors = list(linspace(0, 1, len(range_tuple)))

        for j, value in enumerate(range_tuple):
            # transformada hija (triangulo en apophysis)
            xform = etree.SubElement(flame, 'xform', xform_properties(variation_names[j], value, j, parameter_names[j], tcolors[j]))

        # Añadir un gradiente fijo por defecto
        # flame = add_gradient_apophysis(flame)
        flame = add_gradient_fr0st(flame)

    # Save the XML .flame to a file with _mod to indicate the real_name parameter modification
    flame_file = output_path + batch_name + '/' + batch_name + '_mod.flame'
    create_dir(output_path + batch_name)
    f = open(flame_file, 'w')
    f.write(etree.tostring(flames, pretty_print=True))
    f.close()

    # Save another flame without the real_name parameter (a pure .flame file)
    replace_in_file(r'real_name="[^"]*"', flame_file, output_path + batch_name + '/' + batch_name + '.flame')

    return flames
