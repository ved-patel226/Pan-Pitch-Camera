from ultralytics import YOLO

# Load the YOLO model from best.pt
model = YOLO("best.pt")

# Export the model to ONNX format
model.export(format="onnx")
