import os
import cv2
import numpy as np
from sklearn.model_selection import train_test_split


def load_dataset(data_dir, img_size=128):
    images, labels = [], []

    classes = {"safe": 0, "obstacle": 1}

    for cls, label in classes.items():
        cls_dir = os.path.join(data_dir, cls)
        for file in os.listdir(cls_dir):
            path = os.path.join(cls_dir, file)
            img = cv2.imread(path)

            if img is None:
                continue

            img = cv2.resize(img, (img_size, img_size))
            img = img[:, :, ::-1]  # BGR → RGB  
            img = img / 255.0

            images.append(img)
            labels.append(label)

    X = np.array(images, dtype=np.float32)
    y = np.array(labels)

    return train_test_split(X, y, test_size=0.2, random_state=42)
