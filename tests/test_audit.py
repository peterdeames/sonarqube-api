""" audit unit tests """
import unittest
from unittest.mock import patch, Mock

from nose.tools import assert_equals
from sonarqube import audit


@patch('sonarqube.audit.requests.get')
def test_ping(mock_get):
    mock_get.return_value.text = 'pong'
    response = audit.ping('URL', 'TOKEN')
    assert_equals(response, 'pong')


@patch('sonarqube.audit.requests.get')
def test_get_health(mock_get):
    mock_get.return_value.text = '{"health":"GREEN","causes":[]}'
    response = audit.ping('URL', 'TOKEN')
    assert_equals(response, '{"health":"GREEN","causes":[]}')


""" @patch('sonarqube.audit.requests.get')
def test_get_version(mock_get):
    mock_get.side_effect = [9.7,'{"upgrades":[],"latestLTS":"8.9","updateCenterRefresh":"2022-11-15T21:31:29+0000"}']
    response = audit.get_version('URL', 'TOKEN')
    assert_equals(response, '8.9') """


if __name__ == "__main__":
    unittest.main()
