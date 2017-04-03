import logging
from unittest.mock import MagicMock, patch

from django.test import TestCase

import cra_helper
from cra_helper.templatetags import cra_helper_tags

# Quiet down logging
logging.disable(logging.CRITICAL)


class TestCRAHelperTags(TestCase):
    def test_converts_simple_dict_to_sanitized_json(self):
        props = {
            'foo': 'bar',
            'fizz': 'buzz',
        }
        output = '{"foo": "bar", "fizz": "buzz"}'
        self.assertEqual(cra_helper_tags.json(props), output)

    def test_converts_complex_dict_to_sanitized_json(self):
        props = {
            'foo': 'bar',
            'fizz': {
                'buzz': [1, 'b', 3, 'd'],
            },
        }
        output = '{"foo": "bar", "fizz": {"buzz": [1, "b", 3, "d"]}}'
        self.assertEqual(cra_helper_tags.json(props), output)
