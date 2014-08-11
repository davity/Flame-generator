# -*- coding: utf-8 -*-
import subprocess, sys, os
import Image, ImageDraw, ImageFont
import glob
from lxml import etree
from utils import create_dir
import jinja2
import textwrap


def render_flame_file(file_name, batch_name, output_path='./output/'):
    u"""
    Dada una ruta a un archivo flame, un nombre de lote y una ruta de output opcional,
    renderiza el archivo flame con flam3 y guarda las imágenes resultates en la ruta definida por el
    output y el nombre del lote.

    :param file_name: ruta al archivo flame
    :param batch_name: nombre del lote
    :param output_path: directorio de salida para las imágenes
    :return: boolean: Indica si la función ha tenido éxito
    """

    # Crear la carpeta de salida si no existe
    create_dir(output_path)

    # Crear una carpeta para el conjunto de flames que se van a renderizar (batch)
    current_test_dir = output_path + batch_name + '/'
    create_dir(current_test_dir)

    # Renderizar el archivo XML de flames con flam3
    try:
        flame_file = open(file_name, 'r')
    except IOError:
        print 'Error: El archivo "' + file_name + '" no existe'
        return False
    else:
        # Establecer las variables de entorno para flam3 (en vez de por parámetro se pasar por entorno)
        envy = os.environ.copy()
        envy['prefix'] = current_test_dir
        envy['name_enable'] = '0'  # Debe ser cero para que la opción 'prefix' funcione

        # Llamar a flam3 y renderizar todos los flames
        process = subprocess.Popen('./flam3/flam3-render.exe', stdin=flame_file, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE, env=envy)

        # Imprimir la salida de flam3 para ver que esá pasando
        for e in iter(lambda: process.stderr.read(1), ''):
            sys.stdout.write(e)

        return True


def process_output_images(file_name, batch_name, output_path='./output'):
    u"""
    Dada una ruta a un archivo flame, un nombre de lote y una ruta de output opcional,
    añade a cada imagen generada por la funcion render_flame_file y les añade un subtítulo
    con las variaciones usadas, los valores de cada una de estas y a qué parámetros van asociados

    :param file_name: ruta al archivo flame
    :param batch_name: nombre del lote
    :param output_path: directorio de salida para las imágenes
    :return: boolean: Indica si la función ha tenido éxito
    """

    current_test_dir = output_path + batch_name + '/'
    current_test_file = current_test_dir + file_name

    # Obtener todas las transformaciones de los flames, sus valores y sus parámetros
    flames_properties = get_xform_variations_text(current_test_file)

    # Obtener todas las imágenes generadas por flam3 en la funcion render_flame_file
    flame_images = []
    iterator = glob.glob(current_test_dir + '*.png')
    for element in iterator:
        flame_images.append(element.split('\\')[-1])

    # Añadir un subtítulo con la información a cada imagen
    for i, image in enumerate(flame_images):
        add_image_caption(current_test_dir + image, flames_properties[i])

    return True


def add_image_caption(image_path, text):
    u"""
    Dada la ruta de una imagen y un texto, expande la imagen por la parte inferior en función
    del número de líneas que tenga el texto. El texto se divide de 60 en 60 caractéres para obtener
    las líneas del mismo.
    Dentro del área expandida de la imágen se escriben las líneas de texto correspondientes.

    :param image_path: Ruta a la imagen
    :param text: Texto a escribir en el pie de la imagen creado
    :return: boolean
    """
    img = Image.open(image_path)
    old_size = img.size
    nlines = 3
    font_size = 16
    spacing = font_size/2
    text_start_y = old_size[1] + spacing

    new_size = (old_size[0], old_size[1] + (spacing + (font_size + spacing) * nlines))
    new_img = Image.new("RGB", new_size, color=(240, 240, 240))

    new_img.paste(img, (0, 0))

    draw = ImageDraw.Draw(new_img)
    font = ImageFont.truetype("C:\\Windows\\Fonts\\consola.ttf", font_size)
    lines = textwrap.wrap(text, width=60)
    for i, line in enumerate(lines):
        draw.text((font_size, text_start_y + i * (spacing + font_size)), line, (0, 0, 0), font=font)

    # new_img.show()
    new_img.save(image_path)

    return True


def render_flame_web(batch_name, output_path='./output'):
    u"""
    Renderizar un archivo html con todas las imágenes del lote de flames
    :param batch_name: nombre del lote
    :return: boolean
    """

    current_test_dir = output_path + batch_name + '/'

    # Obtener las imágenes
    flame_images = []
    iterator = glob.glob(current_test_dir + '*.png')
    for element in iterator:
        # Split para systemas windows (notar el \\ para las rutas que se obtienen de glob.glob())
        flame_images.append(element.split('\\')[-1])

    # Cargar template de jinja2
    jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader('./templates/'))
    template = jinja_environment.get_template('flame_template.html')

    # Crear el archivo de salida
    template_output = open(current_test_dir + batch_name + '.html', 'w')
    template_output.write(template.render(name=batch_name, images=flame_images))
    template_output.close()

    return True


def get_xform_variations_text(flame_file):
    u"""
    Lee un archivo .flame y devuelve una lista de cadenas que contienen, para cada flame dentro del archivo y para cada
    transformada del flame:
        1. La variación utilizada por la transformada
        2. El valor de la variación
        3. El parámetro al que está asociada

    Las cadenas están alineadas a 60 caracteres para que tengan todas la misma longitud.

    Por ejemplo, para las siguientes tres transformadas:
        <xform coefs="1 0 0 1 -1 1" color="0"   real_name="Grado Alcoh&#243;lico" swirl="1.0"   weight="0.5"/>
        <xform coefs="1 0 0 1 0 0" color="0"    julia="0.1" real_name="Acidez"                  weight="0.5"/>
        <xform coefs="1 0 0 1 1 -1" color="0"   real_name="Sulfuroso Libre" sinusoidal="5.0"    weight="0.5"/>
    Se obtiene la salida:
        [u'swirl = 1.0000                 - Grado Alcoh\xf3lico
           julia = 0.1000                 - Acidez
           sinusoidal = 5.0000            - Sulfuroso Libre            ']

    :param flame_file: ruta al archivo .flame
    :return: lista de cadenas
    """

    all_vars = ['linear', 'sinusoidal', 'spherical', 'swirl', 'horseshoe', 'polar', 'handkerchief', 'heart', 'disc',
                'spiral', 'hyperbolic', 'diamond', 'ex', 'julia', 'bent', 'waves', 'fisheye', 'popcorn', 'exponential',
                'power', 'cosine', 'rings', 'fan', 'blob', 'pdj', 'fan2', 'rings2', 'eyefish', 'bubble', 'cylinder',
                'perspective', 'noise', 'julian', 'juliascope', 'blur', 'gaussian_blur', 'radial_blur', 'pie', 'ngon',
                'curl', 'rectangles', 'arch', 'tangent', 'square', 'rays', 'blade', 'secant2', 'twintrian', 'cross',
                'disc2', 'super_shape', 'flower', 'conic', 'parabola', 'bent2', 'bipolar', 'boarders', 'butterfly',
                'cell', 'cpow', 'curve', 'edisc', 'elliptic', 'escher', 'foci', 'lazysusan', 'loonie', 'pre_blur',
                'modulus', 'oscilloscope', 'polar2', 'popcorn2', 'scry', 'separation', 'split', 'splits', 'stripes',
                'wedge', 'wedge_julia', 'wedge_sph', 'whorl', 'waves2', 'exp', 'log', 'sin', 'cos', 'tan', 'sec', 'csc',
                'cot', 'sinh', 'cosh', 'tanh', 'sech', 'csch', 'coth', 'auger', 'flux']

    flames_parameters = []
    # Recorrer el xml
    flames = etree.parse(flame_file)
    for flame in flames.getroot():
        # De cada flame obtener todas las xform (transformaciones, triangulos de Apophysis)
        xforms = []
        for child in flame:
            if child.tag == 'xform':
                xforms.append(child)

        # Obtener los nombres y valores de las variaciones y los parámetros, y salvarlos en una cadena
        # cada variación y dato se ajustará a un ancho de 30 caractires añadiendo espacios al final. Tras cada variación
        # se añadirá el parámetro al que corresponde y se ajustará la cadena final a 60 caracteres de ancho.
        txt = ''
        for xform in xforms:
            # Comprobamos si la transformada tiene alguna de las variaciones posibles
            for var in all_vars:
                # Si tiene alguna, la guardamos
                if xform.get(var) is not None:
                    tmp = var + ' = ' + "{:.4f}".format(float(xform.get(var)))
                    # Si tiene asociado un parámetro, también lo guardamos
                    if xform.get('real_name') is not None:
                        tmp = tmp.ljust(30, ' ') + ' - ' + xform.get('real_name')
                    txt += tmp.ljust(60, ' ')

        # Guardar la cadena resultante en el array
        flames_parameters.append(txt)

    return flames_parameters
