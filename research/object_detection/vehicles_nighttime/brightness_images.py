import os
import cv2
import glob
import numpy as np
from tqdm import tqdm

class Modify_lightness():
    def __init__(self, src=None, out=None):
        self.src = src
        self.out = out
        
    def get_lightness(self):
        hsv_image = cv2.cvtColor(self.src, cv2.COLOR_BGR2HSV)
        lightness = hsv_image[:,:,2].mean()
        return lightness
    
    def compute(self, min_percentile, max_percentile):
        max_percentile_pixel = np.percentile(self.src, max_percentile)
        min_percentile_pixel = np.percentile(self.src, min_percentile)
        return max_percentile_pixel, min_percentile_pixel

    def augment(self, src):
        self.src = src
        if self.get_lightness() > 130:
            print("Brightness enough, pass.")
        max_percentile_pixel, min_percentile_pixel = self.compute(1, 99)

        self.src[self.src >= max_percentile_pixel] = max_percentile_pixel
        self.src[self.src <= min_percentile_pixel] = min_percentile_pixel

        self.out = np.zeros(self.src.shape, self.src.dtype)
        cv2.normalize(self.src, self.out, 0, 255, cv2.NORM_MINMAX)
        
        return self.out
    
    def plot_src_out(self):
        plt.figure(figsize=(16, 9))
        
        plt.subplot(221)
        plt.title('Original image')
        plt.xticks([])
        plt.yticks([])
        img = cv2.cvtColor(self.src, cv2.COLOR_BGR2RGB)
        plt.imshow(img)

        plt.subplot(222)
        plt.title('Brightness & reduce noise')
        plt.xticks([])
        plt.yticks([])
        img = cv2.cvtColor(self.out, cv2.COLOR_BGR2RGB)
        plt.imshow(img)
    
    def plot_color_histogram(self):
        ylim = 0
        plt.subplot(223)
        gray = cv2.cvtColor(self.src, cv2.COLOR_BGR2GRAY)
        hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
        hist = hist / sum(hist)
        ylim = hist.max()
        plt.ylim(0, ylim)
        plt.bar(range(1,257), hist[:, 0])

        plt.subplot(224)
        gray = cv2.cvtColor(self.out, cv2.COLOR_BGR2GRAY)
        hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
        hist = hist / sum(hist)
        plt.ylim(0, ylim)
        plt.bar(range(0,256), hist[:, 0])

if __name__ == '__main__':
    modify_lightness = Modify_lightness()
    images = glob.glob('../images/JPEGImages/All/Night_02.mp4/*.jpg')
    sorted(images)

    # confirm whether the file path exists
    save_dir = 'Night_02b.mp4'
    if not os.path.isdir(save_dir):
        os.makedirs(save_dir)
    
    # brightness images
    for image_path in tqdm(images):
        src = cv2.imread(image_path)
        out = modify_lightness.augment(src)
        save_file = image_path.split('/')[-1].replace('.mp4', 'b.mp4')
        cv2.imwrite(os.path.join(save_dir, save_file), out)