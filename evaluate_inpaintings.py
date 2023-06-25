import argparse
from skimage import io
import os
import pathlib
from inpaint_config import InPaintConfig
from inpaint_tools import read_file_list
from skimage.metrics import structural_similarity
from skimage.metrics import mean_squared_error
from skimage.metrics import peak_signal_noise_ratio
from tqdm import tqdm


def compute_inpaint_metrics(org_img, inpainted_img):
    mse_val = mean_squared_error(org_img, inpainted_img)
    ssim = structural_similarity(org_img, inpainted_img, channel_axis=2)
    psnr = peak_signal_noise_ratio(org_img, inpainted_img)

    return {"mse": mse_val, "ssim": ssim, "psnr": psnr}


def evaluate_inpainting(settings):
    input_data_dir = settings["dirs"]["input_data_dir"]
    output_data_dir = settings["dirs"]["output_data_dir"]
    data_set = settings["data_set"]
    inpainted_result_dir = os.path.join(output_data_dir, f"inpainted_{data_set}")

    result_dir = os.path.join(output_data_dir, "evaluations")
    pathlib.Path(result_dir).mkdir(parents=True, exist_ok=True)
    evaluation_file = os.path.join(result_dir, f"{data_set}_results.csv")

    print(f"Evaluating {data_set} and placing evaluations in {evaluation_file}")

    file_list = os.path.join(input_data_dir, "data_splits", data_set + ".txt")
    file_ids = read_file_list(file_list)
    if file_ids is None:
        return

    f = open(evaluation_file, 'w')
    print(f"Evaluating {len(file_ids)} images")

    for idx in tqdm(file_ids):
        org_image_name = os.path.join(input_data_dir, "originals", f"{idx}.jpg")
        inpainted_image_name = os.path.join(inpainted_result_dir, f"{idx}.png")

        im_org = io.imread(org_image_name)
        im_inpainted = io.imread(inpainted_image_name)

        metrics = compute_inpaint_metrics(im_org, im_inpainted)
        # print(f'MSE: {metrics["mse"]} SSIM: {metrics["ssim"]} PSNR: {metrics["psnr"]}')
        f.write(f'{idx}, {metrics["mse"]}, {metrics["ssim"]}, {metrics["psnr"]}\n')


if __name__ == '__main__':
    args = argparse.ArgumentParser(description='EvaluateInPaintings')
    config = InPaintConfig(args)
    if config.settings is not None:
        evaluate_inpainting(config.settings)
