# -*- coding: utf-8 -*-
from utils import *
from numpy import arange
from lxml import etree
from itertools import product


def generate_xml_flame(data_list, file_name):
    """
    Recibe una lista con la siguiente estructura:

        [ [min1, max1, samples1, variation_name1], [min1, max1, samples1, variation_name1], ...]

    Donde los elementos de cada sublista son:
        min: El mínimo del rango. Puede ser de tipo float.
        max: El Máximo del rango. Puede ser de tipo float.
        samples: Número de partes iguales en las que debe dividirse el rango. Should be an integer.
        variation_name: Nombre de la variación a aplicar a la transformada (ex: linear, sinusoidal, swirl...).
                        Debe ser una cadena.

    Devuelve un objeto etree con el XML generado

    :param data_list: lista de listas
    :param file_name: nombre del archivo de flames
    :return: etree
    """

    ranges = []  # Lista de todos los rangos
    variation_names = []  # Lista de todas los nombres de las variaciones
    parameter_names = []  # Lista de todos los parámetros (de la vida real) a los que se corresponde la variacion

    # Procesar la lista de datos
    for element in data_list:
        # Obtener el rango de los datos para el elemento actual
        # definicion de variables por claridad, puede omitirse
        minimum = element[0]
        maximum = element[1]
        samples = element[2]
        var_name = element[3]
        param_name = element[4]

        step = (maximum - minimum) / float(samples)  # Calcular el paso para la funcion arange
        ranges.append(arange(minimum, maximum, step).tolist())

        # Copiar el nombre de la variación y el parámetro a otras dos listas
        variation_names.append(var_name)
        parameter_names.append(param_name)

    all_ranges = list(product(*ranges))
    print('data = ' + str(all_ranges))

    # Crear el árbol XML para el archivo .flame
    # raíz
    flames = etree.Element('Flames', name=file_name)
    i = 0
    for range_tuple in all_ranges:
        # flame hijo
        flame = etree.SubElement(flames, 'flame', flame_properties(str(i)))
        i += 1

        for i, value in enumerate(range_tuple):
            # transformada hija (triangulo en apophysis)
            xform = etree.SubElement(flame, 'xform', xform_properties(variation_names[i], value, i, parameter_names[i]))

        # Añadir un gradiente fijo por defecto
        gradient = etree.SubElement(flame, 'palette', gradient_properties())
        gradient.text = gradient_content()

    return flames