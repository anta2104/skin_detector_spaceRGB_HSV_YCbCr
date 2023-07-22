from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap, QColor
from PyQt5.QtWidgets import QApplication
import cv2
from skin_detect import *
image_name = "1.jpg"

if __name__ == "__main__":
    app = QApplication([])
    image = QImage("1.jpg")
    flags = Mode.HSV | Mode.RGB | Mode.YCbCr | Mode.Full
    processor = ImageProcessor(image, flags)
    processed_image = processor.process()
    processed_image.save("processed_image.jpg")
    # label.show()
    app.exec_()