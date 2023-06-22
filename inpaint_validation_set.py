import argparse
from skimage import io
import os
import pathlib
import numpy as np
from inpaint_config import InPaintConfig
from inpaint_tools import read_file_list

def inpaint_one_image(in_image, mask_image, avg_image):
    mask_image = np.squeeze(mask_image)
    inpainted_mask = np.copy(avg_image)
    inpainted_mask[mask_image == 0] = 0

    inpaint_image = inpainted_mask + in_image
    return inpaint_image
    # inpainted_mask = avg_image[mask_image > 0]
    # return inpainted_mask


def inpaint_validation_set(settings):
    print("InPainting the a validation set")

    input_data_dir = settings["dirs"]["input_data_dir"]
    output_data_dir = settings["dirs"]["output_data_dir"]
    data_set = settings["sets"]["validation_files"]

    inpainted_result_dir = os.path.join(output_data_dir, "inpainted_validation")
    pathlib.Path(inpainted_result_dir).mkdir(parents=True, exist_ok=True)

    avg_img_name = os.path.join(output_data_dir, "average_image.png")
    avg_img = io.imread(avg_img_name)

    file_list = os.path.join(input_data_dir, "data_splits", data_set)
    file_ids = read_file_list(file_list)
    if file_ids is None:
        return

    print(f"Inpainting {len(file_ids)} images")

    for idx in file_ids:
        in_image_name = os.path.join(input_data_dir, "all_cats_masked", f"{idx}_preprocessed_stroke_masked.png")
        in_mask_name = os.path.join(input_data_dir, "all_cats_masked", f"{idx}_preprocessed_stroke_mask.png")
        out_image_name = os.path.join(inpainted_result_dir, f"{idx}.png")

        im_masked = io.imread(in_image_name)
        im_mask = io.imread(in_mask_name)

        inpainted_image = inpaint_one_image(im_masked, im_mask, avg_img)

        io.imsave(out_image_name, inpainted_image)

if __name__ == '__main__':
    args = argparse.ArgumentParser(description='InpaintTrainingSet')
    config = InPaintConfig(args)
    if config.settings is not None:
        inpaint_validation_set(config.settings)
