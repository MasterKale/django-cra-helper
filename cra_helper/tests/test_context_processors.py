import logging
from unittest.mock import MagicMock, patch

from django.test import TestCase

import cra_helper
from cra_helper import context_processors

# Quiet down logging
logging.disable(logging.CRITICAL)

request = {}
mock_response = {'foo': 'bar'}


class TestStatic(TestCase):
    def test_returns_dict(self):
        self.assertIsInstance(context_processors.static(request), dict)

    def test_returns_asset_manifest_if_defined(self):
        context_processors.STATIC_ASSET_MANIFEST = mock_response
        self.assertEqual(context_processors.static(request), mock_response)

    def test_returns_empty_dict_if_no_asset_manifest(self):
        context_processors.STATIC_ASSET_MANIFEST = None
        self.assertEqual(context_processors.static(request), {})
