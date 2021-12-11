#!/usr/bin/env python3

import os
import sys
import requests
import subprocess

from yaml import load, Loader

from bs4 import BeautifulSoup


###########
# Globals #
###########

CONFIG_FILENAME = "./apps.yaml"
OUTPUT_FOLDER = "./output"
SEPARATOR = "-" * 4

def pprint(*args):
    print("[%10s]" % args[0], "[%20s]" % args[1], "-", *args[2:])


def main():

    # Get the scripts folder
    script_folder = os.path.dirname(os.path.realpath(__file__))

    # Parse config file
    with open(os.path.join(script_folder, CONFIG_FILENAME), 'r') as file:
        config_full = load(file.read(), Loader)

    # Check if output folder exists and create it
    out_folder = os.path.join(script_folder, OUTPUT_FOLDER)
    if not os.path.isdir(out_folder):
        os.mkdir(out_folder)

    pprint("Info", "Initializing", SEPARATOR, "Google Play", SEPARATOR)

    # Download all apps from google play
    for each_app in config_full["apps"]["google-play"]:
        break
        download_url = "https://apkpure.com/latest/%s/download" % each_app
        pprint("GPlay", "Downloading", each_app)
        html_app_data = requests.get(download_url)
        bs_app_data = BeautifulSoup(html_app_data.text, "lxml")
        print(bs_app_data)
        print(bs_app_data.find_all("a", id="download_link"))
        download_link = bs_app_data.find_all("a", id="download_link")[-1]
        apk_file = requests.get(download_link)
        open(os.path.join(out_folder, each_app + ".apk"), 'wb').write(apk_file.content)
        pprint("GPlay", "Finished", each_app)

    pprint("Info", "Finished", SEPARATOR, "Google Play", SEPARATOR)
    pprint("Info", "Initializing", SEPARATOR, "FDroid", SEPARATOR)

    # Download apps from F-Droid
    for each_app in config_full["apps"]["fdroid"]:
        version_url = "https://gitlab.com/fdroid/fdroiddata/-/raw/master/metadata/%s.yml" % each_app
        pprint("FDroid", "Getting Version", each_app)
        page_data = load(requests.get(version_url).text, Loader)
        pprint("FDroid", "Downloading", each_app)
        app_url = "https://f-droid.org/repo/%s_%s.apk" % (each_app, page_data["CurrentVersionCode"])
        apk_file = requests.get(app_url)
        open(os.path.join(out_folder, each_app + ".apk"), 'wb').write(apk_file.content)
        pprint("FDroid", "Finished", each_app)

    pprint("Info", "Finished", SEPARATOR, "FDroid", SEPARATOR)
    pprint("Info", "Initializing", SEPARATOR, "Direct", SEPARATOR)

    # Download apps from URLs
    urls_dict = config_full["apps"]["url"]
    for each_app in urls_dict:
        pprint("Direct", "Downloading", each_app)
        apk_file = requests.get(urls_dict[each_app])
        open(os.path.join(out_folder, each_app + ".apk"), 'wb').write(apk_file.content)
        pprint("Direct", "Finished", each_app)

    pprint("Info", "Finished", SEPARATOR, "Direct", SEPARATOR)

if __name__ == '__main__':
    main()
