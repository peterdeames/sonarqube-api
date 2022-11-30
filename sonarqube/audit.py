""" functions to help audit SonarQube """

import logging
import requests
from tabulate import tabulate

# The different levels of logging, from highest urgency to lowest urgency, are:
# CRITICAL | ERROR | WARNING | INFO | DEBUG
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO
)


def __check_version(url, token):
    urltopost = url + "/api/server/version"
    current_version = requests.get(urltopost, auth=(token, ""), timeout=30)
    return current_version


def get_health(url, token):
    """
    Function to return the health of SonarQube
    """
    urltopost = url + "/api/system/health"
    response = requests.get(urltopost, auth=(token, ""), timeout=30)
    health = response.json()
    # print(health)
    health = health["health"]
    if health == "GREEN":
        logging.info("Your SonarQube health is currently: %s", health)
    else:
        logging.error(
            "Your SonarQube health is currently: %s "
            "You should review the cause and remediate the issue ASAP",
            health,
        )
    return response.text


def ping(url, token):
    """simple ping"""
    urltopost = url + "/api/system/ping"
    response = requests.get(urltopost, auth=(token, ""), timeout=30)
    logging.info("%s", response.text)
    return response.text


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
    response = requests.get(urltopost, auth=(token, ""), timeout=30)
    upgradecheck = response.json()
    try:
        lts = upgradecheck["latestLTS"]
    except KeyError:
        lts = "9999999"
    if current_version.ok:
        tmp_version = current_version.text[0:3]
        if len(upgradecheck["upgrades"]) > 0:
            upgrades_available = True
        if float(lts) > float(tmp_version) and float(lts) < 1000:
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
                    "There are %d upgrades available", len(upgradecheck["upgrades"])
                )
        else:
            logging.info("You are currently running version: %s", current_version.text)
            if upgrades_available:
                logging.info(
                    "There are %d upgrades available", len(upgradecheck["upgrades"])
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
    data = []
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
            license_lst = []
            if item.startswith("sonarqube_license_number_of_lines_remaining_total"):
                value = item.split()
                metrics["remaining_loc"] = value[1]
                license_lst.append("Lines of Code Remaining")
                license_lst.append(value[1])
                data.append(license_lst)
            if item.startswith("sonarqube_license_number_of_lines_analyzed_total"):
                value = item.split()
                metrics["used_loc"] = value[1]
                license_lst.append("Lines of Code Used")
                license_lst.append(value[1])
                data.append(license_lst)
            if item.startswith("sonarqube_license_days_before_expiration_total"):
                value = item.split()
                metrics["expiration_days"] = value[1]
                license_lst.append("License Expires")
                license_lst.append(value[1] + " days")
                data.append(license_lst)
    print()
    print(tabulate(data, headers=["Detail", "Value"]))
    print()
    return metrics


def get_languages(url, token):
    """
    Function to get languages supported by SonarQube

    This function is intented to get the system supported languages

    Parameters
    ----------
    arg1 : str
        base URL of SonarQube
    arg2 : str
        token of account to setup the project

    Returns
    -------
    list
        list of language names

    """
    data = []
    urltopost = url + "/api/languages/list"
    response = requests.get(urltopost, auth=(token, ""), timeout=30)
    languages = response.json()
    languages = languages["languages"]
    for language in languages:
        language_lst = []
        language_lst.append(language["key"])
        language_lst.append(language["name"])
        data.append(language_lst)
    print()
    print(tabulate(data, headers=["Key", "Name"]))
    print()
    return data


def get_installed_plugins(url, token):
    """
    Function to get languages supported by SonarQube

    This function is intented to get the system supported languages

    Parameters
    ----------
    arg1 : str
        base URL of SonarQube
    arg2 : str
        token of account to setup the project

    Returns
    -------
    list
        list of language names

    """
    data = []
    urltopost = url + "/api/plugins/installed"
    response = requests.get(urltopost, auth=(token, ""), timeout=30)
    plugins = response.json()
    plugins = plugins["plugins"]
    for plugin in plugins:
        plugin_lst = []
        plugin_lst.append(plugin["name"])
        plugin_lst.append(plugin["description"])
        plugin_lst.append(plugin["version"])
        data.append(plugin_lst)
    print()
    print(tabulate(data, headers=["Name", "Description", "Version"]))
    print()
    return data
