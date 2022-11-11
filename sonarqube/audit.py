""" functions to help audit SonarQube """

import json
import logging
import requests

# The different levels of logging, from highest urgency to lowest urgency, are:
# CRITICAL | ERROR | WARNING | INFO | DEBUG
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO
)


def __check_version(url, token):
    urltopost = url + "/api/server/version"
    current_version = requests.get(urltopost, auth=(token, ""), timeout=30)
    return current_version


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

    Returns
    -------
    str
        current verion of SonarQube

    """
    upgrades_available = False
    current_version = __check_version(url, token)
    urltopost = url + "/api/system/upgrades"
    upgradecheck = requests.get(urltopost, auth=(token, ""), timeout=30)
    try:
        json_object = json.loads(upgradecheck.text)
        lts = json_object["latestLTS"]
    except KeyError:
        lts = 9999999
    if current_version.ok:
        tmp_version = current_version.text[0:3]
        if len(json_object["upgrades"]) > 0:
            upgrades_available = True
        if float(lts) > float(tmp_version) and lts < 1000:
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
    return current_version.text


def get_license_details(url, token):
    """
    Function to get system metrics (expects SonarQube verson 9.3 +)

    This function is intented to get the system metrcis of SonarQube

    Parameters
    ----------
    arg1 : str
        base URL of SonarQube
    arg2 : str
        token of account to setup the project

    Returns
    -------
    dict
        dictionary of metrics

    """
    current_version = __check_version(url, token)
    metrics = {}
    if float(current_version.text[0:3]) <= 9.3:
        logging.warning(
            "Current installation of SonarQube is < 9.3. "
            "This function is only available with version >= 9.3"
        )
    else:
        urltopost = url + "/api/monitoring/metrics"
        response = requests.get(urltopost, auth=(token, ""), timeout=30)
        for item in response.text.split("\n"):
            if item.startswith("sonarqube_license_number_of_lines_remaining_total"):
                value = item.split()
                metrics["remaining_loc"] = value[1]
                logging.info("%s lines of code left before license limit", value[1])
            if item.startswith("sonarqube_license_number_of_lines_analyzed_total"):
                value = item.split()
                metrics["used_loc"] = value[1]
                logging.info("%s lines of code analysed", value[1])
            if item.startswith("sonarqube_license_days_before_expiration_total"):
                value = item.split()
                metrics["expiration_days"] = value[1]
                logging.info("%s days before license expires", value[1])
    return metrics
