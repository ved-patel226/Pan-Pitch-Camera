import os
import shutil
from pathlib import Path
import random
from typing import List, Tuple


def create_train_val_split(
    dataset_dir: str,
    images_subdir: str = "images",
    labels_subdir: str = "labels",
    output_dir: str = "dataset_split",
    train_ratio: float = 0.8,
    seed: int = 42,
) -> None:
    """
    Split dataset into train and validation sets.

    Args:
        dataset_dir: Path to the main dataset directory
        images_subdir: Name of the images subdirectory
        labels_subdir: Name of the labels subdirectory
        output_dir: Output directory for train/val split
        train_ratio: Ratio of data to use for training (0.8 = 80%)
        seed: Random seed for reproducible splits
    """

    # Set random seed for reproducible results
    random.seed(seed)

    # Define paths
    dataset_path = Path(dataset_dir)
    images_path = dataset_path / images_subdir
    labels_path = dataset_path / labels_subdir
    output_path = Path(output_dir)

    # Validate input directories exist
    if not images_path.exists():
        raise FileNotFoundError(f"Images directory not found: {images_path}")
    if not labels_path.exists():
        raise FileNotFoundError(f"Labels directory not found: {labels_path}")

    # Get all image files (png format)
    image_files = list(images_path.glob("*.jpg"))
    if not image_files:
        raise ValueError("No PNG images found in the images directory")

    # Create output directory structure
    train_images_dir = output_path / "train" / "images"
    train_labels_dir = output_path / "train" / "labels"
    val_images_dir = output_path / "val" / "images"
    val_labels_dir = output_path / "val" / "labels"

    for dir_path in [
        train_images_dir,
        train_labels_dir,
        val_images_dir,
        val_labels_dir,
    ]:
        dir_path.mkdir(parents=True, exist_ok=True)

    # Filter images that have corresponding label files
    valid_pairs = []
    for img_file in image_files:
        label_file = labels_path / f"{img_file.stem}.txt"
        if label_file.exists():
            valid_pairs.append((img_file, label_file))
        else:
            print(f"Warning: No label file found for {img_file.name}")

    if not valid_pairs:
        raise ValueError("No valid image-label pairs found")

    # Shuffle the pairs
    random.shuffle(valid_pairs)

    # Calculate split index
    train_count = int(len(valid_pairs) * train_ratio)
    train_pairs = valid_pairs[:train_count]
    val_pairs = valid_pairs[train_count:]

    print(f"Total pairs: {len(valid_pairs)}")
    print(f"Training pairs: {len(train_pairs)}")
    print(f"Validation pairs: {len(val_pairs)}")

    # Copy files to train directory
    print("\nCopying training files...")
    for img_file, label_file in train_pairs:
        shutil.copy2(img_file, train_images_dir / img_file.name)
        shutil.copy2(label_file, train_labels_dir / label_file.name)

    # Copy files to validation directory
    print("Copying validation files...")
    for img_file, label_file in val_pairs:
        shutil.copy2(img_file, val_images_dir / img_file.name)
        shutil.copy2(label_file, val_labels_dir / label_file.name)

    print(f"\nDataset split complete! Output saved to: {output_path}")
    print(f"Train split: {len(train_pairs)} samples ({train_ratio*100:.1f}%)")
    print(f"Val split: {len(val_pairs)} samples ({(1-train_ratio)*100:.1f}%)")


def main():
    """Main function to run the dataset splitting."""

    # Configuration - modify these paths as needed
    DATASET_DIR = "dataset"  # Path to your main dataset directory
    IMAGES_SUBDIR = "images"  # Name of images folder
    LABELS_SUBDIR = "labels"  # Name of labels folder
    OUTPUT_DIR = "dataset_split"  # Output directory
    TRAIN_RATIO = 0.8  # 80% for training, 20% for validation

    try:
        create_train_val_split(
            dataset_dir=DATASET_DIR,
            images_subdir=IMAGES_SUBDIR,
            labels_subdir=LABELS_SUBDIR,
            output_dir=OUTPUT_DIR,
            train_ratio=TRAIN_RATIO,
        )
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
