""" functions to manage SonarQube """

import json
import logging
import requests
from tabulate import tabulate

# The different levels of logging, from highest urgency to lowest urgency, are:
# CRITICAL | ERROR | WARNING | INFO | DEBUG
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO
)


def __check_setup(cresponse, item, rlist):
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
    data = []
    projectlist = names.split(",")
    for project in projectlist:
        project_lst = [project]
        urltopost = url + "/api/projects/search"
        project_name = project.lower().strip()
        response = requests.get(
            urltopost + "?projects=" + project_name, auth=(token, ""), timeout=30
        )
        check_flag = __check_setup(response, project_name, "components")
        if check_flag:
            project_lst.append('Already Exists')
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
                project_lst.append('Setup Successful')
                project_lst.append(response.reason)
            else:
                project_lst.append('Setup Failed')
                error = response.json()
                error = error['errors']
                for msg in error:
                    project_lst.append(msg['msg'])
        data.append(project_lst)
    print()
    print (tabulate(data, headers=["Project", "Status", "Response"]))
    print()


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
    data = []
    projectlist = names.split(",")
    for project in projectlist:
        project_lst = [project]
        urltopost = url + "/api/projects/search"
        project_name = project.lower().strip()
        response = requests.get(
            urltopost + "?projects=" + project_name, auth=(token, ""), timeout=30
        )
        check_flag = __check_setup(response, project_name, "components")
        if not check_flag:
            #logging.info("%s does not exist!", project_name)
            project_lst.append('')
            project_lst.append('Does not Exist')
        else:
            if dryrun:
                logging.warning("This request would delete %s", project_name)
                logging.info(
                    "If this was the intended action "
                    "please re-run with dryrun set to False"
                )
            else:
                project_lst.append('FALSE')
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
                    project_lst.append('Deleted Successfully')
                    project_lst.append(response.reason)
                else:
                    project_lst.append('Setup Failed')
                    error = response.json()
                    error = error['errors']
                    for msg in error:
                        project_lst.append(msg['msg'])
        data.append(project_lst)
    if not dryrun:
        print()
        print (tabulate(data, headers=["Project", "Dry Run", "Status", "Response"]))
        print()
