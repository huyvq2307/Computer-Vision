import matplotlib.pyplot as plt

def read_yolo_data(yolo_file):
    points = []
    with open(yolo_file, 'r') as f:
        lines = f.readlines()
        for line in lines:
            data = line.strip().split()
            if len(data) >= 3:  # Cần ít nhất 3 giá trị: class_id, x, y
                class_id = int(data[0])
                xy_pairs = [(float(data[i]), float(data[i+1])) for i in range(1, len(data), 2)]
                points.append((class_id, xy_pairs))
    return points

def show_image_with_absolute_points(image_path, points, image_width, image_height):
    image = plt.imread(image_path)
    plt.imshow(image)
    for class_id, xy_pairs in points:
        x_abs = [x * image_width for x, _ in xy_pairs]
        y_abs = [y * image_height for _, y in xy_pairs]
        plt.plot(x_abs, y_abs, 'ro')  # 'ro' để vẽ chấm màu đỏ
    plt.show()

# Thay đổi đường dẫn tới file output.txt và ảnh tại đây
output_file = r"*\con20ft (1).txt"
image_path = r"*\con20ft (1).JPG"
image_width = 2048  # Thay đổi kích thước theo kích thước thực của ảnh
image_height = 1536  # Thay đổi kích thước theo kích thước thực của ảnh

# Đọc các điểm từ tệp output.txt
points = read_yolo_data(output_file)

# Hiển thị ảnh và các điểm
show_image_with_absolute_points(image_path, points, image_width, image_height)
