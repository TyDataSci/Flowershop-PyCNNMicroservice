import hyperparameters as hyper
from transform import transform
import torch


def classifier(model, image_path, device=hyper.DEVICE):
    image_tensor = transform(image_path)
    model.eval()
    model.to(device)
    with torch.no_grad():
        # send data to device
        image = image_tensor.to(device)

        # forward pass to get outputs
        y_hat = model(image)

        # accuracy
        _, predicted = torch.max(y_hat.data, 1)
        return hyper.CLASSES[predicted]
