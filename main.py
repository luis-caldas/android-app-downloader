#!/usr/bin/env python3

import os


###########
# Globals #
###########

CONFIG_FILENAME = "./apps.yaml"
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

    # TODO Download apps from GPlay

    # TODO Download apps from F-Droid
    for each_app in config_full["apps"]["fdroid"]:
        print(get_fdroid_url(each_app))

    # TODO Download apps from URLs


if __name__ == '__main__':
    main()

