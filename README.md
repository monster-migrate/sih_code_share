# SIH Models Training Process and Weights Tuning Guide  
<hr/>  

## Gender Classification Model  
 - Get the [Dataset](https://www.kaggle.com/datasets/cashutosh/gender-classification-dataset) here. It has 23k + closeups for male and female each. That should be enough for closeup face detection.
 - We will be using YOLOv5 for the prototype version. You can find the Yolo Weights files --> [HERE](https://github.com/ultralytics/yolov5/releases) <--  
 (Use YOLOv5s-seg or YOLOv5n-seg for faster training and detection)
 - We will also need the [YOLOv5 Repository](https://github.com/ultralytics/yolov5) as they have already created nice training and testing scripts, very useful.  
 <mark>IMPORTANT:</mark>USE PyTorch v2.3.1 and TorchVision v0.18.1.  
 A requirements.txt file can be found inside this yolov5 repository that you just cloned. We will be using almost all of the mentioned package versions. Almost. This requirements.txt installs PyTorch v2.4.0 which has some problems with windows it shows a missing .dll file issue and I do not want to mess around with dll files. So I used pytorch v2.3.1, along with torchvision v0.18.1 which is compatible with our pytorch version, and it works just fine.  
 ```pip install torch==2.3.1 torchvision==0.18.1```
 - Next, if you are on windows, there will be a problem with POSIX complaint path system so inside the cloned yolov5 repository, edit the detect.py file and add the following just below import pathlib, somewhere around line 37:  
 ```
 temp = pathlib.PosixPath  
 pathlib.PosixPath = pathlib.WindowsPath
 ```  
 - We also need to create a config file for our dataset. Create a file dataset_config.yaml and add the following to it:
 ```
    path: /path/to/output/folder # Just change this line
    # Do not change the paths of train, test and val as they are relative to path value and will work
    train: ./images/train
    test: ./images/test
    val: ./images/val

    nc: 2  # Number of classes (male, female)
    names: [ 'male', 'female']
 ```

Before we start training, there are some things to take care of. Firstly, the dataset we downloaded has disorganised file naming, we need to fix that. In the utils folder we have a python file called rename files, run it like:  
```python rename_files.py /path/to/dir1 /path/to/dir2```  
Better test it on a dummy folder before doing the renaming on 50,000+ files.  

Now, to train on custom data, we need to organize our dataset files in a specific format, like so:  
cifar-10-/  
|  
|-- train/  
|&nbsp;&nbsp;&nbsp;&nbsp;|-- airplane/  
|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|-- 10008_airplane.png  
|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|-- 10009_airplane.png  
|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|-- ...  
|&nbsp;&nbsp;&nbsp;&nbsp;|  
|&nbsp;&nbsp;&nbsp;&nbsp;|-- automobile/  
|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|-- 1000_automobile.png  
|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|-- 1001_automobile.png  
|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|-- ...  
|&nbsp;&nbsp;&nbsp;&nbsp;|  
|&nbsp;&nbsp;&nbsp;&nbsp;|-- ...  

We also need a labels folder which is primarily used for multi-object detection in a single frame. All this will be done in organiseTheData.py like so:  
```python organizeTheData.py --dataset_dir='/path/to/GenderClassifficationDataset/' --output_dir='path/to/output_dir/' --classes='{"male": 0, "female": 1}' --update_interval 1000```   

It takes some time so go get some coffee or something.  

Now we can finally start the training process. Everything is done, now go inside the clone yolov5 repo, just run:  
``` python train.py --img 96 --batch 16 --epochs 3 --data /path/to/dataset_config.yaml --cfg /path/to/yolov5s.yaml --weights ../path/to/yolov5s-seg.pt ```  

To test the model, use the detect.py file:  
```python detect.py --weights runs/train/exp11/weights/best.pt --img 96 --conf 0.25 --source 0```  
The ```--source 0``` is for camera, if you want to use a video file, use the path to the video file as the arument to source.  
The best weights file will be saved in the folder runs/train/expxx where xx represents the last folder number, in our example it was exp11