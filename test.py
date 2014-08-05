# -*- coding: utf-8 -*-
from os import listdir
from lxml import etree
from render import get_xform_variations_text, add_image_caption

flame_file = open('testing.flame', 'r')
current_test_dir = './output/my-flame-molon/'

flames_properties = get_xform_variations_text(flame_file)
flame_images = listdir(current_test_dir)

# Add subtitle caption for all generated images
for i, image in enumerate(flame_images):
    add_image_caption(current_test_dir + image, flames_properties[i])

