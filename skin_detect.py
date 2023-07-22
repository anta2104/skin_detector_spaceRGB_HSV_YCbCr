from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap, QColor
from PyQt5.QtWidgets import QApplication
import cv2
from enum import Flag, auto
import os


# Chọn không gian màu 
class Mode(Flag):
    HSV = auto()
    RGB = auto()
    YCbCr = auto()
    Full = auto()

class ImageProcessor:
    def __init__(self, img, flags):
        self.img = img
        self.flags = flags

    def process(self):
        for w in range(self.img.width()):
            for h in range(self.img.height()):
                pixel = self.img.pixel(w, h)
                r, g, b, _ = QColor(pixel).getRgb()

                Y = 0.299*r + 0.587*g + 0.114*b
                Cb = -0.1687*r - 0.3313*g + 0.5*b + 128
                Cr = 0.5*r - 0.4187*g - 0.0813*b + 128

                pixVal = 255
                hsvMask = False
                rgbMask = False
                YCbCrMask = False

                if self.flags & Mode.HSV:
                    hsv = QColor(pixel).toHsv()
                    hsvMask = hsv.hue() >= 0 and hsv.hue() <= 50 \
                            and hsv.saturationF() >= 0.23 and hsv.saturationF() <= 0.68

                if self.flags & Mode.RGB:
                    rgbMask = r > 95 and g > 40 and b > 20 and r > g and r > b and abs(r - g) > 15

                if self.flags & Mode.YCbCr:
                    YCbCrMask = Cr > 135 and Cb > 85 and Y > 80 \
                                and Cr <= (1.5862*Cb)+20 and Cr >= (0.3448*Cb)+76.2069 \
                                and Cr >= (-4.5652*Cb)+234.5652 and Cr <= (-1.15*Cb)+301.75 \
                                and Cr <= (-2.2857*Cb)+432.85

                if self.flags & Mode.Full:
                    pixVal *= (rgbMask and YCbCrMask) or (rgbMask and hsvMask)
                else:
                    pixVal *= rgbMask or YCbCrMask or hsvMask

                self.img.setPixelColor(w, h, QColor(pixVal, pixVal, pixVal))

        return QPixmap.fromImage(self.img)
    
# Đếm số lượng các lớp    
def count_TP_TF_FN_FP(img1, img2) :

    # Chuyển ảnh sang ảnh đen trắng
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)


    # Ảnh 1 là dự đoán , ảnh 2 là nhãn
    num_black_pixels = cv2.countNonZero(gray1)
    num_white_pixels_1 = gray1.size - num_black_pixels

    num_black_pixels = cv2.countNonZero(gray2)
    num_white_pixels_2 = gray2.size - num_black_pixels

    # Tính số lượng pixel đen giống nhau
    TN = cv2.countNonZero(cv2.bitwise_and(gray1, gray2))

    # Tính số lượng pixel trắng giống nhau
    TP = cv2.countNonZero(cv2.bitwise_or(cv2.bitwise_not(gray1), cv2.bitwise_not(gray2)))

    # Tính số lượng pixel của ảnh 1 là trắng và ảnh 2 là đen
    FP = cv2.countNonZero(cv2.bitwise_and(cv2.bitwise_not(gray1), gray2))

    # Tính số lượng pixel của ảnh 1 là đen và ảnh 2 là trắng
    FN = cv2.countNonZero(cv2.bitwise_and(gray1, cv2.bitwise_not(gray2)))

    # In kết quả
    return [TN, TP , FP, FN , num_white_pixels_1, num_white_pixels_2]


if __name__ == "__main__":
    app = QApplication([])

    input_folder = "/home/nhattan/Desktop/skin_detection/photo"
    output_folder = "/home/nhattan/Desktop/skin_detection/predict"
    image_list = os.listdir(input_folder)

    for image_name in image_list:
        image_path = os.path.join(input_folder, image_name)
        image = QImage(image_path)
        flags = Mode.HSV | Mode.RGB | Mode.YCbCr | Mode.Full
        processor = ImageProcessor(image, flags)
        processed_image = processor.process()

        output_path = os.path.join(output_folder, image_name)
        print(output_path)
        processed_image.save(output_path)

    # label = QLabel()
    # label.setPixmap(processed_image)
    # label.setAlignment(Qt.AlignCenter)
    # label.show()
    app.exit()