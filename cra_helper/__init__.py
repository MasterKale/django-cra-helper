import os

from django.conf import settings

from cra_helper.server_check import is_server_live
from cra_helper.asset_manifest import generate_manifest

# Variables to help the template determine if it should try loading assets from the CRA live server
_CRA_DEFAULT_PORT = 3000
_port = _CRA_DEFAULT_PORT

# Allow the user to specify the port create-react-app is running on
if hasattr(settings, 'CRA_PORT') and type(settings.CRA_PORT) is int:
    _port = settings.CRA_PORT

# The URL the create-react-app liveserver is accessible at
CRA_URL = 'http://localhost:{}'.format(_port)

if hasattr(settings, 'CRA_APP_NAME'):
    CRA_APP_NAME = settings.CRA_APP_NAME
else:
    CRA_APP_NAME = 'react'

# The ability to access this file means the create-react-app liveserver is running
CRA_BUNDLE_PATH = '{}/static/js/bundle.js'.format(CRA_URL)

# Check if Create-React-App live server is up and running
CRA_LIVE = is_server_live(CRA_BUNDLE_PATH)

# The path to the CRA project directory, relative to the Django project's base directory
CRA_FS_APP_DIR = os.path.join(settings.BASE_DIR, CRA_APP_NAME)

# A list of entries in CRA's build bundle's
STATIC_ASSET_MANIFEST = generate_manifest(CRA_LIVE, CRA_BUNDLE_PATH, CRA_FS_APP_DIR)
