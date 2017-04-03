import os
import logging
import json

from django.conf import settings

logger = logging.getLogger(__name__)

_asset_filename = 'asset-manifest.json'


def generate_manifest(is_server_live: bool, bundle_path: str, app_dir: str) -> dict:
    # Prepare references to various files frontend
    if is_server_live:
        return {
            'bundle_js': bundle_path,
        }
    else:
        _manifest = {}
        build_dir = os.path.join(app_dir, 'build')

        # Add the CRA static directory to STATICFILES_DIRS so collectstatic can grab files in there
        static_dir = os.path.join(build_dir, 'static')
        settings.STATICFILES_DIRS += [static_dir]

        # CRA generates a JSON file that maps typical filenames to their hashed filenames
        manifest_path = os.path.join(build_dir, _asset_filename)

        # Try to load the JSON manifest from the React build directory first
        try:
            with open(manifest_path) as data_file:
                logger.info('found manifest in React build files')
                data = json.load(data_file)
        except Exception as e:
            # If that doesn't work, try to load it from the Django project's static files directory
            try:
                static_manifest_path = os.path.join(settings.STATIC_ROOT, _asset_filename)
                with open(static_manifest_path) as data_file:
                    logger.info('found manifest in static files')
                    data = json.load(data_file)
            except Exception as e:
                logger.error('can\'t load static asset manifest: {}'.format(e))
                return {}

        # Generate relative paths to our bundled assets
        for filename, path in data.items():
            asset_key = filename.replace('.', '_')
            asset_key = asset_key.replace('/', '_')

            _manifest[asset_key] = os.path.relpath(path, 'static/')

        return _manifest
