import os
import shutil
from glob import glob
import random
import argparse
import json
from tqdm import tqdm

def create_dirs(base_dir, classes):
    """
    Creates directory structure for organizing images and labels into training, validation, and test sets.

    Args:
        base_dir (str): The base directory where the directory structure will be created.
        classes (dict): A dictionary with class names as keys. Each key represents a class for which 
                        separate directories will be created within the 'train', 'val', and 'test' directories.

    Returns:
        None
    """
    os.makedirs(os.path.join(base_dir, 'images', 'train'), exist_ok=True)
    os.makedirs(os.path.join(base_dir, 'images', 'val'), exist_ok=True)
    os.makedirs(os.path.join(base_dir, 'images', 'test'), exist_ok=True)
    for class_name in classes.keys():
        os.makedirs(os.path.join(base_dir, 'images', 'train', class_name), exist_ok=True)
        os.makedirs(os.path.join(base_dir, 'images', 'val', class_name), exist_ok=True)
        os.makedirs(os.path.join(base_dir, 'images', 'test', class_name), exist_ok=True)
    os.makedirs(os.path.join(base_dir, 'labels', 'train'), exist_ok=True)
    os.makedirs(os.path.join(base_dir, 'labels', 'val'), exist_ok=True)
    os.makedirs(os.path.join(base_dir, 'labels', 'test'), exist_ok=True)
    for class_name in classes.keys():
        os.makedirs(os.path.join(base_dir, 'labels', 'train', class_name), exist_ok=True)
        os.makedirs(os.path.join(base_dir, 'labels', 'val', class_name), exist_ok=True)
        os.makedirs(os.path.join(base_dir, 'labels', 'test', class_name), exist_ok=True)

def split_and_move_images(dataset_dir, output_dir, classes, train_val_split_ratio=0.8, test_val_ratio=0.2, update_interval=100):
    """
    Splits images into training, validation, and test sets and moves them to the appropriate directories.

    Args:
        dataset_dir (str): Directory containing the original dataset.
        output_dir (str): Directory where the split images will be saved.
        classes (dict): Dictionary with class names as keys and class IDs as values.
        train_val_split_ratio (float): Ratio to split between training and validation sets (default 0.8).
        test_val_ratio (float): Ratio of validation set to be used for testing (default 0.2).

    Returns:
        None
    """
    # Create directories
    create_dirs(output_dir, classes)

    def copy_images(source_dir, split):
        for class_name, _ in classes.items():
            source_path = os.path.join(source_dir, class_name)
            image_paths = glob(os.path.join(source_path, '*.jpg'))
            destination_dir = os.path.join(output_dir, "images", split, class_name)
            
            total_files = len(image_paths)
            processed_count = 0
            with tqdm(total=total_files, desc=f"Copying {split} images for {class_name}", unit="file") as pbar:
                for image_path in image_paths:
                    image_name = os.path.basename(image_path)
                    shutil.copy(image_path, os.path.join(destination_dir, image_name))
                    
                    processed_count += 1
                    if processed_count % update_interval == 0 or processed_count == total_files:
                        pbar.update(update_interval if processed_count % update_interval == 0 else processed_count % update_interval)

    def create_labels(base_dir):
        splits = ["train", "val", "test"]
        for split in splits:
            for class_name, class_id in classes.items():
                image_paths = glob(os.path.join(base_dir, split, class_name, '*.jpg'))
                for image_path in tqdm(image_paths, desc=f"Creating labels for {split} set", unit="file"):
                    image_name = os.path.basename(image_path)
                    label_path = os.path.join(output_dir, 'labels', split, class_name, image_name.replace('.jpg', '.txt'))
                    with open(label_path, 'w') as label_file:
                        label_file.write(f"{class_id} 0.5 0.5 1.0 1.0\n")  # Dummy YOLO format: class_id x_center y_center width height

    # Copy images to train and val directories
    for split in ["train", "val"]:
        source_dir = os.path.join(dataset_dir, "Training" if split == "train" else "Validation")
        copy_images(source_dir, split)

    

    # Move a portion of validation images to the test set
    for class_name in classes.keys():
        val_images = glob(os.path.join(output_dir, 'images', 'val', class_name, '*.jpg'))
        random.shuffle(val_images)
        test_size = int(len(val_images) * test_val_ratio)
        test_images = val_images[:test_size]
        for test_image in tqdm(test_images, desc=f"Moving images to test set for class {class_name}", unit="file"):
            test_image_name = os.path.basename(test_image)
            shutil.move(test_image, os.path.join(output_dir, 'images', 'test',class_name, test_image_name))
        print(f"Moved images to test set for class: {class_name}")
    # Create label files
    create_labels(os.path.join(output_dir, 'images'))
def main():
    parser = argparse.ArgumentParser(description="Organize dataset into training, validation, and test sets.")
    parser.add_argument('--dataset_dir', type=str, required=True, help='Directory containing the original dataset.')
    parser.add_argument('--output_dir', type=str, required=True, help='Directory where the split images will be saved.')
    parser.add_argument('--classes', type=str, required=True, help='JSON string with class names and IDs, e.g., {"male": 0, "female": 1}')
    parser.add_argument('--train_val_split_ratio', type=float, default=0.8, help='Ratio to split between training and validation sets.')
    parser.add_argument('--test_val_ratio', type=float, default=0.2, help='Ratio of validation set to be used for testing.')
    parser.add_argument('--update_interval', type=int, default=100, help='Number of files to process before updating the progress bar.')
    
    args = parser.parse_args()

    # Parse the classes argument from JSON string
    classes = json.loads(args.classes)

    split_and_move_images(
        dataset_dir=args.dataset_dir,
        output_dir=args.output_dir,
        classes=classes,
        train_val_split_ratio=args.train_val_split_ratio,
        test_val_ratio=args.test_val_ratio,
        update_interval=args.update_interval
    )

if __name__ == "__main__":
    main()
