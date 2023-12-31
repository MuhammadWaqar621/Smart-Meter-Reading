from ultralytics import YOLO

if __name__ == '__main__':
    # Load a model
    model = YOLO("yolov8x.yaml")  # build a new model from scratch
    model = YOLO("yolov8x.pt")  # load a pretrained model (recommended for training)

    # Use the model
    model.train(data="data.yaml", epochs=300,batch=32)  # train the model
    metrics = model.val()  # evaluate model performance on the validation set
    # results = model("https://ultralytics.com/images/bus.jpg")  # predict on an image
    path = model.export(format="pt")  # export the model to ONNX format