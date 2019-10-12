import logging
from urllib import request, error as url_error

from django.conf import settings


def hosted_by_liveserver(file_url: str) -> bool:
    # Ignore the server check if we're in production
    if settings.DEBUG:
        try:
            resp = request.urlopen(file_url)
            if resp.status == 200:
                logging.info('CRA liveserver is running')
                return True
            else:
                logging.warning('CRA liveserver is up but not serving files')
                return False
        except url_error.URLError as err:
            logging.warning('CRA liveserver is not running')
            return False
    else:
        return False
