import os
import json

def convert_to_yolo_segment(json_file, image_width, image_height):
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    classes = {'seck': 0} 
    
    yolo_full = ""
    for shape in data['shapes']:
        if shape['label'] in classes:
            class_id = classes[shape['label']]
            yolo_full += f"{class_id} "
            points = shape['points']
            for point in points:
                x = point[0] / image_width
                y = point[1] / image_height
                yolo_full += f"{x} {y} "
            yolo_full += "\n"
    
    return yolo_full

# Thư mục chứa các file JSON
json_dir = r"*/Containerf40/json" 
# Thư mục đích cho các file txt
output_dir = r"*/Containerf40/text"

# Kiểm tra nếu thư mục đích không tồn tại, tạo mới
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

image_width = 2048  # Thay đổi kích thước theo kích thước thực của ảnh
image_height = 1536


# Duyệt qua các file trong thư mục JSON
for filename in os.listdir(json_dir):
    if filename.endswith('.json'):
        json_file = os.path.join(json_dir, filename)
        output_filename = os.path.splitext(filename)[0] + ".txt"
        output_file = os.path.join(output_dir, output_filename)
        
        # Chuyển đổi và ghi ra file txt
        yolo_data = convert_to_yolo_segment(json_file, image_width, image_height)
        with open(output_file, "w") as f:
            f.write(yolo_data)
