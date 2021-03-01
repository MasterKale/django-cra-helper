import os
import json
import re

from django.conf import settings

from cra_helper.logging import logger
from cra_helper.server_check import hosted_by_liveserver

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
def generate_manifest(cra_url: str, app_dir: str) -> dict:
    manifest = {}

    # The ability to access this file means the create-react-app liveserver is running
    bundle_path = '{}/static/js/bundle.js'.format(cra_url)
    # Check if Create-React-App live server is up and running
    is_server_live = hosted_by_liveserver(bundle_path)

    # Prepare references to various files frontend
    if is_server_live:
        logger.info('Create-React-App liveserver is running')
        # Earlier versions of CRA included everything in a single bundle.js...
        manifest['bundle_js'] = [
            bundle_path,
        ]

        # ...while more recent versions of CRA use code-splitting and serve additional files
        liveserver_bundles = [
            # These two files will alternate being loaded into the page
            '{}/static/js/0.chunk.js'.format(cra_url),
            '{}/static/js/1.chunk.js'.format(cra_url),
            # react-scripts@4.0.0+
            '{}/static/js/vendors~main.chunk.js'.format(cra_url),
            # This bundle seems to contain some vendor files
            '{}/static/js/main.chunk.js'.format(cra_url)
        ]

        for url in liveserver_bundles:
            if hosted_by_liveserver(url):
                manifest['bundle_js'].append(url)
    else:
        logger.info('Create-React-App liveserver is not running')
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
        # filepaths. Support relative path prefixes that might also prefix "/static/".
        static_base_path = re.compile(r'^(?:/[\w.-]+)?/static/', re.IGNORECASE)
        for file_key, path in manifest_items:
            # Don't include index.html, serviceWorker.js, etc...
            if static_base_path.match(path):
                # Generate paths relative to our bundled assets
                # Ex: /static/css/main.99358b65.chunk.css => css/main.99358b65.chunk.css
                manifest[clean_file_key(file_key)] = re.sub(static_base_path, '', path)

        # Later versions of Create-React-App (starting with v3.2.0) will tell us which files to
        # load via an "entrypoints" array
        entrypoints = data.get('entrypoints')
        if entrypoints is not None:
            # Prepare to group entrypoint files by extension
            manifest['entrypoints'] = {
                'js': [],
                'css': [],
            };

            # Map manifest files by their path
            mapped_manifest_items = {}
            for file_key, path in manifest_items:
                # Paths in "entrypoints" in asset-manifest.json don't include the relative path
                # that might be set to "homepage" in package.json. Convert the asset file paths in
                # "files" in asset-manifest.json from `/frontend/static/...` to `static/...` so
                # that our truncated manifest file paths generated above can be matched to
                # the "entrypoints" paths
                normalized_path = re.sub(static_base_path, 'static/', path)
                mapped_manifest_items[normalized_path] = clean_file_key(file_key)

            for path in entrypoints:
                rel_static_path = manifest[mapped_manifest_items[path]]

                if path.endswith('.js'):
                    manifest['entrypoints']['js'].append(rel_static_path)
                elif path.endswith('.css'):
                    manifest['entrypoints']['css'].append(rel_static_path)

    return manifest
