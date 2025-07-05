import kagglehub

# Download latest version
path = kagglehub.dataset_download("fareselmenshawii/face-detection-dataset")

print(
    "Path to dataset files:", path
)  # /home/vedpatel/.cache/kagglehub/datasets/fareselmenshawii/face-detection-dataset/versions/3
