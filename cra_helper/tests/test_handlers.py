import logging
from unittest.mock import MagicMock, patch

from django.test import TestCase
from django.conf import settings
from django.core.servers.basehttp import get_internal_wsgi_application
from django.http import Http404

import cra_helper
from cra_helper.handlers import CRAStaticFilesHandler


# Quiet down logging
logging.disable(logging.CRITICAL)


class TestCRAStaticFilesHandler(TestCase):
    def setUp(self):
        self.handler = CRAStaticFilesHandler(get_internal_wsgi_application())
        self._request = MagicMock(path='/fizz/buzz.jpg')
        setattr(settings, 'DEBUG', True)

    def test_should_serve_when_file_exists(self):
        self.handler._should_handle = MagicMock(return_value=True)
        self.handler.serve = MagicMock()

        self.handler.get_response(self._request)

        self.assertTrue(self.handler.serve.called)

    @patch('cra_helper.handlers.redirect')
    def test_should_redirect_when_file_404s(self, mock_redirect):
        self.handler._should_handle = MagicMock(return_value=True)
        self.handler.serve = MagicMock(side_effect=Http404)

        self.handler.get_response(self._request)

        self.assertTrue(mock_redirect.called)

    @patch('cra_helper.handlers.redirect')
    def test_should_redirect_back_to_cra_liveserver(self, mock_redirect):
        cra_helper.handlers.CRA_URL = 'http://foo.bar'
        self.handler._should_handle = MagicMock(return_value=True)
        self.handler.serve = MagicMock(side_effect=Http404)

        self.handler.get_response(self._request)

        mock_redirect.assert_called_with('http://foo.bar/fizz/buzz.jpg')

    @patch('cra_helper.handlers.redirect')
    def test_should_not_redirect_when_file_404s_in_prod(self, mock_redirect):
        setattr(settings, 'DEBUG', False)
        self.handler._should_handle = MagicMock(return_value=True)
        self.handler.serve = MagicMock(side_effect=Http404)

        self.handler.get_response(self._request)

        self.assertFalse(mock_redirect.called)
