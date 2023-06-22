import argparse
from skimage import io
import os
import pathlib
import numpy as np
from inpaint_config import InPaintConfig
from inpaint_tools import read_file_list
from skimage.metrics import structural_similarity
from skimage.metrics import mean_squared_error
from skimage.metrics import peak_signal_noise_ratio
from datetime import datetime
import shutil


def submit_validation_set(settings):
    print("Submitting a validation set")

    input_data_dir = settings["dirs"]["input_data_dir"]
    output_data_dir = settings["dirs"]["output_data_dir"]
    data_set = settings["sets"]["validation_files"]
    team_name = settings["team_data"]["name"]
    inpainted_result_dir = os.path.join(output_data_dir, "inpainted_validation")
    submission_dir = os.path.join(output_data_dir, "submissions")
    pathlib.Path(submission_dir).mkdir(parents=True, exist_ok=True)
    set_clean = os.path.splitext(data_set)[0]

    timestamp = datetime.now().strftime(r'%d%m%y_%H%M%S')
    submission_file = os.path.join(submission_dir, f"{team_name}-{set_clean}-{timestamp}")
    print(f"Creating {submission_file}")

    shutil.make_archive(submission_file, format='zip', root_dir=inpainted_result_dir)


if __name__ == '__main__':
    args = argparse.ArgumentParser(description='EvaluateValidationSet')
    config = InPaintConfig(args)
    if config.settings is not None:
        submit_validation_set(config.settings)
