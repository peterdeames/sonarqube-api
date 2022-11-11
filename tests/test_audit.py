""" audit unit tests """
import unittest
from unittest.mock import patch
from nose.tools import assert_equals
from sonarqube.audit import ping


@patch('sonarqube.audit.requests.get')
def test_ping(mock_get):
    mock_get.return_value.text = 'pong'
    response = ping('URL', 'TOKEN')
    assert_equals(response, 'pong')


if __name__ == "__main__":
    unittest.main()
