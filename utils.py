# -*- coding: utf-8 -*-
from numpy import arange
import os
from lxml import etree


def create_dir(dirname):
    """
    Dada una ruta, comprueba si existe y si no crea las carpetas que falten en la ruta
    :param dirname: nombre de la carpeta o ruta
    :return: True si se ha creado. False si ya existe.
    """
    if not os.path.exists(dirname):
        print('Creando directorio "' + dirname + '"')
        os.makedirs(dirname)
        return True
    else:
        print('Directorio "' + dirname + '" ya existe, no se hace nada')
        return False

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
    # Define possible transform positions
    positions = (
        (-1, 1),
        (1, -1),
        (0, 0),
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


def xform_properties(variation_name, variation_value, pos, real_name, color_pos):
    """
    Return a dictionary with all the parameters for a xform.

    :param variation_name: Name of the variation. Must match one of the flam3 algorithm.
    :param variation_value: Probability for the variation
    :param pos: Position of the Xform origin. Check Position function for details.
    :param color_pos: Color position for the transform
    :return:
    """
    new_xform = {'weight': '0.5', 'color': str("{:.2f}".format(color_pos)), 'coefs': position(pos), variation_name: str(variation_value), 'real_name': real_name}
    return new_xform


def gradient_properties():
    """
    Return a dictionary with default values for the gradient
    """
    return {'count': '256', 'format': 'RGB'}


def add_gradient_apophysis(etree_element):
    """
    Return a etree element with an Apophysis-style gradient
    """

    gradient_text = '''
        000764010967020C69020E6C03116E041371051673051876
        061B78071D7B081F7D0922800924820A27850B29870C2C8A
        0C2E8C0D308F0E33910F3594103896103A99113D9B123F9E
        1342A01444A31446A51549A8164BAA174EAD1750AF1853B2
        1955B41A57B71B5AB91B5CBC1C5FBE1D61C11E64C31E66C6
        1F69C8206BCB236DCC266FCD2972CD2C74CE3076CF3378D0
        367BD1397DD13C7FD23F81D34284D44586D44888D54B8AD6
        4F8DD7528FD85591D85893D95B96DA5E98DB619ADC649CDC
        679FDD6BA1DE6EA3DF71A5DF74A8E077AAE17AACE27DAEE3
        80B1E383B3E487B5E58AB7E68DB9E790BCE793BEE896C0E9
        99C2EA9CC5EB9FC7EBA2C9ECA6CBEDA9CEEEACD0EEAFD2EF
        B2D4F0B5D7F1B8D9F2BBDBF2BEDDF3C2E0F4C5E2F5C8E4F6
        CBE6F6CEE9F7D1EBF8D4EDF9D7EFF9DAF2FADDF4FBE1F6FC
        E4F8FDE7FBFDEAFDFEEDFFFFEDFEFBEEFCF6EEFBF2EEF9ED
        EFF8E9EFF6E4EFF5E0F0F3DBF0F2D7F0F0D2F0EFCEF1EDC9
        F1ECC5F1EAC0F2E9BCF2E7B7F2E6B3F3E4AEF3E3AAF3E1A6
        F4E0A1F4DE9DF4DD98F5DB94F5DA8FF5D88BF6D786F6D582
        F6D47DF6D279F7D174F7CF70F7CE6BF8CC67F8CB62F8C95E
        F9C859F9C655F9C551FAC34CFAC248FAC043FBBF3FFBBD3A
        FBBC36FCBA31FCB92DFCB728FCB624FDB41FFDB31BFDB116
        FEB012FEAE0DFEAD09FFAB04FFAA00FAA700F6A400F1A100
        EC9E00E89B00E39800DF9500DA9200D58F00D18B00CC8800
        C78500C38200BE7F00B97C00B57900B07600AC7300A77000
        A26D009E6A009967009464009061008B5E00865B00825800
        7D5400795100744E006F4B006B48006645006142005D3F00
        583C005339004F36004A3300463000412D003C2A00382700
        3324002E21002A1D00251A002017001C1400171100130E00
        0E0B0009080005050000020000020300020500020800030B
        00030E00031000031300031600031800031B00031E000420
        00042300042600042900042B00042E000431000533000536
        00053900053B00053E00054100054400064600064900064C
        00064E00065100065400065600065900075C00075F000761
        '''

    gradient = etree.Element('palette', gradient_properties())
    gradient.text = gradient_text
    etree_element.append(gradient)

    return etree_element

def add_gradient_fr0st(etree_element):
    """
    Return a etree element with an Fr0st style gradient
    """

    gradient_text = """<color index="0" rgb="253 172 7"/>
    <color index="1" rgb="254 170 2"/>
    <color index="2" rgb="253 168 0"/>
    <color index="3" rgb="252 165 0"/>
    <color index="4" rgb="250 162 0"/>
    <color index="5" rgb="248 159 0"/>
    <color index="6" rgb="246 155 0"/>
    <color index="7" rgb="245 152 0"/>
    <color index="8" rgb="243 149 0"/>
    <color index="9" rgb="241 146 0"/>
    <color index="10" rgb="239 143 0"/>
    <color index="11" rgb="238 139 0"/>
    <color index="12" rgb="236 136 0"/>
    <color index="13" rgb="234 133 0"/>
    <color index="14" rgb="232 130 0"/>
    <color index="15" rgb="230 127 0"/>
    <color index="16" rgb="229 123 0"/>
    <color index="17" rgb="227 120 0"/>
    <color index="18" rgb="225 117 0"/>
    <color index="19" rgb="223 114 0"/>
    <color index="20" rgb="222 111 0"/>
    <color index="21" rgb="220 107 0"/>
    <color index="22" rgb="218 104 0"/>
    <color index="23" rgb="216 101 0"/>
    <color index="24" rgb="215 98 0"/>
    <color index="25" rgb="213 95 0"/>
    <color index="26" rgb="211 91 0"/>
    <color index="27" rgb="209 88 0"/>
    <color index="28" rgb="208 85 0"/>
    <color index="29" rgb="206 82 0"/>
    <color index="30" rgb="204 78 0"/>
    <color index="31" rgb="202 75 0"/>
    <color index="32" rgb="201 72 0"/>
    <color index="33" rgb="199 69 0"/>
    <color index="34" rgb="197 66 0"/>
    <color index="35" rgb="195 62 0"/>
    <color index="36" rgb="194 59 0"/>
    <color index="37" rgb="192 56 0"/>
    <color index="38" rgb="190 53 0"/>
    <color index="39" rgb="188 50 0"/>
    <color index="40" rgb="187 46 0"/>
    <color index="41" rgb="185 43 0"/>
    <color index="42" rgb="183 40 0"/>
    <color index="43" rgb="181 37 0"/>
    <color index="44" rgb="180 34 0"/>
    <color index="45" rgb="178 30 0"/>
    <color index="46" rgb="176 27 0"/>
    <color index="47" rgb="174 24 0"/>
    <color index="48" rgb="173 21 0"/>
    <color index="49" rgb="171 18 0"/>
    <color index="50" rgb="169 14 0"/>
    <color index="51" rgb="167 11 0"/>
    <color index="52" rgb="166 8 0"/>
    <color index="53" rgb="164 5 0"/>
    <color index="54" rgb="162 2 0"/>
    <color index="55" rgb="160 3 2"/>
    <color index="56" rgb="159 4 5"/>
    <color index="57" rgb="157 5 7"/>
    <color index="58" rgb="156 7 10"/>
    <color index="59" rgb="154 8 12"/>
    <color index="60" rgb="152 9 15"/>
    <color index="61" rgb="151 11 17"/>
    <color index="62" rgb="149 12 20"/>
    <color index="63" rgb="147 13 22"/>
    <color index="64" rgb="146 15 25"/>
    <color index="65" rgb="144 16 27"/>
    <color index="66" rgb="142 17 30"/>
    <color index="67" rgb="141 19 32"/>
    <color index="68" rgb="139 20 35"/>
    <color index="69" rgb="138 21 38"/>
    <color index="70" rgb="136 23 40"/>
    <color index="71" rgb="134 24 43"/>
    <color index="72" rgb="133 25 45"/>
    <color index="73" rgb="131 26 48"/>
    <color index="74" rgb="129 28 50"/>
    <color index="75" rgb="128 29 53"/>
    <color index="76" rgb="126 30 55"/>
    <color index="77" rgb="125 32 58"/>
    <color index="78" rgb="123 33 60"/>
    <color index="79" rgb="121 34 63"/>
    <color index="80" rgb="120 36 66"/>
    <color index="81" rgb="118 37 68"/>
    <color index="82" rgb="116 38 71"/>
    <color index="83" rgb="115 40 73"/>
    <color index="84" rgb="113 41 76"/>
    <color index="85" rgb="112 42 78"/>
    <color index="86" rgb="110 44 81"/>
    <color index="87" rgb="108 45 83"/>
    <color index="88" rgb="107 46 86"/>
    <color index="89" rgb="105 47 88"/>
    <color index="90" rgb="103 49 91"/>
    <color index="91" rgb="102 50 93"/>
    <color index="92" rgb="100 51 96"/>
    <color index="93" rgb="99 53 99"/>
    <color index="94" rgb="97 54 100"/>
    <color index="95" rgb="96 55 103"/>
    <color index="96" rgb="94 56 105"/>
    <color index="97" rgb="92 58 108"/>
    <color index="98" rgb="91 59 110"/>
    <color index="99" rgb="89 60 113"/>
    <color index="100" rgb="88 61 115"/>
    <color index="101" rgb="86 63 118"/>
    <color index="102" rgb="84 64 121"/>
    <color index="103" rgb="83 65 123"/>
    <color index="104" rgb="81 67 126"/>
    <color index="105" rgb="79 68 128"/>
    <color index="106" rgb="78 69 131"/>
    <color index="107" rgb="76 71 133"/>
    <color index="108" rgb="75 72 136"/>
    <color index="109" rgb="73 73 138"/>
    <color index="110" rgb="71 75 141"/>
    <color index="111" rgb="70 76 143"/>
    <color index="112" rgb="68 77 146"/>
    <color index="113" rgb="66 79 148"/>
    <color index="114" rgb="65 80 151"/>
    <color index="115" rgb="63 81 154"/>
    <color index="116" rgb="62 82 156"/>
    <color index="117" rgb="60 84 159"/>
    <color index="118" rgb="58 85 161"/>
    <color index="119" rgb="57 86 164"/>
    <color index="120" rgb="55 88 166"/>
    <color index="121" rgb="54 89 169"/>
    <color index="122" rgb="52 90 171"/>
    <color index="123" rgb="50 92 174"/>
    <color index="124" rgb="49 93 176"/>
    <color index="125" rgb="47 94 179"/>
    <color index="126" rgb="45 96 182"/>
    <color index="127" rgb="44 97 184"/>
    <color index="128" rgb="42 98 187"/>
    <color index="129" rgb="41 100 189"/>
    <color index="130" rgb="39 101 192"/>
    <color index="131" rgb="37 102 194"/>
    <color index="132" rgb="36 104 197"/>
    <color index="133" rgb="34 105 199"/>
    <color index="134" rgb="32 106 202"/>
    <color index="135" rgb="34 108 203"/>
    <color index="136" rgb="37 110 204"/>
    <color index="137" rgb="40 113 205"/>
    <color index="138" rgb="43 115 205"/>
    <color index="139" rgb="47 117 206"/>
    <color index="140" rgb="50 119 207"/>
    <color index="141" rgb="53 122 208"/>
    <color index="142" rgb="56 124 209"/>
    <color index="143" rgb="59 126 209"/>
    <color index="144" rgb="62 128 210"/>
    <color index="145" rgb="65 130 211"/>
    <color index="146" rgb="68 133 212"/>
    <color index="147" rgb="71 135 212"/>
    <color index="148" rgb="74 137 213"/>
    <color index="149" rgb="77 139 214"/>
    <color index="150" rgb="80 142 215"/>
    <color index="151" rgb="83 144 216"/>
    <color index="152" rgb="86 146 216"/>
    <color index="153" rgb="90 148 217"/>
    <color index="154" rgb="93 150 218"/>
    <color index="155" rgb="96 153 219"/>
    <color index="156" rgb="99 155 220"/>
    <color index="157" rgb="102 157 220"/>
    <color index="158" rgb="105 159 221"/>
    <color index="159" rgb="108 162 222"/>
    <color index="160" rgb="111 164 223"/>
    <color index="161" rgb="114 166 223"/>
    <color index="162" rgb="117 168 224"/>
    <color index="163" rgb="120 170 225"/>
    <color index="164" rgb="123 173 226"/>
    <color index="165" rgb="126 175 227"/>
    <color index="166" rgb="129 177 227"/>
    <color index="167" rgb="132 179 228"/>
    <color index="168" rgb="136 182 229"/>
    <color index="169" rgb="139 184 230"/>
    <color index="170" rgb="142 186 230"/>
    <color index="171" rgb="145 188 231"/>
    <color index="172" rgb="148 191 232"/>
    <color index="173" rgb="151 193 233"/>
    <color index="174" rgb="154 195 234"/>
    <color index="175" rgb="157 197 234"/>
    <color index="176" rgb="160 199 235"/>
    <color index="177" rgb="163 202 236"/>
    <color index="178" rgb="166 204 237"/>
    <color index="179" rgb="169 206 238"/>
    <color index="180" rgb="172 208 238"/>
    <color index="181" rgb="175 211 239"/>
    <color index="182" rgb="179 213 240"/>
    <color index="183" rgb="182 215 241"/>
    <color index="184" rgb="185 217 241"/>
    <color index="185" rgb="188 219 242"/>
    <color index="186" rgb="191 222 243"/>
    <color index="187" rgb="194 224 244"/>
    <color index="188" rgb="197 226 245"/>
    <color index="189" rgb="200 228 245"/>
    <color index="190" rgb="203 231 246"/>
    <color index="191" rgb="206 233 247"/>
    <color index="192" rgb="209 235 248"/>
    <color index="193" rgb="212 237 248"/>
    <color index="194" rgb="215 240 249"/>
    <color index="195" rgb="218 242 250"/>
    <color index="196" rgb="221 244 251"/>
    <color index="197" rgb="225 246 252"/>
    <color index="198" rgb="228 248 252"/>
    <color index="199" rgb="231 251 253"/>
    <color index="200" rgb="234 253 254"/>
    <color index="201" rgb="236 254 253"/>
    <color index="202" rgb="236 253 249"/>
    <color index="203" rgb="237 251 244"/>
    <color index="204" rgb="237 250 240"/>
    <color index="205" rgb="237 248 235"/>
    <color index="206" rgb="238 247 231"/>
    <color index="207" rgb="238 245 226"/>
    <color index="208" rgb="238 244 222"/>
    <color index="209" rgb="239 242 217"/>
    <color index="210" rgb="239 241 213"/>
    <color index="211" rgb="239 239 208"/>
    <color index="212" rgb="240 238 204"/>
    <color index="213" rgb="240 236 199"/>
    <color index="214" rgb="240 235 195"/>
    <color index="215" rgb="241 233 191"/>
    <color index="216" rgb="241 232 186"/>
    <color index="217" rgb="241 230 182"/>
    <color index="218" rgb="241 229 177"/>
    <color index="219" rgb="242 227 173"/>
    <color index="220" rgb="242 226 168"/>
    <color index="221" rgb="242 224 164"/>
    <color index="222" rgb="243 223 159"/>
    <color index="223" rgb="243 221 155"/>
    <color index="224" rgb="243 220 150"/>
    <color index="225" rgb="244 218 146"/>
    <color index="226" rgb="244 217 141"/>
    <color index="227" rgb="244 215 137"/>
    <color index="228" rgb="245 214 132"/>
    <color index="229" rgb="245 212 128"/>
    <color index="230" rgb="245 211 123"/>
    <color index="231" rgb="246 209 119"/>
    <color index="232" rgb="246 208 114"/>
    <color index="233" rgb="246 206 110"/>
    <color index="234" rgb="247 205 105"/>
    <color index="235" rgb="247 203 101"/>
    <color index="236" rgb="247 202 96"/>
    <color index="237" rgb="247 200 92"/>
    <color index="238" rgb="248 199 87"/>
    <color index="239" rgb="248 197 83"/>
    <color index="240" rgb="248 196 78"/>
    <color index="241" rgb="249 194 74"/>
    <color index="242" rgb="249 193 69"/>
    <color index="243" rgb="249 191 65"/>
    <color index="244" rgb="250 190 61"/>
    <color index="245" rgb="250 188 56"/>
    <color index="246" rgb="250 187 52"/>
    <color index="247" rgb="251 185 47"/>
    <color index="248" rgb="251 184 43"/>
    <color index="249" rgb="251 182 38"/>
    <color index="250" rgb="252 181 34"/>
    <color index="251" rgb="252 179 29"/>
    <color index="252" rgb="252 178 25"/>
    <color index="253" rgb="253 176 20"/>
    <color index="254" rgb="253 175 16"/>
    <color index="255" rgb="253 173 11"/>"""

    gradient_elements = gradient_text.split('\n')
    for e in gradient_elements:
        etree_element.append(etree.fromstring(e))

    return etree_element