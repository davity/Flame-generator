# -*- coding: utf-8 -*-
import os
from lxml import etree
import re
import csv
from numpy import interp


def create_dir(dirname):
    u"""
    Dada una ruta, comprueba si existe y si no crea las carpetas que falten en la ruta
    :param dirname: nombre de la carpeta o ruta
    :return: True si se ha creado, False si ya existe.
    """
    if not os.path.exists(dirname):
        print('Creando directorio "' + dirname + '"')
        os.makedirs(dirname)
        return True
    else:
        # print('Directorio "' + dirname + '" ya existe, no se hace nada')
        return False


def delete_in_file(regexp, input_path, output_path):
    u"""
    Elimina una cadenad dada por una expresión regular en un archivo
    y guarda el resultado en otro archivo.
    :param regexp: Expresión regular a buscar
    :param input_path: Ruta y nombre del archivo a buscar
    :param output_path: Ruta y nombre del archivo a guardar
    :return:
    """
    input_file = open(input_path, 'r')
    out = open(output_path, 'w')

    for line in input_file:
        out.write(re.sub(regexp, '', line))
    input_file.close()
    out.close()


def read_csv_data(file_path):
    u"""
    Lee de un fichero cvs los datos de los vinos que se desean representar.
    Cada fila del archivo debe corresponder a un vino.
    Cada columna del archivo corresponderá al peso de la variación correspondiente

    Cada fila se convierte en una tupla y se sustituyen las comas por puntos (estilo
    ingles de coma flotante)

    :param file_path: Ruta del fichero csv
    :return: list
    """
    f = open(file_path)
    reader = csv.reader(f, delimiter=';')

    values = []
    for row in reader:
        v = []
        for i, value in enumerate(row):
            v.append(float(value.replace(',', '.')))
        values.append(tuple(v))

    return values


def map_data(data, origin_ranges, tarjet_ranges):
    u"""
    Mapea una lista de tuplas a los rangos provistos dos listas de
    tuplas origin_ranges y tarjet_ranges.

    Cada elemento de cada tupla en los datos de entrada se mapeara utilizando
    las tuplas de rangos correspondiente a la posición del dato en la tupla.
    Así dato[0][0] utilizará para el mapeo origin_ranges[0] y tarjet_ranges[0],
    dato[0][1] utilizará origin_ranges[1] y tarjet_ranges[1], etc.

    Ejemplo
    --------
    >>> origin_ranges = ((1, 10), (1, 100))
    >>> tarjet_ragnes = ((10, 100), (100, 10000))
    >>> data = [(3, 15), (7, 55)]
    >>> map_data(data, origin_ranges, tarjet_ragnes)
    [(30.0, 1500.0), (70.0, 5500.0)]
    """

    morph = []
    for t in data:
        tmp = []
        for i, n in enumerate(t):
            tmp.append(interp(n, origin_ranges[i], tarjet_ranges[i]))
        morph.append(tuple(tmp))
    return morph


def position(pos):
    u"""
    Devuelve unas coordenadas (X,Y) en base a unas posiciones predefinidas. Estas se
    usaran para posicionar las transformaciones del flame (triángulos de Apophysis).

    Coordenadas de las posiciones
    (-1,-1)---(0,-1)---(1,-1)
        |        |        |
        |        |        |
    (-1, 0)---(0, 0)---(1, 0)
        |        |        |
        |        |        |
    (-1, 1)---(0, 1)---(1, 1)

    Notar que la coordenada Y está "invertida": los valores positivos se encuentran en
    el eje inferior. Este es el modo de almacenar las coordenadas en un archivo .flame,
     aunque en Apophysis se muestren con los valores positivos en el eje superior.

    Números de posición (elegidos sin seguir ningún patrón concreto)
    3 --- 5 --- 1
    |     |     |
    6 --- 2 --- 7
    |     |     |
    0 --- 8 --- 4

    :param pos: int
    :return: cadena con posiciones para parametro coefs de xform
    """
    # Definir las posibles posiciones de las transformadas
    positions = (
        (-1, 1),
        (1, -1),
        (0, 0),
        (-1, -1),
        (1, 1),
        (0, -1),
        (-1, 0),
        (1, 0),
        (0, 1)
    )
    return '1 0 0 1 ' + str(positions[pos][0]) + ' ' + str(positions[pos][1])


def flame_properties(name):
    u"""
    Devuelve un diccionario con los parámetros
    necesarios para un nodo flame de un XML .flame

    :param name: Nombre del flame
    :return: diccionario
    """
    return {'name': name,
            # A bunch of nice defaults
            'version': 'Apophisis 2.09',
            'size': '640 480',
            'center': '0 0',
            'scale': '51.2',  # 6.4 * value
            'zoom': '1',
            'oversample': '1',
            'filter': '0.5',
            'quality': '10',
            'background': '0 0 0',
            'brightness': '4',
            'gamma': '4',
            'gamma_threshold': '0.04'  # 0.04 * value
    }


def xform_properties(variation_name, variation_value, pos, real_name, color_pos):
    u"""
    Dados unos datos, devuelve un diccionario con los parametros para una
    transformada (xform) que incluyen dichos datos y otros por defecto

    :param variation_name: Nombre de la variación. Debe coincidir con uno de los
                           disponibles en el algoritmo flam3
    :param variation_value: Peso de la variación
    :param pos: Posición del origen de la transformada. Consultar función 'position'
                para más detalles.
    :param color_pos: Posición del color para la transformada
    :return: dictionary
    """
    new_xform = {'weight': '0.5', 'color': str("{:.2f}".format(color_pos)),
                 'coefs': position(pos), variation_name: str(variation_value),
                 'real_name': real_name}
    return new_xform


def add_gradient_apophysis(etree_element):
    u"""
    Devuelve un elemento etree con un gradiente con el formato de Apophysis
    """

    gradient_text = '''
        000764010967020C69020E6C03116E041371051673051876
        061B78071D7B081F7D0922800924820A27850B29870C2C8A
        ... 28 líneas intermedias omitidas por brevedad ...
        00053900053B00053E00054100054400064600064900064C
        00064E00065100065400065600065900075C00075F000761
        '''

    gradient_properties = {'count': '256', 'format': 'RGB'}

    gradient = etree.Element('palette', gradient_properties)
    gradient.text = gradient_text
    etree_element.append(gradient)

    return etree_element


def add_gradient_fr0st(etree_element):
    u"""
    Devuelve un elemento etree con un gradiente con el formato de Fr0st
    """

    gradient_text = """<color index="0" rgb="253 172 7"/>
    <color index="1" rgb="254 170 2"/>
    <color index="2" rgb="253 168 0"/>
    <... 251 líneas intermedias omitidas por brevedad .../>
    <color index="254" rgb="253 175 16"/>
    <color index="255" rgb="253 173 11"/>"""

    gradient_elements = gradient_text.split('\n')
    for e in gradient_elements:
        etree_element.append(etree.fromstring(e))

    return etree_element
