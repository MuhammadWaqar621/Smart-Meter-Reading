import os
from ultralytics import YOLO
import cv2
import numpy as np
model = YOLO(r"runs\detect\train\weights\best.pt")
# Function to run YOLO inference on an image and save the annotated image
def OCR8(input_folder):
    # Load the YOLO model
    

    # Run YOLO inference
    results = model(input_folder)

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

    # Sort the dictionary based on keys (x1 values)
    sorted_bbox_dict = dict(sorted(bbox_dict.items()))

    # Concatenate the class names into a single string
    output_string = "".join(sorted_bbox_dict.values())
    return output_string