# Data
* First I label by lableme -> export file json -> file json cannot use to train yolo, so I need convert json to txt by file Json2txt.py
* Data is 24 original images, I will use this image as a test image
* I have upgraded to 480 images with 408 train images and 48 valid images
* I use the yolov9c-seg.pt model to use with this project because this problem has many corners that are squeezed, spread out.... so segment will be more optimal than detect.

# Model

* I train with 100 epochs with a training image size of 600x600
* I use colab to train because the data is quite large and my local machine cannot train it.
