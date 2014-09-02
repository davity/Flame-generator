# -*- coding: utf-8 -*-
import os
import random
from numpy import linspace
from itertools import product
from render import render_flame_file
from render import process_output_images
from render import render_flame_web
from render import render_web_index
from xml_generator import generate_xml_flame
from utils import read_csv_data, map_data


def generate_batch_data(data):
    u"""
    Genera un diccionario con la información para crear un lote de flames

    Recibe una lista con la siguiente estructura:

        [ [min1, max1, samples1, var_name1, param_name1],
          [min2, max2, samples2, var_name2, param_name2],
          ... ]

    Donde los elementos de cada sublista son:
        min:        Mínimo del rango del parámetro. Puede ser de tipo float.
        max:        Máximo del rango del parámetro. Puede ser de tipo float.
        samples:    Número de partes iguales en las que dividir el rango.
        var_name:   Nombre de la variación (ex: linear, sinusoidal, swirl...). Cadena.
        param_name: Nombre descriptivo del parámetro. Debe ser una cadena.

    :param data: list
    :return: dict
    """

    ranges = []             # Lista de todos los rangos
    variation_names = []    # Lista de todas los nombres de las variaciones
    parameter_names = []    # Lista de los nombres de los parámetros (de la vida real)

    # Procesar la lista de datos
    for element in data:
        # definicion de variables por claridad, puede omitirse
        minimum = element[0]
        maximum = element[1]
        samples = element[2]
        var_name = element[3]
        param_name = element[4]

        # Muestras de valores dentro del rango actual
        ranges.append(linspace(minimum, maximum, samples))

        # Copiar el nombre de la variación y del parámetro a otras dos listas
        variation_names.append(var_name)
        parameter_names.append(param_name)

    all_values = list(product(*ranges))

    return {'var_values': all_values, 'var_names': variation_names, 'param_names': parameter_names}

def create_batch(batch_name, data, output_path='./output/', render_html_index=True):
    u"""
    Crea los archivos .flame, los renderiza, crea un html con
    las imágenes y actualiza el índice de lotes.

    El diccionario en data debe tener el siguiente formato:
    {
      'var_values': [(v1, v2, v3), (v1, v2, v3), ...]      # Valores de las variaciones
      'var_names': ['nombre_v1', 'nombre_v2', 'nombre_v3'] # Nombres de las variaciones
      'param_names': ['param1', 'param2', 'param3']        # Nombres de los parámetros
    }

    :param batch_name: Nombre del lote. Se usará para la carpeta, el html y los .flame
    :param data: Diccionario
    :param output_path: Cadena con el directorio de salida.
                        Incluir el caracter '/' al final
    :param render_html_index: Indica si se debe renderizar el índice de lotes en la
                              carpeta designada por output_path
    :return: Éxito (boolean)
    """

    # Evitamos sobreescribir el lote si existe
    if os.path.isdir(output_path + batch_name):
        print(u"""
        ¡ATENCION!
        Ya existe un lote con ese nombre (""" + batch_name + u""").
        Elimínelo o renómbrelo y vuelva a ejecutar el creador de lotes.
        """)
        return False

    # Pasar la información al generador de flames
    generate_xml_flame(data['var_values'], data['var_names'], data['param_names'], batch_name, output_path=output_path)

    # Llamar al render flam3
    render_flame_file(batch_name, output_path=output_path)

    # Añadir a cada imagen generada un pie de imagen con la información
    process_output_images(batch_name, output_path=output_path)

    # Crear un archivo html sencillo que contenga todas las imágenes generadas
    render_flame_web(batch_name, output_path=output_path)

    # Crear un índice para mostrar todos los lotes existentes y un enlace a ellos
    if render_html_index: render_web_index(output_path=output_path)
    return True


def create_comparison_batch(batch_name, data,
                            output_path='./output/', render_html_index=True):
    u"""
    Básicamente igual que create_batch, pero los datos de entradas se pasan
    previamente por generate_batch_data y deben tener el siguiente formato:

        [
            [min1, max1, samples1, var_name1, param_name1],
            [min2, max2, samples2, var_name2, param_name2],
            ...
        ]

    con una sub-lista por cada transformada.

    :param batch_name: Nombre del lote. Se usará para la carpeta, el html y los .flame
    :param data: lista de listas
    :param output_path: Cadena con el directorio de salida. Incluir '/' al final
    :param render_html_index: Indica si se debe renderizar el índice de lotes
                              en la carpeta designada por output_path
    :return: Éxito (boolean)
    """
    create_batch(batch_name, generate_batch_data(data), output_path=output_path, render_html_index=render_html_index)


def create_random_batches(quantity, variations=3, sequence_name='Random',
                          sequence_start=0, output_path='./output/'):
    u"""
    Crea un conjunto de lotes eligiendo variaciones y parámetros al azar
    con pesos fijos de 0.5 para cada variación

    :param quantity: Número de lotes a crear
    :param variations: Número de variaciones/transformadas por lote
    :param sequence_start: Número de secuencia inicial del lote
    :param output_path: Directorio de salida
    :return: Éxito (boolean)
    """
    def choose_n(var_list, n):
        v = []
        while len(v) < n:
            t = random.choice(var_list)
            if not t in v:
                v.append(t)
        return v

    # Variaciones disponibles en flam3
    affine_vars = ['linear', 'sinusoidal', 'spherical', 'swirl', 'horseshoe', 'polar',
                   'handkerchief', 'heart', 'disc','spiral', 'hyperbolic', 'diamond',
                   'ex', 'julia', 'bent', 'waves', 'fisheye', 'popcorn', 'exponential',
                   'power', 'cosine', 'rings', 'fan', 'eyefish', 'bubble', 'cylinder',
                   'noise', 'blur', 'gaussian_blur', 'arch', 'tangent', 'square',
                   'rays', 'blade', 'secant2', 'twintrian', 'cross']
    parametric_vars = ['blob', 'pdj', 'fan2', 'rings2', 'perspective', 'julian',
                       'juliascope', 'radial_blur', 'pie', 'ngon', 'curl','rectangles']

    # Parámetros a escoger
    params = [u'Grado Alcohólico', u'Acidez Total', u'Acidez Volátil',u'PH',
              u'Sulfuroso Total', u'Sulfuroso Libre']

    # Evitamos sobreescribir lotes ya existentes
    if os.path.isdir(output_path + sequence_name + ' ' + '%03d' % sequence_start):
        print(u"""
        ¡ATENCION!
        Ya existe una o más carpetas con ese nombre (Random %03d).
        Elimínela o renómbrela y vuelva a ejecutar el creador de lotes.
        """ % sequence_start)
        return False

    for batch_no in range(quantity):
        data = []
        for i, xform in enumerate(range(variations)):
            choosen_vars = choose_n(affine_vars, variations)
            data.append([0.5, 0.5, 1, choosen_vars[i], random.choice(params)])

        batch_data = generate_batch_data(data)
        batch_name = sequence_name + ' ' + str("%03d" % (sequence_start + batch_no))

        print('Creando lote de flames: ' + str((batch_no + 1)) + '/' + str(quantity))
        create_batch(batch_name, batch_data, output_path=output_path,
                     render_html_index=False)

    render_web_index(output_path=output_path)
    return True


def render_csv_file(file_path, batch_name, data_alt_dict=None, output_path='./output/',
                    map_origin_ranges=None, map_tarjet_ranges=None):
    u"""
    Genera un lote de flames a partir de los valores de un archivo csv.

    Existe la posibilidad de mapear la información de entrada de un rango de valores
    a otro mediante los parámetros map_data, map_origin_ranges y map_tarjet_ranges.
    Consultar función map_data en utils.py para más información.

    :param file_path: ruta a archivo csv
    :param batch_name: cadena
    :param data_alt_dict: diccionario con var_names y param_names alternativos
    :param output_path: directorio de salida
    :param map_origin_ranges: lista de tuplas con rangos de origen de cada parámametro
    :param map_tarjet_ranges: lista de tuplas con rangos de destino de cada parámametro
    :return: éxito
    """

    if data_alt_dict:
        data_dict = data_alt_dict
    else:
        data_dict = {
            'var_names': ['noise', 'spherical', 'sinusoidal'],
            'param_names': [u'Grado Alcohólico', u'Acidez Total', u'Sulfuroso total'],
        }

    if map_origin_ranges:
        data_dict['var_values'] = map_data(read_csv_data(file_path),
                                           map_origin_ranges, map_tarjet_ranges)
    else:
        data_dict['var_values'] = read_csv_data(file_path)

    create_batch(batch_name, data_dict, output_path=output_path)
