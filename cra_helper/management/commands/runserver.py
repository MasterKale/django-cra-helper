from cra_helper.handlers import CRAStaticFilesHandler
from django.contrib.staticfiles.management.commands.runserver import \
    Command as StaticRunserverCommand
from django.conf import settings


class Command(StaticRunserverCommand):
    help = '''Starts a lightweight Web server for development and also serves static files.
Redirect static file 404s to Create-React-App\'s liveserver.'''

    def get_handler(self, *args, **options):
        '''
        Return the static files serving handler wrapping the default handler,
        if static files should be served. Otherwise return the default handler.
        '''
        handler = super().get_handler(*args, **options)
        use_static_handler = options['use_static_handler']
        insecure_serving = options['insecure_serving']
        if use_static_handler and (settings.DEBUG or insecure_serving):
            return CRAStaticFilesHandler(handler)
        return handler
