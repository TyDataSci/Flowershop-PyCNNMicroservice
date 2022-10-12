import torch.nn as nn
import torch.nn.functional as F
import hyperparameters as hyper


class CNN(nn.Module):
    def __init__(self,
                 num_channels=hyper.NUM_CHANNELS,
                 num_out_channels=hyper.NUM_OUT_CHANNEL,
                 img_w=hyper.IMAGE_W,
                 img_h=hyper.IMAGE_H,
                 num_classes=hyper.NUM_CLASSES):
        super(CNN, self).__init__()
        self.num_channels = num_channels
        kernel_size = (3, 3)
        stride = (1, 1)
        padding = (1, 1)
        self.num_out_channels = num_out_channels
        self.img_w = img_w
        self.img_h = img_h
        self.conv1 = nn.Conv2d(in_channels=self.num_channels, out_channels=self.num_out_channels[0],
                               kernel_size=kernel_size, stride=stride, padding=padding)
        self.conv2 = nn.Conv2d(in_channels=self.num_out_channels[0], out_channels=self.num_out_channels[1],
                               kernel_size=kernel_size, stride=stride, padding=padding)
        self.m_pool = nn.MaxPool2d(kernel_size=(2, 2), stride=(2, 2))
        self.fully_connect = nn.Linear(in_features=int(self.img_w / 4) * int(self.img_h / 4) * self.num_out_channels[1],
                                       out_features=num_classes)

    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = self.m_pool(x)
        x = F.relu(self.conv2(x))
        x = self.m_pool(x)
        x = self.fully_connect(x.reshape(x.shape[0], -1))

        return x
