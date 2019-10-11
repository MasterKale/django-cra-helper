from django.contrib.staticfiles.handlers import StaticFilesHandler
from django.shortcuts import redirect
from django.conf import settings

from cra_helper import CRA_URL


class CRAStaticFilesHandler(StaticFilesHandler):
    '''
    This file handler redirects static asset 404's to the Create-React-App liveserver
    '''
    def get_response(self, request):
        from django.http import Http404

        if self._should_handle(request.path):
            try:
                # Try to handle the request as usual
                return self.serve(request)
            except Http404 as e:
                # When the file 404's, redirect the request to the CRA liveserver
                if settings.DEBUG:
                    return redirect('{}{}'.format(CRA_URL, request.path))
                # Simply return the 404 outside of DEBUG mode (a.k.a. in production mode)
                return e

        return super().get_response(request)
