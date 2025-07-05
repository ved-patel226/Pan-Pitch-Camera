import os
import torch
from ultralytics import YOLO


def train_yolo():
    print(f"CUDA available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"- GPU device: {torch.cuda.get_device_name(0)}")

    data_yaml = "dataset_split/yolo.yaml"

    model = YOLO("/mnt/Fedora2/code/pi/Servos/yolo11n.pt")

    model.train(
        data=data_yaml,
        epochs=100,
        imgsz=640,
        batch=16,
        patience=20,
        save=True,
        single_cls=True,
    )

    model.val()

    print("Training Completed.")


if __name__ == "__main__":
    train_yolo()
