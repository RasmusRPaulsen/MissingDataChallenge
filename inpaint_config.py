import json
from pathlib import Path

class InPaintConfig:
    def __init__(self, args):
        self.settings = None
        args.add_argument('-c', '--config', default=None, type=str,
                          help='JSON config file (default: None)')
        args = args.parse_args()
        if hasattr(args, 'config') and args.config is not None:
            self.load_settings(args.config)
        else:
            print("Configuration file need to be specified. Add '-c config.json', for example.")

    def load_settings(self, file_name):
        try:
            with open(file_name, 'r') as openfile:
                self.settings = json.load(openfile)
        except IOError as e:
            print(f"I/O error({e.errno}): {e.strerror}: {file_name}")
            self.settings = None

    def save_settings(self, file_name):
        try:
            with Path(file_name).open('wt') as handle:
                json.dump(self.settings, handle, indent=4, sort_keys=False)
        except IOError as e:
            print(f"I/O error({e.errno}): {e.strerror}: {file_name}")
