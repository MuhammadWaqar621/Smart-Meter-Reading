import os
from ultralytics import YOLO
import cv2
import numpy as np

# Function to run YOLO inference on an image and save the annotated image
def run_yolo_and_save(input_folder, output_folder, weights_path):
    # Load the YOLO model
    model = YOLO(weights_path)

    # Ensure the output folder exists, create it if not
    os.makedirs(output_folder, exist_ok=True)

    # Get a list of all image files in the input folder
    image_files = [f for f in os.listdir(input_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    # Run YOLO inference on each image
    for image_file in image_files:
        # Construct the input and output paths
        input_path = os.path.join(input_folder, image_file)
        output_path = os.path.join(output_folder, image_file)

        # Run YOLO inference
        results = model(input_path)

        # Access the boxes attribute
        boxes = results[0].boxes

        # Access the relevant attributes of the Boxes object
        xyxy = boxes.xyxy  # bounding boxes in xyxy format
        conf = boxes.conf  # confidence values
        cls = boxes.cls    # class values

        # Get the number of boxes
        num_boxes = xyxy.shape[0]

        # Load the original image
        original_image = results[0].orig_img

        # Convert the image to BGR format (assuming it's in RGB format)
        original_image_bgr = cv2.cvtColor(original_image, cv2.COLOR_RGB2BGR)

        # Create a dictionary to store bounding box information
        bbox_dict = {}

        # Iterate through each class and draw bounding boxes with class labels
        for class_id in np.unique(cls.cpu().numpy()):
            class_boxes = xyxy[cls == class_id]

            # Sort the class boxes based on x1 value
            sorted_indices = class_boxes[:, 0].argsort()

            # Iterate through the sorted indices
            for i in sorted_indices:
                box = class_boxes[i]
                color = tuple(np.random.randint(0, 256, 3).tolist())  # Random color for each class
                # print(conf[i].item())
                # if conf[i].item()>.5:
                # Draw class label inside the rectangle
                label = f"{results[0].names[class_id]}"
                
                bbox_dict[int(box[0])] = label
                # Draw class label inside the rectangle
                class_name = results[0].names[class_id]
                confidence = conf[i].item()
                label = f"{class_name}: {confidence:.2f}"
        
                cv2.rectangle(original_image_bgr, (int(box[0]), int(box[1])), (int(box[2]), int(box[3])), color, 2)
                cv2.putText(original_image_bgr, label, (int(box[0]), int(box[1]) - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

   

        # Sort the dictionary based on keys (x1 values)
        sorted_bbox_dict = dict(sorted(bbox_dict.items()))

        # Concatenate the class names into a single string
        output_string = "".join(sorted_bbox_dict.values())

        # Define the font and other text properties for the sorted class values
        font_sorted = cv2.FONT_HERSHEY_SIMPLEX
        font_scale_sorted = 1
        font_thickness_sorted = 2
        font_color_sorted = (0, 0, 255)  # Green color for the sorted class values
        text_position_sorted = (10, 60)  # Adjust the position as needed

        # Put the text with the sorted class values on the image
        cv2.putText(original_image_bgr, output_string, text_position_sorted, font_sorted, font_scale_sorted, font_color_sorted, font_thickness_sorted)

        # Save the modified image
        cv2.imwrite(output_path, original_image_bgr)

if __name__ == "__main__":
    # Set your input and output folders
    # input_folder = r"D:\Forbmax User Data\waqar sahi\SmartMeter\yolo\Test_OCR"
    # input_folder=r"D:\Forbmax User Data\waqar sahi\SmartMeter\OCR\images"
    input_folder=r"D:\Forbmax User Data\waqar sahi\SmartMeter\yolo\errorImages"
    output_folder = r"D:\Forbmax User Data\waqar sahi\SmartMeter\yolo\output"
    
    # Set the path to the YOLO weights
    weights_path = r"D:\Forbmax User Data\waqar sahi\SmartMeter\yolo\runs\detect\train\weights\best.pt"

    # Run YOLO and save annotated images
    run_yolo_and_save(input_folder, output_folder, weights_path)
