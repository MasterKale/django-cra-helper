import logging
from importlib import reload
from unittest.mock import patch

from django.test import TestCase
from django.conf import settings

import cra_helper

# Quiet down logging
logging.disable(logging.CRITICAL)

setting_to_test = 'CRA_PACKAGE_JSON_HOMEPAGE'


class TestPackageJSONHomepageSupport(TestCase):
    def setUp(self):
        if hasattr(settings,setting_to_test):
            delattr(settings, setting_to_test)

        # The code we want to test won't run if the liveserver isn't "live"
        patcher = patch('cra_helper.asset_manifest.hosted_by_liveserver')
        mock_hosted = patcher.start()
        mock_hosted.return_value = True
        self.addCleanup(patcher.stop)

    def test_uses_cra_url_by_default(self):
        setattr(settings, 'CRA_PORT', 9999)
        reload(cra_helper)

        from cra_helper import STATIC_ASSET_MANIFEST

        bundle_js = str(STATIC_ASSET_MANIFEST["bundle_js"][0])

        self.assertTrue(bundle_js.startswith('http://localhost:9999/static/'))

        delattr(settings, 'CRA_PORT')

    def test_uses_package_json_homepage_setting_leading_slash(self):
        setattr(settings, setting_to_test, '/frontend')
        reload(cra_helper)

        from cra_helper import STATIC_ASSET_MANIFEST

        bundle_js = str(STATIC_ASSET_MANIFEST["bundle_js"][0])

        self.assertTrue(bundle_js.startswith('http://localhost:3000/frontend/static/'))

    def test_uses_package_json_homepage_setting_trailing_slash(self):
        setattr(settings, setting_to_test, 'frontend/')
        reload(cra_helper)

        from cra_helper import STATIC_ASSET_MANIFEST

        bundle_js = str(STATIC_ASSET_MANIFEST["bundle_js"][0])

        self.assertTrue(bundle_js.startswith('http://localhost:3000/frontend/static/'))

    def test_uses_package_json_homepage_setting_no_slash(self):
        setattr(settings, setting_to_test, 'frontend')
        reload(cra_helper)

        from cra_helper import STATIC_ASSET_MANIFEST

        bundle_js = str(STATIC_ASSET_MANIFEST["bundle_js"][0])

        self.assertTrue(bundle_js.startswith('http://localhost:3000/frontend/static/'))
