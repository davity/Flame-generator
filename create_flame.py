# -*- coding: utf-8 -*-
# import argparse
from pprint import pprint
import random
from render import render_flame_file, process_output_images, render_flame_web, render_web_index
from xml_generator import generate_xml_flame


# parser = argparse.ArgumentParser(description='Create a flame file with a name')
# parser.add_argument('name', help=u'Nombre para el archivo de flames')
#
# args = parser.parse_args()
# print('Nombre = ' + args.name)

# DATOS DE ENTRADA

# Definición de los Rangos de los datos, muestras, variaciones y los parámetros a los que se asocian
# Formato: [min, max, numero_muestras, nombre_variacion, parámetro_asociado]
data = [
    [0.3, 0.7, 3, 'linear', u'Grado Alcohólico'],
    [0.1, 1.0, 3, 'rays', u'Sulfuroso libre'],
    [0.1, 1.0, 3, 'diamond', u'Acidez Total'],
]
batch_name = 'Delta 01'


# PROCESAMIENTO
def create_batch(batch_name, data, output_path='./output/', render_index=True):
    # Pasar la lista de datos al generador de XML-Flame
    generate_xml_flame(data, batch_name, output_path='./output/')

    # Llamar al render flam3 para que procese el archivo .flame y genere las imágenes en la carpeta correspondiente
    render_flame_file(batch_name, output_path='./output/')

    # Añadir a cada imagen generada un pie de imagen con la información relevante del flame
    process_output_images(batch_name, output_path='./output/')

    # Crear un archivo html sencillo que contenga todas las imágenes generadas
    render_flame_web(batch_name, output_path='./output/')

    # Crear un índice para mostrar todos los lotes existentes y un enlace al archivo html de cada lote
    if render_index: render_web_index(output_path='./output/')


def create_random_batches(number_of_batches, number_of_vars=3, name_num_start=0, output_path='./output/'):
    def choose_n(list, n):
        v = []
        while len(v) < (n + 1):
            t = random.choice(list)
            if not t in v:
                v.append(t)
        return v

    # Flame variation definitions
    affine_vars = ['linear', 'sinusoidal', 'spherical', 'swirl', 'horseshoe', 'polar', 'handkerchief', 'heart', 'disc',
                    'spiral', 'hyperbolic', 'diamond', 'ex', 'julia', 'bent', 'waves', 'fisheye', 'popcorn',
                    'exponential', 'power', 'cosine', 'rings', 'fan', 'eyefish', 'bubble', 'cylinder', 'noise', 'blur',
                    'gaussian_blur', 'arch', 'tangent', 'square', 'rays', 'blade', 'secant2', 'twintrian', 'cross']
    parametric_vars = ['blob', 'pdj', 'fan2', 'rings2', 'perspective', 'julian', 'juliascope', 'radial_blur', 'pie',
                       'ngon', 'curl', 'rectangles']

    # Params to choose from
    params = [u'Grado Alcohólico', u'Acidez Total', u'Acidez Volátil', u'PH', u'Sulfuroso Total', u'Sulfuroso Libre']

    more_data = []
    more_name = []
    for number in range(number_of_batches):
        data = []
        for i, xform in enumerate(range(number_of_vars)):
            varvar = choose_n(affine_vars, number_of_vars)
            data.append([0.5, 0.5, 1, varvar[i], random.choice(params)])
        more_data.append(data)
        more_name.append('Random ' + str(name_num_start + number))

    pprint(more_data)

    for i in range(len(more_name)):
        print('Creando lote de flames: ' + str((i + 1)) + '/' + str(len(more_name)))
        create_batch(more_name[i], more_data[i], output_path='./output/', render_index=False)

    render_web_index(output_path='./output/')


# create_batch(batch_name, data, output_path='./output/')
create_random_batches(30, 3, 20, output_path='./output/')
