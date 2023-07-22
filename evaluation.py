import numpy as np
import cv2
import os

from skin_detect import *

ground_true_path = "/home/nhattan/Desktop/skin_detection/ground_true"
predict_path = "/home/nhattan/Desktop/skin_detection/predict"


image_list_predict =sorted(os.listdir(predict_path))
image_list_gt = sorted(os.listdir(ground_true_path))

result = [0,0,0,0,0,0]
for i in range (0,len(image_list_predict)) :

    # tải ảnh dự đoán
    image_predict_path = os.path.join(predict_path, image_list_predict[i])
    img_predict = cv2.imread(image_predict_path)
    
    # tải ảnh đúng 
    image_gt_path = os.path.join(ground_true_path, image_list_gt[i])
    img_gt = cv2.imread(image_gt_path)
    temp = count_TP_TF_FN_FP(img_predict, img_gt)
    result = np.add(temp, result)

print(result)