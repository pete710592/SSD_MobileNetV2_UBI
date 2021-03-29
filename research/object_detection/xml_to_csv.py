import os
import glob
import pandas as pd
import xml.etree.ElementTree as ET
from tqdm import tqdm

def xml_to_csv(path):
    xml_list = []
    for xml_folder in tqdm(glob.glob(path + '/*')):
        for xml_file in glob.glob('{}/*.xml'.format(xml_folder)):
            tree = ET.parse(xml_file)
            root = tree.getroot()
            for member in root.findall('object'):
                if member[1].text == 'vehicle':
                    value = ('JPEGImages/'+member[0].text,
                             1920,
                             1080,
                             member[1].text,
                             int(member[2][0].text),
                             int(member[2][1].text),
                             int(member[2][2].text),
                             int(member[2][3].text)
                             )
                    xml_list.append(value)
    
    column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
    xml_df = pd.DataFrame(xml_list, columns=column_name)
    return xml_df


def main():
    for folder in ['train','test']:
        image_path = os.path.join(os.getcwd(), 'images/{}/Annotations/All'.format(folder))
        xml_df = xml_to_csv(image_path)
        xml_df.to_csv(('images/' + folder + '_labels.csv'), index=None)
        print('Successfully converted xml to csv.')

main()