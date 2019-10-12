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

# The path to the CRA project directory, relative to the Django project's base directory
CRA_FS_APP_DIR = os.path.join(settings.BASE_DIR, CRA_APP_NAME)

# A list of entries in CRA's build bundle's
STATIC_ASSET_MANIFEST = generate_manifest(CRA_URL, CRA_FS_APP_DIR)
