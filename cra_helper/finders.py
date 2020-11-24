import os

from django.contrib.staticfiles import utils
from django.contrib.staticfiles.finders import BaseFinder
from django.conf import settings

from cra_helper import CRA_FS_APP_DIR
from cra_helper.storage import SingleFileStorage
from cra_helper.logging import logger


class CRAManifestFinder(BaseFinder):
    def __init__(self, app_names=None, *args, **kwargs):
        self._manifest_folder = os.path.join(CRA_FS_APP_DIR, 'build')
        self._manifest_filename = 'asset-manifest.json'
        # Generate an absolute path to the manifest file
        self.manifest_location = os.path.join(self._manifest_folder, self._manifest_filename)
        # Default to asset-manifest.json in STATIC_ROOT if the CRA build folder doesn't exist.
        # This file should exist if `collectstatic` has been successfully run
        if not os.path.isfile(self.manifest_location):
            logger.info('Could not find manifest in Create-React-App build folder, trying to '\
                        'access manifest in static root folder')
            self.manifest_location = os.path.join(
                settings.BASE_DIR,
                settings.STATIC_ROOT,
                self._manifest_filename
            )
        # Prepare our custom storage handler
        self.manifest_storage = SingleFileStorage(location=self.manifest_location)
        super().__init__(*args, **kwargs)

    def check(self, **kwargs):
        return []

    def find(self, path, all=False):
        matches = []
        if path == self._manifest_filename and os.path.exists(self.manifest_location):
            matches.append(self.manifest_location)
        return matches

    def list(self, ignore_patterns):
        for path in utils.get_files(self.manifest_storage, ignore_patterns):
            yield path, self.manifest_storage
