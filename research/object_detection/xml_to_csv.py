import os
import glob
import random
import pandas as pd
import xml.etree.ElementTree as ET
from tqdm import tqdm

class Xml_to_csv():
    def __init__(self, folders):
        self.train_total = 0
        self.test_total = 0
        self.train_list = []
        self.test_list = []
        self.test_percentage = 0.1
    
    def split(self):
        for folder in tqdm(folders):
            random.seed(4)
            dataset = glob.glob('{}/*.xml'.format(folder))
            split_num = int(len(dataset)*self.test_percentage)
            sample = random.sample(dataset, split_num)
            
            for test in sample:
                self.test_total += 1
                self.xml_to_list(test, self.test_list)
                dataset.remove(test)

            for train in dataset:
                self.train_total += 1
                self.xml_to_list(train, self.train_list)
    
    def xml_to_list(self, xml, lst):
        tree = ET.parse(xml)
        root = tree.getroot()
        for member in root.findall('object'):
            if member[2].text == 'vehicle':  # name
                value = ('JPEGImages/' + member[0].text,  # filename
                int(member[1][0].text),          # size: width
                int(member[1][1].text),          # size: height
                member[2].text,                  # name
                int(member[3][0].text),          # bndbox: xmin
                int(member[3][1].text),          # bndbox: ymin
                int(member[3][2].text),          # bndbox: xmax
                int(member[3][3].text))          # bndbox: ymax
                lst.append(value)
    
    def list_to_df(self):
        column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
        self.train_df = pd.DataFrame(self.train_list, columns=column_name)
        self.test_df = pd.DataFrame(self.test_list, columns=column_name)
    
    def df_to_csv(self):
        self.train_df.to_csv(('training/train_labels.csv'), index=None)
        self.test_df.to_csv(('training/test_labels.csv'), index=None)
        
    def main(self):
        self.split()
        self.list_to_df()
        self.df_to_csv()
        print('Train: {}, Test: {}'.format(self.train_total, self.test_total))
        print('Done.')

if __name__ == '__main__':
    folders = glob.glob('images/Annotations/All/*')
    
    # Filters
    folders.remove('images/Annotations/All/vehicles_nighttime')
    
    xml_to_csv = Xml_to_csv(folders)
    xml_to_csv.main()