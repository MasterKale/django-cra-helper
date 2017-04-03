import logging
from urllib import request, error as url_error

from django.conf import settings


def is_server_live(server_path: str) -> bool:
    # Ignore the server check if we're in production
    if settings.DEBUG:
        try:
            resp = request.urlopen(server_path)
            if resp.status == 200:
                logging.info('CRA liveserver is running')
                return True
            else:
                logging.warning('CRA liveserver is up but not serving bundle.js')
                return False
        except url_error.URLError as err:
            logging.warning('CRA liveserver is not running')
            return False
    else:
        return False
