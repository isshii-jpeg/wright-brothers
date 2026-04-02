"""
1D-CNN Model for Excretion Detection
=====================================

Lightweight convolutional neural network that processes time-series sensor data
to classify excretion events. Designed to be quantized and deployed on
STM32 via TensorFlow Lite Micro or X-CUBE-AI.

Input: Window of N sensor readings (temperature, humidity, NH3)
Output: Probability distribution over {normal, urine, feces}
"""

import torch
import torch.nn as nn
import torch.nn.functional as F


class ExcretionCNN1D(nn.Module):
    """
    1D-CNN for excretion detection from time-series sensor data.

    Architecture (optimized for STM32 deployment):
        Input: (batch, 3, window_size)  -- 3 channels: temp, humidity, NH3
        Conv1D(3->16, k=5) -> BN -> ReLU -> MaxPool(2)
        Conv1D(16->32, k=3) -> BN -> ReLU -> MaxPool(2)
        Conv1D(32->32, k=3) -> BN -> ReLU -> GlobalAvgPool
        FC(32->16) -> ReLU -> Dropout -> FC(16->3)

    Total params: ~3.5K (fits comfortably in STM32F103 SRAM)
    """

    def __init__(self, window_size: int = 60, num_classes: int = 3, dropout: float = 0.3):
        super().__init__()

        self.conv1 = nn.Conv1d(3, 16, kernel_size=5, padding=2)
        self.bn1 = nn.BatchNorm1d(16)
        self.pool1 = nn.MaxPool1d(2)

        self.conv2 = nn.Conv1d(16, 32, kernel_size=3, padding=1)
        self.bn2 = nn.BatchNorm1d(32)
        self.pool2 = nn.MaxPool1d(2)

        self.conv3 = nn.Conv1d(32, 32, kernel_size=3, padding=1)
        self.bn3 = nn.BatchNorm1d(32)

        self.fc1 = nn.Linear(32, 16)
        self.dropout = nn.Dropout(dropout)
        self.fc2 = nn.Linear(16, num_classes)

    def forward(self, x):
        """
        Args:
            x: (batch, 3, window_size) - sensor time series
        Returns:
            (batch, 3) - log probabilities for {normal, urine, feces}
        """
        x = self.pool1(F.relu(self.bn1(self.conv1(x))))
        x = self.pool2(F.relu(self.bn2(self.conv2(x))))
        x = F.relu(self.bn3(self.conv3(x)))

        # Global average pooling
        x = x.mean(dim=2)

        x = F.relu(self.fc1(x))
        x = self.dropout(x)
        x = self.fc2(x)

        return F.log_softmax(x, dim=1)


class SensorNormalizer(nn.Module):
    """Normalize raw sensor values to [0, 1] range for CNN input."""

    def __init__(self):
        super().__init__()
        # Expected ranges for normalization
        self.register_buffer('temp_min', torch.tensor(30.0))
        self.register_buffer('temp_max', torch.tensor(40.0))
        self.register_buffer('hum_min', torch.tensor(30.0))
        self.register_buffer('hum_max', torch.tensor(100.0))
        self.register_buffer('nh3_min', torch.tensor(0.0))
        self.register_buffer('nh3_max', torch.tensor(60.0))

    def forward(self, temp, humidity, nh3):
        """
        Args:
            temp: (batch, window_size) - temperature in Celsius
            humidity: (batch, window_size) - RH %
            nh3: (batch, window_size) - ppm

        Returns:
            (batch, 3, window_size) - normalized and stacked
        """
        t = (temp - self.temp_min) / (self.temp_max - self.temp_min)
        h = (humidity - self.hum_min) / (self.hum_max - self.hum_min)
        n = (nh3 - self.nh3_min) / (self.nh3_max - self.nh3_min)

        return torch.stack([t.clamp(0, 1), h.clamp(0, 1), n.clamp(0, 1)], dim=1)


def count_parameters(model):
    """Count trainable parameters."""
    return sum(p.numel() for p in model.parameters() if p.requires_grad)


if __name__ == "__main__":
    model = ExcretionCNN1D(window_size=60)
    print(f"Model parameters: {count_parameters(model):,}")
    print(f"\nArchitecture:\n{model}")

    # Test forward pass
    dummy = torch.randn(4, 3, 60)
    output = model(dummy)
    print(f"\nInput shape:  {dummy.shape}")
    print(f"Output shape: {output.shape}")
    print(f"Output (softmax): {torch.exp(output[0]).detach().numpy()}")
