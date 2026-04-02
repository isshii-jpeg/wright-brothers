"""
Training script for 1D-CNN Excretion Detection Model
=====================================================

Trains on synthetic or real sensor data and exports to ONNX for
deployment on STM32 via TensorFlow Lite Micro or X-CUBE-AI.

Usage:
    python train_1dcnn.py --config config.yaml
    python train_1dcnn.py --synthetic --epochs 100
"""

import argparse
import sys
import os
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader, random_split

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'models'))
from cnn_1d import ExcretionCNN1D, SensorNormalizer, count_parameters


# ---------- Synthetic Data Generator ----------

class SyntheticExcretionDataset(Dataset):
    """
    Generate synthetic sensor data for training.

    Simulates realistic sensor patterns:
    - Normal: baseline with random noise
    - Urine: temperature spike + humidity surge + moderate NH3
    - Feces: moderate temp spike + humidity rise + high NH3
    """

    def __init__(self, num_samples: int = 5000, window_size: int = 60, seed: int = 42):
        self.window_size = window_size
        rng = np.random.RandomState(seed)

        self.data = []
        self.labels = []

        for _ in range(num_samples):
            label = rng.randint(0, 3)  # 0=normal, 1=urine, 2=feces

            # Base signals
            temp = 33.0 + rng.randn(window_size) * 0.3
            humidity = 50.0 + rng.randn(window_size) * 5.0
            nh3 = 2.0 + np.abs(rng.randn(window_size)) * 1.0

            if label == 1:  # Urine
                event_start = rng.randint(window_size // 4, window_size // 2)
                rise = np.linspace(0, 1, window_size - event_start)
                temp[event_start:] += rise * (2.5 + rng.rand() * 2.0)
                humidity[event_start:] += rise * (30.0 + rng.rand() * 15.0)
                nh3[event_start:] += rise * (12.0 + rng.rand() * 10.0)

            elif label == 2:  # Feces
                event_start = rng.randint(window_size // 4, window_size // 2)
                rise = np.linspace(0, 1, window_size - event_start)
                temp[event_start:] += rise * (1.5 + rng.rand() * 2.0)
                humidity[event_start:] += rise * (25.0 + rng.rand() * 10.0)
                nh3[event_start:] += rise * (30.0 + rng.rand() * 20.0)

            # Add measurement noise
            temp += rng.randn(window_size) * 0.1
            humidity += rng.randn(window_size) * 2.0
            nh3 += np.abs(rng.randn(window_size)) * 0.5

            sensor_data = np.stack([temp, humidity, nh3], axis=0).astype(np.float32)
            self.data.append(sensor_data)
            self.labels.append(label)

        self.data = np.array(self.data)
        self.labels = np.array(self.labels)

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        return torch.from_numpy(self.data[idx]), self.labels[idx]


# ---------- Training Loop ----------

def train_epoch(model, loader, optimizer, criterion, device):
    model.train()
    total_loss = 0
    correct = 0
    total = 0

    for data, target in loader:
        data, target = data.to(device), target.to(device)
        optimizer.zero_grad()
        output = model(data)
        loss = criterion(output, target)
        loss.backward()
        optimizer.step()

        total_loss += loss.item() * data.size(0)
        pred = output.argmax(dim=1)
        correct += pred.eq(target).sum().item()
        total += data.size(0)

    return total_loss / total, correct / total


def evaluate(model, loader, criterion, device):
    model.eval()
    total_loss = 0
    correct = 0
    total = 0

    with torch.no_grad():
        for data, target in loader:
            data, target = data.to(device), target.to(device)
            output = model(data)
            loss = criterion(output, target)
            total_loss += loss.item() * data.size(0)
            pred = output.argmax(dim=1)
            correct += pred.eq(target).sum().item()
            total += data.size(0)

    return total_loss / total, correct / total


# ---------- Export ----------

def export_onnx(model, window_size, path):
    """Export model to ONNX format for STM32 deployment."""
    model.eval()
    dummy = torch.randn(1, 3, window_size)
    torch.onnx.export(
        model, dummy, path,
        input_names=['sensor_input'],
        output_names=['classification'],
        dynamic_axes={'sensor_input': {0: 'batch'}, 'classification': {0: 'batch'}},
        opset_version=11,
    )
    print(f"Model exported to {path}")


# ---------- Main ----------

def main():
    parser = argparse.ArgumentParser(description="Train 1D-CNN for excretion detection")
    parser.add_argument("--synthetic", action="store_true", help="Use synthetic data")
    parser.add_argument("--data-dir", type=str, default="../data", help="Real data directory")
    parser.add_argument("--epochs", type=int, default=50)
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--lr", type=float, default=1e-3)
    parser.add_argument("--window-size", type=int, default=60)
    parser.add_argument("--num-samples", type=int, default=5000)
    parser.add_argument("--output", type=str, default="oecs_model.onnx")
    args = parser.parse_args()

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Device: {device}")

    # Dataset
    if args.synthetic:
        dataset = SyntheticExcretionDataset(
            num_samples=args.num_samples,
            window_size=args.window_size,
        )
        print(f"Generated {len(dataset)} synthetic samples")
    else:
        print(f"TODO: Implement real data loader from {args.data_dir}")
        return

    # Split
    train_size = int(0.8 * len(dataset))
    val_size = len(dataset) - train_size
    train_set, val_set = random_split(dataset, [train_size, val_size])

    train_loader = DataLoader(train_set, batch_size=args.batch_size, shuffle=True)
    val_loader = DataLoader(val_set, batch_size=args.batch_size)

    # Model
    model = ExcretionCNN1D(window_size=args.window_size).to(device)
    print(f"Parameters: {count_parameters(model):,}")

    optimizer = optim.Adam(model.parameters(), lr=args.lr)
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, patience=5, factor=0.5)
    criterion = nn.NLLLoss()

    best_val_acc = 0

    for epoch in range(1, args.epochs + 1):
        train_loss, train_acc = train_epoch(model, train_loader, optimizer, criterion, device)
        val_loss, val_acc = evaluate(model, val_loader, criterion, device)
        scheduler.step(val_loss)

        if epoch % 5 == 0 or epoch == 1:
            print(f"Epoch {epoch:3d} | "
                  f"Train: loss={train_loss:.4f} acc={train_acc:.3f} | "
                  f"Val: loss={val_loss:.4f} acc={val_acc:.3f}")

        if val_acc > best_val_acc:
            best_val_acc = val_acc
            torch.save(model.state_dict(), "best_model.pth")

    print(f"\nBest validation accuracy: {best_val_acc:.3f}")

    # Export
    model.load_state_dict(torch.load("best_model.pth", weights_only=True))
    export_onnx(model, args.window_size, args.output)


if __name__ == "__main__":
    main()
