import argparse
import os
import pathlib
from inpaint_config import InPaintConfig
from datetime import datetime
import shutil
import re


def sanitize_string(string_in):
    """
    Will replace bad characters with _
    """
    string_in = os.path.basename(string_in)
    string_in = os.path.splitext(string_in)[0]
    string_in = string_in.strip().replace(':', '_')
    string_in = string_in.strip().replace('-', '_')
    string_in = string_in.strip().replace('.', '_')
    re.sub(r'[^\w\-_\. ]', '_', string_in)
    return string_in


def submit_inpainting(settings):
    output_data_dir = settings["dirs"]["output_data_dir"]
    data_set = settings["data_set"]
    inpainted_result_dir = os.path.join(output_data_dir, f"inpainted_{data_set}")
    team_name = settings["team_data"]["name"]
    method_name = settings["training_parms"]["method"]
    submission_dir = os.path.join(output_data_dir, "submissions")
    pathlib.Path(submission_dir).mkdir(parents=True, exist_ok=True)

    team_name = sanitize_string(team_name)
    method_name = sanitize_string(method_name)

    timestamp = datetime.now().strftime(r'%d%m%y_%H%M%S')
    submission_file = os.path.join(submission_dir, f"{team_name}-{method_name}-{data_set}-{timestamp}")
    print(f"Creating {submission_file}.zip from inpaintings in {inpainted_result_dir}")

    shutil.make_archive(submission_file, format='zip', root_dir=inpainted_result_dir)


if __name__ == '__main__':
    args = argparse.ArgumentParser(description='SubmitInpainting')
    config = InPaintConfig(args)
    if config.settings is not None:
        submit_inpainting(config.settings)

