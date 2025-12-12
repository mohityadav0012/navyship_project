import os
import torch
import cv2


class DummyObstacleModel(torch.nn.Module):
    """
    A very small dummy model used when no trained model exists.
    Output: probability of obstacle (always 0.0 here).
    """

    def __init__(self):
        super().__init__()
        self.linear = torch.nn.Linear(1, 1)  # Not used

    def forward(self, x):
        # Always predict "no obstacle"
        return torch.tensor([[0.0]], dtype=torch.float32)


def load_model():
    """
    Load a trained model if available.
    If no checkpoint exists, return DummyObstacleModel().
    """
    model_path = "data/models/obstacle_detector.pth"

    if not os.path.exists(model_path):
        print("⚠️ WARNING: No trained obstacle model found.Using dummy model.")
        model = DummyObstacleModel()
        model.eval()
        return model

    # Replace DummyObstacleModel with your actual architecture later
    model = DummyObstacleModel()

    try:
        state = torch.load(model_path, map_location="cpu")
        model.load_state_dict(state)
        model.eval()
        print("Loaded trained obstacle model.")
    except Exception as exc:
        print(f"⚠️ ERROR loading model: {exc} — using dummy model instead.")
        model = DummyObstacleModel()
        model.eval()

    return model


# Load model once globally
model = load_model()


def preprocess_tile(tile):
    """
    Convert an image tile (NumPy array) into model-ready 1x1x32x32 tensor.
    """
    gray = cv2.cvtColor(tile, cv2.COLOR_BGR2GRAY)
    resized = cv2.resize(gray, (32, 32))

    tensor = torch.tensor(
        resized, dtype=torch.float32
    ).unsqueeze(0).unsqueeze(0)

    return tensor / 255.0


def obstacle_checker_ml(lat, lon, tile_fetcher=None):
    """
    ML-based obstacle detector.
    Returns False unless a real model + tile_fetcher are available.
    """

    if tile_fetcher is None:
        return False

    tile = tile_fetcher(lat, lon)

    if tile is None:
        return False

    x = preprocess_tile(tile)

    with torch.no_grad():
        pred = model(x).item()

    # Threshold: > 0.5 → obstacle
    return pred > 0.5
