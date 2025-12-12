import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import models
from torch.utils.data import TensorDataset, DataLoader

from .preprocess import load_dataset


def build_model():
    model = models.mobilenet_v3_small(weights="IMAGENET1K_V1")
    model.classifier[3] = nn.Linear(model.classifier[3].in_features, 1)
    return model


def train_obstacle_model(data_dir="data/obstacles", img_size=128, epochs=10):
    X_train, X_test, y_train, y_test = load_dataset(data_dir, img_size)

    # Convert to torch tensors
    X_train = torch.tensor(X_train).permute(0, 3, 1, 2)
    X_test = torch.tensor(X_test).permute(0, 3, 1, 2)
    y_train = torch.tensor(y_train).float().unsqueeze(1)
    y_test = torch.tensor(y_test).float().unsqueeze(1)

    train_loader = DataLoader(TensorDataset(X_train, y_train), 
                              batch_size=16, shuffle=True)
    test_loader = DataLoader(TensorDataset(X_test, y_test), 
                             batch_size=16, shuffle=False)

    model = build_model()
    criterion = nn.BCEWithLogitsLoss()
    optimizer = optim.Adam(model.parameters(), lr=1e-4)

    # Training loop
    model.train()
    for epoch in range(epochs):
        epoch_loss = 0
        for Xb, yb in train_loader:
            optimizer.zero_grad()
            pred = model(Xb)
            loss = criterion(pred, yb)
            loss.backward()
            optimizer.step()
            epoch_loss += loss.item()

        print(f"Epoch {epoch+1}/{epochs} - Loss: {epoch_loss:.4f}")

    # Evaluation
    model.eval()
    correct = 0
    total = 0
    with torch.no_grad():
        for Xb, yb in test_loader:
            pred = torch.sigmoid(model(Xb))
            predicted = (pred > 0.5).float()
            correct += (predicted == yb).sum().item()
            total += yb.size(0)

    accuracy = correct / total if total > 0 else 0
    print(f"Validation Accuracy: {accuracy*100:.2f}%")

    # Save model
    torch.save(model.state_dict(), "data/models/obstacle_detector.pth")
    print("Model saved!")
