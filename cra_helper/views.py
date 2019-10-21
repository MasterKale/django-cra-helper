from django.views.decorators.csrf import csrf_exempt
from proxy.views import proxy_view

from cra_helper import CRA_URL


@csrf_exempt
def proxy_cra_requests(request, path):
  '''
  Proxy various requests sent by Create-React-App projects in dev mode ("npm start"), within
  Django-hosted views, to the Create-React-App liveserver

  Works well with the following re_path definitions in your project's urls.py:

  re_path(r'^sockjs-node/(?P<path>.*)$', proxy_sockjs),
  re_path(r'^__webpack_dev_server__/(?P<path>.*)$', proxy_sockjs),
  '''
  path = request.path
  url = '{}{}'.format(CRA_URL, path)
  return proxy_view(request, url)
