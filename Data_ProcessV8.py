import os
import random
import shutil
# Specify the paths to the XML and Image folders
xml_folder = r"D:\Forbmax User Data\waqar sahi\SmartMeter\yolo\Dataset\OCR\labels"
image_folder = r"D:\Forbmax User Data\waqar sahi\SmartMeter\yolo\Dataset\OCR\images"
# Specify the paths for the output train, test, and validate folders
output_folder = 'Dataset\OCR\V8'
train_folder = os.path.join(output_folder, 'train')
# test_folder = os.path.join(output_folder, 'test')
validate_folder = os.path.join(output_folder, 'validate')
# Create output folders if they don't exist
os.makedirs(train_folder, exist_ok=True)
# os.makedirs(test_folder, exist_ok=True)
os.makedirs(validate_folder, exist_ok=True)
# Get a list of all file names without extensions in the Image folder
all_files = [os.path.splitext(file)[0] for file in os.listdir(image_folder) if file.endswith('.jpg')]
# Calculate the number of files for each split
total_files = len(all_files)
train_size = int(0.8 * total_files)
# test_size = int(0.2 * total_files)
validate_size = int(0.2 * total_files)
# Randomly shuffle the file names
random.shuffle(all_files)
# Split the data into train, test, and validate sets
train_files = all_files[:train_size]
# test_files = all_files[train_size:train_size + test_size]
validate_files = all_files[train_size:]
# Move files to respective folders
for file_name in train_files:
    shutil.copy(os.path.join(image_folder, file_name + '.jpg'), os.path.join(train_folder, file_name + '.jpg'))
    shutil.copy(os.path.join(xml_folder, file_name + '.txt'), os.path.join(train_folder, file_name + '.txt'))
# for file_name in test_files:
#     shutil.copy(os.path.join(image_folder, file_name + '.jpg'), os.path.join(test_folder, file_name + '.jpg'))
#     shutil.copy(os.path.join(xml_folder, file_name + '.txt'), os.path.join(test_folder, file_name + '.txt'))
for file_name in validate_files:
    shutil.copy(os.path.join(image_folder, file_name + '.jpg'), os.path.join(validate_folder, file_name + '.jpg'))
    shutil.copy(os.path.join(xml_folder, file_name + '.txt'), os.path.join(validate_folder, file_name + '.txt'))
print("Data splitting completed. Files are organized into train, test, and validate folders.")



import os
import shutil
# Specify the path to your XML and JPG files
# source_folder = r"D:\Forbmax User Data\waqar sahi\SmartMeter\yolo\Dataset\OCR\V8\train"
source_folder = r"D:\Forbmax User Data\waqar sahi\SmartMeter\yolo\Dataset\OCR\V8\validate"
# Create separate folders for YOLO and JPG files
yolo_folder = os.path.join(source_folder, 'labels')
image_folder = os.path.join(source_folder, 'images')
# Create folders if they don't exist
os.makedirs(yolo_folder, exist_ok=True)
os.makedirs(image_folder, exist_ok=True)
# Iterate through files in the source folder and move YOLO and JPG files to their respective folders
for filename in os.listdir(source_folder):
    if filename.endswith('.txt'):
        yolo_file_path = os.path.join(source_folder, filename)
        shutil.move(yolo_file_path, os.path.join(yolo_folder, filename))
        print(f"Moved {filename} to YOLO folder.")
    elif filename.endswith('.jpg'):
        image_file_path = os.path.join(source_folder, filename)
        shutil.move(image_file_path, os.path.join(image_folder, filename))
        print(f"Moved {filename} to Image folder.")
print("Separation of YOLO and JPG files completed.")