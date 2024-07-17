from ultralytics import YOLO
import cv2 as cv


model = YOLO("*\yolov9c_100e.pt")
img_path = r"*\con40ft (9).JPG"
img = cv.imread(img_path)
img = cv.resize(img, (600,600))

model.predict(source= img, show = False, show_labels = False,
              conf = 0.7, save_txt = True, save_crop = False, line_width  = 2, save= True)