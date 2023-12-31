from ROI import main as roi_detection
from OCR8 import OCR8 as ocr_detection
from pathlib import Path
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



