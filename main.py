#!/usr/bin/env python3

import os
import requests

from yaml import load, Loader


###########
# Globals #
###########

CONFIG_FILENAME = "./apps.yaml"
OUTPUT_FOLDER = "./output"


def parse_config(file_name):

    # Parses YAML file
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

    # Download apps from F-Droid
    for each_app in config_full["apps"]["fdroid"]:
        version_url = "https://gitlab.com/fdroid/fdroiddata/-/raw/master/metadata/" + each_app + ".yml"
        page = requests.get(version_url)
        page_data = load(page.text, Loader)
        version_app = page_data["CurrentVersionCode"]
        app_url = "https://f-droid.org/repo/" + each_app + "_" + str(version_app) + ".apk"
        apk_file = requests.get(app_url)
        print("Downloading", each_app)
        open(os.path.join(out_folder, each_app + ".apk"), 'wb').write(apk_file.content)
        print("Downloaded", each_app)

    # TODO Download apps from URLs


if __name__ == '__main__':
    main()
