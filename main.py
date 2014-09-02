# -*- coding: utf-8 -*-
from batch_generator import create_comparison_batch
from batch_generator import create_random_batches
from batch_generator import render_csv_file


# COMPARACIÓN DE RANGOS
# Formato: [min, max, numero_muestras, nombre_variacion, parámetro_asociado]
data = [
    [0.3, 1, 3, 'swirl', u'Grado Alcohólico'],
    [0.3, 1, 3, 'julia', u'Sulfuroso libre'],
    [1.2, 2.2, 3, 'sinusoidal', u'Acidez Total'],
]
batch_name = 'Experimento 01'
create_comparison_batch(batch_name, data, output_path='./output/')

# GENERADOR DE LOTES ALEATORIOS
create_random_batches(3, variations=2, sequence_name='Aleatorio', sequence_start=2, output_path='./output/')

# GENERACION A PARTIR DE ARCHIVO CSV
origin_ranges = ((11.3, 15.43), (4.3, 10.67), (7.68, 33.0))
tarjet_ranges = ((0.1, 1.0), (0.1, 1.0), (1.2, 2.2))
render_csv_file('./datos_reales.csv', 'AAAAAAEpsilon con datos reales', map_origin_ranges=origin_ranges, map_tarjet_ranges=tarjet_ranges,output_path='./output/')
