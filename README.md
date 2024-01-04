# Smart Meter Reader

Smart Meter Reader is an innovative project addressing the evolving landscape of meter reading in a smart and efficient manner. In a world where autonomous technologies are reshaping transportation safety, our focus is on revolutionizing the way utility meters are read.

## Project Overview

This repository encapsulates the Smart Meter Reader project, a solution designed to streamline the meter reading process. The primary objective is to leverage AI capabilities to detect and interpret digits on utility meters accurately.

### Key Objectives

- **Digit Detection:** Implement a robust system to identify and locate digits on meter displays, ensuring precise recognition in varying conditions.

- **Crop Image Generation:** Develop a mechanism to extract and generate cropped images of digit regions, optimizing input for subsequent processing.

- **Digit Recognition:** Employ advanced AI models to accurately recognize and interpret the digits within the cropped images, ensuring reliable meter readings.


This project aims to automate smart meter reading using computer vision and optical character recognition (OCR). Below is the image processing flow:

1. **Input Image:**
   ![Input Image](https://github.com/MuhammadWaqar621/Smart-Meter-Reading/raw/master/TestImg/5.jpeg)

2. **ROI Model Output:**
   ![ROI Model Output](https://github.com/MuhammadWaqar621/Smart-Meter-Reading/raw/master/Test_OCR/5.jpg)

3. **Final OCR Result:**
   ![Final OCR Result](https://github.com/MuhammadWaqar621/Smart-Meter-Reading/raw/master/OCR_Result/5.jpg)


## Why It Matters

In a world increasingly reliant on accurate and efficient utility management, Smart Meter Reader offers a transformative solution. By automating the digit reading process, we not only enhance accuracy but also pave the way for smart utility management systems.


## Getting Started

Follow the steps below to get started with this project:

## Using This Repository
### Environment
* Python 3.11.4
* pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
### Installation
1. Clone the repository
```
git clone https://github.com/MuhammadWaqar621/Smart-Meter-Reading.git
```

2. Install the requirements
```
conda create -n smart_meter python=3.11.4
conda activate smart_meter
pip install -r requirements.txt
```
3. Prepare Dataset
```
    Dataset/
    │
    ├── ROI_Dataset/
    │   ├── images/
    │   │   ├── img1.jpg
    │   │   ├── img2.jpg
    │   │   └── ...
    │   │
    │   └── labels/
    │       ├── img1.txt
    │       ├── img2.txt
    │       └── ...
    |
    ├── OCR_Dataset/
    │   ├── images/
    │   │   ├── img1.jpg
    │   │   ├── img2.jpg
    │   │   └── ...
    │   │
    │   └── labels/
    │       ├── img1.txt
    │       ├── img2.txt
    │       └── ...
    
```

4. Training
```
# Train the model for Area of Interest (ROI) detection
python train_ROI.py

# Train the model for Meter Digit Detection using Optical Character Recognition (OCR)
python train_OCR.py

```

4. Testing
```
# Test the model for Area of Interest (ROI) detection
python test_ROI.py

# Test the model for Meter Digit Detection using Optical Character Recognition (OCR)
python test_OCR.py

```
4. Integration
```
python main.py
```
5. Download Pretrain Models
```
python .\model_checkpoints_download.py
```
6. FastAPI
```
uvicorn API:app --host 0.0.0.0 --port 1003 --reload
```


## Contact
* [Muhammad Waqar](https://www.linkedin.com/in/muhammad-waqar-1a594411a/)
* [Email](waqarsahi621@gmail.com)

## Contribution

Feel free to customize this template to better fit the specifics of your project. Provide clear instructions on how to get started and contribute, and include any additional details that potential users or contributors might find helpful.


