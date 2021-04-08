"""
    calculate xml & jpg files in images/
    ========================================
    Input: None
    Output: Number of dataset
    ========================================
"""

import glob

class Calculate_dataset():
    def __init__(self):
        self.xml_total = 0
        self.jpg_total = 0
        self.xml_folders = glob.glob('images/Annotations/All/*')
        self.jpg_folders = glob.glob('images/JPEGImages/All/*')
    
    def remove(self, folders):
        for folder in folders:
            self.xml_folders.remove('images/Annotations/All/{}'.format(folder))
            self.jpg_folders.remove('images/JPEGImages/All/{}'.format(folder))
    
    def calculate(self):
        for folder in self.xml_folders:
            xml = glob.glob(f'{folder}/*.xml')
            self.xml_total += len(xml)
        
        for folder in self.jpg_folders:
            jpg = glob.glob(f'{folder}/*.jpg')
            self.jpg_total += len(jpg)
        
        return self.xml_total, self.jpg_total

if __name__ == '__main__':
    calculate_dataset = Calculate_dataset()
    calculate_dataset.remove(['vehicles_nighttime'])
    xml, jpg = calculate_dataset.calculate()
    print('xml: {}, jpg: {}'.format(xml, jpg))