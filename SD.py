import time
import keras_cv
from tensorflow import keras
import matplotlib.pyplot as plt
import argparse

parser = argparse.ArgumentParser(description='Creates a photomosaic from input images')
parser.add_argument('--prompt', required=True, default="create an image", help="create an image with a prompt")
args = parser.parse_args()

model = keras_cv.models.StableDiffusion(img_width=512, img_height=512)

images = model.text_to_image("photograph of an astronaut riding a horse", batch_size=3)


def plot_images(images):
    plt.figure(figsize=(20, 20))
    for i in range(len(images)):
        ax = plt.subplot(1, len(images), i + 1)
        plt.imshow(images[i])
        plt.axis("off")


plot_images(images)