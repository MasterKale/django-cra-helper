import logging
from unittest.mock import MagicMock, patch
from urllib import error as url_error

from django.conf import settings
from django.test import TestCase

from cra_helper import CRA_URL, server_check

# Quiet down logging
logging.disable(logging.CRITICAL)


class TestHostedByLiveserver(TestCase):
    def setUp(self):
        setattr(settings, 'DEBUG', True)

    def test_returns_boolean(self):
        self.assertIsInstance(server_check.hosted_by_liveserver(CRA_URL), bool)

    @patch('urllib.request.urlopen')
    def test_returns_true_when_cra_running_and_debug(self, mock_urlopen):
        mock_urlopen.return_value = MagicMock(status=200)
        self.assertTrue(server_check.hosted_by_liveserver(CRA_URL))

    @patch('urllib.request.urlopen')
    def test_returns_false_when_cra_running_and_production(self, mock_urlopen):
        mock_urlopen.return_value = MagicMock(status=200)
        setattr(settings, 'DEBUG', False)
        self.assertFalse(server_check.hosted_by_liveserver(CRA_URL))

    @patch('urllib.request.urlopen')
    def test_returns_false_when_cra_errors(self, mock_urlopen):
        mock_urlopen.return_value = MagicMock(status=500)
        self.assertFalse(server_check.hosted_by_liveserver(CRA_URL))

    @patch('urllib.request.urlopen')
    def test_returns_false_when_cra_not_running(self, mock_urlopen):
        mock_urlopen.side_effect = url_error.URLError('CRA not running')
        self.assertFalse(server_check.hosted_by_liveserver(CRA_URL))
