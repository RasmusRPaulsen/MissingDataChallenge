import argparse
import os
import pathlib
from inpaint_config import InPaintConfig
from datetime import datetime
import shutil
import re
import requests


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
    server_name = settings["challenge_server"]["address"]
    submission_dir = os.path.join(output_data_dir, "submissions")
    pathlib.Path(submission_dir).mkdir(parents=True, exist_ok=True)

    team_name = sanitize_string(team_name)
    method_name = sanitize_string(method_name)

    timestamp = datetime.now().strftime(r'%d%m%y_%H%M%S')
    submission_file = os.path.join(submission_dir, f"{team_name}-{method_name}-{data_set}-{timestamp}")
    print(f"Creating {submission_file}.zip from inpaintings in {inpainted_result_dir}")

    shutil.make_archive(submission_file, format='zip', root_dir=inpainted_result_dir)

    print(f"Uploading to server: {server_name}")
    file_name = f"{submission_file}.zip"
    #file_name = "C://data//Cats//missing_data_output//submissions//RasMouse-MeanImageInpaint-validation_100-290623_211751.zip"
    test_file = open(file_name, "rb")
    test_url = server_name
    # test_url = "http://fungi.compute.dtu.dk:8080"
    # test_url = "http://httpbin.org/post"
    # test_url = "http://10.197.110.212:8080"
    # test_url = "http://localhost:8080"
    test_response = requests.post(test_url, files={"form_field_name": test_file})

    if test_response.ok:
        print("Upload completed successfully!")
        print(test_response.text)
    else:
        print("Something went wrong!")


if __name__ == '__main__':
    args = argparse.ArgumentParser(description='SubmitInpainting')
    config = InPaintConfig(args)
    if config.settings is not None:
        submit_inpainting(config.settings)

