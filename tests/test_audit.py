""" audit unit tests """
import unittest
from unittest.mock import patch

from nose.tools import assert_equals
from sonarqube import audit


@patch('sonarqube.audit.requests.get')
def test__check_version(mock_get):
    """
    Test for checking the version of SonarQube
    """
    mock_get.return_value = '9.7.1.62043'
    response = audit.__check_version('URL', 'TOKEN')
    assert_equals(response, '9.7.1.62043')


@patch('sonarqube.audit.requests.get')
def test_ping(mock_get):
    """
    Test ping SonarQube
    """
    mock_get.return_value.text = 'pong'
    response = audit.ping('URL', 'TOKEN')
    assert_equals(response, 'pong')


@patch('sonarqube.audit.requests.get')
def test_get_health_green(mock_get):
    """
    Test the health of SonarQube
    """
    mock_get.return_value.text = '{"health":"GREEN","causes":[]}'
    response = audit.get_health('URL', 'TOKEN')
    assert_equals(response, '{"health":"GREEN","causes":[]}')


@patch('sonarqube.audit.requests.get')
def test_get_health_yellow(mock_get):
    """
    Test the health of SonarQube
    """
    mock_get.return_value.text = '{"health":"YELLOW","causes":[]}'
    response = audit.get_health('URL', 'TOKEN')
    assert_equals(response, '{"health":"YELLOW","causes":[]}')


@patch('sonarqube.audit.requests.get')
def test_get_health_red(mock_get):
    """
    Test the health of SonarQube
    """
    mock_get.return_value.text = '{"health":"RED","causes":[]}'
    response = audit.get_health('URL', 'TOKEN')
    assert_equals(response, '{"health":"RED","causes":[]}')


""" @patch('sonarqube.audit.requests.get')
def test_get_version(mock_get):
    mock_get.side_effect = [9.7,'{"upgrades":[],"latestLTS":"8.9","updateCenterRefresh":"2022-11-15T21:31:29+0000"}']
    response = audit.get_version('URL', 'TOKEN')
    assert_equals(response, '8.9') """


if __name__ == "__main__":
    unittest.main()
