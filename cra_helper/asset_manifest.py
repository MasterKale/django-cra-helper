import os
import logging
import json
import re

from django.conf import settings

logger = logging.getLogger(__name__)

_asset_filename = 'asset-manifest.json'


# Sanitize characters that Django's `static` template tag can't handle
def clean_file_key(filename: str) -> str:
    cleaned = filename.replace('.', '_')
    cleaned = cleaned.replace('/', '_')
    cleaned = cleaned.replace('~', '_')
    cleaned = cleaned.replace('-', '_')
    return cleaned

# Create a dictionary of keys that can be passed to the `static` template tag to load CRA assets
# from Django's STATIC_ROOT directory
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

        # Older versions of Create-React-App (through v2.1.8) had flat manifests. If a "files"
        # property doesn't exist in the manifest JSON, then we're probably working with an older
        # version of CRA.
        if data.get('files') is None:
            manifest_items = data.items()
        else:
            manifest_items = data.get('files').items()

        # Prepare a regex that'll help us detect and remove the leading "/static/" from manifest
        # filepaths
        static_base_path = re.compile(r'^/static/', re.IGNORECASE)
        for file_key, path in manifest_items:
            # Don't include index.html, serviceWorker.js, etc...
            if static_base_path.match(path):
                # Generate paths relative to our bundled assets
                # Ex: /static/css/main.99358b65.chunk.css => css/main.99358b65.chunk.css
                _manifest[clean_file_key(file_key)] = re.sub(static_base_path, '', path)

        # Later versions of Create-React-App (starting with v3.2.0) will tell us which files to
        # load via an "entrypoints" array
        entrypoints = data.get('entrypoints')
        if entrypoints is not None:
            # Prepare to group entrypoint files by extension
            _manifest['entrypoints'] = {
                'js': [],
                'css': [],
            };

            # Map manifest files by their path
            mapped_manifest_items = {}
            for file_key, path in manifest_items:
                # Paths in "entrypoints" don't start with a leading "/" so we have to trim it off
                # with the `[1:]`
                mapped_manifest_items[path[1:]] = clean_file_key(file_key)

            for path in entrypoints:
                rel_static_path = _manifest[mapped_manifest_items[path]]

                if path.endswith('.js'):
                    _manifest['entrypoints']['js'].append(rel_static_path)
                elif path.endswith('.css'):
                    _manifest['entrypoints']['css'].append(rel_static_path)

        return _manifest
