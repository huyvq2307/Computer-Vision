import os
import cv2
import numpy as np

def read_yolo_data(yolo_file):
    points = []
    with open(yolo_file, 'r') as f:
        for line in f:
            data = line.strip().split()
            if len(data) >= 3:
                class_id = int(data[0])
                xy_pairs = [(float(data[i]), float(data[i+1])) for i in range(1, len(data), 2)]
                points.append((class_id, xy_pairs))
    return points

def rotate_point(point, angle, center):
    angle_rad = np.deg2rad(angle)
    new_x = (point[0] - center[0]) * np.cos(angle_rad) - (point[1] - center[1]) * np.sin(angle_rad) + center[0]
    new_y = (point[0] - center[0]) * np.sin(angle_rad) + (point[1] - center[1]) * np.cos(angle_rad) + center[1]
    return new_x, new_y

def rotate_image(image, angle):
    h, w = image.shape[:2]
    center = (w / 2, h / 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    return cv2.warpAffine(image, M, (w, h))

def rotate_points(points, angle, center, image_width, image_height):
    rotated_points = []
    for class_id, xy_pairs in points:
        rotated_xy_pairs = [rotate_point((x * image_width, y * image_height), -angle, center) for x, y in xy_pairs]
        rotated_points.append((class_id, rotated_xy_pairs))
    return rotated_points

def adjust_brightness(image, factor):
    return np.clip(image.astype(np.int16) + factor, 0, 255).astype(np.uint8)

def add_noise(image, noise_type='gaussian', mean=0, sigma=5, amount=0.01):
    if noise_type == 'gaussian':
        noise = np.random.normal(mean, sigma, image.shape).astype(np.uint8)
        noisy_image = cv2.add(image, noise)
    elif noise_type == 'salt_pepper':
        noisy_image = np.copy(image)
        num_salt = np.ceil(amount * image.size * 0.2)
        coords = [np.random.randint(0, i - 1, int(num_salt)) for i in image.shape]
        noisy_image[coords[0], coords[1], :] = 255

        num_pepper = np.ceil(amount * image.size * 0.2)
        coords = [np.random.randint(0, i - 1, int(num_pepper)) for i in image.shape]
        noisy_image[coords[0], coords[1], :] = 0
    else:
        raise ValueError("Invalid noise type. Choose from 'gaussian' or 'salt_pepper'.")
    return noisy_image

def save_rotated_points_as_new_output(points, output_file, image_width, image_height):
    with open(output_file, 'w') as f:
        for class_id, xy_pairs in points:
            line = f"{class_id} " + " ".join(f"{x / image_width} {y / image_height}" for x, y in xy_pairs) + "\n"
            f.write(line)

def rotate_image_and_save(image_path, output_file, angle, output_image_folder, output_output_folder, image_width, image_height, brightness_factor, add_noise_flag):
    points = read_yolo_data(output_file)
    center = (image_width / 2, image_height / 2)
    image = cv2.imread(image_path)

    if brightness_factor != 0:
        image = adjust_brightness(image, brightness_factor)

    if add_noise_flag:
        image = add_noise(image, noise_type= "salt_pepper")

    rotated_image = rotate_image(image, angle)
    rotated_points = rotate_points(points, angle, center, image_width, image_height)

    rotated_image_name = os.path.splitext(os.path.basename(image_path))[0] + f"_angle{angle}_brightness{brightness_factor}.jpg"
    rotated_output_name = os.path.splitext(os.path.basename(output_file))[0] + f"_angle{angle}_brightness{brightness_factor}.txt"

    cv2.imwrite(os.path.join(output_image_folder, rotated_image_name), rotated_image)
    save_rotated_points_as_new_output(rotated_points, os.path.join(output_output_folder, rotated_output_name), image_width, image_height)

def process_images(input_image_folder, output_file_folder, output_image_folder, output_output_folder, image_width, image_height, angle_range, brightness_range, add_noise_flag):
    for angle, brightness in zip(range(angle_range[0], angle_range[1] + 1), range(brightness_range[0], brightness_range[1] + 1)):
        for filename in os.listdir(input_image_folder):
            if filename.endswith(".JPG"):
                image_path = os.path.join(input_image_folder, filename)
                output_file = os.path.join(output_file_folder, os.path.splitext(filename)[0] + ".txt")
                rotate_image_and_save(image_path, output_file, angle, output_image_folder, output_output_folder, image_width, image_height, brightness, add_noise_flag)

# Input parameters
input_image_folder_images = r"*\Containerf20\images"
input_file_folder_txt = r"*\Containerf20\text"
output_image_folder_valid = r"*\Data_valid\images"
output_output_folder_valid = r"*\Data_valid\labels"

output_image_folder_train = r"*\Data_train\images"
output_output_folder_train = r"*\Data_train\labels"

image_width = 2048
image_height = 1536

# Get input ranges from user
angle_range = list(map(int, input("Enter angle range (e.g., -10 - 10): ").split()))
brightness_range = list(map(int, input("Enter brightness range (e.g., -30 - 30): ").split()))
add_noise_flag = input("Do you want to add noise? (yes/no): ").strip().lower() == 'yes'

# Process the images
process_images(input_image_folder_images, 
               input_file_folder_txt, 
               output_image_folder_train, 
               output_output_folder_train, 
               image_width, 
               image_height, 
               angle_range, 
               brightness_range, 
               add_noise_flag)
