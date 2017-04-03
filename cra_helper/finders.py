import os

from django.contrib.staticfiles import utils
from django.contrib.staticfiles.finders import BaseFinder

from cra_helper import CRA_FS_APP_DIR
from cra_helper.storage import SingleFileStorage


class CRAManifestFinder(BaseFinder):
    def __init__(self, app_names=None, *args, **kwargs):
        self._manifest_folder = os.path.join(CRA_FS_APP_DIR, 'build')
        self._manifest_filename = 'asset-manifest.json'
        # Generate an absolute path to the manifest file
        self.manifest_location = os.path.join(self._manifest_folder, self._manifest_filename)
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
