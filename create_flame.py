# -*- coding: utf-8 -*-
# import argparse
from render import render_flame_file, process_output_images, render_flame_web
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
    [0.2, 1.5, 3, 'swirl', u'Grado Alcohólico'],    # N - 9 + 1
    [0.1, 1.3, 3, 'julia', u'Acidez'],              # N + 0.1
    [3, 5, 3, 'sinusoidal', u'Sulfuroso Libre']     # N/10
]
batch_name = 'test-arandano'


# PROCESAMIENTO

# Pasar la lista de datos al generador de XML-Flame
generate_xml_flame(data, batch_name, output_path='./output/')

# Llamar al render flam3 para que procese el archivo .flame y genere las imágenes en la carpeta correspondiente
render_flame_file(batch_name, output_path='./output/')

# Añadir a cada imagen generada un pie de imagen con la información relevante del flame
process_output_images(batch_name, output_path='./output/')

# Crear un archivo html sencillo que contenga todas las imágenes generadas
render_flame_web(batch_name, output_path='./output/')