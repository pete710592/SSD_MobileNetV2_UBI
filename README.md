# SSD_MobileNetV2_UBI  
Tensorflow implementation of object detections using lightweight models.  
 - [Part 1: Environment setup](https://github.com/pete710592/SSD_MobileNetV2_UBI#part-1-environment-setup)  
 - [Part 2: Data preprocessing](https://github.com/pete710592/SSD_MobileNetV2_UBI#part-2-data-preprocessing)  
 - [Part 3: Ready for training](https://github.com/pete710592/SSD_MobileNetV2_UBI#part-3-ready-for-training)  
 - [Part 4: Export frozen inference graph for TensorFlow Lite](https://github.com/pete710592/SSD_MobileNetV2_UBI#part-4-export-frozen-inference-graph-for-tensorflow-lite)  

## Part 1: Environment setup  
This code was tested with Tensorflow 1.15.0, CUDA 10.0 and Ubuntu 16.04.  
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
### 2-1. Download dataset  
Download vehicle-dataset at ```images```.  
```
cd ~/SSD_MobileNetV2_UBI/research/object_detection
git clone https://github.com/pete710592/UBI_Dataset.git images
```  

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

### 3-3. Generate ```training/train_labels.csv``` & ```training/test_labels.csv```  
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
python generate_tfrecord.py \
    --csv_input=training/train_labels.csv \
    --image_dir=images \
    --output_path=training/train.record  
```  
```shell
python generate_tfrecord.py \
    --csv_input=training/test_labels.csv \
    --image_dir=images \
    --output_path=training/test.record
```  

### 3-5. Start training  
```shell
python train.py \
    --logtostderr \
    --train_dir=training \
    --pipeline_config_path=training/ssd_mobilenet_v2_quantized_300x300_coco.config
```  

## Part 4: Export frozen inference graph for TensorFlow Lite  
The model can be exported for conversion to TensorFlow Lite using the export_tflite_ssd_graph.py script. First, create a folder in ```./object_detection``` called ```TFLite_model``` by issuing:  
```shell
cd ~/SSD_MobileNetV2_UBI/research/object_detection
mkdir TFLite_model
```  

### 4-1. Export the model for TensorFlow Lite:  
Generate ```tflite_graph.pb``` and ```tflite_graph.pbtxt```.  
```shell
python export_tflite_ssd_graph.py \
    --pipeline_config_path='training/ssd_mobilenet_v2_quantized_300x300_coco.config' \
    --trained_checkpoint_prefix='training/model.ckpt-xxxx' \
    --output_directory='TFLite_model' \
    --add_postprocessing_op=true
```  
Generate ```detect.tflite```.  
```shell
tflite_convert \
    --graph_def_file='TFLite_model/tflite_graph.pb' \
    --output_file='TFLite_model/detect.tflite' \
    --output_format=TFLITE \
    --input_shapes=1,300,300,3 \
    --input_arrays=normalized_input_image_tensor \
    --output_arrays='TFLite_Detection_PostProcess','TFLite_Detection_PostProcess:1','TFLite_Detection_PostProcess:2','TFLite_Detection_PostProcess:3'  \
    --inference_type=QUANTIZED_UINT8 \
    --mean_values=128 \
    --std_dev_values=127 \
    --change_concat_input_ranges=false \
    --allow_custom_ops
```  

## Reference  
1. https://github.com/EdjeElectronics/TensorFlow-Object-Detection-API-Tutorial-Train-Multiple-Objects-Windows-10  
2. https://github.com/EdjeElectronics/TensorFlow-Lite-Object-Detection-on-Android-and-Raspberry-Pi  
