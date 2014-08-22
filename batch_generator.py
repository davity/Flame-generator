# -*- coding: utf-8 -*-
import os
import random
from render import render_flame_file, process_output_images, render_flame_web, render_web_index
from xml_generator import generate_xml_flame


# PROCESAMIENTO
def create_batch(batch_name, data, output_path='./output/', render_html_index=True):
    u"""
    Renderiza todas las imágenes a partir de los datos de entrada, les añade la información del flame (variaciones
    usadas, valores y parámetro que representa) y crea un archivo html con todas esas imágenes.

    Además crea dos archivos .flame, el primero correspondiente al archivo que se renderiza y un segundo ("*_mod.flame)
    en donde las transformadas (nodos xform del XML) tienen un parámetro adicional 'real_name' que se usa para
    almacenar el nombre del parámetro "en la vida real" que representa.
    Se crean dos archivos ya que algunos programas como Fr0st (alternativa a Apophysis) pueden dar errores si se
    encuentran con parámetros no esperados como 'real_name'.

    El formato de data debe ser:
        [
            [rng_min, rng_max, var, param],
            [rng_min, rng_max, var, param],
            ...
        ]
    Donde rng_min y rng_max son números (puede ser en coma flotante) y
    var y param son cadenas de texto.

    :param batch_name: Nombre del lote. Se usará para la carpeta, el html y los .flame
    :param data: Lista de listas con formato [ [rng_min, rng_max, var, param], ...]
    :param output_path: Cadena con el directorio de salida. Incluir el caracter '/' al final
    :param render_html_index: Indica si se debe renderizar el índice de lotes en la carpeta designada por output_path
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

    # Pasar la lista de datos al generador de XML-Flame
    generate_xml_flame(data, batch_name, output_path=output_path)

    # Llamar al render flam3 para que procese el archivo .flame y genere las imágenes en la carpeta correspondiente
    render_flame_file(batch_name, output_path=output_path)

    # Añadir a cada imagen generada un pie de imagen con la información relevante del flame
    process_output_images(batch_name, output_path=output_path)

    # Crear un archivo html sencillo que contenga todas las imágenes generadas
    render_flame_web(batch_name, output_path=output_path)

    # Crear un índice para mostrar todos los lotes existentes y un enlace al archivo html de cada lote
    if render_html_index: render_web_index(output_path=output_path)
    return True


def create_random_batches(number_of_batches, number_of_vars=3, name_num_start=0, output_path='./output/'):
    u"""
    Crea un conjunto de lotes eligiendo variaciones y parámetros al azar con valores fijos de 0.5 para cada variación

    :param number_of_batches: Número de lotes a crear
    :param number_of_vars: Número de variaciones/transformadas por lote
    :param name_num_start: Número de secuencia inicial del lote (por si hemos creado más aleatorios antes)
    :param output_path: Directorio de salida
    :return: Éxito (boolean)
    """
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

    # Evitamos sobreescribir lotes ya existentes
    if os.path.isdir(output_path + 'Random %03d' % name_num_start):
        print(u"""
        ¡ATENCION!
        Ya existe una o más carpetas con ese nombre (Random %03d).
        Elimínela o renómbrela y vuelva a ejecutar el creador de lotes.
        """ % name_num_start)
        return False

    more_data = []
    more_name = []
    for number in range(number_of_batches):
        data = []
        for i, xform in enumerate(range(number_of_vars)):
            varvar = choose_n(affine_vars, number_of_vars)
            data.append([0.5, 0.5, 1, varvar[i], random.choice(params)])
        more_data.append(data)
        more_name.append('Random ' + str("%03d" % (name_num_start + number)))

    for i in range(len(more_name)):
        print('Creando lote de flames: ' + str((i + 1)) + '/' + str(len(more_name)))
        create_batch(more_name[i], more_data[i], output_path=output_path, render_html_index=False)

    render_web_index(output_path=output_path)
    return True
