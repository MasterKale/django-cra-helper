import os

from django.conf import settings

from cra_helper.asset_manifest import generate_manifest

# Variables to help the template determine if it should try loading assets from the CRA live server
_CRA_DEFAULT_PORT = 3000
_CRA_DEFAULT_HOST = 'localhost'
_port = _CRA_DEFAULT_PORT
_host = _CRA_DEFAULT_HOST

# Allow the user to specify the port create-react-app is running on
if hasattr(settings, 'CRA_PORT') and type(settings.CRA_PORT) is int:
    _port = settings.CRA_PORT

# Allow the user to specify the host create-react-app is running on
if hasattr(settings, 'CRA_HOST'):
    _host = settings.CRA_HOST

# The URL the create-react-app liveserver is accessible at
CRA_URL = 'http://{}:{}'.format(_host, _port)

if hasattr(settings, 'CRA_APP_NAME'):
    CRA_APP_NAME = settings.CRA_APP_NAME
else:
    CRA_APP_NAME = 'react'

# Be mindful of CRA's relative paths when bootstraping from the CRA liveserver
_cra_liveserver_url = CRA_URL
if hasattr(settings, 'CRA_PACKAGE_JSON_HOMEPAGE'):
    relative_path = str(settings.CRA_PACKAGE_JSON_HOMEPAGE)
    # Normalize homepage path if it starts with / or ends with /
    if relative_path.startswith('/'):
        # Strip leading /
        relative_path = relative_path[1:]
    if relative_path.endswith('/'):
        # Strip trailing /
        relative_path = relative_path[0:-1]

    # Should result in something like 'http://localhost:3000/frontend'
    _cra_liveserver_url = '{}/{}'.format(_cra_liveserver_url, relative_path)

# The path to the CRA project directory, relative to the Django project's base directory
CRA_FS_APP_DIR = os.path.join(settings.BASE_DIR, CRA_APP_NAME)

# A list of entries in CRA's build bundle's
STATIC_ASSET_MANIFEST = generate_manifest(_cra_liveserver_url, CRA_FS_APP_DIR)
