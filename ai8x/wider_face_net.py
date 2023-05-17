###################################################################################################
# WIDER Faces dataloader
# Lionnus Kesting
# Machine Learning on Microcontrollers
# 2023 - ETH Zurich
###################################################################################################
"""
WIDERFaceNet network description
"""
from signal import pause
from torch import nn

import ai8x

import matplotlib
import matplotlib.pyplot as plt

class WIDERFaceNet(nn.Module):
    def __init__(self, num_classes=10, dimensions=(28, 28), num_channels=1, bias=False, **kwargs):
        super().__init__()

        dim_x, dim_y = dimensions

        self.conv1 = nn.Sequential(
            nn.Conv2d(in_channels=num_channels, out_channels=96, kernel_size=11, stride=4, padding=0, bias=bias),
            nn.ReLU(inplace=True)
        )
        dim_x = ((dim_x - 11) // 4) + 1
        dim_y = ((dim_y - 11) // 4) + 1

        self.pool1 = nn.MaxPool2d(kernel_size=3, stride=2)
        dim_x = ((dim_x - 3) // 2) + 1
        dim_y = ((dim_y - 3) // 2) + 1

        self.lrn1 = nn.LocalResponseNorm(5)

        self.conv2 = nn.Sequential(
            nn.Conv2d(in_channels=96, out_channels=256, kernel_size=5, stride=2, padding=1, bias=bias),
            nn.ReLU(inplace=True)
        )

        self.pool2 = nn.MaxPool2d(kernel_size=3, stride=2)
        dim_x = ((dim_x - 3) // 2) + 1
        dim_y = ((dim_y - 3) // 2) + 1

        self.lrn2 = nn.LocalResponseNorm(5)

        self.conv3 = nn.Sequential(
            nn.Conv2d(in_channels=256, out_channels=384, kernel_size=3, padding=1, bias=bias),
            nn.ReLU(inplace=True)
        )
        # padding 1 -> no change in dimensions

        self.conv4 = nn.Sequential(
            nn.Conv2d(in_channels=384, out_channels=384, kernel_size=3, padding=1, bias=bias),
            nn.ReLU(inplace=True)
        )
        # padding 1 -> no change in dimensions

        self.conv5 = nn.Sequential(
            nn.Conv2d(in_channels=384, out_channels=256, kernel_size=3, padding=1, bias=bias),
            nn.ReLU(inplace=True)
        )
        # padding 1 -> no change in dimensions

        self.pool5 = nn.MaxPool2d(kernel_size=3, stride=2)
        dim_x = ((dim_x - 3) // 2) + 1
        dim_y = ((dim_y - 3) // 2) + 1

        self.conv6 = nn.Sequential(
            nn.Conv2d(in_channels=256, out_channels=256, kernel_size=4, padding=0, bias=bias),
            nn.ReLU(inplace=True)
        )
        dim_x = ((dim_x - 4) // 1) + 1
        dim_y = ((dim_y - 4) // 1) + 1

        self.conv7 = nn.Sequential(
            nn.Conv2d(in_channels=256, out_channels=4096, kernel_size=1, padding=0, bias=bias),
            nn.ReLU(inplace=True)
        )
        dim_x = ((dim_x - 1) // 1) + 1
        dim_y = ((dim_y - 1) // 1) + 1

        # Fully connected layer?
        self.fcx = nn.Linear(dim_x * dim_y * 96, num_classes, bias=True)

        # Initialize weights with normal distribution
        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                nn.init.kaiming_normal_(m.weight, mode='fan_out', nonlinearity='relu')
    """
    Assemble the model
    """
    def forward(self, x):  # pylint: disable=arguments-differ
            """Forward prop"""
            x = self.conv1(x)
            x = self.pool1(x)
            x = self.lrn1(x)
            x = self.conv2(x)
            x = self.pool2(x)
            x = self.lrn2(x)
            x = self.conv3(x)
            x = self.conv4(x)
            x = self.conv5(x)
            x = self.pool5(x)
            x = self.conv6(x)
            x = self.conv7(x)
            x = x.view(x.size(0), -1)
            x = self.fcx(x)

            return x

def WIDERFaceNet(pretrained=False, **kwargs):
    """
    Constructs a WIDERFaceNet model.
    """
    assert not pretrained
    return WIDERFaceNet(**kwargs)

"""
Network description
"""
models = [
    {
        'name': 'WIDERFaceNet',
        'min_input': 1,
        'dim': 2,
    }
]