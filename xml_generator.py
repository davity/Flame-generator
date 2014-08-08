# -*- coding: utf-8 -*-
from utils import *
from numpy import arange
from lxml import etree
from itertools import product


def generate_xml_flame(data_list, file_name):
    """
    Receives a list of lists with the next structure:

        [ [min1, max1, samples1, variation_name1], [min1, max1, samples1, variation_name1], ...]

    Where each sublist item must be:
        min: Minimum of the range. Could be a float.
        max: Maximum of the range. Could be a float.
        samples: Number of equal parts that the range must be divided on. Should be an integer.
        variation_name: Name of the variation to apply to the transform (ex: linear, sinusoidal, swirl...). Must be a string.

    Return a etree object with the generated xml.

    :param data_list: list of lists
    :param file_name: name of the flame file to output
    :return: etree
    """

    ranges = []  # List of all the input ranges
    variation_names = []  # List of all the variation names

    # Process the data list
    for element in data_list:
        # Get the range of data for actual element
        # var declaration for easy understanding (could be omitted)
        minimum = element[0]
        maximum = element[1]
        samples = element[2]

        step = (maximum - minimum) / float(samples)  # Calculate the step for arange function
        ranges.append(arange(minimum, maximum, step).tolist())

        # Copy the name to another list
        variation_names.append(element[3])

    all_ranges = list(product(*ranges))
    print('data = ' + str(all_ranges))

    # Create the XML tree for the .flame file
    # root
    flames = etree.Element('Flames', name=file_name)
    i = 0
    for range_tuple in all_ranges:
        # flame child
        flame = etree.SubElement(flames, 'flame', flame_properties(str(i)))
        i += 1

        for i, value in enumerate(range_tuple):
            # transform child (triangles in apophysis)
            xform = etree.SubElement(flame, 'xform', xform_properties(variation_names[i], value, i))

        # And add a default gradient
        gradient = etree.SubElement(flame, 'palette', gradient_properties())
        gradient.text = gradient_content()

    return flames