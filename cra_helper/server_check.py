from urllib import request, error as url_error

from django.conf import settings

from cra_helper.logging import logger


def hosted_by_liveserver(file_url: str) -> bool:
    # Ignore the server check if we're in production
    if settings.DEBUG:
        try:
            resp = request.urlopen(file_url)
            if resp.status == 200:
                logger.debug('{} is being hosted by liveserver'.format(file_url))
                return True
            else:
                logger.warning('Create-React-App liveserver is up but not serving files')
                return False
        except url_error.URLError as err:
            logger.debug('{} is not being hosted by liveserver'.format(file_url))
            return False
    else:
        logger.debug('Liveserver host check disabled in production')
        return False
