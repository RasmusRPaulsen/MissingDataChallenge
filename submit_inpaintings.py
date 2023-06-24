import argparse
import os
import pathlib
from inpaint_config import InPaintConfig
from datetime import datetime
import shutil


def submit_inpainting(settings):
    output_data_dir = settings["dirs"]["output_data_dir"]
    data_set = settings["data_set"]
    inpainted_result_dir = os.path.join(output_data_dir, f"inpainted_{data_set}")
    team_name = settings["team_data"]["name"]
    submission_dir = os.path.join(output_data_dir, "submissions")
    pathlib.Path(submission_dir).mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime(r'%d%m%y_%H%M%S')
    submission_file = os.path.join(submission_dir, f"{team_name}-{data_set}-{timestamp}")
    print(f"Creating {submission_file} from inpaintings in {inpainted_result_dir}")

    shutil.make_archive(submission_file, format='zip', root_dir=inpainted_result_dir)


if __name__ == '__main__':
    args = argparse.ArgumentParser(description='SubmitInpainting')
    config = InPaintConfig(args)
    if config.settings is not None:
        submit_inpainting(config.settings)
