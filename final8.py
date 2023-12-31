from ROI import main as roi_detection
from OCR8 import OCR8 as ocr_detection
from pathlib import Path
import base64
import os
import datetime
def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        base64_encoded = base64.b64encode(image_file.read()).decode("utf-8")
    return base64_encoded

def pipeline(source):
    # print(source)
    path=roi_detection(source)
    # print(path)
    if path is not None:
        # Convert the string to a Path object
        image_path = Path(path)
        if image_path.exists():
            status="1"
            result=ocr_detection(path)
            # print(result)
            return status,"Ocr Completed",result,image_path
    return "0","OCR Error","","No Crop Image found"




def final(image_data):
    # Define a directory to store uploaded images
    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)
    # Decode base64 image data
   
    try:
        image_content = base64.b64decode(image_data)
    except:
        return {"status": 0, "message": "Invalid Base64",        
            "data": {
            "outputImage": "",
            "meterNumber": ""
            }}

    image_name = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")

    # Save the decoded image in the uploads folder
    image_path = os.path.join(upload_dir, f"{image_name}.jpeg")
    with open(image_path, "wb") as temp_image_file:
        temp_image_file.write(image_content)
    status,message, result,path = pipeline(source=image_path)
    if Path(path).exists():
        img64=image_to_base64(path)
    else:
        img64=path
    response = {
        "status": status,
        "message": message,
        "data": {
            "outputImage": img64,
            "meterNumber": result
        }
    }
    return response
