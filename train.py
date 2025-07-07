import os
import torch
from ultralytics import YOLO
import platform
import time


def train_yolo():
    print(f"CUDA available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"- GPU device: {torch.cuda.get_device_name(0)}")

    data_yaml = "dataset_split/yolo.yaml"

    model = YOLO("/mnt/Fedora2/code/pi/Servos/yolo11n.pt")

    model.train(
        data=data_yaml,
        epochs=9999999,  # stop when patience runs out (get the best model)
        imgsz=640,
        batch=8,
        patience=5,
        save=True,
        single_cls=True,
        name="v3",
    )

    model.val()

    print("Training Completed.")

    # Shutdown the computer after completion
    print("Shutting down the computer in 1 minute...")
    system = platform.system().lower()
    if system == "linux":
        os.system("shutdown -h 1")
    elif system == "windows":
        os.system("shutdown /s /t 60")
    elif system == "darwin":  # macOS
        os.system("sudo shutdown -h +1")

    time.sleep(65)


if __name__ == "__main__":
    train_yolo()
