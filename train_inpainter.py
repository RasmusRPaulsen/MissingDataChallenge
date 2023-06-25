import argparse
from skimage import io
import os
import pathlib
import numpy as np
from inpaint_config import InPaintConfig
from inpaint_tools import read_file_list


def train_in_painter(settings):
    """
    Computes an average image based on all images in the training set.
    """
    input_data_dir = settings["dirs"]["input_data_dir"]
    output_data_dir = settings["dirs"]["output_data_dir"]
    training_set = settings["data_set"] + ".txt"
    output_dir = os.path.join(output_data_dir, "trained_model")
    pathlib.Path(output_dir).mkdir(parents=True, exist_ok=True)

    print(f'Training inpainter with data set: {training_set} and placing model in {output_dir}')

    file_list = os.path.join(input_data_dir, "data_splits", training_set)
    file_ids = read_file_list(file_list)
    if file_ids is None:
        return

    print(f"Training on {len(file_ids)} images")

    sum_image = None
    for idx in file_ids:
        in_image_name = os.path.join(input_data_dir, "originals", f"{idx}.jpg")

        im_org = io.imread(in_image_name)
        im_shape = im_org.shape

        if sum_image is None:
            sum_image = np.zeros(im_shape, dtype=np.float64)
        sum_image = sum_image + im_org

    n_images = len(file_ids)
    avg_img = np.divide(sum_image, n_images)
    avg_img_name = os.path.join(output_dir, "average_image.png")
    io.imsave(avg_img_name, avg_img)


if __name__ == '__main__':
    args = argparse.ArgumentParser(description='TrainInPainter')
    config = InPaintConfig(args)
    if config.settings is not None:
        train_in_painter(config.settings)
