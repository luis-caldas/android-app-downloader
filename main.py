#!/usr/bin/env python3

import os
import sys
import subprocess


###########
# Globals #
###########

CONFIG_FILENAME = "./apps.yaml"
GAPI_CONFIG = "./gapi.conf"
OUTPUT_FOLDER = "./output"


def parse_config(file_name):

    # Parses YAML file
    from yaml import load, Loader
    with open(file_name, "r") as file:
        return load(file.read(), Loader)


def main():

    # Get the scripts folder
    script_folder = os.path.dirname(os.path.realpath(__file__))

    # Parse config file
    config_full = parse_config(os.path.join(script_folder, CONFIG_FILENAME))

    # Check if output folder exists and create it
    out_folder = os.path.join(script_folder, OUTPUT_FOLDER)
    if not os.path.isdir(out_folder):
        os.mkdir(out_folder)

    # Download all apps from google play
    config_file = os.path.join(script_folder, GAPI_CONFIG)
    gplay_command = ["gplaycli", "-d", *config_full["apps"]["google-play"], "-y", "-f", out_folder, "-c", config_file]
    subprocess.run(gplay_command, stdout=sys.stdout, stderr=sys.stderr, universal_newlines=True)

    # TODO Download apps from F-Droid
    pass

    # TODO Download apps from URLs


if __name__ == '__main__':
    main()

