## Part 1: Environment setup  
## 1-1. Install necessary packages by issuing the following commands:  
```shell
pip install tensorflow-object-detection-api
pip install tf-slim==1.0
pip install tensorflow-gpu==1.15
```  

## 1-2. Download this repository from GitHub  
```shell
cd
git clone https://github.com/pete710592/SSD_MobileNetV2_UBI.git
```  

## 1-3. Run setup  
```shell
cd ~/SSD_MobileNetV2_UBI/research/slim
python setup.py build
python setup.py install
```  

## Part 2: Data preprocessing  

## Part 3: Ready for training  
First, moving your path to:  
```shell
cd ~/SSD_MobileNetV2_UBI/research/object_detection
```  

### 3-1. Config ```training/labelmap.pbtxt```  
```
item {
  id: 1
  name: 'vehicle'
}
```  

### 3-2. Config ```training/ssd_mobilenet_v2_quantized_300x300_coco.config```  
 - Line 9. Change num_classes to the number of different objects you want the classifier to detect. Ex: ```num_classes: 1```  
 - Line 141. Change batch_size. The smaller batch size will prevent OOM (Out of Memory) errors during training. Ex: ```batch_size: 6```  
 - Line 156. Change fine_tune_checkpoint to: ```/root/notebooks/SSD_MobileNetV2_UBI/research/object_detection/pretrained_model/ssd_mobilenet_v2_quantized_300x300_coco_2019_01_03/model.ckpt```  
 - Line 175. Change input_path to: ```/root/notebooks/SSD_MobileNetV2_UBI/research/object_detection/training/train.record```  
 - Line 177. Change label_map_path to: ```/root/notebooks/SSD_MobileNetV2_UBI/research/object_detection/training/labelmap.pbtxt```  
 - Line 181. Change num_examples to the number of images you have in the images/test directory. Ex: ```num_examples: 9951```  
 - Line 189. Change input_path to: ```/root/notebooks/SSD_MobileNetV2_UBI/research/object_detection/training/test.record```  
 - Line 191. Change label_map_path to: ```/root/notebooks/SSD_MobileNetV2_UBI/research/object_detection/training/labelmap.pbtxt```  

### 3-3. Generate ```images/train_labels.csv``` & ```images/test_labels.csv```  
```shell
python xml_to_csv.py
```  

### 3-4. Generate tfrecorder  
Config ```generate_tfrecord.py``` at Line 36.  
```python
# TO-DO replace this with label map
def class_text_to_int(row_label):
    if row_label == 'vehicle':
        return 1
    else:
        None
```  

Then, generate ```train.record``` and ```test.record```.  
```shell
python generate_tfrecord.py --csv_input=images/train_labels.csv --image_dir=images/train --output_path=training/train.record
python generate_tfrecord.py --csv_input=images/test_labels.csv --image_dir=images/test --output_path=training/test.record
```  

### 3-5. Start training  
```shell
python train.py --logtostderr –train_dir=training/ --pipeline_config_path=training/ssd_mobilenet_v2_quantized_300x300_coco.config
```  

## Part 4: Export frozen inference graph for TensorFlow Lite  
The model can be exported for conversion to TensorFlow Lite using the export_tflite_ssd_graph.py script. First, create a folder in ```./object_detection``` called ```TFLite_model``` by issuing:  
```shell
cd ~/SSD_MobileNetV2_UBI/research/object_detection
mkdir TFLite_model
```  

Export the model for TensorFlow Lite:  
```shell
python export_tflite_ssd_graph.py \
    --pipeline_config_path='training/ssd_mobilenet_v2_quantized_300x300_coco.config' \
    --trained_checkpoint_prefix='training/model.ckpt-xxxx' \
    --output_directory='TFLite_model' \
    --add_postprocessing_op=true
```  

## Reference  
1. https://github.com/EdjeElectronics/TensorFlow-Object-Detection-API-Tutorial-Train-Multiple-Objects-Windows-10  
2. https://github.com/EdjeElectronics/TensorFlow-Lite-Object-Detection-on-Android-and-Raspberry-Pi  
