# -*- coding: utf-8 -*-
import subprocess, sys, os
import Image, ImageDraw, ImageFont
from os import listdir
from lxml import etree


def render_flame_file(file_name, batch_name, output_path='./output/'):
    def create_dir(dirname):
        if not os.path.exists(dirname):
            print('Creando directorio "' + dirname + '"')
            os.makedirs(dirname)
        else:
            print('Directorio "' + dirname + '" ya existe, no se hace nada')

    # Create an output folder if not exist
    create_dir(output_path)

    # Create a test folder inside the output dir for the current flame file
    current_test_dir = output_path + batch_name + '/'
    create_dir(current_test_dir)

    # Render the flame XML file with flam3
    try:
        # Open the flame file to render
        flame_file = open(file_name, 'r')
    except IOError:
        print 'Error: El archivo "' + file_name + '" no existe'
    else:
        # Set environment vars for flam3 render
        envy = os.environ.copy()
        envy['prefix'] = current_test_dir
        envy['name_enable'] = '0'  # Must be zero in order of prefix to work...

        # Call flam3 and render all the images
        process = subprocess.Popen('./flam3/flam3-render.exe', stdin=flame_file, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE, env=envy)

        # Print output from the script
        for e in iter(lambda: process.stderr.read(1), ''):
            sys.stdout.write(e)

    # Add the transforms variations and values to each image
    try:
        flame_file = open(file_name, 'r')
    except IOError:
        print 'Error: El archivo "' + file_name + '" no existe'
    else:
        # Get all the flames xform variations and values

        flames_properties = get_xform_variations_text(flame_file)
        flame_images = listdir(current_test_dir)

        # Add subtitle caption for all generated images
        for i, image in enumerate(flame_images):
            add_image_caption(current_test_dir + image, flames_properties[i])


def get_xform_variations_text(flame_file):
    all_vars = ['linear', 'sinusoidal', 'spherical', 'swirl', 'horseshoe', 'polar', 'handkerchief', 'heart', 'disc',
                'spiral',
                'hyperbolic', 'diamond', 'ex', 'julia', 'bent', 'waves', 'fisheye', 'popcorn', 'exponential', 'power',
                'cosine',
                'rings', 'fan', 'blob', 'pdj', 'fan2', 'rings2', 'eyefish', 'bubble', 'cylinder', 'perspective',
                'noise',
                'julian', 'juliascope', 'blur', 'gaussian_blur', 'radial_blur', 'pie', 'ngon', 'curl', 'rectangles',
                'arch',
                'tangent', 'square', 'rays', 'blade', 'secant2', 'twintrian', 'cross', 'disc2', 'super_shape', 'flower',
                'conic', 'parabola', 'bent2', 'bipolar', 'boarders', 'butterfly', 'cell', 'cpow', 'curve', 'edisc',
                'elliptic',
                'escher', 'foci', 'lazysusan', 'loonie', 'pre_blur', 'modulus', 'oscilloscope', 'polar2', 'popcorn2',
                'scry',
                'separation', 'split', 'splits', 'stripes', 'wedge', 'wedge_julia', 'wedge_sph', 'whorl', 'waves2',
                'exp',
                'log', 'sin', 'cos', 'tan', 'sec', 'csc', 'cot', 'sinh', 'cosh', 'tanh', 'sech', 'csch', 'coth',
                'auger',
                'flux']

    SPACER = '     '
    flames_parameters = []
    # Go over xml
    flames = etree.parse(flame_file)
    for flame in flames.getroot():
        # Get all the xform nodes
        xforms = []
        for child in flame:
            if child.tag == 'xform':
                xforms.append(child)

        # Get the variation name and its value and save it to a string
        txt = ''
        for xform in xforms:
            for var in all_vars:
                if xform.get(var) is not None:
                    txt += var + ' = ' + "{:.4f}".format(float(xform.get(var)))
                    if not xform == xforms[len(xforms) - 1]:
                        txt += SPACER # Add a little space to separate things


        # Save all the parameters in the array
        flames_parameters.append(txt)

    return flames_parameters


def add_image_caption(image_path, text):
    img = Image.open(image_path)
    old_size = img.size

    new_size = (old_size[0], old_size[1] + 32)
    new_img = Image.new("RGB", new_size, color=(240, 240, 240))

    new_img.paste(img, (0, 0))

    draw = ImageDraw.Draw(new_img)
    font = ImageFont.truetype("C:\\Windows\\Fonts\\consola.ttf", 16)
    line1 = text  # u'swirl=0,26     julia=0,30     sinusoidal=3,4'
    draw.text((16, new_size[1] - 24), line1, (0, 0, 0), font=font)

    # new_img.show()
    new_img.save(image_path)