""" functions to help audit SonarQube """

import json
import logging
import requests

# The different levels of logging, from highest urgency to lowest urgency, are:
# CRITICAL | ERROR | WARNING | INFO | DEBUG
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO
)


def get_version(url, token):
    """
    Function to get current version.

    This function is intented to get the current version of SonarQube,
    and it will inform if current version is behind LTS or if there are upgrades available

    Parameters
    ----------
    arg1 : str
        base URL of SonarQube
    arg2 : str
        token of account to setup the project

    """
    upgrades_available = False
    urltopost = url + "/api/server/version"
    current_version = requests.get(urltopost, auth=(token, ""), timeout=30)
    urltopost = url + "/api/system/upgrades"
    upgradecheck = requests.get(urltopost, auth=(token, ""), timeout=30)
    json_object = json.loads(upgradecheck.text)
    lts = json_object["latestLTS"]
    if current_version.ok:
        tmp_version = current_version.text[0:3]
        if len(json_object["upgrades"]) > 0:
            upgrades_available = True
        if float(lts) > float(tmp_version):
            logging.warning(
                "You are running a version of SonarQube that is behind the LTS"
                ": %s.\nYou should consider upgrading to %s LTS",
                current_version.text,
                lts,
            )
        elif float(lts) == float(tmp_version):
            logging.info(
                "Congratulations! You are currently running the LTS version (%s)",
                current_version.text,
            )
            if upgrades_available:
                logging.info(
                    "There are %d upgrades available", len(json_object["upgrades"])
                )
        else:
            logging.info("You are currently running version: %s", current_version.text)
            if upgrades_available:
                logging.info(
                    "There are %d upgrades available", len(json_object["upgrades"])
                )
    else:
        logging.error("Failed to get version")
