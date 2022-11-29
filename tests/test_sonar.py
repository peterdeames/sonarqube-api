""" audit unit tests """
import unittest
from unittest.mock import patch

from nose.tools import assert_equals
from sonarqube import sonar


@patch('sonarqube.audit.requests.post')
def test_permission_add_group(mock_post):
    """
    Test adding group to a permision
    """
    mock_post.status_code = 204
    status = sonar.permission_add_group('URL', 'TOKEN', 'Test', 'admin', 'admins')
    assert_equals(status, True)
