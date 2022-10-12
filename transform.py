import torchvision.transforms as transforms
import hyperparameters as hyper
from skimage.io import imread


def transform(image_path):
    flower_transform = transforms.Compose(
        [
            transforms.ToPILImage(),
            transforms.Resize((hyper.IMAGE_W, hyper.IMAGE_H)),
            transforms.ToTensor(),
            transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225))
        ])
    image = imread(image_path)
    return flower_transform(image).unsqueeze(0)
