import argparse
import os
import pathlib
from inpaint_config import InPaintConfig
from datetime import datetime
import shutil
import requests


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

# https://stackabuse.com/how-to-upload-files-with-pythons-requests-library/
# Currently not working for fungi server
def upload_to_challenge_server():
    print("Uploading to server")
    file_name = "C://data//Cats//missing_data_output//submissions//RasMouse-validation_200-220623_234343.zip"
    test_file = open(file_name, "rb")
    # test_url = "http://fungi.compute.dtu.dk:8080"
    test_url = "http://httpbin.org/post"
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
        # upload_to_challenge_server()
        