"""
    Convert txt files to xml format.
    dataset download: https://github.com/ntnu-arl/vehicles-nighttime
    ========================================
    Input: gt10913.txt
    Output: All/Vehicles_NightTime/*.xml
    ========================================
"""

import os
from tqdm import tqdm

class Xml_writer():
    def __init__(self, filename):
        self.filename = filename
        self.write_title()
    
    def write_title(self):
        self.f = open('All/Vehicles_NightTime/{}.xml'.format(self.filename), 'a')
        self.f.write('<?xml version="1.0" encoding="utf-8"?>\n')
        self.f.write('<annotation>\n')

    def write_object(self, x, y, w, h):
        self.f.write('  <object>\n')
        self.f.write('    <filename>All/Vehicles_NightTime/{}.jpg</filename>\n'.format(self.filename))
        self.f.write('    <name>vehicle</name>\n')
        self.f.write('    <bndbox>\n')
        self.f.write('      <xmin>{}</xmin>\n'.format(x))
        self.f.write('      <ymin>{}</ymin>\n'.format(y))
        self.f.write('      <xmax>{}</xmax>\n'.format(x+w))
        self.f.write('      <ymax>{}</ymax>\n'.format(y+h))
        self.f.write('    </bndbox>\n')
        self.f.write('  </object>\n')

    def write_end(self):
        self.f.write('</annotation>\n')
        self.f.close()

# read .txt ground truth
gt10913 = open('gt10913.txt', 'r')
gt = gt10913.readlines()

# confirm whether the file path exists
if not os.path.isdir('All/Vehicles_NightTime'):
    os.makedirs('All/Vehicles_NightTime')

for file in tqdm(gt):
    elements = file.split(' ')
    file_idx = int(elements[0])
    object_num = int(elements[1])
    if file_idx == 254 or file_idx == 422:
        # missing jpg files, skipped
        print('img_{}.jpg not found, skipping.'.format(file_idx))
        continue
    elif (2006 < file_idx < 10000):
        filename = 'img_0{}'.format(file_idx)
    else:
        filename = 'img_{}'.format(file_idx)
    
    # xml writer
    xml_writer = Xml_writer(filename)
    for idx in range(object_num):
        xml_writer.write_object(int(elements[idx+2]), int(elements[idx+3]), int(elements[idx+4]), int(elements[idx+5]))
    xml_writer.write_end()