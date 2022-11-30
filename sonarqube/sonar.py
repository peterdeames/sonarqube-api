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
            project_lst.append("Already Exists")
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
                project_lst.append("Setup Successful")
                project_lst.append(response.reason)
            else:
                project_lst.append("Setup Failed")
                error = response.json()
                error = error["errors"]
                for msg in error:
                    project_lst.append(msg["msg"])
        data.append(project_lst)
    print()
    print(tabulate(data, headers=["Project", "Status", "Response"]))
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
            project_lst.append("")
            project_lst.append("Does not Exist")
        else:
            if dryrun:
                project_lst.append("FALSE")
                project_lst.append("This request would delete the project")
            else:
                project_lst.append("FALSE")
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
                    project_lst.append("Deleted Successfully")
                    project_lst.append(response.reason)
                else:
                    project_lst.append("Delete Failed")
                    error = response.json()
                    error = error["errors"]
                    for msg in error:
                        project_lst.append(msg["msg"])
        data.append(project_lst)
    print()
    print(tabulate(data, headers=["Project", "Dry Run", "Status", "Response"]))
    print()


def create_permission(url, token, name, description="", pattern=None):
    """
    Function to setup permission templates.

    This function is intented setup a basic permission template

    Parameters
    ----------
    arg1 : str
        base URL of SonarQube
    arg2 : str
        token of account to setup the project
    arg3 : str
        name of permission to be setup
    arg4 : str
        description of the permission (optional)
    arg5 : str
        Project key pattern. Must be a valid Java regular expression (optional)

    Returns
    -------
    bool
        true or false of permissin setup

    """
    urltopost = url + "/api/permissions/search_templates"
    permission_name = name.lower().strip()
    response = requests.get(
        urltopost + "?q=" + permission_name, auth=(token, ""), timeout=30
    )
    check_flag = __check_setup(response, permission_name, "permissionTemplates")
    if check_flag:
        logging.info("Permission (%s) Already Exists", permission_name)
        return False
    else:
        if pattern is None:
            urltopost = (
                url
                + "/api/permissions/create_template?name="
                + permission_name
                + "&description="
                + description
            )
        else:
            urltopost = (
                url
                + "/api/permissions/create_template?name="
                + permission_name
                + "&description="
                + description
                + "&projectKeyPattern="
                + pattern
            )
        response = requests.post(urltopost, auth=(token, ""), timeout=30)
        if response.ok:
            logging.info("Permission (%s) has been setup", permission_name)
            return True
        else:
            logging.error("Failed setup permission (%s)", permission_name)
            error = response.json()
            error = error["errors"]
            for msg in error:
                logging.error("%s", msg["msg"])
            return False


def permission_add_group(url, token, template_name, permissions, group_name):
    """
    Function to setup permission templates.

    This function is intented setup a basic permission template

    Parameters
    ----------
    arg1 : str
        base URL of SonarQube
    arg2 : str
        token of account to setup the project
    arg3 : str
        name of permission to be updated
    arg4 : str
        comma seperated list of permissions to add
        Possible values: admin, codeviewer, issueadmin, securityhotspotadmin, scan, user
    arg4 : str
        name of group to be added to the permission

    Returns
    -------
    bool
        true or false of permissin setup

    """
    result = ""
    permissionlist = permissions.split(",")
    for permission in permissionlist:
        urltopost = url + "/api/permissions/add_group_to_template"
        response = requests.post(
            urltopost
            + "?templateName="
            + template_name
            + "&permission="
            + permission.lower()
            + "&groupName="
            + group_name,
            auth=(token, ""),
            timeout=30,
        )
        if response.ok:
            logging.info(
                "%s added to template %s with permission %s",
                group_name,
                template_name,
                permission,
            )
            if result is not False:
                result = True
        else:
            logging.error("Failed add %s to permission (%s)", group_name, template_name)
            error = response.json()
            error = error["errors"]
            for msg in error:
                logging.error("%s", msg["msg"])
                result = True
    return result
