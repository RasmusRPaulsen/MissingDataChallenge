import argparse
from skimage import io
import os
import pathlib
import numpy as np
from inpaint_config import InPaintConfig
from inpaint_tools import read_file_list
from tqdm import tqdm


def inpaint_one_image(in_image, mask_image, avg_image):
    mask_image = np.squeeze(mask_image)
    inpainted_mask = np.copy(avg_image)
    inpainted_mask[mask_image == 0] = 0

    inpaint_image = inpainted_mask + in_image
    return inpaint_image


def inpaint_images(settings):
    input_data_dir = settings["dirs"]["input_data_dir"]
    output_data_dir = settings["dirs"]["output_data_dir"]
    data_set = settings["data_set"]
    model_dir = os.path.join(output_data_dir, "trained_model")

    inpainted_result_dir = os.path.join(output_data_dir, f"inpainted_{data_set}")
    pathlib.Path(inpainted_result_dir).mkdir(parents=True, exist_ok=True)

    print(f"InPainting {data_set} and placing results in {inpainted_result_dir} with model from {model_dir}")

    avg_img_name = os.path.join(model_dir, "average_image.png")
    avg_img = io.imread(avg_img_name)

    file_list = os.path.join(input_data_dir, "data_splits", data_set + ".txt")
    file_ids = read_file_list(file_list)
    if file_ids is None:
        return

    print(f"Inpainting {len(file_ids)} images")

    for idx in tqdm(file_ids):
        in_image_name = os.path.join(input_data_dir, "masked", f"{idx}_stroke_masked.png")
        in_mask_name = os.path.join(input_data_dir, "masks", f"{idx}_stroke_mask.png")
        out_image_name = os.path.join(inpainted_result_dir, f"{idx}.png")

        im_masked = io.imread(in_image_name)
        im_mask = io.imread(in_mask_name)

        inpainted_image = inpaint_one_image(im_masked, im_mask, avg_img)
        io.imsave(out_image_name, inpainted_image)


if __name__ == '__main__':
    args = argparse.ArgumentParser(description='InpaintImages')
    config = InPaintConfig(args)
    if config.settings is not None:
        inpaint_images(config.settings)
