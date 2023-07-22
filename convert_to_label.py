from PIL import Image
import os

input_folder = "/home/nhattan/Desktop/skin_detection/GT"
output_folder = "/home/nhattan/Desktop/skin_detection/label"

# Lấy danh sách tất cả các file ảnh trong thư mục đầu vào
# Lấy danh sách tất cả các file ảnh trong thư mục đầu vào
image_list = os.listdir(input_folder)

for image_name in image_list:
    # Kiểm tra xem file có phải là file ảnh hay không
    if image_name.endswith(".jpg") or image_name.endswith(".jpeg") or image_name.endswith(".png"):

        # Đọc file ảnh và chuyển đổi sang ảnh đen trắng với giá trị pixel là 0 hoặc 255
        image_path = os.path.join(input_folder, image_name)
        im = Image.open(image_path).convert('L')
        im = im.point(lambda x: 0 if x < 1 else 255, '1')

        # Lưu ảnh mới vào thư mục đầu ra với tên tương ứng
        output_path = os.path.join(output_folder, image_name)
        im.save(output_path)