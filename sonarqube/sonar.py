""" functions to manage SonarQube """

import json
import logging
import requests

# The different levels of logging, from highest urgency to lowest urgency, are:
# CRITICAL | ERROR | WARNING | INFO | DEBUG
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO
)


def _check_setup(cresponse, item, rlist):
    """
    Function to check existance of item.

    This function is intented to allow for the checking of the existance of a
    specific item in SonarQube such as if a project exists before craeting it

    Parameters
    ----------
    arg1 : str
        response to parse
    arg2 : str
        name of the item to check for
    arg3 : str
        list within the reposnse to parse

    Returns
    -------
    bool
        boolean value if the item exists or not

    """
    check_flag = False
    json_object = json.loads(cresponse.text)
    try:
        response = json_object[rlist]
        for i in response:
            if item == str(i["name"]):
                check_flag = True
    except KeyError as exception:
        logging.warning("Failed to evaluate the json response - %s", exception)
    return check_flag


def setup_project(url, token, names):
    """
    Function to setup initial project.

    This function is intented setup a basic project within SonarQube

    Parameters
    ----------
    arg1 : str
        base URL of SonarQube
    arg2 : str
        token of account to setup the project
    arg3 : str
        comma seperated string of project names

    """
    projectlist = names.split(",")
    for project in projectlist:
        urltopost = url + "/api/projects/search"
        project_name = project.lower().strip()
        response = requests.get(
            urltopost + "?projects=" + project_name, auth=(token, ""), timeout=30
        )
        check_flag = _check_setup(response, project_name, "components")
        if check_flag:
            logging.info("%s already exists!", project_name)
        else:
            urltopost = url + "/api/projects/create"
            response = requests.post(
                urltopost
                + "?name="
                + project_name.lower()
                + "&project="
                + project_name.lower(),
                auth=(token, ""),
                timeout=30,
            )
            if response.ok:
                logging.info("%s setup successfully!", project_name)
            else:
                logging.error("%s not setup", project_name)


def delete_project(url, token, names, dryrun=True):
    """
    Function to setup initial project.

    This function is intented setup a basic project within SonarQube

    Parameters
    ----------
    arg1 : str
        base URL of SonarQube
    arg2 : str
        token of account to setup the project
    arg3 : str
        comma seperated string of project names
    arg4 : bool
        True or False flag whether to delete project or not

    """
    projectlist = names.split(",")
    for project in projectlist:
        urltopost = url + "/api/projects/search"
        project_name = project.lower().strip()
        response = requests.get(
            urltopost + "?projects=" + project_name, auth=(token, ""), timeout=30
        )
        check_flag = _check_setup(response, project_name, "components")
        if not check_flag:
            logging.info("%s does not exist!", project_name)
        else:
            if dryrun:
                logging.warning("This request would delete %s", project_name)
                logging.info(
                    "If this was the intended action "
                    "please re-run with dryrun set to False"
                )
            else:
                urltopost = url + "/api/projects/delete"
                response = requests.post(
                    urltopost
                    + "?name="
                    + project_name.lower()
                    + "&project="
                    + project_name.lower(),
                    auth=(token, ""),
                    timeout=30,
                )
                if response.ok:
                    logging.info("%s deleted successfully!", project_name)
                else:
                    logging.error("%s not deleted", project_name)
