# -*- coding: utf-8 -*-
from batch_generator import *


# DATOS DE ENTRADA
# Definición de los Rangos de los datos, muestras, variaciones y los parámetros a los que se asocian
# Formato: [min, max, numero_muestras, nombre_variacion, parámetro_asociado]
data = [
    [0.1, 0.8, 4, 'waves', u'Grado Alcohólico'],
    [0.1, 0.8, 4, 'heart', u'Sulfuroso libre'],
    [0.1, 0.8, 4, 'rings', u'Acidez Total'],
]
batch_name = 'Zeta 02'

# Llamar a la función para crear los flames
create_batch(batch_name, data, output_path='./output/')

# Generador de lotes aleatorios
# create_random_batches(30, 3, 21, output_path='./output/')