# -*- coding: utf-8 -*-
from numpy import arange


def position(pos):
    """
    Return the coordinates of the transform: X-axis, Y-axis and Origin (the triangle in Apophysis).
    By default, X and Y axis are not modified, just the origin, which could be placed in the nex positions:

    Position Coordinates (for a step = 1)
    (-1,-1)---(0,-1)---(1,-1)
        |        |        |
        |        |        |
    (-1, 0)---(0, 0)---(1, 0)
        |        |        |
        |        |        |
    (-1, 1)---(0, 1)---(1, 1)

    Note that the Y-coordinates are inverted, so, positive axis is in bottom and negative in top.
    This is only for flame files, in Apophysis the representation is with positive at top.

    Position number (pos) (for a step = 1)
    6 --- 7 --- 8
    |     |     |
    3 --- 4 --- 5
    |     |     |
    0 --- 1 --- 2

    :param pos:
    :return: string
    """
    # Generate transform possible positions
    positions = (
        (-1, 1),
        (0, 0),
        (1, -1),
        (-1, -1),
        (1, 1),
        (0, -1),
        (-1, 0),
        (1, 0),
        (0, 1)
    )
    return '1 0 0 1 ' + str(positions[pos][0]) + ' ' + str(positions[pos][1])


def flame_properties(name):
    """
    Return a dictionary with all the parameters for a flame xml node.

    :param name: Name of the flame (showed under the image in Apophysis
    :return: dictionary
    """
    return {'name': name,
            # A bunch of nice defaults
            'version': 'Apophisis 2.09',
            'size': '640 480',
            'center': '0 0',
            'scale': '38.4',  # 7.77 * value
            'filter': '0.5',
            'quality': '10',
            'background': '0 0 0',
            'brightness': '4',
            'gamma': '4',
            'gamma_threshold': '0.04'  # 0.04 * value
    }


def xform_properties(variation_name, variation_value, pos):
    """
    Return a dictionary with all the parameters for a xform.

    :param variation_name: Name of the variation. Must match one of the flam3 algorithm.
    :param variation_value: Probability for the variation
    :param pos: Position of the Xform origin. Check Position function for details.
    :return:
    """
    new_xform = {'weight': '0.5', 'color': '0', 'coefs': position(pos), variation_name: str(variation_value)}
    return new_xform


def gradient_properties():
    """
    Return a dictionary with default values for the gradient
    """
    return {'count': '256', 'format': 'RGB'}


def gradient_content():
    """
    Return a default gradient for the flame palette
    """
    return '''
        707B875F6A784F59694751643F4A60263360253462253665
        1D3162162D60162B5D16295B15275E182B6324386D3F517F
        5A6B927686A992A1C1A5B1CAB8C2D4E4EAF3EEF3F8F9FCFD
        FBFCFDFEFCFDFEFCFDFEFDFDFCFDFFF5F7FBE1E6EED2D6E2
        C3C7D6B9BFD5AFB8D5B2B8D3B6B9D2CCD1E6DADEEAE8EBEE
        E3EAEFDFEAF1D8E3EBD1DDE6BACAD89DB0D28199BF7790B5
        6E87AC6C84A66B82A05C72934A5B7B2935531F2D45162638
        1525351524321625341727371A2B442536563B4D8955689E
        6F84B37A90BF869DCCA3B6D7B9C6DFCAD6E7C5CDDDC0C4D3
        BCC1CDB9BFC7B1B6C0ACB3BFB2BBC1BCC2C6D8DEE1E2E7EB
        ECF0F5EDF1F6EFF3F8E9EFF7DDE3EFBAC0D8ABB1D19CA3CA
        98A1CA949FCB8E9BD097A2D5A9B3E2BBC6EADFE4F4E3EAF7
        E8F1FBE8F3FADEE9EECAD8E4B3C3D98D9AAB808DA474809E
        737D9A737B977178925F6D9A4E5E954552841B2D61152454
        0F1C47091236080F2A080D22070C2011162D151E3A1A2648
        2332532C3E5E42567557688B71839F8C9AB0BDC6C9BEC7C9
        C0C9CAC9C9C6C7CAC4B4BFB9A9AEA99499A09198A08E97A1
        929C9D939FA08F9CA5899397767F82586873343A51272F49
        1B2542141B360E142C0A0F250B0D200B12270E152E111935
        1721461D2A5622316127387126397C22367C253581222F7E
        1D2C7722317E333B824A5289636FA2ACB3D0BAC1DAC8D0E4
        D5E1E7D8E3E2D0DBDBB7C8C69AA8AC788695596786465276
        3240672432611E2D5D19275717225511224F0D1D410F1A39
        101E350F202C0F1F23101B1E0C161C08151A060E14040A12
        040D13050D12060C11050D12050D11050B0F05080F05080D
        04080C04080E050912040A18030C250410350616450A1E56
        0F2362122768172B63192B5D16295913234F1020420B1E3C
        0B1B380D19300E1A280D18200C191E0D1C200F1C1E0D1A1D
        0A171E0B171C0B1119070A1504061103050E01050C00060C
        01060C03090D0612130815160710120813160B1420081022
        060C2405092604072802052801042900042F060B3B0C1247
        17255A22396D3B4E815564955D6F9B667AA28593AC7A8799
        '''
