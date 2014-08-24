# -*- coding: utf-8 -*-
from batch_generator import *


# Generador de rangos de datos para comparación
# Formato: [min, max, numero_muestras, nombre_variacion, parámetro_asociado]
# data = [
#     [0.1, 0.8, 2, 'waves', u'Grado Alcohólico'],
#     [0.1, 0.8, 2, 'heart', u'Sulfuroso libre'],
#     [0.1, 0.8, 2, 'rings', u'Acidez Total'],
# ]
# batch_name = 'CC 01'
# Generamos el diccionario con  los datos de los flames
# create_comparison_batch(batch_name, data, output_path='./output/')

# Generador de lotes aleatorios
create_random_batches(50, variations=2, sequence_name='ZRandom(2 var)', sequence_start=31, output_path='./output/')

# Generador de flames a partir de csv
# origin_ranges = ((10,17), (4,7), (15,35))
# tarjet_ranges = ((0.2,0.9), (0.1,1), (1.2,2.2))
# render_csv_file('./RecopilacionDatos.csv', 'Coinoculacion07-08 02',
#                 map_input_data=True, map_origin_ranges=origin_ranges, map_tarjet_ranges=tarjet_ranges)